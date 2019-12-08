import re

def parse_nodes(lines):
    assignment_info = lines[:3]
    size_options = lines[3]
    node_lines = lines[4:]
    nodes = []
    for line in node_lines:
        line_arr = line.split(";")
        line_dict = {}
        for attribute in line_arr:
            pair = attribute.split(":=")
            line_dict[pair[0]] = pair[1]
        nodes.append(line_dict)
    return assignment_info, size_options, nodes

def add_html(output_file):
    """Adds HTML structure (control panel, buttons, etc.) to final compact HTML file
    
    Parameters:
      output_file (file) Output file
      
    Returns:
      Void function (Adds structure to final file)
    """
    html_file = open("structure.html", "r")
    lines = html_file.read().splitlines()
    for line in lines:
        if not ("mydata.js" in line or "visual.js" in line or "style.css" in line or line == lines[len(lines)-1]): # filtering imports from original html version
            output_file.write(line + "\n")

def parse_size_options(size_options):
    size_options = size_options[1:]
    arr = size_options.split(",")
    return arr[0].split("=")[1], arr[1].split("=")[1], arr[2].split("=")[1], arr[3].split("=")[1], arr[4].split("=")[1], arr[5].split("=")[1], arr[6].split("=")[1], arr[7].split("=")[1]

def set_style_size_options(f, description, variable_label, node_label):
    """Adds font size configuration
    
    Parameters:
      f (file) Output file
      description (string) Initial font size (string number) of description   
      variable_label (string) Initial font size (string number) of variable labels
      node_label (string) Initial font size (string number) of node labels
      
    Returns:
      Void function (Adds font siez config to final file)
    """
    f.write("    #description { font-size : " + description + "px; }\n")
    f.write("    .domain_label { font-size : " + variable_label + "px; }\n")
    f.write("    .sideLabels, .nodeLabel, .nodeName, .edgeLabels { font-size : " + node_label + "px; }\n")
    f.write("</style>\n")

def add_css(output_file, size_options):
    """Adds CSS part to final compact HTML file
    
    Parameters:
      output_file (file) Output file
      size_options (string) Initial configurations
      
    Returns:
      Void function (Adds CSS to final file)
    """
    css_file = open("style.css", "r")
    lines = css_file.read().splitlines()
    output_file.write("<style>\n")
    for line in lines:
        output_file.write(line + "\n")
    desc, _, _, variable_label, node_label, _, _, _ = parse_size_options(size_options)
    set_style_size_options(output_file, desc, variable_label, node_label)
    
def add_javascript(output_file, problem_description, size_options, config_str):
    """Adds JavaScript part to final compact HTML file
    
    Parameters:
      output_file (file) Output file
      problem_description (list) CSP description: algorithm name, domains, constraints
      size_options (string) Initial configurations
      config_str (string) Represents input data file 
      
    Returns:
      Void function (Adds JavaScript to final file)
    """
    def add_labels(f, problem_description):
        f.write("<script>\n")
        f.write("var labels = [")
        labels = problem_description[1][1:].split(",")
        for label in labels:
            f.write('"' + label.split(" ")[0] + '"')
            if label != labels[len(labels)-1]:
                f.write(",")
        f.write("];\n")
    
    def add_script(f, size_options, problem_description):
        def add_assignment(problem_description):
            algorithm_name = problem_description[0][1:]
            domains_array = problem_description[1][1:].split(",")
            constraint_array = problem_description[2][1:].split(",")
            description_string = "<p><strong>" + algorithm_name
            if problem_description[2][1:]:
                description_string += "</strong></p>" + "<table><tr><th>Variable</th><th>Domain</th></tr>"
                for domain in domains_array:
                    reg_search = re.search("([^\s]+)", domain)
                    domain_name = domain[:reg_search.span()[1]]
                    domain_values = ",".join(domain[reg_search.span()[1]:].split())
                    description_string += "<tr><td>" + domain_name + "</td><td>{ " + domain_values + " " + "}</td></tr>"
                description_string += "<tr><th>Constraints</th></tr>"
                for constraint in constraint_array:
                    constraint = constraint.replace("<", "&#60;") # character < is special char in html for ending header
                    description_string += "<tr><td>" + constraint + "</td></tr>"
                description_string += "</table>"
            return description_string
        
        def addAdditionalConstants():
            _, node_size, edge, _, _, show_frame, colored_limit, animation_speed = parse_size_options(size_options)
            f.write("/*----------------This section is generated from config file-----------------*/\n")
            f.write("node_size=" + node_size + ";\n")
            f.write("stroke_width=" + edge + ";\n")
            if colored_limit != "none":
                f.write("coloredLimit=" + colored_limit + ";\n")
            f.write("show_frame=" + show_frame + ";\n")
            f.write("animation_speed=" + animation_speed + ";\n")
            f.write("/*---------------------------------------------------------------------------*/\n")

        javascript_file = open("visual.js", "r")
        lines = javascript_file.read().splitlines()
        for line in lines:
            f.write(line + "\n")
            if "#AdditionalVariableTag" in line:
                addAdditionalConstants()
        f.write("document.getElementById(" + '"' + "description" + '"' + ").innerHTML = " + '"' + add_assignment(problem_description) + '"' + ";\n")
        config_str_br = config_str.replace("\n", "\\n")
        f.write("document.getElementById(" + '"' + "configFile" + '"' + ").value = " + '"' +  config_str_br + '"' + ";\n")
        f.write("</script>\n")
        f.write("</html>")

        
    def add_tree(f):
        f.write("var treeData=\n")
        tree_data = open("tree_data.json", "r")
        lines = tree_data.read().splitlines()
        for line in lines:
            f.write(line + "\n")
    add_labels(output_file, problem_description)
    add_tree(output_file)
    add_script(output_file, size_options, problem_description)


def merge(header, f_name, config_str):
    """Merges JavaScript, CSS, HTML, JSON files into single and independent HTML file representing the visualization
    
    Parameters:
      header (list) List of strings representing individual components of header part of the input data file
      f_name (string) Name of the output HTML file
      config_str (string) Represents input data file 
      
    Returns:
      Void function (Creates output file)
    """
    output_file = open(f_name, "w+")
    add_html(output_file)
    add_css(output_file, header[-1])
    add_javascript(output_file, header[:-1], header[-1], config_str)
    
if __name__ == "__main__":
    header = ["#algorithm_name",
              "#A 1 2,B 1 2",
              "#c1 : A > B, c2 : B > C",
              "#description_size=16,node_size=400,edge_size=1.5,variable_label_size=20,node_label_size=16,show_frame=false,colored_limit=none"]
    merge(header, "output.html", "Content of the previous HTML file should be displayed here for a mo")

    
        
