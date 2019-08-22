import re

class Tree:
    def __init__(self):
        self.root = None

class Node:
    def __init__(self):
        self.path = None
        self.name = None
        self.order = None
        self.shape = None
        self.color = None
        self.bottom_label = None
        self.side_label = None
        self.edge_label = None
        self.dash = None
        self.arrow = None
        self.edge_label_position = None
        self.children = []

def getValues(params):
    path = params.get("path")
    name = params.get("name")
    order = params.get("order")
    shape = params.get("shape")
    color = params.get("color")
    bottom_label = params.get("bottom_label")
    side_label = params.get("side_label")
    edge_label = params.get("edge_label")
    dashed_line = params.get("dash")
    arrow = params.get("arrow")
    edge_label_position = params.get("edge_label_position")
    return path,name,order,shape,color,bottom_label,side_label,edge_label,dashed_line,arrow,edge_label_position


def createNode(params, parent):
    n = Node()
    n.path,n.name,n.order,n.shape,n.color,n.bottom_label,n.side_label,n.edge_label,n.dash,n.arrow,n.edge_label_position = getValues(params)
    if parent != None:
        parent.children.append(n)
    return n

def appendChildren(params,node,length):
    for node_params in params:
        node_path = node_params.get("path")
        if node.path in node_path and len(re.compile(r"[a-z,A-Z]").findall(node_path)) == length:
            new = createNode(node_params, node)
            appendChildren(params, new, length+1)

def buildTree(node_params):
    tree = Tree()
    tree.root = createNode(node_params[0], None)
    appendChildren(node_params, tree.root, 2)
    return tree

def parse_lines(lines):
    assignment_info = lines[:3]
    size_options = lines[3]
    node_lines = lines[4:]
    nodes = []
    for line in node_lines:
        line_arr = line.split(",")
        line_dict = {}
        for attribute in line_arr:
            pair = attribute.split(":=")
            line_dict[pair[0]] = pair[1]
        nodes.append(line_dict)
    return assignment_info, size_options, nodes

def parse_size_options(size_options):
    size_options = size_options[1:]
    arr = size_options.split(",")
    return arr[0].split("=")[1], arr[1].split("=")[1], arr[2].split("=")[1], arr[3].split("=")[1], arr[4].split("=")[1]

def set_style_size_options(f, description, edge, variable_label, node_label):
    f.write("    #description { font-size : " + description + "px; }\n")
    f.write("    .level { font-size : " + variable_label + "px; }\n")
    f.write("    .sideLabels, .label1, .nodeName, .edgeLabelsLeft, .edgeLabelsRight { font-size : " + node_label + "px; }\n")
    f.write("    .link { stroke-width : " + edge + "px; }\n")
    f.write("</style>\n")

def add_html(output_file):
    html_file = open("tree.html", "r")
    lines = html_file.read().splitlines()
    for line in lines:
        if not ("mydata.js" in line or "visual.js" in line or "style.css" in line or line == lines[len(lines)-1]): # filtering imports from original html version
            output_file.write(line + "\n")
            
def add_css(output_file, size_options):
    css_file = open("style.css", "r")
    lines = css_file.read().splitlines()
    output_file.write("<style>\n")
    for line in lines:
        output_file.write(line + "\n")
    desc, _, edge, variable_label, node_label = parse_size_options(size_options)
    set_style_size_options(output_file, desc, edge, variable_label, node_label)

