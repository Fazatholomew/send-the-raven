Send The Raven
===============

Send the Raven is a Python library that provides a comprehensive collection of toolkits and algorithms for handling US addresses. It aims to simplify the process of working with US addresses, offering functionalities such as parsing, validation, formatting, and more.

.. image:: /_static/d782276f-b708-4c7d-a077-5354d19f06fe.gif
   :alt: Game of Thrones Send the Ravens GIF
   :align: center

Checkout the official `documentation <https://send-the-raven.jimmyganteng.com>`_.

Features
---------

- **Address Parsing**: Extract structured information from US addresses, including street names, house numbers, city, state, and ZIP codes.
- **Address Validation**: Validate US addresses to ensure accuracy and compliance with USPS standards.  
- **Address Formatting**: Format US addresses in a consistent and standardized manner for various purposes.
- **Address Geocoding**: Convert US addresses into Longitude and Latitude.
- **Additional Utilities**: Additional utilities to enhance address handling, such as address comparison, address normalization, and more.

Installation
-------------

send_the_raven can be installed from PyPI:

.. code-block:: bash

   pip install send-the-raven

Usage
------

Here is a quick example of using send_the_raven to validate addresses into USPS Database:

.. code-block:: python

   from send_the_raven import Validator
   
   addresses = [
      {"street": "123 Main St", "city": "Anytown", "state": "CA", "zip_code": "12345"},
      {"street": "456 Oak Rd", "city": "Forest", "state": "VT", "zip_code": "67890"}
   ]
   
   validator = Validator(addresses, usps_id="MY_ID")
   valid_addresses = validator()
   
send_the_raven handles parsing the address data, constructing the validation requests, and returning the corrected addresses.

The :py:class:`~send_the_raven.address.Address` class also provides methods for normalizing, geocoding, and working with addresses.


Acknowledgments
----------------

send_the_raven uses the following open source libraries:

- `usaddress-scourgify <https://github.com/GreenBuildingRegistry/usaddress-scourgify>`_ for parsing addresses.
- `xmltodict <https://github.com/martinblech/xmltodict>`_ for working with XML. 
- `aiohttp <https://github.com/aio-libs/aiohttp>`_ for asynchronous HTTP requests.
- `geopy <https://github.com/geopy/geopy>`_ for geocoding.
- `h3-py <https://github.com/uber/h3-py>`_ for geospatial indexing.

We thank the developers of these libraries for their contributions.

.. toctree::
   :maxdepth: 2
   :hidden:
   
   example
   api
   contribute