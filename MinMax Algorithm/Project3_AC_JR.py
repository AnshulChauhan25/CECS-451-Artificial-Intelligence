# -*- coding: utf-8 -*-
"""
(c) 2021 James & Anshul
Date: 8/2/2021
Name: James Rozsypal & Anshul Chauhan
Student ID: 015668339 & 016246735
Email: james.rozsypal@student.csulb.edu & anshul.chauhan@student.csulb.edu
"""
import csv


class Tree(object):
    
    def __init__(self):
        self.node_dict = {}
        self.num_node = 0
        self.root = None
        self.depth = 0
    
    
    def add_node(self, node_id, node_val, parent_id, node_minmax):       
        # if the root node is being read then parent must be passed in as None
        if parent_id == '': 
            parent = None
            new_n = Node(node_id, node_val, parent, node_minmax)
            self.root = new_n
        # otherwise we get parent from the node dictionary
        else:
            parent = self.node_dict[parent_id]
            new_n = Node(node_id, node_val, parent, node_minmax)
            parent.add_child(node_id, new_n)
        
        # set the dictionary instance of the node as new_n
        self.node_dict[node_id] = new_n
        
        # increment the count of nodes in the tree
        self.num_node += 1
            
    
    def get_node(self, node_id):
        # if the node is in the dictionary then return it
        if node_id in self.node_dict:
            return self.node_dict[node_id]
        # otherwise the node can't be found so return None
        else:
            return None
    
    
    def get_nodes(self):
        # return the keys from the node dictionary
        return self.node_dict.keys()
    
    
    # only works for balanced trees
    def set_depth(self, node):
        # if the current node has children add 1 to depth and search the next layer
        if len(node.get_children_node()) > 0:
            self.depth += 1
            next_node = node.get_children_node()[0]
            self.set_depth(next_node)
        # otherwise we've reached the end of the tree so add one and finish    
        else:
            self.depth += 1
                
    
    def parse(self, file):        
        with open(file) as csvfile:
            csv_reader = csv.reader(csvfile, delimiter=',')
            
            # for tracking the number of lines read (mainly distinguishing root row)
            lines = 0
            
            for row in csv_reader:
                # first read root node row
                if lines == 0:
                    # row[0] defines whether to minimize or maximize
                    root_minmax = row[0].strip()
                    
                    # row[1] contains the name of the parent node
                    root_parent = row[1].strip()
                    
                    # row[2] contains the root node's id and value
                    root_name = row[2].strip()[0:1]
                    root_val = row[2].strip()[2:]  #[row[2].find('='):]
                    
                    # add the root node to the tree
                    self.add_node(root_name, root_val, root_parent, root_minmax)
                    self.root = self.get_node(root_name)
                    print("Tree root = ", self.root.get_id())
                    
                    # print line to verify functionality
                    line = root_minmax.capitalize()+", Parent = "+root_parent+", Root: ("+root_name+", "+root_val+")"
                    print(line)
                    
                # then read the following child node rows
                else:
                    # printable line for verifying functionality
                    line = ""
                    
                    # for counting the number of children found in the row
                    child_count = 1
                    
                    for n in row:
                        # row[0] defines whether to minimize or maximize
                        if n == row[0]:
                           new_minmax = n.strip()
                           line += new_minmax.capitalize()+", "
                           
                        # row[1] contains the name of the parent node
                        elif n == row[1]:
                            new_parent = n.strip()
                            line += "Parent = "+new_parent
                            
                        # the following rows contain children nodes and their data
                        else:
                            new_name = n.strip()[0:n.find('=') - 1]
                            new_val = n.strip()[n.find('='):]
                            self.add_node(new_name, new_val, new_parent, new_minmax)
                            line += ", Child "+str(child_count)+" = ("+new_name+", "+new_val+")"
                            child_count += 1
                    
                    # print line to verify functionality
                    print(line)
                
                # increment lines for loop
                lines += 1
            
            # get and set the depth of the new tree
            self.set_depth(self.root)
            print("Tree depth = ", self.depth)
            
            
    def minimax(self, node, depth, alpha, beta):
        # if the deepest layer of the tree has been reached return the value of the current node
        if depth == self.depth:
            return node.get_val()
        
        # if the current node is on a maximizing layer
        if node.get_minmax() == 'max':
            
            # for each child of the current node
            for c in range(len(node.get_children_node())):
                # get the child node from the c'th index
                child = node.children[c]
                child.isPruned = False
                
                # recur for the children of child
                minimax_eval = self.minimax(child, depth + 1, alpha, beta)
                
                # set alpha as the max between the previous alpha and the value returned from minimax
                alpha = max(alpha, minimax_eval) #best)
                
                
                if alpha > int(node.value):
                    node.value = alpha
                
                # determine if the node should be pruned
                if beta <= alpha:
                    #child.isPruned = True
                    break
                
            return alpha
        
        # otherwise the current node is on a minimizing layer
        else:
            
            # for each child of the current node
            for c in range(len(node.get_children_node())):
                # get the child node from the c'th index
                child = node.children[c]
                child.isPruned = False
                
                # recur for the children of child
                minimax_eval = self.minimax(child, depth + 1, alpha, beta)
    
                # set beta as the min between the previous alpha and the value returned from minimax
                beta = min(alpha, minimax_eval) #best)
                
                if beta > int(node.value):
                    node.value = beta
                
                # determine if the node should be pruned
                if beta <= alpha:
                    #child.isPruned = True
                    break
                
            return beta
                

# =============================================================================
# END OF TREE/START OF NODE
# =============================================================================

class Node:
    
    def __init__(self, name, value, parent, minmax):
        self.name = name
        self.value = value
        self.parent = parent
        self.minmax = minmax
        self.visited = False
        self.isPruned = True
        self.children = []
    
    
    def add_child(self, child_id, child_node):    
        if child_id not in self.children:
            self.children.append(child_node)
    
    
    def get_children_node(self):
        return self.children
    
    
    def get_parent(self):
        return self.parent
    
    
    def get_id(self):
        return self.name
   
    
    def get_val(self):
        return self.value
    
    
    def get_minmax(self):
        return self.minmax
    
    
# =============================================================================
# END OF NODE/START OF MAIN
# =============================================================================

class main():
    
    tree = Tree()
    tree.parse("tree1.txt")
    
    print("The optimal value found =", tree.minimax(tree.root, 0, float('-inf'), float('inf')))

    output = ""
    for n in tree.get_nodes():
        curr = tree.node_dict[n]
        output += (curr.get_id() + '[' + str(curr.get_val())+'] ' + str(curr.isPruned) + '\n')        
    print(output)
    
    print("\n")
    
    tree2 = Tree()
    tree2.parse("tree2.txt")

    print("The optimal value found =", tree2.minimax(tree2.root, 0, float('-inf'), float('inf')))

    output = ""
    for n in tree2.get_nodes():
        curr = tree2.node_dict[n]
        output += (curr.get_id() + '[' + str(curr.get_val())+'] ' + str(curr.isPruned) + '\n')        
    print(output)
