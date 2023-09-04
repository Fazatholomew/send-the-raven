from send_the_raven.usps import Validator, prepare_xml
from send_the_raven.address import Address, Addresses
from xmltodict import parse
from os import getenv


def test_prepare_xml():
    xml = prepare_xml(
        [
            Address(
                street="123 Main St",
                city="law",
                state="VA",
                zip_code="22222",
            ),
            Address(
                street="123 Main St",
                city="Anytown",
                state="VA",
                zip_code="22222",
            ),
        ],
        "12345",
    )
    parsed = parse(xml)
    assert parsed["AddressValidateRequest"]["@USERID"] == "12345"
    assert len(parsed["AddressValidateRequest"]["Address"]) == 2
    assert parsed["AddressValidateRequest"]["Address"][0]["Address1"] is None

def test_validator():
    addresses = Addresses(
        [
            Address(street="12 main st", city="lawrence", state="MA"),
            Address(city="lawrence", state="MA"),
        ]
    )
    validator = Validator(addresses)
    result = validator(getenv("USPS_USERID"))
    assert len(result.addresses) == 2
    assert len(validator.errors) == 1
