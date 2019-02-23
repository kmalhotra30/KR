from DPLL import *
from helperfunctions import * 

#Parse system arguments (command line args)
heuristic1Bool , heuristic2Bool = sysArgParse()

rules_file_content = read_dimacs_format('./files/sudoku-rules.txt')
dimacs_sudoku_test_set = parseTestSudokus('./files/1000 sudokus.txt')

# List for storing split counts 
splitCountList = []

for idx,sudoku_puzzle in enumerate(dimacs_sudoku_test_set) :

    c2vDict , v2cDict , countVarDict , assignments = simplifyTautologyAndPrepareDataStructures(rules_file_content + sudoku_puzzle)

    dpllResult = naiveDPLL(c2vDict,v2cDict,countVarDict,assignments,number_of_splits_list= [0],singleStepSimplification = True, heuristic1 = heuristic1Bool,heuristic2=heuristic2Bool)

    # Prininting index and result on terminal , to keep a track on the current status
    print("Sudoku Number " + str(idx + 1))
    print("Solvable ? : " + str(dpllResult[0]))
    print("Number of Splits = " + str(dpllResult[2][0]))

    # Uncomment the below line to print the sudoku grid
    # printSudokuGrid(dpllResult[1])
    splitCountList.append(dpllResult[2][0])

appendSplitCountToFile(splitCountList,heuristic1Bool,heuristic2Bool)

