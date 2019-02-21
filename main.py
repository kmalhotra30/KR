from copy import deepcopy
import numpy as np

def printSudokuGrid(assignments):

    #Helper function to visualize solved soduko
    M = np.zeros([9,9])
    for l in assignments[1]:
      if assignments[1][l] == 1:
          i = int(l[0])-1
          j = int(l[1]) - 1
          v = int(l[2]) 
          M[i][j]= v

    for i in range(9):
      for j in range(9):
          print(str(M[i][j]) + " ",end = '')
      print("")
def return_var_and_negated_var(variable):

    #Helper function to return variable and it's negation
    if(variable[0] == '-'):
        return variable , variable[1:]
    else:
        return variable , '-' + variable

def modifyClausesWithVariableSetToTrue(variable,c2vDict , v2cDict , countVarDict, assignments):

    #Assign literal as true or false (depending on first character)
    #Remove variable from c2vDict
    #Decrement Count from countVarDict

    variable , negatedVariable = return_var_and_negated_var(variable)
    if variable[0] == '-':

        assignments[variable[1:]] = 0 # Not of False is True
    else:
        assignments[variable] = 1 

    #Removing variable from c2vDict by using v2cDict as a helper

    for clause_index in v2cDict[variable]:

        #Check if clause is active or not
        if len(c2vDict[clause_index]) != 0: 

            for var in c2vDict[clause_index]:

                #Decrement count of var
                countVarDict[var] -= 1

                #Remove all variables from clause


                c2vDict[clause_index] = []

    if negatedVariable in countVarDict: 
        if countVarDict[negatedVariable] !=0:
            c2vDict , v2cDict , countVarDict , assignments = modifyClausesWithVariableSetToFalse(negatedVariable,c2vDict , v2cDict , countVarDict , assignments)

    return c2vDict , v2cDict , countVarDict , assignments

def modifyClausesWithVariableSetToFalse(variable,c2vDict , v2cDict , countVarDict, assignments):

    #Assign literal as true or false (depending on first character)
    #Remove variable from c2vDict
    #Decrement Count from countVarDict
    
    variable , negatedVariable = return_var_and_negated_var(variable)

    if variable[0] == '-':

        assignments[variable[1:]] = 1 # Not of True is False
    else:
        assignments[variable] = 0

    #Removing variable from c2vDict by using v2cDict as a helper

    for clause_index in v2cDict[variable]:

        #Check if clause is active or not
        if len(c2vDict[clause_index]) != 0: 

            #Decrement count of var
            countVarDict[variable] -= 1
            
            #If the only variable in the clause is false , then the whole CNF becomes false
            if len(c2vDict[clause_index]) == 1:
                assignments['failiureFlag'] = True
            #Remove variable from clause list
            c2vDict[clause_index].remove(variable)


    if negatedVariable in countVarDict:
        if countVarDict[negatedVariable] !=0:
        
            c2vDict , v2cDict , countVarDict , assignments = modifyClausesWithVariableSetToTrue(negatedVariable,c2vDict , v2cDict , countVarDict , assignments)
        

    return c2vDict , v2cDict , countVarDict , assignments

def read_dimacs_format(filepath):

    #Function for parsing DIMACS format 
    #Returns lines as lists of lists
    #Each list is a line
    with open(filepath) as filePointer:
        dimacs_file_content = filePointer.readlines()

    return dimacs_file_content

def simplifyTautologyAndPrepareDataStructures(rules_file_content):

    # This function needs to be executed oncly once.
    # Because tautology once simplified / removed , will not occur again.
    # This function also intialises all data structures.

    c2vDict = {} # Data Structure to map clause Ids with variables
    v2cDict = {} # Data Structure to map variables with clause Ids
    countVarDict = {} # Data Strucutre to maintain a count of all seen varibles (positive or negative)
    assignments = {} # Data Structure which contains status of current assignments to literals , -1 = Unknown , 1 = True , 0  = False

    #Read all lines
    #Ignore the ones which begin with 'p' or 'c'
    #Check if clause contains tautology
    #Ignore tautology clauses
    #Assign initial values to c2vDict , v2cDict , countVarDict , assignments
    for index,line in enumerate(rules_file_content):
        line = str.rstrip(line)
        if line[0] in ['p','c']:
            continue
        else:
            clause = line
            clause = clause.split(' ')
            clause = clause[:-1] # Getting rid of the 0 at the end
            
            tautologyFlag = False
            dummyDict = {} # Temporary Dict for each clause to remove tautology
            for variable in clause:

                variable , negatedVariable = return_var_and_negated_var(variable)
                
                if negatedVariable in dummyDict:
                    tautologyFlag = True
                

                if variable not in dummyDict :
                    dummyDict[variable] = True

                #Need to add literal to assignment list over here
                if variable[0]=='-':
                    if negatedVariable not in assignments:
                        assignments[negatedVariable] = -1
                else:
                    if variable not in assignments:
                        assignments[variable] = -1


            if tautologyFlag == False: # The clause is not a tautology
                
                c2vDict[index] = clause
                
                for variable in clause:

                    if variable not in v2cDict:

                        v2cDict[variable] = []
                        countVarDict[variable] = 0

                    v2cDict[variable].append(index)                 
                    countVarDict[variable] += 1

    return c2vDict , v2cDict , countVarDict, assignments

