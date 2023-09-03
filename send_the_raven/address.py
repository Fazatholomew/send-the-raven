from pydantic import BaseModel
from typing import Optional, Iterable, Any
from .utils import generate_id
from multiprocessing import Pool
from scourgify import normalize_address_record
from scourgify.exceptions import (
    UnParseableAddressError,
    AmbiguousAddressError,
    AddressNormalizationError,
)
from difflib import SequenceMatcher
from re import compile

STREET_ADDRESS_NUMBER_REGEX_PATTERN = compile(r"\d+")

DEFAULT_ADDRESS_MAPPING = {
    "full_address": "full_address",
    "street": "street",
    "address_line_2": "address_line_2",
    "city": "city",
    "state": "state",
    "zip_code": "zip_code",
    "id": "id",
}


class Address(BaseModel):
    """
    Represents a US address.

    Args:
        full_address (str): full address.
        street (str): The street name and number.
        address_line_2 (str): The second line of the address.
        city (str): The city name.
        state (str): The state or province name.
        zip_code (str): The ZIP code or postal code.
        id (str): The address ID. If not present, one will be generated to keep track of the address.

    Attributes:
        full_address (str): full address.
        street (str): The street name and number.
        address_line_2 (str): The second line of the address.
        city (str): The city name.
        state (str): The state or province name.
        zip_code (str): The ZIP code or postal code.
        id (str): The address ID.
    """

    full_address: Optional[str] = None
    street: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    id: Optional[str] = generate_id()

    def __str__(self):
        """
        Generates the full address from the address fields.
        Omitting empty or None value.
        """
        not_empty_values = [
            value
            for value in [
                self.street,
                self.address_line_2,
                self.city,
                self.state,
                self.zip_code,
            ]
            if value is not None and value != ""
        ]
        return ", ".join(not_empty_values)

    def normalize(self):
        """
        Normalize address
        using https://github.com/GreenBuildingRegistry/usaddress-scourgify/
        """
        normalized = None
        try:
            normalized = normalize_address_record(
                self.full_address
                if self.full_address is not None
                else {
                    "address_line_1": self.street or "",
                    "address_line_2": self.address_line_2 or "",
                    "city": self.city or "",
                    "state": self.state or "",
                    "zip_code": self.zip_code or "",
                }
            )

        except (
            UnParseableAddressError,
            AmbiguousAddressError,
            AddressNormalizationError,
        ) as e:
            if len(e.args) == 3:
                normalized = e.args[2]
        if normalized is not None:
            self.street = normalized["address_line_1"]
            self.address_line_2 = normalized["address_line_2"]
            self.city = normalized["city"]
            self.state = normalized["state"]
            self.zip_code = normalized["postal_code"]

    def __eq__(self, b) -> bool:
        return compare(self, b) > 0.7


class Addresses:
    """
    Represents a list of addresses.

    Args:
        addresses (iterable): iterable of any to construct Address object.
        field_mapping (dict): A dictionary of field names to be used when constructing the Address objects.

    Attributes:
        addresses (list[Address]): A list of Address objects.
        field_mapping (dict): A dictionary of field names to be used when constructing the Address objects.
    """

    def __init__(
        self,
        addresses: Iterable[Any],
        field_mapping: dict[str, str] = DEFAULT_ADDRESS_MAPPING,
    ):
        self.field_mapping = field_mapping
        for field in DEFAULT_ADDRESS_MAPPING:
            if field not in self.field_mapping:
                self.field_mapping[field] = field
        self.addresses = [
            Address(
                **{
                    self.field_mapping[k]: v
                    for k, v in address.items()
                    if k in self.field_mapping
                }
            )
            for address in addresses
        ]

    def normalize(self, number_of_proccesses: int | None):
        """
        Normalize all addresses in parallel. Uses pool.map().

        Args:
            number_of_proccesses (int): number of process

        """
        with Pool(number_of_proccesses) as pool:
            pool.map(lambda x: x.normalize, self.addresses)

    def __iter__(self):
        return iter(self.addresses)

    def __len__(self):
        return len(self.addresses)


def _process_street(street: str):
    """
    Extract street into components for comparing purposes.
    Also extracting address number such as 151-153 boston ave
    into a list of numbers [151, 153]

    e.g
    12 main st -> ([12], 'main st')
    12-16 main st -> ([12, 14, 16], 'main st')
    12 16 main st -> ([12, 14, 16], 'main st')


    Args:
        street (str): street string to extract


    returns:
        tuple[list[int], str]: street number and street name
    """
    splitted = street.split(" ")
    street_number = splitted[0]
    if len(splitted) > 1 and splitted[1].isdigit():
        street_number = f"{splitted[0]} {splitted[1]}"
    street_name = street.replace(street_number, "")
    street_numbers: list[str] = STREET_ADDRESS_NUMBER_REGEX_PATTERN.findall(
        street_number
    )
    if len(street_numbers) == 2:
        try:
            already_sorted = sorted(street_numbers)
            upper = int(already_sorted[1])
            lower = int(already_sorted[0])
            if upper - lower > 2:
                for number in range(lower, upper + 2, 2):
                    current_number = f"{number}"
                    if current_number not in street_numbers:
                        street_numbers.append(current_number)
        except ValueError:
            pass
    return (street_numbers, street_name)


def compare(a: Address, b: Address) -> float:
    """
    Compare 2 Address instances using difflib.
    The comparison will take into account street number,
    unit, north, south, west, east, etc.

    Please do Address.normalize() first to maximize accuracy.
    return 0 if either a.street or b.street is None.
    doesn't check full_address

    e.g
    12 main st, boston, ma -> 12 main street, boston, ma
    will have higher score than
    13 main st, boston, ma -> 12 main st, boston, ma


    Args:
        a,b (Address): Address to compare


    returns:
        float: similarity between 0.0 and 1.0
    """
    if a.street is None or b.street is None:
        return 0.0

    # process street
    street_number1, street_name1 = _process_street(a.street)
    street_number2, street_name2 = _process_street(b.street)
    scores = 0

    # compare street number
    if any([number in street_number2 for number in street_number1]):
        scores += 1

    for current_element1, current_element2 in [
        (street_name1, street_name2),
        (a.address_line_2, b.address_line_2),
        (a.city, b.city),
        (a.zip_code, b.zip_code),
    ]:
        if not (current_element1 is None or current_element2 is None):
            scores += SequenceMatcher(None, current_element1, current_element2).ratio()

    return scores / 5
