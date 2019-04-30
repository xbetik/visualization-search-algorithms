import sys

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
        
def readData(fileName):
    f = open(fileName, "r")
    r = f.read().splitlines()
    lines = []
    comments = []
    for l in r:
        if l[0] == '#':
            comments.append(l[1:])
        else:
            s = l.split(",")   
            lines.append(s)
    return lines, comments

def parse(l):
    value = l[0]
    params = l[1]
    p = params.split(" ")
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
    if parent != None:
        parent.children.append(n)
    return n

def appendChildren(lines,node,length):
    for l in lines:
        if node.value in l[0] and len(l[0]) == length:
            new = createNode(l, node)
            appendChildren(lines, new, length+2)

def buildTree(lines):
    tree = Tree()
    tree.root = createNode(lines[0], None)
    appendChildren(lines, tree.root, 4)
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
    
def getLongestNode(lines):
    longest = lines[0][0]
    for l in lines:
        if len(l[0]) > len(longest):
            longest = l[0]
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
    if comments != []:
        f.write("<body>" + "\n")
        f.write("<textarea rows=" + '"' + "3" + '"' + "cols=" + '"' + "80" + '"' + ">" + "\n")
        for comment in comments:
            f.write(comment + '\n')
        f.write("</textarea>" + "\n")
        f.write("</body>" + "\n")
    
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

def main(argv):
    configFile = "config.txt"
    if len(argv) == 3:
        configFile = argv[2]    
    lines, comments = readData(configFile)
    tree = buildTree(lines)    
    writeToFile(tree.root, argv[1], getLongestNode(lines), comments)
    print argv[1] + " has been created" 
    
if __name__ == "__main__":
    main(sys.argv)