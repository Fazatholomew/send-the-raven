from pydantic import BaseModel
from typing import Optional, Iterable, Any
from .utils import generate_id
from multiprocessing import Pool
from scourgify import normalize_address_record
from scourgify.exceptions import UnParseableAddressError, AmbiguousAddressError

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

    def generate_full_address(self):
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

        except (UnParseableAddressError, AmbiguousAddressError) as e:
            if len(e.args) == 3:
                normalized = e.args[2]
        if normalized is not None:
            self.street = normalized["address_line_1"]
            self.address_line_2 = normalized["address_line_2"]
            self.city = normalized["city"]
            self.state = normalized["state"]
            self.zip_code = normalized["zipcode"]


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
            Address(**{self.field_mapping[k]: v for k, v in address.items()})
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
