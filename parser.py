import sys
import re

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
    for l in r:
        if l[0] == '#':
            comments.append(l[1:])
        else:
            path_and_args, label1, label2, label3 = parseLabels(l)
            path, args = split_path_and_arguments(path_and_args)
            data.append((path, args, label1, label2, label3))
    return data, comments

def parse(data):
    value = data[0]
    args = data[1]
    name = args[0]
    orderRank = args[1]
    shape, color, arrowDirection, edgePosition, label1, label2, label3 = None, None, None, None, data[2], data[3], data[4]

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
        
    return value, name, orderRank, shape, color, arrowDirection, edgePosition, label1, label2, label3

def createNode(data, parent):
    n = Node()
    n.value, n.name, n.orderRank, n.shape, n.color, n.arrowDirection, n.edgePosition, n.label1, n.label2, n.label3 = parse(data)
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
    
def writeTreeData(node, f, gap):
    f.write(mGap(gap) + '"name" : ' + '"' + node.name + '"' + ",\n")
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
    if node.label1 != None:
        f.write(",\n")
        f.write(mGap(gap) + '"label1" : ' + '"' + node.label1 + '"')
    if node.label2 != None:
        f.write(",\n")
        f.write(mGap(gap) + '"label2" : ' + '"' + node.label2 + '"')
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
    f = open("index.html", "r")
    return f.read().splitlines()
    
def writeHtml(f, comments):
    lines = readHtml()
    for line in lines:
        if not ("mydata.js" in line or "visual.js" in line or "style.css" in line or line == lines[len(lines)-1]): # filtering imports from original html version
            f.write(line + "\n")

def writeComments(comments):
    bigString = ""
    for comment in comments:
        bigString = bigString + comment + "\\" + "n" 
    return bigString

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

def writeToFile(root, fileName, longest, comments):
    f = open(fileName, "w+")
    writeHtml(f, comments)
    writeCss(f)
    
    f.write("<script>\n")
    
    f.write("var labels = [")
    writeLabels(root, f, longest)
    f.write("]\n")
    
    f.write("var treeData = {\n")
    writeTreeData(root, f, 1)
    f.write("};\n")

    writeJavaScript(f)
    writeDescription(f, comments)
    
    f.write("</script>\n")
    f.write("</html>")
         
def printTree(n,c):
    print 2*c * " " + n.value
    for i in n.children:
        printTree(i, 2*(c+1))

def main(argv):
    configFile = "config.txt"
    if len(argv) == 3:
        configFile = argv[2]    
    data, comments = readData(configFile)
    tree = buildTree(data)
    writeToFile(tree.root, argv[1], getLongestNode(data), comments)
    print argv[1] + " has been created" 
    
if __name__ == "__main__":
    main(sys.argv)