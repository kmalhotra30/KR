from helperfunctions import *
import numpy as np
from operator import itemgetter
from decimal import *

def jeroslowEpsilonGreedy(c2vDict, v2cDict, assignments, epsilon = 0.1, topKpercent = 0.1):

    # This heuristic implements an epsilon-greedy version
    # of Jeroslow-Wang. With an epsilon-probability, we choose 
    # a random variable from the top k-ranked variables, 
    # instead of the highest ranked candidate 

    # 0. Retrieve all unassigned variables
    unassigned = [key for key, value in assignments.items() if value == -1]
    print("unassigned are:", unassigned)
    JWscore = []

    # 1. For each unassigned variable, calculate its JW-score 
    #   *** J(x) = for each clause where x appears, sum : 2 ^ (-1 * len(clause))
    for variable in unassigned:
        J = 0
        for clauseID in v2cDict[variable]: 
            # print("variable ", variable, " is in ", c2vDict[clauseID])          
            J += pow(2, (-1) * len(c2vDict[clauseID]))
        JWscore.append((variable, J))

    # print("JW-scores:")
    # print(JWscore)

    # 2. Sort the variables in descending order
    JWscore = sorted(JWscore, key = itemgetter(1))

    # print("JW-scores (sorted):")
    print(JWscore)

    # 3. Make a selection based on chance
    if (np.random.choice([True, False], p = [epsilon, 1 - epsilon])):
        # 4. Choose a random variable from the topKpercent 
        topK = int(len(JWscore) * topKpercent)
        return JWscore[np.random.choice(range(topK))][0]
    else:
        # 5. If we choose to use JW-ranking, simply pick the best variable
        return JWscore[0][0]





def decideSplitAssignForLiteralBasedOnProbDistribution(literal, c2vDict , v2cDict , countVarDict , assignments):

    # Function to implement heuristic 2 i.e to choose to set a 
    #variable to True or False during a split based on a probability distribution.

    variable , negatedVariable = return_var_and_negated_var(literal)

    # Calculating metric for positive literal

    #1. Obtaing count of positive variable

    if variable in v2cDict:
        variable_pos_count = countVarDict[variable]
    else:
        variable_pos_count = 0


    #2. Obtaining sum of 2 ** clause lenghts

    non_linear_sum_clause_length_pos = 0
    for clause in v2cDict[variable]:
        non_linear_sum_clause_length_pos += 2 ** len(c2vDict[clause])

    #3. Metric calucation

    metric_variable_pos = (np.sqrt(variable_pos_count)) / non_linear_sum_clause_length_pos


    # Calculating metric for negative literal

    #1. Obtaing count of negative variable

    if negatedVariable in v2cDict:
        variable_neg_count = countVarDict[negatedVariable]
    else:
        variable_neg_count = 0


    #2. Obtaining sum of 2 ** clause lenghts

    non_linear_sum_clause_length_neg = 0
    for clause in v2cDict[negatedVariable]:
        non_linear_sum_clause_length_neg += 2 ** len(c2vDict[clause])

    #3. Metric calucation

    metric_variable_neg = (np.sqrt(variable_neg_count)) / non_linear_sum_clause_length_neg


    # Defining Probability Distribution by Normalization

    probability_literal_true = (metric_variable_pos) / (metric_variable_pos + metric_variable_neg)
    probability_literal_false = 1 - probability_literal_true

    sampled_decision = np.random.choice([True,False],p=[probability_literal_true,probability_literal_false])
    return sampled_decision