def removePureLiterals(c2vDict , v2cDict , countVarDict , assignments):

    for variable  in v2cDict :

        pureLiteral = False # Flag

        variable,negatedVariable = return_var_and_negated_var(variable)
        if negatedVariable in countVarDict:

            if countVarDict[variable] | countVarDict[negatedVariable] != 0 :
                if countVarDict[negatedVariable] == 0:
                    pureLiteral = True

        elif countVarDict[variable]!=0:
            pureLiteral = True

        if pureLiteral == True:


            c2vDict , v2cDict , countVarDict, assignments = modifyClausesWithVariableSetToTrue(variable,c2vDict , v2cDict , countVarDict, assignments)

    return c2vDict , v2cDict , countVarDict, assignments


def removeUnitClauses(c2vDict , v2cDict , countVarDict , assignments):

    for clause_index , clause_var_list in c2vDict.items():

        if len(clause_var_list) == 1:

            variable = clause_var_list[0]
            c2vDict , v2cDict , countVarDict, assignments = modifyClausesWithVariableSetToTrue(variable,c2vDict , v2cDict , countVarDict, assignments)
    
    return c2vDict , v2cDict , countVarDict, assignments

def naiveChooseLiteral(assignments):

    for literal in assignments:
        if assignments[literal] == -1:
            return literal
    return []

def decideSplitAssignForLiteralBasedOnProbDistribution(literal,c2vDict , v2cDict , countVarDict , assignments):

    # Function to implement heuristic 2 i.e to choose to set a variable to True or False during a split based on a probability distribution.

    variable , negatedVariable = return_var_and_negated_var(literal)

    # Calculating metric for positive literal

    #1. Obtaing count of positive variable

    if variable in v2cDict:
        variable_pos_count = countVarDict[variable]
    else:
        variable_pos_count = 0


    #2. Obtaining sum of 2 ** clause lenghts

    non_linear_sum_clause_length_pos = 0
    for clause in v2cDict[variable]:
        non_linear_sum_clause_length_pos += 2 ** len(c2vDict[clause])

    #3. Metric calucation

    metric_variable_pos = (np.log(variable_pos_count) + 1) / non_linear_sum_clause_length_pos


    # Calculating metric for negative literal

    #1. Obtaing count of negative variable

    if negatedVariable in v2cDict:
        variable_neg_count = countVarDict[negatedVariable]
    else:
        variable_neg_count = 0


    #2. Obtaining sum of 2 ** clause lenghts

    non_linear_sum_clause_length_neg = 0
    for clause in v2cDict[negatedVariable]:
        non_linear_sum_clause_length_neg += 2 ** len(c2vDict[clause])

    #3. Metric calucation

    metric_variable_neg = (np.log(variable_neg_count) + 1) / non_linear_sum_clause_length_neg


    # Defining Probability Distribution by Normalization

    probability_literal_true = (metric_variable_pos) / (metric_variable_pos + metric_variable_neg)
    probability_literal_false = 1 - probability_literal_true

    sampled_decision = np.random.choice([True,False],p=[probability_literal_true,probability_literal_false])
    return sampled_decision

