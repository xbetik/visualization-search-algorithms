#!/usr/bin/python3

'''
This file represents is called by CGI script modify.cgi
It takes the input data form with the modified input data and generates new visualization
'''

import cgi, main

form = cgi.FieldStorage()
config_str = form.getvalue('new_config_file')
config_str = config_str.replace("\r", "")
main.generate_visualization(config_str, "output.html", True)
