from .address import Addresses, Address
from .utils import split_into_n_elements
from xmltodict import parse, unparse
from urllib.parse import quote_plus
from aiohttp import ClientSession
from aiohttp.connector import TCPConnector
import asyncio

XML_DOC = """ <?xml version="1.0"?>
              <AddressValidateRequest USERID="{}">
              <Revision>1</Revision>
              </AddressValidateRequest>"""


def prepare_xml(current_addresses: list[Address], usps_id: str) -> str:
    xml = parse(XML_DOC)
    xml["AddressValidateRequest"]["@USERID"] = usps_id
    xml["AddressValidateRequest"]["Address"] = []
    for address in current_addresses:
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


class Validator:
    def __init__(self, data: Addresses, usps_id: str, request_limit: int = 10):
        self.usps_id = usps_id
        self.request_limit = request_limit
        self.data = split_into_n_elements(data)
        self.results: list[Address] = []
        self.errors: list[tuple[Address, Exception]] = []

    async def validate(self, data: list[Address], client: ClientSession):
        xml_string = quote_plus(prepare_xml(data, self.usps_id))
        url = f"https://secure.shippingapis.com/ShippingAPI.dll?API=Verify&XML={xml_string}"
        try:
            res = await client.get(url)
            result = parse(await res.text())
            for address in result["AddressValidateRequest"]["Address"]:
                self.results.append(
                    Address(
                        street=address["Address2"],
                        address_line_2=address["Address1"],
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
        connector = TCPConnector(limit_per_host=self.request_limit)
        async with ClientSession(connector=connector) as session:
            await asyncio.gather(
                *[
                    self.validate(current_addresses, session)
                    for current_addresses in self.data
                ]
            )

    def start(self):
        self.results = []
        self.errors = []
        try:
            asyncio.run(self.start_validation())
        except RuntimeError:
            asyncio.create_task(self.start_validation())
        return self.results