def naiveDPLL(c2vDict , v2cDict , countVarDict , assignments):

    #Perform Simplification
    #1. Remove Pure literals
    #2. Remove Unit Clauses
    
    c2vDict , v2cDict , countVarDict , assignments  = removePureLiterals(c2vDict ,v2cDict,countVarDict,assignments)
    c2vDict , v2cDict , countVarDict , assignments = removeUnitClauses(c2vDict,v2cDict,countVarDict, assignments)

    #Simplification caused a false clause , hence our previous split was wrong!
    if 'failiureFlag' in assignments:
        return False,{}

    #Solution Attaintment Check 
    if any(c2vDict.values()) == False:

        return True , assignments

    else:
        literal = naiveChooseLiteral(assignments)
        
        if literal == []:
            return False,{}
        else:

            c2vDictCopy = deepcopy(c2vDict)
            v2cDictCopy = deepcopy(v2cDict)
            countVarDictCopy = deepcopy(countVarDict)
            assignmentsCopy = deepcopy(assignments)

            #decisionFromProbDist = decideSplitAssignForLiteralBasedOnProbDistribution(literal,c2vDict,v2cDict,countVarDict,v2cDict)

            # decisionFromProbDistCopy = deepcopy(decisionFromProbDist)
            # print(decisionFromProbDist)

            # if decisionFromProbDist == True:

            #     c2vDict , v2cDict ,countVarDict , assignments = modifyClausesWithVariableSetToTrue(literal,c2vDict,v2cDict,countVarDict,assignments)
            # else:

            #     c2vDict , v2cDict ,countVarDict , assignments = modifyClausesWithVariableSetToFalse(literal,c2vDict,v2cDict,countVarDict,assignments)

            c2vDict , v2cDict ,countVarDict , assignments = modifyClausesWithVariableSetToTrue(literal,c2vDict,v2cDict,countVarDict,assignments)
            naiveDPLLResult1 = naiveDPLL(c2vDict , v2cDict ,countVarDict , assignments)

            if naiveDPLLResult1[0] == True:
                return naiveDPLLResult1

            else:

                # if decisionFromProbDistCopy == True:

                #     c2vDict , v2cDict, countVarDict , assignments = modifyClausesWithVariableSetToFalse(literal,c2vDictCopy,v2cDictCopy,countVarDictCopy,assignmentsCopy)
                # else:

                #     c2vDict , v2cDict, countVarDict , assignments = modifyClausesWithVariableSetToTrue(literal,c2vDictCopy,v2cDictCopy,countVarDictCopy,assignmentsCopy)

                c2vDict , v2cDict, countVarDict , assignments = modifyClausesWithVariableSetToFalse(literal,c2vDictCopy,v2cDictCopy,countVarDictCopy,assignmentsCopy)
                naiveDPLLResult2 = naiveDPLL(c2vDict , v2cDict, countVarDict , assignments)

                if naiveDPLLResult2[0] == True:
                    return naiveDPLLResult2
                else:
                    return False,{}              



def parseTestSudokus(filename):

    with open(filename) as filePointer:
        file_content = filePointer.readlines()

    dimacs_sudoku_test_set = []
    for sudoku in file_content: 
        
        sudoku = str.rstrip(sudoku)
        dimacs_sudoku = []
        for idx,character in enumerate(sudoku) :
            if character == '.':
                continue
            else:
                row = int(idx/9) + 1
                col = int(idx % 9) + 1
        
                dimacs_string = str(row) + str(col) + character + " " + str(0)
                dimacs_sudoku.append(dimacs_string)

        if len(dimacs_sudoku)!=0:
            dimacs_sudoku_test_set.append(dimacs_sudoku)

    return dimacs_sudoku_test_set

# dimacs_sudoku_test_set = parseTestSudokus('./files/damnhard.sdk.txt')

# for idx,sudoku_puzzle in enumerate(dimacs_sudoku_test_set) :


#     c2vDict , v2cDict , countVarDict , assignments = simplifyTautologyAndPrepareDataStructures(deepcopy(rules_file_content) + deepcopy(sudoku_puzzle))
#     naiveDPLLResult = naiveDPLL(deepcopy(c2vDict),deepcopy(v2cDict),deepcopy(countVarDict),deepcopy(assignments))
#     print(idx,naiveDPLLResult[0])

#rules_file_content = read_dimacs_format('./files/sudoku-rules.txt')
rules_file_content = read_dimacs_format('./files/dummy.txt')
c2vDict , v2cDict , countVarDict, assignments = simplifyTautologyAndPrepareDataStructures(rules_file_content)

print(naiveDPLL(c2vDict,v2cDict,countVarDict,assignments))
