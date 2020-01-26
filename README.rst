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

    Some of the tests require special setup.

    The Chapter_01 tests make an internet connection and download a
    file. In case you have connectivity problems, you might want to
    either delete the test examples, or include ``#doctest: +SKIP`` at the end of each ``>>>`` line.

    Change::

        >>> import urllib.request

    To::

        >>> import urllib.request  # doctest: +SKIP

    On each of the six of lines with ``>>>`` found between the "may need to be skipped" comments.

    The Chapter_05 examples make OS requests that work for Darwin and Linux,
    but are not designed to work for Windows. In this chapter's examples, also,
    you might need to use ``#doctest: +SKIP`` to skip over tests that are not relevant
    for your specific OS.

To run a specific example as a main program, be sure to set the ``PYTHONPATH`` environment variable.

::

    PYTHONPATH=. python Chapter_13/ch13_r06.py data/ch13*.yaml
