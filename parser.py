import re, sys

class Tree:
    """Custom tree datastructure representing our graph
    Parameters
      root (Node) Root node
    """
    def __init__(self):
        self.root = None

class Node:
    """Custom node datastructure
    Parameters
        path (string) Place of the node in hierarchy(R0A1B2:R0-root,A1-first child of root,B2: second child of node A)
        name (string) Name of the node
        order (string) Appearance order (timestamp) of nodes(number between 1-infinity)
        shape (string) Shape of the node (circle,square,default value:circle)
        color (string) Color of the node(red, black, blank(solution)
        bottom_label (string) Name of the label under the node
        side_label (string) Name of the label on the right side of the node
        dash (string) Edge directing to this node is dashed
        arrow (string) Edge has arrow pointing to node or from node (values:to,from,both)
        jump (string) Edge from current node to the node with order=value, where value is a parameter
        action_order (string) Gives an action special timestamp
        left_edge_label (string) Left edge label name
        right_edge_label (string) Right edge label
        children (list) List of children nodes
    """
    def __init__(self):
        self.path = None
        self.name = None
        self.order = None
        self.shape = None
        self.color = None
        self.bottom_label = None
        self.side_label = None
        self.dash = None
        self.arrow = None
        self.jump = None
        self.action_order = None
        self.left_edge_label = None
        self.right_edge_label = None
        self.children = []

def getValues(params):
    """Extracts the attribute data
    
    Parameters:
      params (dict) Dictionary (node_attribute: value)
      
    Returns:
      (tuple) Tuple of the node attributes 
    """
    path = params.get("path")
    name = params.get("name")
    order = params.get("order")
    shape = params.get("shape")
    color = params.get("color")
    bottom_label = params.get("bottom_label")
    side_label = params.get("side_label")
    dashed_line = params.get("dash")
    arrow = params.get("arrow")
    jump = params.get("jump")
    action_order = params.get("action_order")
    left_edge_label = params.get("left_edge_label")
    right_edge_label = params.get("right_edge_label")
    return path,name,order,shape,color,bottom_label,side_label,dashed_line,arrow,jump,action_order,left_edge_label,right_edge_label

def createNode(nodes, parent):
    """Creates a node and set up all the attributes
    
    Parameters:
      (list) List of dictionaries each representing one node 
      
    Returns:
      n (Node) Root node
    """
    n = Node()
    n.path,n.name,n.order,n.shape,n.color,n.bottom_label,n.side_label,n.dash,n.arrow, n.jump, n.action_order, n.left_edge_label, n.right_edge_label = getValues(nodes)
    if parent != None:
        parent.children.append(n)
    return n

def appendChildren(nodes,node,length):
    """Recursive function for children appending
    
    Parameters:
      nodes (list) List of dictionaries each representing one node 
      node (Node) Current node to append
      length (int) Identifies all the children by comparing the current and other node length 
      
    Returns:
      tree (Tree) Returns a built tree datastructure ready to print to JSON
    """
    for node_keys in nodes:
        node_path = node_keys.get("path")
        if node.path in node_path and len(re.compile(r"[A-Z]").findall(node_path)) == length:
            new = createNode(node_keys, node)
            appendChildren(nodes, new, length+1)

def buildTree(nodes):
    """Builds a tree datastructure to be easily transformed into JSON
    
    Parameters:
      nodes (list) List of dictionaries each representing one node 
      
    Returns:
      tree (Tree) Returns a built tree datastructure ready to print to JSON
    """
    tree = Tree()
    tree.root = createNode(nodes[0], None)
    appendChildren(nodes, tree.root, 2)
    return tree

def parseToDict(nodes):
    nodes_dicts = []
    for n in nodes:
        if n.strip():
            node_attributes = n.split(";")
            node_dict = {}
            for attribute in node_attributes:
                pair = attribute.split(":=")
                node_dict[pair[0]] = pair[1]
            nodes_dicts.append(node_dict)
    return nodes_dicts

def createJSON(f, node, gap):
    """Creates JSON file by starting at root node and recursively adding children nodes
    
    Parameters:
      f (file) Output JSON file
      node (Node) A node in our custom made tree datastructure
      gap (int) Counts the spaces for indentation for JSON format
      
    Returns:
      Void function (Creates JSON file)
    """
    def mGap(gap):
        return gap * "  "

    def multipleLabel(multiple_label, f, gap):
        labels = multiple_label.split("&&")
        f.write(mGap(gap) + '"sideLabels" : [')
        for i in range(len(labels)):
            if i!=0:
                f.write(",")
            f.write('"' + labels[i] + '"')
        f.write("]")

    f.write(mGap(gap-1) + "{\n")
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
        f.write(mGap(gap) + '"nodeLabel" : ' + '"' + node.bottom_label + '"')
    if node.side_label != None:
        f.write(",\n")
        multipleLabel(node.side_label, f, gap)
    if node.left_edge_label != None:
        f.write(",\n")
        f.write(mGap(gap) + '"edgeLabelLeft" : ' + '"' + node.left_edge_label + '"')
    if node.right_edge_label != None:
        f.write(",\n")
        f.write(mGap(gap) + '"edgeLabelRight" : ' + '"' + node.right_edge_label + '"')
    if node.jump != None:
        f.write(",\n")
        f.write(mGap(gap) + '"jump" : ' + node.jump)
    if node.action_order != None:
        f.write(",\n")
        f.write(mGap(gap) + '"actionOrder" : ' + node.action_order)
    if node.children != []:
        f.write(",\n" + mGap(gap) + '"children" : ' + "[\n")
        for ch in node.children:
            if not (ch == node.children[0]):
                f.write(",\n")
            createJSON(f, ch, gap+2)
        f.write("\n" + mGap(gap) + "]")
    f.write("\n" + mGap(gap-1) + "}")

def parse(nodes):
    """Parses the text input data file and transform it into JSON file
    
    Parameters:
      nodes (list) List of strings (every string represents one line from input data file i.e. node)
      
    Returns:
      Void function (Creates JSON file)
    """
    nodes_dict = parseToDict(nodes)
    tree = buildTree(nodes_dict)
    f = open("tree_data.json", "w+")
    createJSON(f, tree.root, 1)

if __name__ == "__main__":
    args = sys.argv
    input_file = open(args[1], "r")
    nodes = input_file.read().splitlines()[4:]
    parse(nodes)
    
