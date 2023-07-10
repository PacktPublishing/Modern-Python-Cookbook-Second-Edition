****************************************
Modern Python Cookbook - Second Edition
Modern Python Cookbook - Second Edition
****************************************

This is the code repository for `Modern Python Cookbook - Second Edition <https://www.packtpub.com/programming/modern-python-cookbook-second-edition>`_, published by `Packt <https://www.packtpub.com/>`_. It contains all the supporting project files necessary to work through the book from start to finish.

About the Book
===============
This book comes with over 133 recipes on the latest version of ``Python 3.9``, that will touch upon all necessary Python concepts related to data structures, OOP, functional, and statistical programming to get acquainted with nuances of Python syntax and how to effectively take advantage of it.
By the end of this Python book, you will be equipped with the knowledge of testing, web services, configuration and application integration tips and tricks. You will be armed with the knowledge of creating applications with flexible logging, powerful configuration, and command-line options, automated unit tests, and good documentation.





Instructions and Navigation
=============================
All of the code is organized into folders. Each folder is numbered chapterwise ``Chapter_03`` and further inside recipewise ``Ch03_r01.py``, some execution is also shown in the ``example.txt`` file.

Installation and Setup
***********************

1.  Install either Miniconda or Anaconda.

2.  Create the book's environment.

    ::

        conda create -n cookbook python=3.9

    Note that python >= 3.9 is required for all of the examples.

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

    - ``tox`` (or ``tox -e py39,network``) will run all tests.

    - ``tox -e py39`` will run the subset of tests that do not need an internet connection.

6.  Windows.

    The Chapter_05 examples make OS requests that work for Darwin and Linux,
    but are not designed to work for Windows. In this chapter's examples, also,
    you might need to use ``#doctest: +SKIP`` to skip over tests that are not relevant
    for your specific OS.

7.  To run the Chapter 12 tests that require the proper SSL setup.

    ::

        tox -e ssl

To run a specific example as a main program, be sure to set the ``PYTHONPATH`` environment variable.

::

    PYTHONPATH=. python Chapter_13/ch13_r06.py data/ch13*.yaml

To run a number of main program demos, use the following tox environment

::

    tox -e main

Related Products
=================
- `Python Machine Learning - Third Edition <https://www.packtpub.com/data/python-machine-learning-third-edition>`_

- `Python Automation Cookbook - Second Edition <https://www.packtpub.com/programming/python-automation-cookbook-second-edition>`_
