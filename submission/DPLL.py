from copy import deepcopy
import numpy as np
from helperfunctions import *
from heuristics import *

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

    # Retrieve all unassigned variables
    unassigned = [key for key, value in assignments.items() if value == -1]
    if len(unassigned) == 0 : # No unassigned variable
        return []
    else:
        return np.random.choice(unassigned) # Picking a random variable to split on


def singleStepSimplificationFunction(c2vDict,v2cDict,countVarDict,assignments):
    #1. Remove Pure literals

    c2vDict , v2cDict , countVarDict , assignments  = removePureLiterals(c2vDict , \
                                                            v2cDict,countVarDict,assignments)
    #2. Remove Unit Clauses
    c2vDict , v2cDict , countVarDict , assignments = removeUnitClauses(c2vDict, \
                                                            v2cDict,countVarDict, assignments)

    return c2vDict , v2cDict , countVarDict , assignments

def repeatedSimplificationFunction(c2vDict,v2cDict,countVarDict,assignments):

    while True: # Loop for performing repeated simplification

        #Deep copies for ensuring repeated simplification
        c2vDictNonSimplified = deepcopy(c2vDict)
        v2cDictNonSimplified = deepcopy(v2cDict)
        countVarDictNonSimplified = deepcopy(countVarDict)
        assignmentsNonSimplified = deepcopy(assignments)

        #1. Remove Pure literals

        c2vDict , v2cDict , countVarDict , assignments  = removePureLiterals(c2vDict , \
                                                            v2cDict,countVarDict,assignments)
        #2. Remove Unit Clauses
        c2vDict , v2cDict , countVarDict , assignments = removeUnitClauses(c2vDict, \
                                                            v2cDict,countVarDict, assignments)

        if c2vDictNonSimplified != c2vDict or v2cDictNonSimplified != v2cDict or \
            countVarDictNonSimplified != countVarDict or assignmentsNonSimplified != assignments:

            #Keep simplifying
            continue
        else:
            #No more simplifcations possible
            break

    return c2vDict , v2cDict , countVarDict , assignments

def naiveDPLL(c2vDict , v2cDict , countVarDict , assignments,number_of_splits_list = [0], singleStepSimplification = True ,heuristic1 = False, heuristic2 = False,trackerList=[]):

    #Just for plotting the graph

    # nonEmptyClauseCount = determineNonEmptyClauses(c2vDict)
    # if nonEmptyClauseCount <= number_of_splits_list[1]:
    #     trackerList.append((nonEmptyClauseCount,number_of_splits_list[0]))
    #     number_of_splits_list[1] = nonEmptyClauseCount


    #Perform Simplification
    
    if singleStepSimplification == True:
        c2vDict , v2cDict , countVarDict , assignments = singleStepSimplificationFunction(c2vDict , v2cDict , countVarDict , assignments)
    else:
        c2vDict , v2cDict , countVarDict , assignments = repeatedSimplificationFunction(c2vDict , v2cDict , countVarDict , assignments)
     
    #Simplification caused a false clause , hence our previous split was wrong!
    if 'failiureFlag' in assignments:
        return False,{},number_of_splits_list,trackerList

    #Solution Attaintment Check 
    if any(c2vDict.values()) == False:

        return True , assignments , number_of_splits_list,trackerList

    else:
        
        branchToFalse = False # This is a flag which can be used to branch to false first and then true when backtracking.
        # If we want to use heuristic 1:
        if heuristic1 == True:
            variable = jeroslowEpsilonGreedy2(c2vDict, v2cDict, assignments, epsilon = 0.05, topKpercent = 0.1)
            
            if variable[0] == '-':
                branchToFalse = True
                literal = variable[1:]
            else:
                literal = variable
            
        
        # Now we need to see if heuristic 2 is toggled to True

        elif heuristic2 == True:
            
            literal = naiveDLCSLiteralSelection(countVarDict,assignments)
            decisionFromProbDist = decideSplitAssignForLiteralBasedOnProbDistribution(literal,c2vDict,v2cDict,countVarDict,v2cDict)

            if decisionFromProbDist == True:
                branchToFalse = False
            else:
                branchToFalse = True

        # Else, not using any heuristic:
        else:
            literal = naiveChooseLiteral(assignments)
       
        # At this step , literal has been chosen 
        # Deepcopy - as the same will be used again to branch differently
        branchToFalseCopy = deepcopy(branchToFalse)
                 

        if literal == []:
            return False,{},number_of_splits_list,trackerList
        else:

            c2vDictCopy = deepcopy(c2vDict)
            v2cDictCopy = deepcopy(v2cDict)
            countVarDictCopy = deepcopy(countVarDict)
            assignmentsCopy = deepcopy(assignments)

            # Increment split count
            number_of_splits_list[0] += 1
            
                
            if branchToFalse == False:

                c2vDict , v2cDict ,countVarDict , assignments = modifyClausesWithVariableSetToTrue(literal,c2vDict,v2cDict,countVarDict,assignments)
            else:
                c2vDict , v2cDict ,countVarDict , assignments = modifyClausesWithVariableSetToFalse(literal,c2vDict,v2cDict,countVarDict,assignments)

            # Recursive call
            
            naiveDPLLResult1 = naiveDPLL(c2vDict , v2cDict ,countVarDict , assignments,number_of_splits_list = number_of_splits_list,singleStepSimplification = singleStepSimplification ,heuristic1 = heuristic1,heuristic2 = heuristic2,trackerList=trackerList)
            
            if naiveDPLLResult1[0] == True:
                return naiveDPLLResult1

            else:

                # Increment split count
                number_of_splits_list[0] += 1
                if branchToFalseCopy == False:

                    c2vDict , v2cDict, countVarDict , assignments = modifyClausesWithVariableSetToFalse(literal,c2vDictCopy,v2cDictCopy,countVarDictCopy,assignmentsCopy)
                else:

                    c2vDict , v2cDict, countVarDict , assignments = modifyClausesWithVariableSetToTrue(literal,c2vDictCopy,v2cDictCopy,countVarDictCopy,assignmentsCopy)
                
                # Recursive Call
                naiveDPLLResult2 = naiveDPLL(c2vDict , v2cDict ,countVarDict , assignments,number_of_splits_list= number_of_splits_list,singleStepSimplification = singleStepSimplification ,heuristic1 = heuristic1,heuristic2 = heuristic2,trackerList=trackerList)
                
                if naiveDPLLResult2[0] == True:
                    return naiveDPLLResult2
                else:
                    return False,{},number_of_splits_list,trackerList