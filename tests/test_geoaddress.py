from send_the_raven.geoaddress import GeoAddress, Geocoder
from send_the_raven.address import Address
from time import time
import pytest


def test_geoaddress_methods():
    address = GeoAddress(longitude=-115.8236948, latitude=37.2716702)
    assert address.h3_index is None
    address.calculate_h3_index()
    assert address.h3_index == "8d298061e16a63f"
    address.latitude = 36.2706712
    assert address.h3_index == "8d29846d50cba3f"


def test_geoaddress_equality():
    address = GeoAddress()
    address1 = Address()
    with pytest.raises(Exception) as exc_info:
        assert address == address1
    assert "different types" in str(exc_info.value)

    with pytest.raises(Exception) as exc_info:
        address.latitude = 37.2716702
        address.longitude = -115.8236948
        address2 = GeoAddress(h3_resolution=10)
        assert address == address2
    assert "resolutions" in str(exc_info.value)

    with pytest.raises(Exception) as exc_info:
        assert address == GeoAddress()
    assert "indexes" in str(exc_info.value)


def test_geoaddress_hash():
    address = GeoAddress()
    with pytest.raises(Exception) as exc_info:
        hash(address)
    assert "without H3 index" in str(exc_info.value)
    address.latitude = 37.2716702
    address.longitude = -115.8236948
    address2 = GeoAddress(longitude=-115.8236948, latitude=37.2716702)
    address2.calculate_h3_index()
    assert hash(address) == hash(address2)
    address2.latitude = 37.1716702
    assert hash(address) != hash(address2)

def test_geocoder():
    addresses = [GeoAddress(street='12 main st', city='lawrence'), GeoAddress()]
    geocoder = Geocoder(addresses=addresses)
    geocoder('nominatim', dict(user_agent=f'send_the_raven_{time()}', timeout=30))
    assert geocoder.addresses[0].latitude is not None
    assert geocoder.addresses[1].longitude is None



