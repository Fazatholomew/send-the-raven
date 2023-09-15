Examples
#########

Working with :py:class:`~send_the_raven.address.Address`
*********************************************************

Comparing 2 addresses can be tidious process. Sometimes street component can be ``12 main street`` or ``12 main st``.
That's why :py:class:`~send_the_raven.address.Address` instances could be easily compared using ``==``.
Furthermore, in order to increase the comparing result and extracting address components, :py:func:`~send_the_raven.address.Addresses.normalize` can be used.

.. literalinclude:: ../examples/Working with Address.py
   :language: python

Convert Address into Longitude and Latitude using :py:class:`~send_the_raven.geoaddress.Geocoder`
*************************************************************************************************

One needs to convert 1 million addresses into Longitude and Latitude? It's :py:class:`~send_the_raven.geoaddress.Geocoder` comes to the rescue.

:py:class:`~send_the_raven.address.Address` instances could be easily compared using ``==``. Furthermore, extracting addresss components can be done in parallel using :py:func:`~send_the_raven.address.Addresses.normalize`.

.. literalinclude:: ../examples/Get Long Lat.py
   :language: python

Validate addresses to USPS using :py:class:`~send_the_raven.validator.Validator`
*********************************************************************************

USPS API is not the most developer friendly API. Therefore, :py:class:`~send_the_raven.validator.Validator` is here to help.

:py:class:`~send_the_raven.address.Address` instances could be easily compared using ``==``. Furthermore, extracting addresss components can be done in parallel using :py:func:`~send_the_raven.address.Addresses.normalize`.

.. literalinclude:: ../examples/Validate USPS.py
   :language: python