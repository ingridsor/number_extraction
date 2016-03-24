import sys, difflib, re

# Result file as first argument, gold file as second
fileA = sys.argv[1]
fileB = sys.argv[2]

num_count = 0  # Counts number of lines, i.e. messages
sugg_nr = []   # Counts where numbers have been suggested
    
with open(fileA, 'r') as file1:
    with open(fileB, 'r') as file2:
        same = set(file1).intersection(file2)
        
with open(fileA,'r') as file1:
    num_count = len(file1.readlines())
    
perc_corr = 100 * len(same) / num_count
print('Total percentage correct: ', perc_corr)
