Contributing
#############

Contributions to send_the_raven are welcome! Check out the `GitHub repo`_ to get started.

.. _GitHub repo: https://github.com/fazatholomew/send_the_raven

The code is MIT licensed and actively maintained. Please open issues for any bugs or feature requests.
If you are interested to help people from your own country, please feel free to shoot me an email ``thereverend.sullivan@yahoo.co.id``

Development
============

1. Fork the repository
-----------------------

Fork the `repository <https://github.com/fazatholomew/send-the-raven>`_ by clicking "Fork" in the top right corner of the page. This will create a copy of the repository in your own GitHub account.

2. Clone your fork locally
--------------------------

Clone your forked repository to your local machine:

.. code-block:: bash

   git clone https://github.com/fazatholomew/send-the-raven

3. Create a branch
------------------

It's good practice to create a new branch for each new feature or bugfix: 

.. code-block:: bash
   
   git checkout -b your-branch-name

4. Install Poetry
-----------------

This project uses Poetry for packaging and dependency management. Install Poetry if you don't already have it:

.. code-block:: bash

   pip install poetry
   
5. Install dependencies
-----------------------

Install the project dependencies including dev requirements:

.. code-block:: bash

   poetry install

6. Make your changes
--------------------

Make the changes to the code or documentation. Be sure to add:

- Unit tests for any new functionality
- Docstrings and comments for new code
- Documentation updates as needed

7. Prepare for test
--------------------

If you haven't already, get USPS API key for free here. Then, create a ``.env.dev`` and put your ID there.

.. code-block:: bash
   
  USPS_USERID=YOUR_API_KEY

8. Run tests  
------------

To run the test suite:

.. code-block:: bash
   
   poe test

All tests should pass before submitting a pull request. If you add new functionality, add unit tests accordingly.

8. Commit and push
------------------

Commit your changes and push to your fork:

.. code-block:: bash

  git commit -m "Your commit message"
  git push origin your-branch-name

9. Submit a pull request
------------------------

On GitHub, submit a pull request from your branch to the main repository branch.

The maintainers will review your code and may ask for revisions before merging. Be sure to address any feedback or issues raised during review.

Thanks for your contribution!