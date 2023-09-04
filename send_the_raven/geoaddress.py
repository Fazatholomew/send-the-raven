from send_the_raven.address import Address, Addresses, DEFAULT_ADDRESS_MAPPING
from typing import Optional, Iterable, Any
from geopy.geocoders import get_geocoder_for_service
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
        return self.h3_index.__hash__()

    def __setattr__(self, name: str, value: Any) -> None:
        if name in ["longitude", "latitude", "h3_resolution"]:
            if (
                self.latitude is not None
                and self.longitude is not None
                and self.h3_resolution is not None
            ):
                self.h3_index = geo_to_h3(self.latitude, self.longitude, self.latitude)
        return super().__setattr__(name, value)


class Geocoder(Addresses):
    """
    Geocode Geoaddresses.
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
        try:
            result: Location | None = await geocoder(str(address))
            if result is not None:
                address.longitude = result.longitude
                address.latitude = result.latitude
        except Exception as e:
            self.errors.append((address, e))

    async def start_geocode(self, *args):
        async with get_geocoder_for_service(*args) as current_geocoder:
            geocoder = AsyncRateLimiter(
                current_geocoder.geocode,
                min_delay_seconds=1 / 60,
                max_retries=3,
                error_wait_seconds=randint(1 * 100, 2 * 100) / 100,
            )
            await asyncio.gather(
                *[self.geocode(address, geocoder) for address in self.addresses]
            )

    def __call__(self, geocoder_name, *args):
        """
        Start validation process. Will return after all async process
        are completed.

        Args:
            usps_id (str): Addresses to validate.
            request_limit (int): Initialized aiohttp ClientSession

        returns:
            Addresses: validated addresses.
        """
        self.errors: list[tuple[GeoAddress, Exception]] = []
        try:
            asyncio.run(self.geocode(geocoder_name, *args))
        except RuntimeError:
            asyncio.create_task(self.geocode(geocoder_name, *args))
        return self.addresses
