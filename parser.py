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
        self.label = None
        self.children = []
        

def readData():
    f = open("config.txt", "r")
    r = f.read().splitlines()
    lines = []
    for l in r:
        s = l.split(" ")
        lines.append(s)
    return lines        
        
def parse(l):
    value = l[0]
    params = l[2]
    p = params.split(",")
    name = p[0]
    orderRank = p[1]
    nodeType, color, label = None, None, None
    if len(p) > 2:
        nodeType = p[2]
    if len(p) > 3:
        color = p[3]
    if len(p) > 4:
        label = p[4]
    return value, name, orderRank, nodeType, color, label
    

def createNode(rawLine, parent):
    n = Node()
    n.value, n.name, n.orderRank, n.nodeType, n.color, n.label = parse(rawLine)
    if not isRoot(rawLine):
        parent.children.append(n)
    return n
    
def isRoot(l):
    return l[1] == "--"
            
def appendChildren(lines, nodes):
    while nodes != []:
        node = nodes.pop()
        for l in lines:
            parent = l[1]
            if parent == node.value:
                new = createNode(l, node)
                nodes.append(new)

def buildTree(lines):
    tree = Tree()
    for l in lines:
        if isRoot(l):
            tree.root = createNode(l, None)
    appendChildren(lines, [tree.root])
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
    if node.label != None:
        f.write(",\n")
        f.write(mGap(gap) + '"label" : ' + '"' + node.label + '"')
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
    
def writeLabels(node, f, visited):
    if (not node.value[0] == "r") and (node.value[0] not in visited):
        f.write('"' + node.value[0].upper() + '"')
        visited.append(node.value[0])
    if node.children != []:
        for ch in node.children:
            if ch.value[0] not in visited and node.value[0] != "r":
                f.write(",")
            writeLabels(ch, f, visited)
    
def readHtml():
    f = open("index.html", "r")
    return f.read().splitlines()
    
def writeHtml(f):
    lines = readHtml()
    for line in lines:
        if not ("mydata.js" in line or "visual.js" in line or line == lines[len(lines)-1]):
            f.write(line + "\n")
    
def readJavaScript():
    f = open("visual.js", "r")
    return f.read().splitlines()
    
def writeJavaScript(f):
    lines = readJavaScript()
    for line in lines:
        f.write(line + "\n")    

def writeToFile(root, fileName):
    f = open(fileName, "w+")
    writeHtml(f)
    
    f.write("<script>\n")
    
    f.write("var labels = [")
    writeLabels(root, f, [])
    f.write("]\n")
    
    f.write("var treeData = {\n")
    writeTreeData(root, f, 1)
    f.write("};\n")

    writeJavaScript(f)
    
    f.write("</script>\n")
    f.write("</html>")
         
def printTree(n,c):
    print c* " ", n.value
    print c* " ", "{"
    for i in n.children:
        print 4*c* " ", i.value
    print c* " ", "}"
    for i in n.children:
        printTree(i,c+1)    
    
def main():
    lines = readData()
    tree = buildTree(lines)
    fileName = raw_input("Enter name of the file\n")
    writeToFile(tree.root, fileName)

main()