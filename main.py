from copy import deepcopy
import numpy as np
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

# print(c2vDict)
# print(v2cDict)
# print(countVarDict)
# print(assignments)

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


# c2vDict , v2cDict , countVarDict , assignments = removePureLiterals(c2vDict , v2cDict , countVarDict , assignments)

# print(len(c2vDict))
# print(len(v2cDict))
# print(len(countVarDict))
# print(len(assignments))


def removeUnitClauses(c2vDict , v2cDict , countVarDict , assignments):

	for clause_index , clause_var_list in c2vDict.items():

		if len(clause_var_list) == 1:

			variable = clause_var_list[0]
			c2vDict , v2cDict , countVarDict, assignments = modifyClausesWithVariableSetToTrue(variable,c2vDict , v2cDict , countVarDict, assignments)
	
	return c2vDict , v2cDict , countVarDict, assignments

# print("Removing unit clauses")
# c2vDict , v2cDict , countVarDict , assignments = removeUnitClauses(c2vDict , v2cDict , countVarDict , assignments)

# print((c2vDict))
# print((v2cDict))
# print((countVarDict))
# print((assignments))


# print("Removing pure literals")
# c2vDict , v2cDict , countVarDict , assignments = removePureLiterals(c2vDict , v2cDict , countVarDict , assignments)

# print((c2vDict))
# print((v2cDict))
# print((countVarDict))
# print((assignments))

def naiveChooseLiteral(assignments):

	for literal in assignments:
		if assignments[literal] == -1:
			return literal
	return []

# def naiveDPLL(c2vDict , v2cDict , countVarDict , assignments):

# 	#Perform Simplification
# 	#1. Remove Pure literals
# 	#2. Remove Unit Clauses
# 	print("Before Simplification")
# 	print(c2vDict)
# 	print(v2cDict)
# 	print(countVarDict)
# 	print(assignments)

# 	c2vDict , v2cDict , countVarDict , assignments = removePureLiterals(deepcopy(c2vDict),deepcopy(v2cDict),deepcopy(countVarDict),deepcopy(assignments))

# 	c2vDict , v2cDict , countVarDict , assignments = removeUnitClauses(deepcopy(c2vDict), deepcopy(v2cDict) , deepcopy(countVarDict) , deepcopy(assignments))
	
# 	print("After Simplification")
# 	print(c2vDict)
# 	print(v2cDict)
# 	print(countVarDict)
# 	print(assignments)


# 	#Check if solution has been attained
# 	#If it has , then return assignments
# 	#Else peform recursion

# 	#Solution Attaintment Check 
# 	if any(c2vDict.values()) == False and 'failiureFlag' not in assignments:

# 		print("triggers in if " ,assignments)
# 		return True , assignments
# 	elif 'failiureFlag' not in assignments:


# 		#Assign a variable to True
# 		#Change Clauses
# 		#Recurse

# 		c2vDictCopy , v2cDictCopy , countVarDictCopy , assignmentsCopy = deepcopy(c2vDict) , deepcopy(v2cDict) , deepcopy(countVarDict) , deepcopy(assignments)
# 		literal = naiveChooseLiteral(deepcopy(assignments))
# 		print("literal " + str(literal) + " has been picked")
# 		if literal != []:
# 			print(literal)
# 			c2vDict , v2cDict , countVarDict , assignments = modifyClausesWithVariableSetToFalse(literal,deepcopy(c2vDictCopy) , deepcopy(v2cDictCopy) , deepcopy(countVarDictCopy) , deepcopy(assignmentsCopy))
# 			naiveDPLLResult = naiveDPLL(deepcopy(c2vDict) , deepcopy(v2cDict) , deepcopy(countVarDict) , deepcopy(assignments))
# 			#If solution has not been attained , then assign the variable to False
# 			#Change Clauses
# 			#Check

# 			if naiveDPLLResult[0] == False:

# 				print("setting " + str(literal) + "to true")
# 				c2vDict , v2cDict , countVarDict , assignments = modifyClausesWithVariableSetToTrue(literal,deepcopy(c2vDictCopy) , deepcopy(v2cDictCopy) , deepcopy(countVarDictCopy) , deepcopy(assignmentsCopy))
# 				naiveDPLLResult = naiveDPLL(deepcopy(c2vDict) , deepcopy(v2cDict) , deepcopy(countVarDict) , deepcopy(assignments))
# 				if naiveDPLLResult[0] == False and 'failiureFlag' in naiveDPLLResult[1]:
# 					print("False case")
# 					return False, {}
# 				else:
# 					return True,naiveDPLLResult[1]	

# 			else:
# 				print("arvid")
# 				return True, naiveDPLLResult[1]

# 		else:
# 			print("False case")
# 			return False,{}

# 	else:
# 		return False , {}




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

			c2vDict , v2cDict ,countVarDict , assignments = modifyClausesWithVariableSetToFalse(literal,c2vDict,v2cDict,countVarDict,assignments)
			
			naiveDPLLResult1 = naiveDPLL(c2vDict , v2cDict ,countVarDict , assignments)

			if naiveDPLLResult1[0] == True:
				return naiveDPLLResult1

			else:
				c2vDict , v2cDict, countVarDict , assignments = modifyClausesWithVariableSetToTrue(literal,c2vDictCopy,v2cDictCopy,countVarDictCopy,assignmentsCopy)

				naiveDPLLResult2 = naiveDPLL(c2vDict , v2cDict, countVarDict , assignments)

				if naiveDPLLResult2[0] == True:
					return naiveDPLLResult2
				else:
					return False,{}				 


rules_file_content = read_dimacs_format('./files/sudoku-rules.txt')
c2vDict , v2cDict , countVarDict , assignments = simplifyTautologyAndPrepareDataStructures(rules_file_content)
naiveDPLLResult = naiveDPLL(c2vDict,v2cDict,countVarDict,assignments)

M = np.zeros([9,9])
for l in naiveDPLLResult[1]:
	if naiveDPLLResult[1][l] == 1:
		i = int(l[0])-1
		j = int(l[1]) - 1
		v = int(l[2]) - 1
		M[i][j]= v

for i in range(9):
	for j in range(9):
		print(str(M[i][j]) + " ",end = '')
	print("")