**********
User guide
**********

Installation
============

1. Install and run ``Remme`` node with required RPC API methods enabled, you can check out how to do that at |remmecore|.

.. |remmecore| raw:: html

   <a href="https://github.com/Remmeauth/remme-core" target="_blank">Remme protocol repo</a>

2. Before installing the library, make sure that all the dependencies listed are installed:

**Python3.6**

.. code-block:: console

    $ sudo add-apt-repository ppa:deadsnakes/ppa
    $ sudo apt-get update
    $ sudo apt-get install python3.6-dev
    $ python3.6 -V or python3.6 --version


**Pip**

.. code-block:: console

    $ sudo apt-get -y install python3-pip
    $ pip3 --version or pip3 -V

**Some dependency**

.. code-block:: console

    $ sudo apt-get install build-essential automake libtool pkg-config libffi-dev -y
    $ sudo apt-get update && apt-get install pkg-config


2. Install the latest version of library to your Python project from terminal using ``pip``

.. code-block:: console

    $ pip3 install remme-client-python
