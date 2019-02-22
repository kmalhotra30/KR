
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

    for literal in assignments:
        if assignments[literal] == -1:
            return literal
    return []


def naiveDPLL(c2vDict , v2cDict , countVarDict , assignments, heuristic1 = False, heuristic2 = False):

    #Perform Simplification
    #1. Remove Pure literals
    
    c2vDict , v2cDict , countVarDict , assignments  = removePureLiterals(c2vDict , \
    													v2cDict,countVarDict,assignments)
    #2. Remove Unit Clauses
    c2vDict , v2cDict , countVarDict , assignments = removeUnitClauses(c2vDict, \
    													v2cDict,countVarDict, assignments)

    #Simplification caused a false clause , hence our previous split was wrong!
    if 'failiureFlag' in assignments:
        return False,{}

    #Solution Attaintment Check 
    if any(c2vDict.values()) == False:

        return True , assignments

    else:
        # If we want to use heuristic 1:
        if heuristic1 == True:
            literal = jeroslowEpsilonGreedy(c2vDict, v2cDict, assignments, epsilon = 0.1, topKpercent = 0.1)
        # Else, do NOT use heuristic 1:
        else:
            literal = naiveChooseLiteral(assignments)
        
        if literal == []:
            return False,{}
        else:

            c2vDictCopy = deepcopy(c2vDict)
            v2cDictCopy = deepcopy(v2cDict)
            countVarDictCopy = deepcopy(countVarDict)
            assignmentsCopy = deepcopy(assignments)

            # If we want to use heuristic 2:
            # if heuristic2 == True:
            #     decisionFromProbDist = decideSplitAssignForLiteralBasedOnProbDistribution(literal,c2vDict,v2cDict,countVarDict,v2cDict)

            #     decisionFromProbDistCopy = deepcopy(decisionFromProbDist)
            #     print(decisionFromProbDist)

            #     if decisionFromProbDist == True:

            #         c2vDict , v2cDict ,countVarDict , assignments = modifyClausesWithVariableSetToTrue(literal,c2vDict,v2cDict,countVarDict,assignments)
            #     else:

            #         c2vDict , v2cDict ,countVarDict , assignments = modifyClausesWithVariableSetToFalse(literal,c2vDict,v2cDict,countVarDict,assignments)
            
            #     # Else, do NOT use heuristic 2
            # else:
            c2vDict , v2cDict ,countVarDict , assignments = modifyClausesWithVariableSetToTrue(literal,c2vDict,v2cDict,countVarDict,assignments)
            naiveDPLLResult1 = naiveDPLL(c2vDict , v2cDict ,countVarDict , assignments)
            
            if naiveDPLLResult1[0] == True:
                return naiveDPLLResult1

            else:

                # if heuristic2 == True:
                #     if decisionFromProbDistCopy == True:

                #         c2vDict , v2cDict, countVarDict , assignments = modifyClausesWithVariableSetToFalse(literal,c2vDictCopy,v2cDictCopy,countVarDictCopy,assignmentsCopy)
                #     else:

                #         c2vDict , v2cDict, countVarDict , assignments = modifyClausesWithVariableSetToTrue(literal,c2vDictCopy,v2cDictCopy,countVarDictCopy,assignmentsCopy)
                # else:
                c2vDict , v2cDict, countVarDict , assignments = modifyClausesWithVariableSetToFalse(literal,c2vDictCopy,v2cDictCopy,countVarDictCopy,assignmentsCopy)
                naiveDPLLResult2 = naiveDPLL(c2vDict , v2cDict, countVarDict , assignments)
                
                if naiveDPLLResult2[0] == True:
                    return naiveDPLLResult2
                else:
                    return False,{}    