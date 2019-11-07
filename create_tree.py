import re, sys

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
        self.jump = None
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
    jump = params.get("jump")
    return path,name,order,shape,color,bottom_label,side_label,edge_label,dashed_line,arrow,edge_label_position,jump


def createNode(params, parent):
    n = Node()
    n.path,n.name,n.order,n.shape,n.color,n.bottom_label,n.side_label,n.edge_label,n.dash,n.arrow,n.edge_label_position, n.jump = getValues(params)
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
        line_arr = line.split(";")
        line_dict = {}
        for attribute in line_arr:
            pair = attribute.split(":=")
            line_dict[pair[0]] = pair[1]
        nodes.append(line_dict)
    return assignment_info, size_options, nodes

def parse_size_options(size_options):
    size_options = size_options[1:]
    arr = size_options.split(",")
    return arr[0].split("=")[1], arr[1].split("=")[1], arr[2].split("=")[1], arr[3].split("=")[1], arr[4].split("=")[1], arr[5].split("=")[1], arr[6].split("=")[1]

def set_style_size_options(f, description, variable_label, node_label):
    f.write("    #description { font-size : " + description + "px; }\n")
    f.write("    .level { font-size : " + variable_label + "px; }\n")
    f.write("    .sideLabels, .label1, .nodeName, .edgeLabelsLeft, .edgeLabelsRight { font-size : " + node_label + "px; }\n")
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
    desc, _, _, variable_label, node_label, _, _ = parse_size_options(size_options)
    set_style_size_options(output_file, desc, variable_label, node_label)

def add_javascript(output_file, root, info, size_options, config_str):
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
            description_string = "<p><strong>" + algorithm_name
            if info[2][1:]:
                description_string += "</strong></p>" + "<table><tr><th>Variable</th><th>Domain</th></tr>"
                for domain in domains_array:
                    reg_search = re.search("([^\s]+)", domain)
                    domain_name = domain[:reg_search.span()[1]]
                    domain_values = domain[reg_search.span()[1]:]
                    description_string += "<tr><td>" + domain_name + "</td><td>{" + domain_values + " " + "}</td></tr>"
                description_string += "<tr><th>Constraints</th></tr>"
                for constraint in constraint_array:
                    constraint = constraint.replace("<", "&#60;") # character < is special char in html for ending header
                    description_string += "<tr><td>" + constraint + "</td></tr>"
                description_string += "</table>"
            return description_string
        
        f.write("};\n")
        _, node_size, edge, _, _, show_frame, colored_limit = parse_size_options(size_options)
        f.write("const node_size=" + node_size + ";\n")
        f.write("const stroke_width=" + edge + ";\n")
        if colored_limit != "none":
            f.write("const coloredLimit=" + colored_limit + ";\n")
        f.write("let show_frame=" + show_frame + ";\n")
        javascript_file = open("visual.js", "r")
        lines = javascript_file.read().splitlines()
        for line in lines:
            f.write(line + "\n")
        f.write("document.getElementById(" + '"' + "description" + '"' + ").innerHTML = " + '"' + add_assignment(info) + '"' + ";\n")
        config_str_br = config_str.replace("\n", "\\n")
        f.write("document.getElementById(" + '"' + "configFile" + '"' + ").value = " + '"' +  config_str_br + '"' + ";\n")
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

        if node.name == "none":
            f.write(mGap(gap) + '"name" : ' + '"' + '"' + ",\n")
        else:
            f.write(mGap(gap) + '"name" : ' + '"' + node.name + '"' + ",\n")
        f.write(mGap(gap) + '"nodeOrder" : ' + node.order)
        if node.shape == "square":
            f.write(",\n")
            f.write(mGap(gap) + '"shape" : ' + '"' + "rectangle" + '"')
        if node.color != None:
            f.write(",\n")
            f.write(mGap(gap) + '"nodeColor" : ' + '"' + node.color + '"')
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
        if node.jump != None:
            f.write(",\n")
            f.write(mGap(gap) + '"jump" : ' + node.jump )                
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
    
def create_file(output, size_options, root, info, config_str):
    output_file = open(output, "w+")
    add_html(output_file)
    add_css(output_file, size_options)
    add_javascript(output_file, root,info, size_options, config_str)
    
def dfs(node, limit, i, lines):
    if node.children == []:
        if i <= limit:
            node.bottom_label = str(i)
            lines[int(node.order)+3] = re.sub(r'bottom_label.*$',"bottom_label:="+str(i),lines[int(node.order)+3])
            i+=1
        else:
            lines[int(node.order)+3] = re.sub(r';bottom_label.*$',"",lines[int(node.order)+3])
            node.bottom_label = None
    for child in node.children:
        i = dfs(child, limit, i, lines)
    return i

def count_total(node, limit, i, add):
    if node.bottom_label != None and int(node.bottom_label) == limit:
        add = False
    if add:
        i+=1
    for child in node.children:
        i,add = count_total(child, limit, i, add)
    return i,add

def make_html_incomplete_search(config_str, output, value, algorithm):
    config_str = config_str.replace("show_frame=false","show_frame=true")
    lines = config_str.split("\n")
    assignment_info, size_options, node_params = parse_lines(lines)
    tree = buildTree(node_params)
    if algorithm == "dfs":
        dfs(tree.root, value, 1, lines)
        if value == 0:
            total = 0
        else:
            total,_ = count_total(tree.root,value,1,True)
            total-=1
        size_options = size_options.replace("colored_limit=none","colored_limit=" + str(total))
        lines[3] = lines[3].replace("colored_limit=none","colored_limit=" + str(total))
    config_str = ""
    for l in lines:
        config_str += l + "\n"
    create_file(output, size_options, tree.root, assignment_info, config_str)
    
def make_html(config_str, output):
    lines = config_str.split("\n")
    assignment_info, size_options, node_params = parse_lines(lines)
    tree = buildTree(node_params)
    create_file(output, size_options, tree.root, assignment_info, config_str)

if __name__ == "__main__":
    args = sys.argv
    config_str = args[1]
    output_file_name = args[2]
    make_html(config_str, output_file_name)
