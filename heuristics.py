from helperfunctions import *
import numpy as np
from operator import itemgetter
from decimal import *

def jeroslowEpsilonGreedy2(c2vDict, v2cDict, assignments, epsilon = 0.1, topKpercent = 0.1):

    # This heuristic implements an epsilon-greedy version
    # of Jeroslow-Wang. With an epsilon-probability, we choose 
    # a random variable from the top k-ranked variables, 
    # instead of the highest ranked candidate 

    # 0. Retrieve all unassigned variables
    unassigned = [key for key, value in assignments.items() if value == -1]
    JWscore = []

    # 1. For each unassigned variable, calculate its JW-score 
    #   *** J(x) = for each clause where x appears, sum : 2 ^ (-1 * len(clause))
    for literal in unassigned:
        
        var , negatedVar = return_var_and_negated_var(literal)
        if var in v2cDict:
            
            J = 0
            for clauseID in v2cDict[var]: 
                         
                J += pow(2, (-1) * len(c2vDict[clauseID]))
            JWscore.append((var, J))

        if negatedVar in v2cDict:
            
            J = 0
            for clauseID in v2cDict[negatedVar]: 
                         
                J += pow(2, (-1) * len(c2vDict[clauseID]))
            JWscore.append((negatedVar, J))

    # 2. Sort the variables in ascending order
    JWscore = sorted(JWscore, key = itemgetter(1))
    # 3. Reverse the sorted list.
    JWscore = JWscore[::-1]

    # 4. Make a selection based on chance
    if (np.random.choice([True, False], p = [epsilon, 1 - epsilon])):
        # 4. Choose a random variable from the topKpercent 
        topK = int(len(JWscore) * topKpercent)
        if topK !=0 :
            return JWscore[np.random.choice(range(topK))][0]
        else:
            return JWscore[0][0]
    else:
        # 5. If we choose to use JW-ranking, simply pick the best variable
        return JWscore[0][0]

def naiveDLCSLiteralSelection(countVarDict,assignments):

    # Retreive all unassigned items
    unassigned = [key for key, value in assignments.items() if value == -1]
    
    # This variable will contain the final chosen literal. 
    chosenLiteral = ""
    # Max sum tracker , initialized with -1.
    max_sum = -1

    # Loop for stroing the counts
    for literal in unassigned:

        pos_var , negated_var = return_var_and_negated_var(literal)
        # Retreive positive count from countVarDict
        pos_count = 0
        if pos_var in countVarDict:
            pos_count = countVarDict[pos_var]
        # Retrieve negative count from countVarDict
        neg_count = 0
        if negated_var in countVarDict:
            neg_count = countVarDict[negated_var]

        if pos_count + neg_count > max_sum:
            max_sum = pos_count + neg_count
            chosenLiteral = literal

    return chosenLiteral 


def decideSplitAssignForLiteralBasedOnProbDistribution(literal, c2vDict , v2cDict , countVarDict , assignments):

    # Function to implement heuristic 2 i.e to choose to set a 
    #variable to True or False during a split based on a probability distribution.

    variable , negatedVariable = return_var_and_negated_var(literal)

    # Calculating metric for positive literal

    #1. Obtaining count of positive variable

    if variable in v2cDict:
        variable_pos_count = countVarDict[variable]
    else:
        variable_pos_count = 0


    #2. Obtaining sum of 2 ** clause lenghts
    if variable_pos_count!=0:

        non_linear_sum_clause_length_pos = 0
        for clause in v2cDict[variable]:
            non_linear_sum_clause_length_pos += 2 ** len(c2vDict[clause])
        #3. Metric calucation
        metric_variable_pos = Decimal(np.sqrt(variable_pos_count)) / Decimal(non_linear_sum_clause_length_pos)
    else:
        metric_variable_pos = 0

    

    # Calculating metric for negative literal

    #1. Obtaining count of negative variable

    if negatedVariable in v2cDict:
        variable_neg_count = countVarDict[negatedVariable]
    else:
        variable_neg_count = 0


    #2. Obtaining sum of 2 ** clause lenghts
    if variable_neg_count!= 0:
    
        non_linear_sum_clause_length_neg = 0
        for clause in v2cDict[negatedVariable]:
            non_linear_sum_clause_length_neg += 2 ** len(c2vDict[clause])

        #3. Metric calucation
        metric_variable_neg = Decimal(np.sqrt(variable_neg_count)) / Decimal(non_linear_sum_clause_length_neg)
    else:
        metric_variable_neg = 0


    # Defining Probability Distribution by Normalization

    # If metric for both is 0 , then first set to true and then false
    if metric_variable_pos == 0 and metric_variable_neg == 0:
        probability_literal_true  = 1
    else:
        probability_literal_true = (metric_variable_pos) / (metric_variable_pos + metric_variable_neg)
    probability_literal_false = 1 - probability_literal_true

    sampled_decision = np.random.choice([True,False],p=[probability_literal_true,probability_literal_false])
    return sampled_decision