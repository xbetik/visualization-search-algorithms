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
        self.nodeType = None
        self.color = None
        self.label1 = None
        self.label2 = None
        self.children = []
        
def parseLabels(line):
    splitter = " " + '"'
    result = line.split(splitter)
    argLen = len(result)
    args = None
    label1 = None
    label2 = None
    args = result[0]
    if argLen > 1:
        label1 = result[1]
    if argLen > 2:
        label2 = result[2]
        
    return args, label1, label2

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
            path_and_args, label1, label2 = parseLabels(l)
            path, args = split_path_and_arguments(path_and_args)
            data.append((path, args, label1, label2))
    return data, comments

def parse(data):
    value = data[0]
    args = data[1]
    name = args[0]
    orderRank = args[1]
    nodeType, color, label1, label2 = None, None, data[2], data[3]
    if len(args) > 2:
        nodeType = args[2]
    if len(args) > 3:
        color = args[3]
    return value, name, orderRank, nodeType, color, label1, label2
    

def createNode(data, parent):
    n = Node()
    n.value, n.name, n.orderRank, n.nodeType, n.color, n.label1, n.label2 = parse(data)
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
    if node.nodeType == "s":
        f.write(",\n")
        f.write(mGap(gap) + '"nodeType" : ' + '"' + "rectangle" + '"')
    if node.color == "r":
        f.write(",\n")
        f.write(mGap(gap) + '"nodeColor" : ' + '"' + "red" + '"')
    elif node.color == "b":
        f.write(",\n")
        f.write(mGap(gap) + '"nodeColor" : ' + '"' + "blank" + '"')        
    if node.label1 != None:
        f.write(",\n")
        f.write(mGap(gap) + '"label1" : ' + '"' + node.label1 + '"')
    if node.label2 != None:
        f.write(",\n")
        f.write(mGap(gap) + '"label2" : ' + '"' + node.label2 + '"')
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
        if not ("mydata.js" in line or "visual.js" in line or line == lines[len(lines)-1]):
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

def writeToFile(root, fileName, longest, comments):
    f = open(fileName, "w+")
    writeHtml(f, comments)
    
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