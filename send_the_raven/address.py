from pydantic import BaseModel, validator
from random import getrandbits


class Address(BaseModel):
    """
    Represents an address.

    Attributes:
        street (str): The street name and number.
        address_line_2 (str): The second line of the address.
        city (str): The city name.
        state (str): The state or province name.
        zip_code (str): The ZIP code or postal code.
        id (str): The address ID. If not present, one will be generated to keep track of the address.
    """

    street: str | None
    address_line_2: str | None
    city: str | None
    state: str | None
    zip_code: str | None
    id: str | None

    @validator("id")
    def generate_id(cls, value):
        """
        Generate ID when not present.
        """
        if value is None:
            return "%010x" % getrandbits(60)
        return value
