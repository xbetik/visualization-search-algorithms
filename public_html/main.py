#!/usr/bin/python3

import solver, cgi, create_tree

def printHtml():
    print("Content-type:text/html\r\n\r\n")
    f = open("/home/xbetik/public_html/output.html", "r")
    lines = f.read().splitlines()
    for line in lines:
        print(line)
    f.close()

form = cgi.FieldStorage()
algorithm = form.getvalue('algorithm') 
domains = form.getvalue('domains')
constraints = form.getvalue('constraints')

#algorithm = '1'
#domains = '{"A" : {1,2,3}, "B" : {1,2,3}, "C" : {1,2,3}}'
#constraints = 'A>B,B>C'

solver.solve(algorithm, domains, constraints)
create_tree.makeHtml("/home/xbetik/public_html/input.txt", "/home/xbetik/public_html/output.html")
printHtml()
