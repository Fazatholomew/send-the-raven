from pydantic import BaseModel
from typing import Optional
from .utils import generate_id


class Address(BaseModel):
    """
    Represents a US address.

    Args:
        full_address (str): full address. Automatically normalized
        street (str): The street name and number.
        address_line_2 (str): The second line of the address.
        city (str): The city name.
        state (str): The state or province name.
        zip_code (str): The ZIP code or postal code.
        id (str): The address ID. If not present, one will be generated to keep track of the address.

    Attributes:
        full_address (str): Combination of normalized address fields.
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
