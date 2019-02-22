from DPLL import *




dimacs_sudoku_test_set = parseTestSudokus('./files/damnhard.sdk.txt')
rules_file_content = read_dimacs_format('./files/dummy.txt')

# for idx,sudoku_puzzle in enumerate(dimacs_sudoku_test_set) :

#     c2vDict , v2cDict , countVarDict , assignments = simplifyTautologyAndPrepareDataStructures(deepcopy(rules_file_content) + deepcopy(sudoku_puzzle))
#     naiveDPLLResult = naiveDPLL(deepcopy(c2vDict), deepcopy(v2cDict), 
#     							deepcopy(countVarDict), deepcopy(assignments), 
#     							heuristic1 = False, heuristic2 = True)
#     print(idx,naiveDPLLResult[0])
#     printSudokuGrid(naiveDPLLResult)


# rules_file_content = read_dimacs_format('./files/dummy.txt')
c2vDict , v2cDict , countVarDict, assignments = simplifyTautologyAndPrepareDataStructures(rules_file_content)

print(naiveDPLL(c2vDict,v2cDict,countVarDict,assignments))
