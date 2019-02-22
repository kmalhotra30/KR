from DPLL import *




dimacs_sudoku_test_set = parseTestSudokus('./files/damnhard.sdk.txt')
rules_file_content = read_dimacs_format('./files/dummy.txt')

for idx,sudoku_puzzle in enumerate(dimacs_sudoku_test_set) :

    c2vDict , v2cDict , countVarDict , assignments = simplifyTautologyAndPrepareDataStructures(deepcopy(rules_file_content) + deepcopy(sudoku_puzzle))
    naiveDPLLResult = naiveDPLL(deepcopy(c2vDict), deepcopy(v2cDict), 
    							deepcopy(countVarDict), deepcopy(assignments), 
    							heuristic1 = False, heuristic2 = True)
    print(idx,naiveDPLLResult[0])
    printSudokuGrid(naiveDPLLResult)


# rules_file_content = read_dimacs_format('./files/dummy.txt')
rules_file_content = read_dimacs_format('./files/sudoku-rules.txt')
sudoku_puzzle = read_dimacs_format('./files/sudoku-example.txt')

c2vDict , v2cDict , countVarDict, assignments = simplifyTautologyAndPrepareDataStructures(rules_file_content + sudoku_puzzle)
result = naiveDPLL(c2vDict,v2cDict,countVarDict,assignments, heuristic1 = True)
print(result[0])
printSudokuGrid(result)

<<<<<<< HEAD
print(naiveDPLL(c2vDict,v2cDict,countVarDict,assignments))
=======
c2vDict , v2cDict , countVarDict, assignments = simplifyTautologyAndPrepareDataStructures(rules_file_content + sudoku_puzzle)
result = naiveDPLL(c2vDict,v2cDict,countVarDict,assignments, heuristic1 = False)
print(result[0])
printSudokuGrid(result)
>>>>>>> 142b4a4fc4da5af897dfd12fe2f72c956e89b991
