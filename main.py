#!/usr/bin/python3

import solver, cgi, merge, parser, sys

def printHtml():
    """Printing the output file to server. HTTP header Content-type represents a format. 
    """
    print("Content-type:text/html\r\n\r\n")
    f = open("output.html", "r")
    lines = f.read().splitlines()
    for line in lines:
        print(line)
    f.close()
    
def values_to_strings(domains):
    s = ""
    for l in domains:
        if l.islower():
            s += '"' + l + '"' 
        else:
            s += l
    return s

def generate_visualization(cfg, output_file_name, executed_from_server):
    """Generates the visualizations
    
    Parameters:
      cfg (string) String representing the input text file
      output_file_name (string) Output file name
      executed_from_server (boolean) If true, send an output to server and update the website 
    Returns:
      Void function
    """
    # split into lines and separate header options and node data
    nodes = cfg.split("\n")[4:]
    # parser create json file
    parser.parse(nodes)
    header = cfg.split("\n")[:4]
    merge.merge(header, output_file_name, cfg)
    if executed_from_server:
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
        generate_visualization(config_str, "output.html", True)
    else:
        # load the data from file
        config_str = open(args[1], "r").read()
        generate_visualization(config_str, "output.html", False)
        print("Visualization created. File name: output.html")
            