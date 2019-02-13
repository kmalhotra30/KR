def return_var_and_negated_var(variable):

	#Helper function to return variable and it's negation
	if(variable[0] == '-'):
		return variable , variable[1:]
	else:
		return variable , '-' + variable

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
					break

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
rules_file_content = read_dimacs_format('./files/sudoku-rules.txt')
c2vDict , v2cDict , countVarDict , assignments = simplifyTautologyAndPrepareDataStructures(rules_file_content)

print(len(c2vDict))
print(len(v2cDict))
print(len(countVarDict))
print(len(assignments))

def removePureLiterals(c2vDict , v2cDict , countVarDict , assignments):

	for variable  in v2cDict :

		pureLiteral = False # Flag

		variable,negatedVariable = return_var_and_negated_var(variable)
		if negatedVariable in countVarDict:

			if countVarDict[negatedVariable] == 0:
				pureLiteral = True
		else:
			pureLiteral = True

		if pureLiteral == True:

			#Assign literal as true or false (depending on first character)
			#Remove variable from c2vDict
			#Decrement Count from countVarDict

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

	return c2vDict , v2cDict , countVarDict, assignments



c2vDict , v2cDict , countVarDict , assignments = removePureLiterals(c2vDict , v2cDict , countVarDict , assignments)

print(len(c2vDict))
print(len(v2cDict))
print(len(countVarDict))
print(len(assignments))


def removeUnitClauses(c2vDict , v2cDict , countVarDict , assignments):

	for clause_index , clause_var_list in c2vDict.items():

		if len(clause_var_list) == 1:

			#Assign unit clause literal to true or false (depending on first character)
			var = clause_var_list[0]
			if var[0] == '-':
				assignments[var[1:]] = 0 # Not of False is True
			else:
				assignments[var] = 1

			#Decrement the count of var
			countVarDict[var] -= 1
			clause_var_list = []

			#Update c2vDict
			c2vDict[clause_index] = clause_var_list

	
	return c2vDict , v2cDict , countVarDict, assignments

c2vDict , v2cDict , countVarDict , assignments = removeUnitClauses(c2vDict , v2cDict , countVarDict , assignments)

print(len(c2vDict))
print(len(v2cDict))
print(len(countVarDict))
print(len(assignments))






