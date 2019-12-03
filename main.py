#!/usr/bin/python3

import solver, cgi, merge, parser, sys

def printHtml():
    print("Content-type:text/html\r\n\r\n")
    f = open("output.html", "r")
    lines = f.read().splitlines()
    for line in lines:
        print(line)
    f.close()
    
# Transforms values to strings if they are lowercase letters. Does not effect number values.
# E.g. "A" : {r,b,g}  ---- > "A" : {"r","b","g"}
def values_to_strings(domains):
    s = ""
    for l in domains:
        if l.islower():
            s += '"' + l + '"' 
        else:
            s += l
    return s

def generate_visualization(cfg, output_file_name):
    # split into lines and separate header options and node data
    nodes = cfg.split("\n")[4:]
    # parser create json file
    parser.parse(nodes)
    header = cfg.split("\n")[:4]
    merge.merge(header, output_file_name, cfg)
    printHtml()
    
if __name__ == "__main__":
    args = sys.argv
    config_str = ""
    if (len(args) == 1):
        # solve and create the data file
        form = cgi.FieldStorage()
        algorithm = form.getvalue('algorithm')
        domains = form.getvalue('domains')
        constraints = form.getvalue('constraints')
        domains = values_to_strings(domains)
        config_str = solver.solve(algorithm, domains, constraints)
    else:
        # load the data from file
        config_str = open(args[1], "r").read()
    generate_visualization(config_str, "output.html")
            