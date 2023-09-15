from send_the_raven.address import Address, Addresses, DEFAULT_ADDRESS_MAPPING
from typing import Optional, Iterable, Any
from geopy.geocoders import get_geocoder_for_service
from geopy.adapters import AioHTTPAdapter
from geopy.extra.rate_limiter import AsyncRateLimiter
from geopy.location import Location
from h3 import geo_to_h3
import asyncio
from random import randint

DEFAULT_GEOADDRESS_MAPPING = {
    "longitude": "longitude",
    "latitude": "latitude",
} | DEFAULT_ADDRESS_MAPPING


class GeoAddress(Address):
    """
    Represents a US address with geographic information and methods.

    Args:

        longitude (float): longitude
        latitude (float): latitude
        h3_index (str): index generated from h3
        h3_resolution (int): resolution used to generate h3_index

    Attributes:

        longitude (float): longitude
        latitude (float): latitude
        h3_index (str): index generated from h3
        h3_resolution (int): resolution used to generate h3_index
    """

    longitude: Optional[float] = None
    latitude: Optional[float] = None
    h3_index: Optional[str] = None
    h3_resolution: Optional[int] = 13

    def __eq__(self, b) -> bool:
        """
        Compare addresses using H3 index.
        """
        if not isinstance(b, GeoAddress):
            raise Exception("Cannot compare addresses with different types")
        if self.h3_resolution != b.h3_resolution:
            raise Exception("Cannot compare addresses with different H3 resolutions")
        if self.h3_index is None or b.h3_index is None:
            raise Exception("Cannot compare addresses without H3 indexes")
        return self.h3_index == b.h3_index

    def __hash__(self) -> int:
        """
        Return hash of h3_index
        """
        if self.h3_index is None:
            raise Exception("Cannot hash address without H3 index")
        return hash(self.h3_index)

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Trigger calculate h3_index whenever
        longitude or latitude or h3_resolution changed
        """
        super().__setattr__(name, value)
        if name in ["longitude", "latitude", "h3_resolution"]:
            if (
                self.latitude is not None
                and self.longitude is not None
                and self.h3_resolution is not None
            ):
                self.calculate_h3_index()

    def calculate_h3_index(self) -> str:
        """
        Calculate `h3_index <https://h3geo.org/docs/core-library/h3Indexing/>`_
        """

        self.h3_index = geo_to_h3(self.latitude, self.longitude, self.h3_resolution)
        return self.h3_index


class Geocoder(Addresses):
    """
    Geocoder for Geoaddresses.
    When the instance is called, it will start
    geocoding addresses with geopy_geocoder of your choice.

    Example:

        >>> addresses = [GeoAddress(...), ...]
        >>> geocoder = Geocoder(addresses)
        >>> geocoder("nominatim", {"user_agent": "my_app"})
        >>> for address in geocoder.addresses:
        >>>     print(address.latitude, address.longitude)
    """

    def __init__(
        self,
        addresses: Iterable[Any],
        field_mapping: dict[str, str] = DEFAULT_GEOADDRESS_MAPPING,
    ):
        self.field_mapping = field_mapping
        for field in DEFAULT_GEOADDRESS_MAPPING:
            if field not in self.field_mapping:
                self.field_mapping[field] = field
        self.addresses = [
            GeoAddress(
                **{k: address[v] for k, v in self.field_mapping.items() if v in address}
            )
            if not isinstance(address, GeoAddress)
            else address
            for address in addresses
        ]

    async def geocode(self, address: GeoAddress, geocoder: AsyncRateLimiter):
        """
        Geocode address with geopy_geocoder.
        If geocoding fails, the address is added to the errors list.
        When you are bringing your own async runner, limiter, geocoder,
        feel free to use this function by providing it the geocoder.

        Args:
            address (GeoAddress): Address to geocode.
            geocoder (geopy.extra.rate_limiter.AsyncRateLimiter): Geocoder
            instance wraped with RateLimiter.
        """

        try:
            result: Location | None = await geocoder(str(address))
            if result is not None:
                address.longitude = result.longitude
                address.latitude = result.latitude
        except Exception as e:
            self.errors.append((address, e))

    async def start_geocode(self, geocoder_name: str, args):
        """
        Start geocoding process asyncronously.
        If you want to use a less stricting
        :py:class:`~geopy.extra.rate_limiter.AsyncRateLimiter`, feel free to use your own.
        If you have your own async runner, feel free to run
        this function on your own.

        Args:
            geocoder_name (str): Geocoder to use.
            *args: Arguments to pass to :py:func:`geopy.geocoders.get_geocoder_for_service`.

        """
        async with get_geocoder_for_service(geocoder_name)(
            adapter_factory=AioHTTPAdapter, **args
        ) as current_geocoder:
            geocoder = AsyncRateLimiter(
                current_geocoder.geocode,
                min_delay_seconds=1 / 60,
                max_retries=3,
                error_wait_seconds=randint(1 * 100, 2 * 100) / 100,
                swallow_exceptions=False,
            )
            await asyncio.gather(
                *[self.geocode(address, geocoder) for address in self.addresses]
            )

    def __call__(self, geocoder_name: str, args: dict[str, Any]):
        """
        Start Geocode the addresses. This function will return adter
        all addresses are geocoded.

        Args:
            geocoder_name (str): Geocoder to use.
            args: Arguments to pass to :py:meth:`geopy.geocoders.get_geocoder_for_service`.
        """
        self.errors: list[tuple[GeoAddress, Exception]] = []
        try:
            asyncio.run(self.start_geocode(geocoder_name, args))
        except RuntimeError:
            asyncio.create_task(self.start_geocode(geocoder_name, args))
