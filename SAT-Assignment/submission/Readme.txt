In order to run this module , hit './SAT -Sn inputfile' in the terminal.

Incase an error occurs , then ensure that the 'SAT' shell script is executable. To do so hit 'chmod +x SAT' in the terminal.

-S1 , -S2 , -S3 corresponds to DPLL , DPLL + heuristic 1 , DPLL + heuristic 2 and 'inputfile' corresponds to the input file containing the SAT problem in DIMACS format.

For example: './SAT -S2  input.txt' - This will execute DPLL + heuristic 1 for the SAT problem in 'input.txt' file.

Note : -
1) We assume that this module is being executed on a regular linux envoirnment. 
2) We assume that the input file and this module are in the same directory.