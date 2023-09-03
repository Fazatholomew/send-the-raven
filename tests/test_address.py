from send_the_raven.address import Address, compare, _process_street
from unittest.mock import patch


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


def test_generate_full_address():
    """
    Test that full address is generated correctly.
    """
    address = Address(id="testest")
    assert address.generate_full_address() == ""
    address = Address(street="12 main st", city="boston")
    assert address.generate_full_address() == "12 main st, boston"
    address = Address(street="12 main st", state="ma")
    assert address.generate_full_address() == "12 main st, ma"


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
