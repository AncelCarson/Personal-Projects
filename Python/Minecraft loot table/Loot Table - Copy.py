import matplotlib.pyplot as plt
import networkx as nx

#Create graph
tree = nx.read_graphml("minecraft.graph")


def getLayer(node, graph=tree):
    return graph.nodes[node]["layer"]
def getHeight(node, graph=tree):
    return graph.nodes[node]["height"]
def getWidth(node, graph=tree):
    return graph.nodes[node]["width"]
def getPParent(node, graph=tree):
    if node == "Root": return
    return graph.nodes[node]["pParent"]

def layerCal(node, graph, cascade=True):
    if node == "Root":
        for c in list(graph.successors(node)): layerCal(c, graph)
        return
    oldLr = getLayer(node, graph)
    lr = getLayer(getPParent(node, graph), graph)+1
    if oldLr != lr:
        graph.nodes[node]["layer"] = lr
        if cascade:
            for c in list(graph.successors(node)): layerCal(c, graph)

def heightCal(node, graph):
    if node == "Root":
##        for c in list(graph.successors("Root")): heightCal(c, graph)
        return
    parent = getPParent(node, graph)
    h = getHeight(parent, graph)
    siblings = sorted(list(graph.successors(parent)), reverse=True)
    for s in siblings:
        if s == node:
            graph.nodes[node]["height"] = h
            break
        if getPParent(s, graph) == parent: h += getWidth(s, graph)
##    for c in list(graph.successors(node)): heightCal(c, graph)

def widthCal(node, graph):
    oldW = getWidth(node, graph)
    children = list(graph.successors(node))
    if len(children) == 0: w = 1
    else:
        w=0
        for c in children:
            if getPParent(c, graph) == node:
                w += getWidth(c, graph)
    graph.nodes[node]["width"] = max(w, 1)       #max() is for case of all children having other primary parents
    if w != oldW:
        for p in list(graph.predecessors(node)): widthCal(p, graph)

def pParentCal(node, graph):
    if node == "Root": return
    if "pParent" in graph[node]: oldP = getPParent(node, graph)
    else: oldP = "Root"
    parents = list(graph.predecessors(node))
    parent = parents[0]
    for p in parents:
        if getLayer(p, graph) > getLayer(parent, graph): parent = p
    graph.nodes[node]["pParent"] = parent
    oldLr = getLayer(node, graph)
    layerCal(node, graph, cascade=False)
    if oldP != parent or oldLr != getLayer(node, graph):
        for c in list(graph.successors(node)): pParentCal(c, graph)
        if oldP in graph: widthCal(oldP, graph)
        widthCal(parent, graph)
        


def addNode(parent, node):
    tree.add_node(node, width = 0, layer = 0)
    tree.add_edge(parent, node)
    pParentCal(node, tree)
    layerCal(node, tree)
    widthCal(node, tree)
def remNode(node):
    children = list(tree.successors(node))
    parent = getPParent(node)
    tree.remove_node(node)
    for c in children: pParentCal(c, tree)
    widthCal(parent, tree)
    
def remEdge(parent, child):
    tree.remove_edge(parent, child)
    pParentCal(child, tree)
    for c in list(tree.successors(child)): pParentCal(c, tree)
    widthCal(parent, tree)

def save():
    nx.write_graphml_xml(tree, "minecraft.graph")
    print("Successful!")
def show(graph = tree):
    t = []
    for n in graph.nodes: t.append(n)
    t = sorted(t, key = lambda x: (len(t)-getLayer(x, graph), x), reverse = True)
    for n in t: heightCal(n, graph)
    pos = {}
    for node in list(graph.nodes):
        pos[node] = (getLayer(node, graph), getWidth(node, graph)/2 + getHeight(node, graph))
    if graph == tree: pos["N/A"] = (getLayer("N/A", graph), getWidth("Root", graph)/2)
    
    plt.close()
    nx.draw(graph, pos, with_labels=True, node_color="white", edge_color='#A0D000', font_size=7.5)
    plt.xlim(left = -.3)
    plt.ylim([-.05, getWidth("Root", graph)+.05])
    plt.show(block=False)

def add():
    addNode(input("Parent: "), input("New Node: "))
def addm(t = 'blank'):
    if t == 'blank': t = input("Parent: ")
    t1 = input("New Node: ")
    if t1=='stop' or t1=='s' or t1=='quit' or t1=='q' or t1=='exit' or t1=='e': return
    if t1=='N': t1 = 'N/A'
    addNode(t, t1)
    if t1=='N/A': return
    print("Complete! Type 'stop' to exit")
    addm(t1)
def rem():
    remNode(input("Node to remove: "))
def remE():
    remEdge(input("Parent: "), input("Child: "))

def getAllParents(node, graph):
    t = [node]
    if node != "Root":
        for p in list(graph.predecessors(node)):
            t.extend(getAllParents(p, graph))
    return t
def getAllChildren(node, graph):
    t = []
    children = list(graph.successors(node))
    if len(children) != 0:
        for c in children:
            t.append(c)
            t.extend(getAllChildren(c, graph))
    return t
def search():
    node = [input("Item to search for: ")]
    if node[0] not in tree:
        for n in list(tree.nodes):
            if node[0].lower() in n.lower(): node.append(n)
        print(node[0] + " is not on the list.")
        node.pop(0)
        if len(node) == 0: return
    subtree = []
    for n in node:
        subtree.extend(getAllParents(n, tree))
        subtree.extend(getAllChildren(n, tree))
    subtree = tree.subgraph(subtree).copy()
    stack = []
    for n in getAllChildren("Root", subtree):
        pParentCal(n, subtree)
        stack.insert(0, n)
    for n in stack:
        widthCal(n, subtree)
    show(graph = subtree)

##tree = nx.DiGraph()
##tree.add_node("Root", width = 1, height = 0, layer = 0)

show()
