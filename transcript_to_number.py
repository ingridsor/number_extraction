# Number recognition project, Speech Technology DT2112
# By Ingrid Sör, Manon Knoertzer and Carina Rawein

# Works only for wav files at the moment

# For filesystem support
import os, re


def cut_extras(number):
    number = number.replace(' ','').replace('(','').replace(')','')
    return number

# Folder where the transcriptions reside as xml files
folder = "/home/ingrid/Documents/Utbildning/MPLT/speech/project/xml_data"

# Dictionary for country codes (European + US and Canada)
# Format: country dialing code:(0,min_numbers,max_numbers)
# OR country dialing code:(1,length1,length2,length3,etc) Note: greatest length last
# 0 as first item of language list means min and max values next
# 1 as first item of language list means all possible lengths listed
cc_dict = {376:[1,6,9],43:[0,4,13],32:[0,8,9],359:[0,7,9],385:[0,8,9],357:[1,8],45:[1,8],372:[0,7,8],298:[1,6],358:[0,5,12],33:[1,9],350:[1,8],49:[0,3,12],30:[1,10],36:[0,8,9],354:[1,7,9],353:[0,7,10],39:[0,8,12],371:[1,8],423:[0,6,12],370:[1,8],352:[0,6,9],356:[1,8],377:[0,8,9],31:[1,10],47:[0,4,12],48:[1,9],351:[1,9],40:[1,9],378:[0,6,12],421:[1,9],386:[1,8],34:[1,9],46:[0,6,9],41:[1,9],44:[1,7,9,10],1:[1,10]
}

files = os.listdir(folder)
# To remove possible ~-files from Emacs made when making test files...
files = [x for x in files if not x.endswith('~')]
j = 0 # Counter for found numbers
res_file = 'results.txt' # file for results
print("Transcript files to go through: ",files)

# For all transcript files in folder
for file in files:
    # Setting empty transcription string for each file
    transcription = ''
    number = ''
    nr_found = False
    
    # Change directory to the path with xml files
    os.chdir(folder)
    with open(file, 'r') as fin:
        print("Now looking at file: ", file)

        # Finding name of subject for saving of result.
        s = re.search(r'(.*).xml',file)
        subject = s.group(1)
        print('Subject: ', subject)

        for line in fin:


            # Finding transcription
            if re.search(r"<t>.*</t>",line) != None:
                t = re.search(r"<t>(?P<trans>.*)</t>",line)
                # Concatenating recognised words with spaces in between
                transcription += t.group('trans') + ' '
        
        print('Transcription: ', transcription)


        # First check for number with + or 00, 4-20 digits long
        # In that case a number is considered to be found. -> Check country code and adjust length.
        # If no +/00, check for "phone number phrases" and set following digits to number.
        # Other numbers might be phone numbers, but should not be suggested to user,
        # as it is too uncertain they would be correct.

        # First check for number with + or 00, any length
        if re.search(r"(\s|^)(\+|00) ?( \d+)*", transcription) != None:
            
            # Check for one of the specific country codes (in front of any number of digits)
            for item in cc_dict:
                item = str(item)
                n1 = re.search(r"""(?:\s|^)          # Starting with either whitespace or start of line
                                   ((?:(?:\+)|(?:00))    # Either + or 00
                                   {})\ ?                # String 'item', i.e. country code
                                   \d+(\ \d+)*           # The rest of the number including possible spaces
                                   """.format(item), transcription, re.VERBOSE)
            
                # If there is a number found with country code first
                if n1 != None:
                    number = n1.group()
                    number = cut_extras(number)
                
                    if n1.group(1) != None:
                        country_code = int(n1.group(1).replace('+','').replace('00','')) # Removing + and make into int
                        print("Found a country code from the dict!")
                        print("Country code is: ", country_code)
                        
                        # Below are two ways of finding number length and number if a country code has been found.
                        # If the number after country code is longer than the length specified in number
                        # dict, the number is "cut" at the end to conform to country specific length.
            
                        # In the case of min and max values for length (0 as first item in country list)
                        if cc_dict[country_code][0] == 0:
                            minl = str(cc_dict[country_code][1])
                            maxl = str(cc_dict[country_code][2])
                            n2 = re.search(r"""(?:\s|^)            # Starting with either whitespace or start of line
                                               ((?:(?:\+)|(?:00))  # Either + or 00
                                               {0})                # String 'item', i.e. country code
                                               \d{{{1},{2}}}       # The rest of the number has x-y digits
                                               """.format(country_code,minl,maxl), number, re.VERBOSE)
                
                        # In the case of all possible length values listed in dictionary (1 as first item in language list)
                        # Finds the longest number acceptable in that country
                        if cc_dict[country_code][0] == 1:
                            #found = [] # List to save all possible numbers
                            for item in cc_dict[country_code][1:]: # Trying all possibilities
                                n2 = re.search(r"""(?:\s|^)            # Starting with either whitespace or start of line
                                                  ((?:(?:\+)|(?:00))  # Either + or 00
                                                  {0})                # String 'item', i.e. country code
                                                  \d{{{1}}}           # The rest of the number has x digits
                                                  """.format(country_code,item), number, re.VERBOSE)
                                
                        # If a number is found in either of the two regex searches above
                        if n2 != None:
                            nr_found = True
                            number = n2.group(0)
                            print("Number found after country code search: ", number)

                        break # Breaks if number with country code is found

        else:
            # Checking for a key phrase to indicate there will be a number coming up
            print(transcription)
            n1 = re.search(r"""number\ is\                 # With number directly following
                               |call\ me(?:\ on|at)\         # -||-
                               |(?:my|phone)\ number\D{1,15}? # Every number following 1-15 chars after "phone number" or "my number"
                               (                           # Catch number
                               \(?                         # Number possibly starts with parenthesis (for some reason)
                               \+?                         # Number possibly starts with +
                               \d+                         # Number (first part or whole number)
                               \)?                         # Number possibly ends with parenthesis
                               (?:\ \(?\d+\)?)*            # Possibly numbers following space
                               )                        
                               """,transcription, flags=re.I|re.X) # Ignoring case
            
            if n1 != None:
                number = n1.group(1)
                number = cut_extras(number)
                n2 = re.search(r"(\d{6,10})", number)
                if n2 != None:
                    print('Number was found after "phone phrases"! ',n2)
                    number = n2.group(1)
                    nr_found = True
            
        '''# Finding number in case of no country code
        else:
                # 6-10 digits as a default length, as the typical case would probably be a Swedish
                # number when no country code is given (i.e. in our specific study)
                n = re.search(r"(\b\d{6,10}\b)",transcription) 
                # Add: In this case, print "warning" for user, that it is not as certainly a phone number...
                if n != None:
                    number = n.group()
        '''
                    
    # Maybe add a check if cc_regex gives a longer number than that of regex with specific
    # country number length or the default regex. This could give indication to user
    # that it is perhaps not the correct number - do they want the longer/shorter number
    # instead??
    
    if nr_found == True:
        
        # Check results folder exists or create
        if not os.path.isdir('../results'):
            os.makedirs('../results')
        os.chdir('../results')
        
        # If a result file exists, give new name (first time only)
        i = 1
        while os.path.isfile(res_file) and j == 0:
            res_file = 'results' + str(i) + '.txt'
            i += 1
        
        # Appending phone number to result file
        to_print = subject + ', ' + number + '\n'
        with open(res_file,'a') as fout:
            fout.write(to_print)
            
        print("Phone number found: ",number,'\n')
        j += 1
    else:
        print('No phone number found.\n')
