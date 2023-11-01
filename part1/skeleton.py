import argparse
import re

def local_value_numbering(f):
    f = open(f)
    s = f.read()
    f.close()

    pre = s.split("// Start optimization range")[0]
    post = s.split("// Start optimization range")[1].split("// End optimization range")[1]
    to_optimize = s.split("// Start optimization range")[1].split("// End optimization range")[0]

    # hint: perform the local value numbering optimization here on to_optimize

    Current_val = dict()
    H = dict()
    counter = 4
    lines = to_optimize.split("\n")
    new_lines = []
    statments = []
    for line in lines:
        if '=' in line:
            new_lines.append(line.lstrip().rstrip(';'))
    for i in range(len(new_lines)):
        statement = ''
        var1 = new_lines[i][0]
        var2 = new_lines[i][4]
        var3 = new_lines[i][8]
        operator = new_lines[i][6]
        if(i==0):
            statement = var1 + '3' + ' = ' + var2 + '1' + ' ' + operator + ' ' + var3 + '2'
            Current_val[var1] = 3
            Current_val[var2] = 1
            Current_val[var3] = 2
            H[var2 + '1' + ' ' + operator + ' ' + var3 + '2'] = [var1 + '3']
        else:
            print('Here ', Current_val)
            if var2 not in Current_val.keys():
                Current_val[var2] = counter
                counter+=1
            if var3 not in Current_val.keys():
                Current_val[var3] = counter
                counter+=1
            Current_val[var1] = counter
            counter+=1
            if operator == '+':
                index1 = var2 + str(Current_val[var2]) +' + ' + var3 + str(Current_val[var3])
                index2 = var3 + str(Current_val[var3]) +' + '+ var2 + str(Current_val[var2])
                if index1 in H.keys():
                    statement = var1 + str(Current_val[var1]) + ' = ' + H[index1][-1]
                    H[index1].append(var1+str(Current_val[var1]))
                elif index2 in H.keys():
                    statement = var1 + str(Current_val[var1]) + ' = ' + H[index2][-1]
                    H[index2].append(var1+str(Current_val[var1]))
                else:
                    statement = var1 + str(Current_val[var1]) + ' = ' + var2 + str(Current_val[var2]) +' + ' + var3 + str(Current_val[var3])
                    H[statement.split(' = ')[1]] = [var1 + str(Current_val[var1])]
            else:
                index1 = var2 + str(Current_val[var2]) +' - ' + var3 + str(Current_val[var3])
                if index1 in H.keys():
                    statement = var1 + str(Current_val[var1]) + ' = ' + H[index1][-1]
                    H[index1].append(var1+str(Current_val[var1]))

                else:
                    statement = var1 + str(Current_val[var1]) + ' = ' + var2 + str(Current_val[var2]) +' - ' + var3 + str(Current_val[var3])
                    H[statement.split(' = ')[1]] = [var1 + str(Current_val[var1])]
        statments.append(statement)


    print('Statements ',statments)
    print()
    print('Hashtable ', H)
    print()
    print('Current Values ', Current_val)
    
    #print(pre)

    # hint: print out any new variable declarations you need here

    # hint: print out the optimized local block here

    # hint: store any new numbered variables back to their unumbered counterparts here
    
    #print(post)

    # You should keep track of how many instructions you replaced
    #print("// replaced: " + str(replaced))    
    

# if you run this file, you can give it one of the python test cases
# in the test_cases/ directory.
# see solutions.py for what to expect for each test case.
if __name__ == '__main__': 
    parser = argparse.ArgumentParser()   
    parser.add_argument('cppfile', help ='The cpp file to be analyzed') 
    args = parser.parse_args()
    local_value_numbering(args.cppfile)
