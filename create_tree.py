import sys, re

class Tree:
    def __init__(self):
        self.root = None

class Node:
    def __init__(self):
        self.value = None
        self.name = None
        self.orderRank = None
        self.shape = None
        self.color = None
        self.arrowDirection = None
        self.edgePosition = None
        self.dashLine = None
        self.label1 = None
        self.label2 = None
        self.label3 = None
        self.children = []
                
def parseLabels(line):
    splitter = " " + '"'
    line_split = line.split(splitter)
    args = None
    label1, label2, label3 = None, None, None
    args = line_split[0]
    for i in range(1,len(line_split)):
        if line_split[i][:2] == "l1":
            label1 = line_split[i][3:] # looks like this: "l1 name_of_the_label
        elif line_split[i][:2] == "l2":# the space is third character thats why [3:]
            label2 = line_split[i][3:]
        elif line_split[i][:2] == "l3":
            label3 = line_split[i][3:]
    return args, label1, label2, label3

def split_path_and_arguments(line):
    s = line.split(" ")
    path = s[0]
    args = s[1:]
    return path, args
        
def readData(fileName):
    f = open(fileName, "r")
    r = f.read().splitlines()
    comments = []
    data = []
    domain_labels = []
    for l in r:
        if l[0] == '#':
            comments.append(l[1:])
        elif "label_names" in l:
            s1 = l.split(":")
            s2 = s1[1].split(",")
            for label in s2:
                domain_labels.append(label)
        else:
            path_and_args, label1, label2, label3 = parseLabels(l)
            path, args = split_path_and_arguments(path_and_args)
            data.append((path, args, label1, label2, label3))
    return data, comments, domain_labels

def parse(data):
    value = data[0]
    args = data[1]
    name = args[0]
    orderRank = args[1]
    shape, color, arrowDirection, edgePosition, dashLine, label1, label2, label3 = None, None, None, None, None, data[2], data[3], data[4]

    args = args[2:]
    if "s" in args:
        shape = "s"
    if "r" in args:
        color = "r"
    if "b" in args: # blank
        color = "b"
    if "at" in args:
        arrowDirection = "to"
    if "af" in args:
        arrowDirection = "from"
    if "ab" in args:
        arrowDirection = "both"
    if "el" in args:
        edgePosition = "left"
    if "er" in args:
        edgePosition = "right"
    if "dl" in args:
        dashLine = "yes"
        
    return value, name, orderRank, shape, color, arrowDirection, edgePosition, dashLine, label1, label2, label3

def createNode(data, parent):
    n = Node()
    n.value, n.name, n.orderRank, n.shape, n.color, n.arrowDirection, n.edgePosition, n.dashLine, n.label1, n.label2, n.label3 = parse(data)
    if parent != None:
        parent.children.append(n)
    return n

def appendChildren(data,node,length):
    for d in data:
        if node.value in d[0] and len(re.compile(r"[a-z,A-Z]").findall(d[0])) == length:
            new = createNode(d, node)
            appendChildren(data, new, length+1)

def buildTree(data):
    tree = Tree()
    tree.root = createNode(data[0], None)
    appendChildren(data, tree.root, 2)
    return tree
    
def mGap(gap):
    return gap * " "
    
def writeToMultipleLabel(multiple_label, f, gap):
    labels = multiple_label.split(",,")
    f.write(mGap(gap) + '"sideLabels" : [')
    for i in range(len(labels)):
        if i!=0:
            f.write(",")
        f.write('"' + labels[i] + '"')
    f.write("]")

def writeTreeData(node, f, gap):
    if node.name != "root" and node.name != "r" and node.name != "Root":
        f.write(mGap(gap) + '"name" : ' + '"' + node.name + '"' + ",\n")
    else:
        f.write(mGap(gap) + '"name" : ' + '"' + '"' + ",\n")
    f.write(mGap(gap) + '"nodeOrder" : ' + node.orderRank)
    if node.shape == "s":
        f.write(",\n")
        f.write(mGap(gap) + '"shape" : ' + '"' + "rectangle" + '"')
    if node.color == "r":
        f.write(",\n")
        f.write(mGap(gap) + '"nodeColor" : ' + '"' + "red" + '"')
    elif node.color == "b":
        f.write(",\n")
        f.write(mGap(gap) + '"nodeColor" : ' + '"' + "blank" + '"')
    if node.arrowDirection == "to":
        f.write(",\n")
        f.write(mGap(gap) + '"arrowToNode" : ' + '"' + "yes" + '"')
    if node.arrowDirection == "from":
        f.write(",\n")
        f.write(mGap(gap) + '"arrowFromNode" : ' + '"' + "yes" + '"')
    if node.arrowDirection == "both":
        f.write(",\n")
        f.write(mGap(gap) + '"arrowToNode" : ' + '"' + "yes" + '"')
        f.write(",\n")
        f.write(mGap(gap) + '"arrowFromNode" : ' + '"' + "yes" + '"')
    if node.dashLine == "yes":
        f.write(",\n")
        f.write(mGap(gap) + '"dashLine" : ' + '"' + "yes" + '"')
    if node.label1 != None:
        f.write(",\n")
        f.write(mGap(gap) + '"label1" : ' + '"' + node.label1 + '"')
    if node.label2 != None:
        f.write(",\n")
        writeToMultipleLabel(node.label2, f, gap)
        #f.write(mGap(gap) + '"label2" : ' + '"' + node.label2 + '"')
    if node.label3 != None:
        f.write(",\n")
        if node.edgePosition == "left":
            f.write(mGap(gap) + '"edgeLabelLeft" : ' + '"' + node.label3 + '"')
        if node.edgePosition == "right":
            f.write(mGap(gap) + '"edgeLabelRight" : ' + '"' + node.label3 + '"')
    if node.children != []:
        f.write(",\n")
        f.write(mGap(gap) + '"children" : ' + "[\n")
        for ch in node.children:
            if not (ch == node.children[0]):
                f.write(",\n")
            f.write(mGap(gap) + "{\n")
            writeTreeData(ch, f, gap+1)
            f.write(mGap(gap) + "\n}")
        f.write(mGap(gap) + "\n]\n")
    
