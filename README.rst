Visualization of tree search algorithms
=================

Introduction
------------
This application help with generating interactive visualizations of various tree search algorithms for CSP problem. The application is mainly used from web browser on website reffered below, but you can download the files and execute it locally with commands described below.

Application website reference
----------
Online website is located at: https://www.fi.muni.cz/~hanka/vis/

The source code documentation of application is located at /doc subdirectory.

The usage
~~~~~~~~~~~~~

We can execute the application with command:

.. code-block:: console

    $ python3 main.py tree_data.txt
where tree_data.txt represents our input text data file.

We either write the input file manually or generate it using the solver with with parameters: algorithm, domains, constraints. For instance, lets solve a particular CSP with 3 attributes A,B,C, domain values 1,2,3 for each attribute and constraints A>B and B>C. The following commands do the job:

.. code-block:: console

    $ python3 solver.py '2' '{"A" : {1,2,3}, "B" : {1,2,3}, "C" : {1,2,3}}' 'A>B,B>C'

This command will generate our input text file. Now we need to generate the visualization with the previous command.

Syntax of the solver parameters:

1.Algorihm '1' - Backtracking '2' - Forward-checking '3' - Look-ahead

2.Domains - template: '{"Variable1" : {value1,value2,value3}, "Variable2" : {value1,value2,value3}}'

3.Constraints template: 'Variable1 operator Variable2' ,where operator is Python operator (we use == instead of =)
