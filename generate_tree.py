#!/usr/bin/python3

import cgi, create_tree

def printHtml(file):
    print("Content-type:text/html\r\n\r\n")
    f = open(file, "r")
    lines = f.read().splitlines()
    for line in lines:
        print(line)
    f.close()

form = cgi.FieldStorage()
config_str = form.getvalue('new_config_file')
output_file_name = "output.html"
config_str = config_str.replace("\r", "")
create_tree.make_html(config_str, output_file_name)
printHtml(output_file_name)

