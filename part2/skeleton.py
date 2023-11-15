# skeleton file for UCSC CSE211 Homework 2: part 1

from pycfg.pycfg import PyCFG, CFGNode, slurp 
import argparse 
import re

# Acks: I used
# https://www.geeksforgeeks.org/draw-control-flow-graph-using-pycfg-python/
# to get started with PyCFG. 


def compute_LiveOut_RPO(CFG, dic):
    LiveOut = {}
    count = 1
    for i in CFG:
        LiveOut[i] = set()
    rpo = compute_rpo(CFG)
    print("RPO for the CFG is ")
    print(rpo)
    print()
    changed = True
    while changed:

        changed = False
        for i in rpo:
            prev_set = LiveOut[i]
            successors = get_node_successors(CFG,i)
            
            new_set = set()
            for s in successors:
                
                new_set = new_set.union(LiveOut[s].intersection(dic[s][2]))
                
                new_set = new_set.union(dic[s][0])
                
                
            LiveOut[i] = new_set

            if new_set.difference(prev_set) != set():
                changed = True
        count = count + 1
      


    

    # hint: you will eventually implement a fixed point iteration. It
    # should look a lot like figure 8.14b in the EAC book.
    print("No of iterations RPO ",count)
    return LiveOut

def compute_LiveOut_RPO_CFGReversed(CFG, dic):
    reversed_cfg = reverse_and_compute_rpo(CFG)
    print("reversed_cfg")
    print(reversed_cfg)
    LiveOut = {}
    count = 1
    for i in reversed_cfg:
        LiveOut[i] = set()
    #print("LiveOut for the CFG is ")
    #print(LiveOut)
    changed = True
    while changed:
        changed = False
        
        for i in reversed_cfg:
            prev_set = LiveOut[i]
            new_set = set()
            for s in i:
                print(dic[s][2])
                print(dic[s])
                new_set = new_set.union(LiveOut[s].intersection(dic[s][2]))
                new_set = new_set.union(dic[s][0])
                
                
            LiveOut[i] = new_set

            if new_set.difference(prev_set) != set():
                changed = True
        count = count + 1
      


    

    # hint: you will eventually implement a fixed point iteration. It
    # should look a lot like figure 8.14b in the EAC book.
    print("No of iterations RPO ",count)
    return LiveOut



# Given a node, returns the instruction as a string
# instructions are of the form:
def get_node_instruction(n):
    return n.attr["label"]

# Given a CFG and a node, return a list of successor nodes
def get_node_successors(CFG, n):
    return CFG.successors(n)

# use PyCFG to get a CFG of the python input file.  Graph is returned
# as a PyGraphviz graph.  Don't worry too much about this function. It
# just uses the PyCFG API
def get_graph(input_file):
    cfg = PyCFG()
    cfg.gen_cfg(slurp(input_file).strip())
    arcs = []
    return CFGNode.to_graph(arcs)


# You can use get_node_successors(CFG, n) to get a list of n's
# successor nodes.
def compute_LiveOut(CFG, dic):

    LiveOut = {}
    count = 1
    for i in CFG:
        LiveOut[i] = set()

    changed = True
    while changed:

        changed = False
        for i in CFG:
            prev_set = LiveOut[i]
            successors = get_node_successors(CFG,i)
            
            new_set = set()


            for s in successors:
                
                new_set = new_set.union(LiveOut[s].intersection(dic[s][2]))
                
                new_set = new_set.union(dic[s][0])
                
                
            LiveOut[i] = new_set

            #Checking if any entry is different from the previous one
            if new_set.difference(prev_set) != set():
                changed = True
        count = count + 1
    

    # hint: you will eventually implement a fixed point iteration. It
    # should look a lot like figure 8.14b in the EAC book.
    print("No of iterations ",count)
    return LiveOut


#Utility functions for finding the post order traversal
def dfs(node, visited, rpo_order,CFG):
    visited[node] = True
    for successor in get_node_successors(CFG,node):
        if not visited[successor]:
            dfs(successor, visited, rpo_order, CFG)
    rpo_order.append(node)


