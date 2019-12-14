Visualization of tree search algorithms
=================

Introduction
------------
This application help with generating interactive visualizations of various tree search algorithms for CSP problem.

Subheading
----------
Online website is located at: https://www.fi.muni.cz/~hanka/vis/

The source code is available at at: https://github.com/xbetik/visualization-search-algorithms

The code documentation is located at /doc subdirectory.

The usage
~~~~~~~~~~~~~

We can execute the application with command:

.. code-block:: console

    $ python3 main.py tree_data.txt
where tree_data.txt represents our input text data file.

We either write the input file manually or generate it using the solver with following command: (The first line is a template. The second line represents a particular example of calling. We need to insert the arguments in single quotation marks.)

.. code-block:: console
    $python3 solver.py algorithm domains constraints python3 solver.py '2' '{"A" : {1,2,3}, "B" : {1,2,3}, "C" : {1,2,3}}' 'A>B,B>C'

Syntax of the solver arguments:

Algorihm list (First argument) '1' - Backtracking '2' - Forward-checking '3' - Look-ahead Domains (Second argument) template: '{"Variable1" : {value1,value2,value3}, "Variable2" : {value1,value2,value3}}' Constraints (Third argument) template: 'Variable1 operator Variable2' ,where operator is Python operator (we use == instead of =)
