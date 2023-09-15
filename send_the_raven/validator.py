from .address import Addresses, Address, DEFAULT_ADDRESS_MAPPING
from .utils import split_into_n_elements
from xmltodict import parse, unparse
from urllib.parse import quote_plus
from aiohttp import ClientSession
from aiohttp.connector import TCPConnector
import asyncio
from typing import Iterable, Any

XML_DOC = """<?xml version="1.0"?>
              <AddressValidateRequest USERID="{}">
              <Revision>1</Revision>
              </AddressValidateRequest>"""


def _prepare_xml(current_addresses: list[Address], usps_id: str) -> str:
    """
    Prepare XML based on USPS Standard
    https://www.usps.com/business/web-tools-apis/address-information-api.pdf

    Up to 5 addresses per request.

    Args:
        current_addresses (list[Address]): Addresses to validate

    returns:
        string: not URLencoded XML string
    """

    xml = parse(XML_DOC)
    xml["AddressValidateRequest"]["@USERID"] = usps_id
    xml["AddressValidateRequest"]["Address"] = []
    for address in current_addresses[:5]:
        xml["AddressValidateRequest"]["Address"].append(
            {
                "@ID": address.id,
                "Address1": address.address_line_2,
                "Address2": address.street,
                "City": address.city,
                "State": address.state,
                "Zip5": address.zip_code,
                "Zip4": None,
            }
        )
    return unparse(xml)


class Validator(Addresses):
    """
    Class to validate addresses to `USPS database <https://www.usps.com/business/web-tools-apis/documentation-updates.htm>`_.

    Args:
        data (Addresses): Addresses to validate.
        usps_id (str): USPS ID to use for validation. Get it `here <https://registration.shippingapis.com/>`_.
        request_limit (int): Maximum number of requests per second.

    Attributes:
        data (list[Address]): full address.
        results (list[Addresses]): validated addresses.
        errors (list[tuple[Address, Exception]]): addresses with errors.

    Example:

        >>> addresses = [
            {"street": "123 Main St", "city": "Anytown", "state": "CA", "zip": "12345"},
            {"street": "456 Oak Rd", "city": "Forest", "state": "VT", "zip": "67890"}
        ]
        >>> validator = Validator(addresses, usps_id="MY_ID")
        >>> valid_addresses = validator()
        >>> for addr in valid_addresses:
        >>>     print(addr.street, addr.city, addr.state, addr.zip_code)
    """

    def __init__(
        self,
        addresses: Iterable[Any],
        usps_id: str,
        request_limit: int = 10,
        field_mapping: dict[str, str] = DEFAULT_ADDRESS_MAPPING,
    ):
        super().__init__(addresses, field_mapping)
        self.usps_id = usps_id
        self.request_limit = request_limit

    async def validate(self, data: list[Address], client: ClientSession):
        """
        Request validation data to USPS database

        Args:
            data (list[Address]): Addresses to validate.
            client (aiohttp.ClientSession): Initialized aiohttp ClientSession
        """
        xml_string = _prepare_xml(data, self.usps_id)
        url = f"https://secure.shippingapis.com/ShippingAPI.dll?API=Verify&XML={quote_plus(xml_string)}"
        try:
            res = await client.get(url)
            result = parse(await res.text())
            for address in result["AddressValidateResponse"]["Address"]:
                if "Error" in address:
                    current_error_address = Address(id=address["@ID"])
                    self.errors.append(
                        (
                            current_error_address,
                            Exception(address["Error"]["Description"]),
                        )
                    )
                    self.results.append(current_error_address)
                else:
                    self.results.append(
                        Address(
                            street=address["Address2"],
                            address_line_2=address["Address1"]
                            if "Address1" in address
                            else None,
                            city=address["City"],
                            state=address["State"],
                            zip_code=address["Zip4"],
                            id=address["@ID"],
                        )
                    )
        except Exception as e:
            for address in data:
                self.errors.append((address, e))
                self.results.append(address)

    async def start_validation(self):
        """
        Initialize aiohttp TCPConnector with limit and ClientSession.
        Start validation in asyncio.
        """
        connector = TCPConnector(limit_per_host=self.request_limit or 10)
        async with ClientSession(connector=connector) as session:
            await asyncio.gather(
                *[
                    self.validate(current_addresses, session)
                    for current_addresses in split_into_n_elements(self.addresses)
                ]
            )

    def __call__(self):
        """
        Start validation process. Will return after all async process
        are completed.

        returns:
            Addresses: validated addresses.
        """
        self.results = []
        self.errors = []
        try:
            asyncio.run(self.start_validation())
        except RuntimeError:
            asyncio.create_task(self.start_validation())
        self.addresses = self.results
        return self.addresses
