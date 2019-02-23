import numpy as np
import sys

def sysArgParse():
    # Parsing System Arguments for running heuristics
    sysArguments = sys.argv
    strBoolHeuristic1 = (sys.argv[1]).split('=')[-1]
    strBoolHeuristic2 = (sys.argv[2]).split('=')[-1]
    heuristic1Bool = False
    heuristic2Bool = False

    if strBoolHeuristic1 in ['True','true','1']: 
        heuristic1Bool = True
    if strBoolHeuristic2 in ['True','true','1']:
        heuristic2Bool = True

    return heuristic1Bool , heuristic2Bool

def appendSplitCountToFile(splitCountList,heuristic1Bool,heuristic2Bool):

    f= open("./output_files/splitCounts.txt","a+")
    f.write("Heuristic 1  = " + str(heuristic1Bool) + "------" + "Heuristic 2  = " + str(heuristic2Bool) + 
        "\n\n" )
    f.write(str(splitCountList) + "\n\n\n\n")
    f.close()


def return_var_and_negated_var(variable):

    #Helper function to return variable and it's negation
    if(variable[0] == '-'):
        return variable , variable[1:]
    else:
        return variable , '-' + variable

def printSudokuGrid(assignments):

    #Helper function to visualize solved soduko
    M = np.zeros([9,9])
    for l in assignments:
      if assignments[l] == 1:
          i = int(l[0])-1
          j = int(l[1]) - 1
          v = int(l[2]) 
          M[i][j]= v

    for i in range(9):
      for j in range(9):
          print(str(M[i][j]) + " ", end = '')
      print("")

def read_dimacs_format(filepath):

    #Function for parsing DIMACS format 
    #Returns lines as lists of lists
    #Each list is a line
    with open(filepath) as filePointer:
        dimacs_file_content = filePointer.readlines()

    return dimacs_file_content

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
            clause = [s for s in clause if s != ''] # Removing additional spaces
            
            tautologyFlag = False
            dummyDict = {} # Temporary Dict for each clause to remove tautology and duplicates
            for variable in clause:

                if variable in dummyDict: # Checking for Duplicates
                    continue
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