def add_javascript(output_file, root, info, size_options):
    def add_labels(f, info):
        f.write("<script>\n")
        f.write("var labels = [")
        labels = info[1][1:].split(",")
        for label in labels:
            f.write('"' + label.split(" ")[0] + '"')
            if label != labels[len(labels)-1]:
                f.write(",")
        f.write("];\n")
        f.write("var treeData = {\n")
    
    def add_script(f, size_options, info):
        def add_assignment(info):
            algorithm_name = info[0][1:]
            domains_array = info[1][1:].split(",")
            constraint_array = info[2][1:].split(",")
            description_string = "<p>" + algorithm_name + "</p>" + "<table><tr><th>Variable</th><th>Domain</th></tr>"
            for domain in domains_array:
                description_string += "<tr><td>" + domain[0] + "</td><td>{" + domain[2:] + "}</td></tr>"
            description_string += "<tr><th>Constraints</th></tr>"
            for constraint in constraint_array:
                constraint = constraint.replace("<", "&#60;") # character < is special char in html for ending header
                description_string += "<tr><td>" + constraint + "</td></tr>"
            description_string += "</table>"
            return description_string

        f.write("};\n")
        _, node_size, _, _, _ = parse_size_options(size_options)
        f.write("const node_size=" + node_size + ";\n")
        javascript_file = open("visual.js", "r")
        lines = javascript_file.read().splitlines()
        for line in lines:
            f.write(line + "\n")
        f.write("document.getElementById(" + '"' + "description" + '"' + ").innerHTML = " + '"' + add_assignment(info) + '"' + ";\n")
        f.write("</script>\n")
        f.write("</html>")
        
        
    def add_tree(f, node, gap):
        def mGap(gap):
            return gap * " "

        def writeToMultipleLabel(multiple_label, f, gap):
            labels = multiple_label.split("&&")
            f.write(mGap(gap) + '"sideLabels" : [')
            for i in range(len(labels)):
                if i!=0:
                    f.write(",")
                f.write('"' + labels[i] + '"')
            f.write("]")

        if node.name == "root":
            f.write(mGap(gap) + '"name" : ' + '"' + '"' + ",\n")
        else:
            f.write(mGap(gap) + '"name" : ' + '"' + node.name + '"' + ",\n")
        f.write(mGap(gap) + '"nodeOrder" : ' + node.order)
        if node.shape == "s":
            f.write(",\n")
            f.write(mGap(gap) + '"shape" : ' + '"' + "rectangle" + '"')
        if node.color == "r":
            f.write(",\n")
            f.write(mGap(gap) + '"nodeColor" : ' + '"' + "red" + '"')
        elif node.color == "b":
            f.write(",\n")
            f.write(mGap(gap) + '"nodeColor" : ' + '"' + "blank" + '"')
        if node.arrow == "to":
            f.write(",\n")
            f.write(mGap(gap) + '"arrowToNode" : ' + '"' + "yes" + '"')
        if node.arrow == "from":
            f.write(",\n")
            f.write(mGap(gap) + '"arrowFromNode" : ' + '"' + "yes" + '"')
        if node.arrow == "both":
            f.write(",\n")
            f.write(mGap(gap) + '"arrowToNode" : ' + '"' + "yes" + '"')
            f.write(",\n")
            f.write(mGap(gap) + '"arrowFromNode" : ' + '"' + "yes" + '"')
        if node.dash == "yes":
            f.write(",\n")
            f.write(mGap(gap) + '"dashLine" : ' + '"' + "yes" + '"')
        if node.bottom_label != None:
            f.write(",\n")
            f.write(mGap(gap) + '"label1" : ' + '"' + node.bottom_label + '"')
        if node.side_label != None:
            f.write(",\n")
            writeToMultipleLabel(node.side_label, f, gap)
        if node.edge_label != None:
            f.write(",\n")
            if node.edge_label_position == "left":
                f.write(mGap(gap) + '"edgeLabelLeft" : ' + '"' + node.edge_label + '"')
            if node.edge_label_position == "right":
                f.write(mGap(gap) + '"edgeLabelRight" : ' + '"' + node.edge_label + '"')
        if node.children != []:
            f.write(",\n")
            f.write(mGap(gap) + '"children" : ' + "[\n")
            for ch in node.children:
                if not (ch == node.children[0]):
                    f.write(",\n")
                f.write(mGap(gap) + "{\n")
                add_tree(f, ch, gap+1)
                f.write(mGap(gap) + "\n}")
            f.write(mGap(gap) + "\n]\n")
        
    add_labels(output_file, info)
    add_tree(output_file, root, 1)
    add_script(output_file, size_options, info)

def create_file(output, size_options, root, info):
    output_file = open(output, "w+")
    add_html(output_file)
    add_css(output_file, size_options)
    add_javascript(output_file, root,info, size_options)

def make_html(input, output):
    f = open(input, "r")
    lines = f.read().splitlines()
    assignment_info, size_options, node_params = parse_lines(lines)
    tree = buildTree(node_params)
    create_file(output, size_options, tree.root, assignment_info)

if __name__ == "__main__":
    args = sys.argv
    input_file_name = args[1]
    output_file_name = args[2]
    make_html(input_file_name, output_file_name)
