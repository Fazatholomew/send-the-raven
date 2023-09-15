from send_the_raven.address import Address, compare, _process_street, Addresses
from unittest.mock import patch
import pytest


def test_id_creation():
    """
    Test that when ID is not present, should be created correctly.
    """
    address = Address()
    assert address.id is not None


def test_no_id_creation():
    """
    Test that when ID is present, it should be preserved.
    """
    address = Address(id="testest")
    assert address.id == "testest"


def test_equality():
    a = Address(id="testest", street="13 main street", city="boston", state="ma")
    b = Address(id="testest", street="12 main street", city="boston", state="ma")
    assert a != b


def test_generate_full_address():
    """
    Test that full address is generated correctly.
    """
    address = Address(id="testest")
    assert str(address) == ""
    address = Address(street="12 main st", city="boston")
    assert str(address) == "12 main st, boston"
    address = Address(street="12 main st", state="ma")
    assert str(address) == "12 main st, ma"


def test_normalize_full_address_or_components():
    with patch("send_the_raven.address.normalize_address_record") as mock_scourgify:
        address = Address(full_address="12 main street, boston, ma")
        address.normalize()
        mock_scourgify.assert_called_once_with("12 main street, boston, ma")
        address = Address(
            full_address="12 main street, boston, ma", street="12 main street"
        )
        address.normalize()
        mock_scourgify.assert_called_with("12 main street, boston, ma")
        address = Address(street="12 main street", city="boston", state="ma")
        address.normalize()
        mock_scourgify.assert_called_with(
            {
                "address_line_1": "12 main street",
                "address_line_2": "",
                "city": "boston",
                "state": "ma",
                "zip_code": "",
            }
        )


def test_saved_address_even_normalizing_error():
    address = Address(full_address="main street, boston, ma")
    address.normalize()
    assert address.street == "MAIN STREET, BOSTON, MA"


def test_process_street():
    assert _process_street("12 main st") == (["12"], " main st")
    assert _process_street("12-16 main st") == (["12", "16", "14"], " main st")
    assert _process_street("12 16 main st") == (
        ["12", "16", "14"],
        " main st",
    )


def test_compare():
    assert compare(
        Address(street="12 main st"), Address(street="12 main street")
    ) > compare(Address(street="12 main st"), Address(street="13 main st"))

    assert compare(
        Address(street="12 main st", city="south boston"),
        Address(street="12 main st", city="boston"),
    ) > compare(
        Address(street="12 main st", city="lawrence"),
        Address(street="12 main st", city="boston"),
    )

    assert compare(
        Address(street="12 main st", address_line_2="unit 5"),
        Address(street="12 main st", address_line_2="unit 5"),
    ) > compare(
        Address(street="12 main st", address_line_2="unit 5"),
        Address(street="12 main st", address_line_2="unit 5a"),
    )


def test_adding_two_addresses():
    addresses = Addresses(addresses=[Address(), Address()])
    addresses1 = Addresses(
        addresses=[Address(), Address()], field_mapping={"zip_code": "zipcode"}
    )
    assert len(addresses + addresses1) == 4


def test_fill_in_city():
    no_city = Address()
    no_city.fill_in_city()
    assert no_city.city is None
    boston = Address(city="bostn")
    boston.fill_in_city()
    assert boston.city == "boston"
    new_york = Address(city="ewyork")
    new_york.fill_in_city()
    assert new_york.city == "new york"


def test_fill_in_zipcode():
    four_zipcode = Address(zip_code="3345")
    four_zipcode.fill_in_zipcode()
    assert four_zipcode.zip_code == "03345"
    four_zipcode = Address(zip_code="03345")
    four_zipcode.fill_in_zipcode()
    assert four_zipcode.zip_code == "03345"
    four_zipcode = Address()
    four_zipcode.fill_in_zipcode()
    assert four_zipcode.zip_code is None
    four_zipcode = Address(city="southwick")
    four_zipcode.fill_in_zipcode()
    assert four_zipcode.zip_code == "01077"


def test_fill_in_state():
    no_state = Address()
    no_state.fill_in_state()
    assert no_state.state is None
    washington = Address(state="washington")
    washington.fill_in_state()
    assert washington.state == "WA"
    washington = Address(state="massechusts")
    washington.fill_in_state()
    assert washington.state == "MA"
    washington = Address(state="NY")
    washington.fill_in_state()
    assert washington.state == "NY"
