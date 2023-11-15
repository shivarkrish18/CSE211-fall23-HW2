import argparse
import re


def create_new_variables(statements, H):
    new_hash = dict()
    replaced = 0
    var_counter = 0
    return_statements = []
    for key in H:
        if len(H[key]) > 1:
            new_hash[key] = ['var' + str(var_counter),False]
            var_counter += 1

    for statement in statements:
        final_statement = ''
        declaration_statement = ''
        statement_parts = statement.split('=')
        rhs_statement = statement_parts[1].lstrip().rstrip()
        if rhs_statement in new_hash.keys():
            if new_hash[rhs_statement][1] == False:
                new_hash[rhs_statement][1] = True
                declaration_statement = 'double ' + new_hash[rhs_statement][0] + ' = ' + rhs_statement + ';'
                return_statements.append(declaration_statement)
            else:
                replaced  = replaced + 1
            final_statement = statement_parts[0] + '= ' + new_hash[rhs_statement][0] + ';'
            return_statements.append(final_statement)
        else:
            return_statements.append(statement+';')


    return replaced, return_statements
                  


def remove_numbering(statements):
    removed_statements = []
    for stmt in statements:        
        new_statement = ''
        statement_split = stmt.split('=')

        if 'var' not in statement_split[0]:
            temp_statement = ''
            for j in statement_split[0]:
                if j not in '0123456789':
                    temp_statement += j
            new_statement += temp_statement
        else:
            new_statement += statement_split[0]
        
        new_statement = new_statement + ' = '

        if 'var' not in statement_split[1]:
            temp_statement = ''
            for j in statement_split[1]:
                if j not in '0123456789':
                    temp_statement += j
            new_statement += temp_statement
        else:
            new_statement += statement_split[1]

        removed_statements.append(new_statement)

    return removed_statements

def local_value_numbering(f):
    f = open(f)
    s = f.read()
    f.close()

    pre = s.split("// Start optimization range")[0]
    post = s.split("// Start optimization range")[1].split("// End optimization range")[1]
    to_optimize = s.split("// Start optimization range")[1].split("// End optimization range")[0]
    statements, H = hash_and_numbering(to_optimize)
    replaced, returned_statements = create_new_variables(statements, H)
    returned_statements = remove_numbering(returned_statements)
    print(pre)
    for returned_statement in returned_statements:
        print(returned_statement)
    print(post)
    print("// replaced: " + str(replaced))    




    # hint: perform the local value numbering optimization here on to_optimize
def hash_and_numbering(to_optimize):
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
        #replaced = 0
        if(i==0):
            statement = var1 + '3' + ' = ' + var2 + '1' + ' ' + operator + ' ' + var3 + '2'
            Current_val[var1] = 3
            Current_val[var2] = 1
            Current_val[var3] = 2
            H[var2 + '1' + ' ' + operator + ' ' + var3 + '2'] = [var1 + '3']
        else:
            #print('Here ', Current_val)
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
                    statement = var1 + str(Current_val[var1]) + ' = ' + index1
                    H[index1].append(var1+str(Current_val[var1]))
                    #replaced = replaced + 1
                elif index2 in H.keys():
                    statement = var1 + str(Current_val[var1]) + ' = ' + index2
                    H[index2].append(var1+str(Current_val[var1]))
                    #replaced = replaced + 1
                else:
                    statement = var1 + str(Current_val[var1]) + ' = ' + var2 + str(Current_val[var2]) +' + ' + var3 + str(Current_val[var3])
                    H[statement.split(' = ')[1]] = [var1 + str(Current_val[var1])]
            else:
                index1 = var2 + str(Current_val[var2]) +' - ' + var3 + str(Current_val[var3])
                if index1 in H.keys():
                    statement = var1 + str(Current_val[var1]) + ' = ' + index1
                    H[index1].append(var1+str(Current_val[var1]))
                    #replaced = replaced + 1

                else:
                    statement = var1 + str(Current_val[var1]) + ' = ' + var2 + str(Current_val[var2]) +' - ' + var3 + str(Current_val[var3])
                    H[statement.split(' = ')[1]] = [var1 + str(Current_val[var1])]
        statments.append(statement)
        
    return statments, H


# if you run this file, you can give it one of the python test cases
# in the test_cases/ directory.
# see solutions.py for what to expect for each test case.
if __name__ == '__main__': 
    parser = argparse.ArgumentParser()   
    parser.add_argument('cppfile', help ='The cpp file to be analyzed') 
    args = parser.parse_args()
    local_value_numbering(args.cppfile)
