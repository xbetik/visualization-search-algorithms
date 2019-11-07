#!/usr/bin/python3

import solver, cgi, create_tree

def printHtml():
    print("Content-type:text/html\r\n\r\n")
    f = open("output.html", "r")
    lines = f.read().splitlines()
    for line in lines:
        print(line)
    f.close()

# Uncomment if input comes from website

form = cgi.FieldStorage()
algorithm = form.getvalue('algorithm')
#algorithm = "dfs"
 
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
algorithm = '2'
domains = '{"D1" : {1,2,3,4}, "D2" : {1,2,3}, "D3" : {1,2,3}}'
constraints = 'D1>D3,D2==3*D3'
'''

