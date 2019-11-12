#!/usr/bin/python3

import solver, cgi, create_tree

def printHtml():
    print("Content-type:text/html\r\n\r\n")
    f = open("output.html", "r")
    lines = f.read().splitlines()
    for line in lines:
        print(line)
    f.close()

form = cgi.FieldStorage()
algorithm = form.getvalue('algorithm')
if algorithm.isdigit():
    domains = form.getvalue('domains')
    constraints = form.getvalue('constraints')
    output_file_name = "output.html"
    config_str = solver.solve(algorithm, domains, constraints)
    create_tree.make_html(config_str, output_file_name)
    printHtml()
else:
    domains = '{"A" : {1,2,3,4,5}, "B" : {1,2,3}, "C" : {1,2}}'
    constraints = 'A>C'
    value = int(form.getvalue('value'))
    #value = int("3")
    output_file_name = "output.html"
    config_str = solver.solve('1', domains, constraints)
    create_tree.make_html_incomplete_search(config_str, output_file_name, value, algorithm)
    printHtml()

'''
algorithm = '3'
domains = '{"V1" : {1,2,3,4}, "V2" : {1,2,3}, "V3" : {1,2,3}}'
constraints = 'V1>V2,V2==3*V3'
config_str = solver.solve(algorithm, domains, constraints)
create_tree.make_html(config_str, "output.html")
'''
