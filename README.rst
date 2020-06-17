###############################
Modern Python Cookbook, 2nd ed
###############################

Modern-Python-Cookbook-Second-Edition, published by Packt

Installation and Setup
======================

1.  Install either Miniconda or Anaconda.

2.  Create the book's environment.

    ::

        conda create -n cookbook python=3.8

    Note that python 3.8 is required. A few of the examples will not
    work with Python 3.7.

3.  Activate the environment.

    ::

        conda activate cookbook

3.  Install the required components. This will download and install all of the
    packages listed in the ``requirements.txt`` file.

    ::

        python -m pip install --requirement requirements.txt

4.  Run the **tox** tool to test all of the modules.

    ::

        tox

5.  No Internet.

    - ``tox`` (or ``tox -e py38,network``) will run all tests.

    - ``tox -e py38`` will run the tests that do not need an internet connection.

6.  Windows.

    The Chapter_05 examples make OS requests that work for Darwin and Linux,
    but are not designed to work for Windows. In this chapter's examples, also,
    you might need to use ``#doctest: +SKIP`` to skip over tests that are not relevant
    for your specific OS.

To run a specific example as a main program, be sure to set the ``PYTHONPATH`` environment variable.

::

    PYTHONPATH=. python Chapter_13/ch13_r06.py data/ch13*.yaml
