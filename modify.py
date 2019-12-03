#!/usr/bin/python3

import cgi, main

form = cgi.FieldStorage()
config_str = form.getvalue('new_config_file')
config_str = config_str.replace("\r", "")
main.generate_visualization(config_str, "output.html")