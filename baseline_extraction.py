# Number recognition project, Speech Technology DT2112
# By Ingrid Sör, Manon Knoertzer and Carina Rawein
# A script for acquiring a "baseline" of number extraction from ASR

# For filesystem support
import os, re

def cut_extras(number):
    number_cut = number.replace(' ','').replace('(','').replace(')','')
    return number_cut

# Folder where the transcriptions reside as xml files
# TO BE ADAPTED TO YOUR OWN COMPUTER
folder = "/home/ingrid/Documents/Utbildning/MPLT/speech/project/xml_data"

files = os.listdir(folder)
# To remove possible ~-files from Emacs made when making test files...
files = [x for x in files if x.endswith('.b.xml')]
j = 0 # Counter for found numbers
res_file = 'results_baseline.txt' # file for results
print("Transcript files to go through: ",files)

# For all transcript files in folder
for file in files:
    # Setting empty transcription string for each file
    transcription = ''
    number = ''
    nr_found = False
    
    # Change directory to the path with xml files
    os.chdir(folder)
    with open(file, 'r', encoding='ISO-8859-1') as fin:
        print("Now looking at file: ", file)

        # Finding name of subject for saving of result.
        s = re.search(r'(.*)\.b\.xml',file)
        subject = s.group(1)
        print('Subject: ', subject)

        for line in fin:

            # Finding transcription
            if re.search(r"<t>.*</t>",line) != None:
                t = re.search(r"<t>(?P<trans>.*)</t>",line)
                # Concatenating recognised words with spaces in between
                transcription += t.group('trans') + ' '
        
        print('Transcription: ', transcription)

        # Find number
        # Needs to find numbers with spaces in between as the numbers
        # are sometimes split up by the ASR and then separated by spaces
        # in script when finding transcription
        n = re.search(r"\d+(?: \d+)*", transcription)
            
        if n != None:
            nr_found = True
            number = cut_extras(n.group())
    
    if nr_found == True:
        
        # Check results folder exists or create
        if not os.path.isdir('../results'):
            os.makedirs('../results')
        os.chdir('../results')
        
        # If a result file exists, give new name (first time only)
        i = 1
        while os.path.isfile(res_file) and j == 0:
            res_file = 'results_baseline' + str(i) + '.txt'
            i += 1
        
        # Appending phone number to result file
        to_print = subject + ', ' + number + '\n'
        with open(res_file,'a') as fout:
            fout.write(to_print)
            
        print("Phone number found: ",number,'\n')
        j += 1
    else:
        print('No phone number found.\n')
