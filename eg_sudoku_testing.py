from DPLL import *
from helperfunctions import * 

#Parse system arguments (command line args)
heuristic1Bool , heuristic2Bool = sysArgParse()

rules_file_content = read_dimacs_format('./files/sudoku-rules.txt')
sudoku_puzzle = read_dimacs_format('./files/sudoku-example.txt')
c2vDict , v2cDict , countVarDict, assignments = simplifyTautologyAndPrepareDataStructures(rules_file_content + sudoku_puzzle)
result = naiveDPLL(c2vDict,v2cDict,countVarDict,assignments,number_of_splits_list= [0],singleStepSimplification = True, heuristic1 = heuristic1Bool,heuristic2=heuristic2Bool)
print("Solvable ? : " + str(result[0]))
print("Number of Splits = " + str(result[2][0]))
printSudokuGrid(result[1])