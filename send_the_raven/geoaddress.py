from send_the_raven.address import Address
from typing import Optional


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
