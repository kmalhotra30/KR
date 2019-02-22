from DPLL import *
          

rules_file_content = read_dimacs_format('./files/dummy.txt')
c2vDict , v2cDict , countVarDict, assignments = simplifyTautologyAndPrepareDataStructures(rules_file_content)

print(c2vDict)
print(v2cDict)
print(assignments)


print("Chose " , jeroslowEpsilonGreedy(c2vDict, v2cDict, 
	assignments, epsilon = 0.1, topKpercent = 0.1))

# print(naiveDPLL(c2vDict,v2cDict,countVarDict,assignments, heuristic1 = True))