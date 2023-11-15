# skeleton file for UCSC CSE211 Homework 2: part 1

from pycfg.pycfg import PyCFG, CFGNode, slurp 
import argparse 
import re

# Acks: I used
# https://www.geeksforgeeks.org/draw-control-flow-graph-using-pycfg-python/
# to get started with PyCFG. 

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

            if new_set.difference(prev_set) != set():
                changed = True
        count = count + 1
             
        
            
            
        


    

    # hint: you will eventually implement a fixed point iteration. It
    # should look a lot like figure 8.14b in the EAC book.
        
    return LiveOut

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

    dic = dict()
    VarDomain = set()
    #Regular expression to check for input and assignment statements
    input_or_assignment_re = r'([0-9]+):\s*([a-z]+)\s*=\s*(input\(\)|[a-z]+)\s*'
    #Regular expression to check for while and if statements
    while_or_if_re = r'([0-9]+):\s*(while|if):\s*([a-z]+)'

    for i in CFG:
        statement = get_node_instruction(i)

        dic[i] = [set(),set(),set()] #3 sets corresponding to UEVAR, VarKill and ~VarKill

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
    
    

        
    

    

    successors = get_node_successors(CFG,i)
    

    
            
    # Get LiveOut
    LiveOut = compute_LiveOut(CFG, dic)
    
    
    # Return a set of unintialized variables
    return get_uninitialized_variables_from_LiveOut(CFG, LiveOut)

# if you run this file, you can give it one of the python test cases
# in the test_cases/ directory.
# see solutions.py for what to expect for each test case.
if __name__ == '__main__': 
    parser = argparse.ArgumentParser()   
    parser.add_argument('pythonfile', help ='The python file to be analyzed') 
    args = parser.parse_args()
    find_undefined_variables(args.pythonfile)
