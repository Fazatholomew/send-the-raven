from pydantic import BaseModel
from typing import Optional
from .utils import generate_id

class Address(BaseModel):
    """
    Represents a US address.

    Args:
        street (str): The street name and number.
        address_line_2 (str): The second line of the address.
        city (str): The city name.
        state (str): The state or province name.
        zip_code (str): The ZIP code or postal code.
        id (str): The address ID. If not present, one will be generated to keep track of the address.

    Attributes:
        street (str): The street name and number.
        address_line_2 (str): The second line of the address.
        city (str): The city name.
        state (str): The state or province name.
        zip_code (str): The ZIP code or postal code.
        id (str): The address ID.
    """

    street: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    id: Optional[str] = generate_id()
