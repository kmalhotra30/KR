from DPLL import *
from helperfunctions import * 

#Parse system arguments (command line args)
heuristic1Bool , heuristic2Bool ,inputFileName = sysArgParse(filename=True)

rules_file_content = read_dimacs_format(inputFileName)
c2vDict , v2cDict , countVarDict, assignments = simplifyTautologyAndPrepareDataStructures(rules_file_content)
dpllResult = naiveDPLL(c2vDict,v2cDict,countVarDict,assignments,number_of_splits_list= [0],singleStepSimplification = True, heuristic1 = heuristic1Bool,heuristic2=heuristic2Bool,trackerList=[])
writeOutputDimacs(inputFileName,dpllResult[1])