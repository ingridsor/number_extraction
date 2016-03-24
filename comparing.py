import sys, difflib

fileA = sys.argv[1]
fileB = sys.argv[2]

diff_count = 0
num_count = 0

with open(fileA, 'r') as file1:
    with open(fileB, 'r') as file2:
        same = set(file1).intersection(file2)
        
with open(fileA,'r') as file1:
    num_count = len(file1.readlines())

perc_corr = 100 * len(same) / num_count
print('Percentage correct: ', perc_corr)