def getLongestNode(data):
    longest = data[0][0]
    for d in data:
        if len(d[0]) > len(longest):
            longest = d[0]
    return longest

def writeLabels(node, f, longest):
    for i in range(2,len(longest),2):
        if not (i == 2 or i==len(longest)):
            f.write(",")
        f.write('"' + longest[i].upper() + '"')

def readHtml():
    f = open("tree.html", "r")
    return f.read().splitlines()
    
def writeHtml(f, comments):
    lines = readHtml()
    for line in lines:
        if not ("mydata.js" in line or "visual.js" in line or "style.css" in line or line == lines[len(lines)-1]): # filtering imports from original html version
            f.write(line + "\n")

def writeComments(description):
    algorithm_name = description[0]
    domains_array = description[1].split(",")
    constraint_array = description[2].split(",")
    description_string = "<p>" + algorithm_name + "</p>" + "<table><tr><th>Variable</th><th>Domain</th></tr>"
    for domain in domains_array:
        description_string += "<tr><td>" + domain[0] + "</td><td>{" + domain[2:] + "}</td></tr>"
    description_string += "<tr><th>Constraints</th></tr>"
    for constraint in constraint_array:
        constraint = constraint.replace("<", "&#60;") # character < is special char in html for ending header
        description_string += "<tr><td>" + constraint + "</td></tr>"
    description_string += "</table>"
    return description_string
            
def writeDescription(f, comments):
    f.write("document.getElementById(" + '"' + "description" + '"' + ").innerHTML = " + '"' + writeComments(comments) + '"' + ";\n")
    
def readJavaScript():
    f = open("visual.js", "r")
    return f.read().splitlines()
    
def writeJavaScript(f):
    lines = readJavaScript()
    for line in lines:
        f.write(line + "\n")    

def writeCss(file):
    f = open("style.css", "r")
    lines = f.read().splitlines()
    file.write("<style>\n")
    for line in lines:
        file.write(line + "\n")
    file.write("</style>\n")

def parse_size_options(size_options):
    arr = size_options.split(",")
    return arr[0].split("=")[1], arr[1].split("=")[1], arr[2].split("=")[1], arr[3].split("=")[1], arr[4].split("=")[1]

# Sets constants placed inside javascript as variables
def set_var_size_options(f, nodeSize):
    f.write("const node_size=" + nodeSize + ";\n")
    
# Sets size of elements in style brackets
def set_style_size_options(f, description, edge, variable_label, node_label):
    f.write("<style>\n")
    f.write("    #description { font-size : " + description + "px; }\n")
    f.write("    .level { font-size : " + variable_label + "px; }\n")
    f.write("    .sideLabels, .label1, .nodeName, .edgeLabelsLeft, .edgeLabelsRight { font-size : " + node_label + "px; }\n")
    f.write("    .link { stroke-width : " + edge + "px; }\n")
    f.write("</style>\n")

def writeToFile(root, fileName, longest, comments, domain_labels):
    f = open(fileName, "w+")
    writeHtml(f, comments)
    writeCss(f)
    desc, node, edge, variable_label, node_label = parse_size_options(comments[3])
    set_style_size_options(f, desc, edge, variable_label, node_label)
    
    f.write("<script>\n")
    
    f.write("var labels = [")
    if domain_labels == []:
        writeLabels(root, f, longest)
        f.write("];\n")
    else:
        for i in range(len(domain_labels)):
            if i!=0:
                f.write(",")
            f.write('"' + domain_labels[i] + '"')
        f.write("]\n")
    
    f.write("var treeData = {\n")
    writeTreeData(root, f, 1)
    f.write("};\n")

    set_var_size_options(f, node)
    writeJavaScript(f)
    writeDescription(f, comments)
    
    f.write("</script>\n")
    f.write("</html>")
         
def makeHtml(input, output):
    data, comments, domain_labels = readData(input)
    tree = buildTree(data)
    writeToFile(tree.root, output, getLongestNode(data), comments, domain_labels)
    
if __name__ == "__main__":
    args = sys.argv
    input_file_name = args[1]
    output_file_name = args[2]
    makeHtml(input_file_name, output_file_name)
    
    

    