def compute_rpo(CFG):
    visited = {node: False for node in CFG}
    rpo_order = []

    for node in CFG:
        if not visited[node]:
            dfs(node, visited, rpo_order, CFG)

    return rpo_order[::-1]




def reverse_and_compute_rpo(CFG):
    def dfs_CFGR(node, visited, rpo_order,CFG):
        visited[node] = True
        for successor in reverse_cfg[node]:
            if not visited[successor]:
                dfs_CFGR(successor, visited, rpo_order, CFG)
        rpo_order.append(node)

    reverse_cfg = {node: [] for node in CFG}

    for node in CFG:
        for successor in get_node_successors(CFG,node):
            reverse_cfg.setdefault(successor,[]).append(node)

    visited = {node: False for node in reverse_cfg}
    rpo_order = []

    for node in CFG:
        if not visited[node]:
            dfs_CFGR(node, visited, rpo_order, reverse_cfg)

    reversed_cfg_dict = {node: reverse_cfg[node] for node in rpo_order[::-1]}
    return reversed_cfg_dict       

# The uninitialized variables are the LiveOut variables from the start
# node. It is fine if your implementation needs to change this
# function. It simply needs to return a set of uninitialized variables
def get_uninitialized_variables_from_LiveOut(CFG, LiveOut):
    return LiveOut[CFG.get_node(0)]

# The testing function. Keep the signature of this function the
# same as it will be used for grading. I highly recommend you keep the
# function exactly the same and simply implement the constituent
# functions.
def find_undefined_variables(input_python_file):

    # Convert the python file into a CFG
    CFG = get_graph(input_python_file)    
    #Dictionary with node index as key and a list of 3 sets as values
    #First set corresponds to UEVAR, second set to VarKill and third to ~VarKill
    dic = dict()

    #Storing all the variables used in the script
    VarDomain = set()

    #Regular expression to check for input and assignment statements
    input_or_assignment_re = r'([0-9]+):\s*([a-z]+)\s*=\s*(input\(\)|[a-z]+)\s*'
    #Regular expression to check for while and if statements
    while_or_if_re = r'([0-9]+):\s*(while|if):\s*([a-z]+)'

    for i in CFG:
        statement = get_node_instruction(i)

        dic[i] = [set(),set(),set()] #3 sets corresponding to UEVAR, VarKill and ~VarKill

        #Adding LHS of assignment statement to VarKill and RHS to UEVAR
        if re.match(input_or_assignment_re, statement):
            re_result = re.search(input_or_assignment_re,statement)
            dic[i][1].add(re_result.group(2))
            VarDomain.add(re_result.group(2))

            if re_result.group(3) != 'input()':
                dic[i][0].add(re_result.group(3))
                VarDomain.add(re_result.group(3))

        elif re.match(while_or_if_re, statement):
            re_result = re.search(while_or_if_re, statement)
            dic[i][0].add(re_result.group(3))
            VarDomain.add(re_result.group(3))
    

    #Computing complement of VarKill
    for i in CFG:                
        dic[i][2] = VarDomain.difference(dic[i][1])
    
            
    # Get LiveOut
    LiveOut = compute_LiveOut(CFG, dic)
    #print(LiveOut)
    RPO_LiveOut = compute_LiveOut_RPO_CFGReversed(CFG, dic)

    print("RPO Liveout is ")
    print(RPO_LiveOut)
    #print()
    # Return a set of unintialized variables
    return get_uninitialized_variables_from_LiveOut(CFG, RPO_LiveOut)

# if you run this file, you can give it one of the python test cases
# in the test_cases/ directory.
# see solutions.py for what to expect for each test case.
if __name__ == '__main__': 
    parser = argparse.ArgumentParser()   
    parser.add_argument('pythonfile', help ='The python file to be analyzed') 
    args = parser.parse_args()
    find_undefined_variables(args.pythonfile)
