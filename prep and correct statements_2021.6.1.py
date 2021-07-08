#-------------------------------------------------------------------------------------------#
# Python script for performing spelling and other corrections based on glossary
# (after temporarily removing geonames, spellchecking, eyeballing, etc.)
#
## DATA:        xx
## OUTPUT:      xx
#
## AUTHORS:     Pamela Paxton and Nicholas E. Reith
## DATE:        14 March 2019
## UPDATED:     14 March 2019
#
## Revised and Adapted by Brad R. Fulton 2021.6.1
#
#-------------------------------------------------------------------------------------------#

# Note: This script is only a suggestion for how to use the glossary to clean mission statements.
#      It is not a complete program
# Note: Prior to using the glossary we undertook other basic cleaning. 
#      The cleaning we undertook included:
#       - Strip all extra white space, especially at beginning and end of the text string
#       - Convert all letters to lower case
#       - Add spaces around some punctuation
#       - Remove other non-essential punctuation
# You can use the "prep_text" function below or skip this step and move to glossary further below
# However, please note that some of the corrections (especially the last 355 lines in the glossary)
# depend on the text being properly prepped, e.g.,  'under - represent' to 'underrepresent'

import numpy as np  # Numpy for calculations
import os           # OS for operating system functions
import pandas as pd # Pandas for data manipulation
import shutil       # High-level file operations

pd.options.display.max_colwidth = 1000


#BRF: Assign the working directory for the program 
os.chdir('C:\\Users\\fulton\\Documents\\Datasets\\990PF Data') 

def prep_text(x):
    x = x.str.strip()                   # Remove extra white space
    x = x.str.lower()                   # Convert all letters to lowercase
    x = x.str.replace('\t',' ')         # Replace tabs with spaces
#   x = x.str.replace('\[sc\]', ' ;; ') # Replace semicolons with 2 semicolons
    x = x.str.replace(';',' ;; ')       # Replace semicolons with 2 semicolons
#   x = x.str.replace('\,',' ; ')       # comma = semicolon
#   x = x.str.replace('\[c\]',' ; ')    # comma = semicolon
    x = x.str.replace(',',' ; ')        # Replace commas with semicolons
#   x = x.str.replace('\[dq\]',' " ')   # double quote with spaces
    x = x.str.replace('"',' " ')        # Add spaces around double quotes
#   x = x.str.replace('\[sq\]', " ' ")  # single quote with spaces
#   x = x.str.replace("\'", " ' ")      # apostrophe with spaces
    x = x.str.replace("'", " ' ")       # Add spaces around single quotes / apostrophes
#   x = x.str.replace("\`", " ' ")      # weird apostrophe as apostrophe with spaces
    x = x.str.replace("`", " ' ")       # Replace reverse apostrophe with an apostrophe with spaces
#   x = x.str.replace('\_', ' \_ ')     # underscore with spaces
    x = x.str.replace('_', ' _ ')       # Add spaces around underscores
#   x = x.str.replace('\-', ' - ')      # dash with spaces
    x = x.str.replace('-', ' - ')       # Add spaces around dashes
    x = x.str.replace(':', ' : ')       # Add spaces around colons
    x = x.str.replace('!', ' ! ')       # Add spaces around exclamation marks
    x = x.str.replace('?', ' ? ')       # Add spaces around question marks
#   x = x.str.replace('\.', ' . ')      # period with spaces
    x = x.str.replace('.', ' . ')       # Add spaces around periods
    x = x.str.replace('(', ' ( ')       # Add spaces around left parentheses
    x = x.str.replace(')', ' ) ')       # Add spaces around right parentheses
    x = x.str.replace('@', ' @ ')       # Add spaces around at signs
#   x = x.str.replace('\$', ' $ ')      # dollar with spaces
    x = x.str.replace('$', ' $ ')       # Add spaces around dollar signs
#   x = x.str.replace('\*', ' * ')      # asterisk with spaces
    x = x.str.replace('*', ' * ')       # Add spaces around asterisks
#   x = x.str.replace('\&', ' & ')      # and with spaces
    x = x.str.replace('&', ' & ')       # Add spaces around ampersands
#   x = x.str.replace('\#', ' # ')      # hash with spaces
    x = x.str.replace('#', ' # ')       # Add spaces around hashtags
#   x = x.str.replace('\%', ' % ')      # percent with spaces
    x = x.str.replace('%', ' % ')       # Add spaces around percent signs
#   x = x.str.replace('\+', ' + ')      # plus with spaces
    x = x.str.replace('+', ' + ')       # Add spaces around plus signs
    x = x.str.replace('([0-9]+)', r' \1 ') # Add spaces around all digits/numbers
#   x = x.str.replace(r'[^0123456789abcdefghijklmnopqrstuvwxyz;"\'_\-:!?\.()@$*&#%+ ]', ' ') 
    x = x.str.replace(r'[^0123456789abcdefghijklmnopqrstuvwxyz;"\'_\-:!?.()@$*&#%+ ]', ' ') 
                                        # Replace any characters other than those listed here with a space
    x = " " + x + " "                   # Add a space at beginning and end of the text string
    x = x.str.replace('([ ]+)', ' ')    # Replace multiple spaces with one space
    return(x)


df_mission = pd.read_csv("Mission Data_Raw (Test).csv", low_memory=False)

# Apply prepping function above to the mission text
#df_mission['mission_original'] = df_mission['mission']
df_mission['mission_prepped'] = prep_text(df_mission['mission_original']) 

print(df_mission)

#
# Next
# Correcting misspelled words and other patterns
#

# Read in the glossary used to correct the words
#BRF: Why do I need pd.DataFrame(), when I did not need it for df_mission?
df_glossary = pd.DataFrame(pd.read_csv('Glossary (Test).csv', header=0, sep=',',index_col=None, dtype='unicode')) # Import data

# Adding a space to the beginning and end of each word and fixed word (fix) in the glossary
df_glossary['word'] = ' ' + df_glossary['word'] + ' '
df_glossary['fix']  = ' ' + df_glossary['fix']  + ' '

#BRF: I'm not sure what the line of code below is for?
df_glossary.reset_index(inplace=True)

# Applyinng glossary corrections
def correct_text(x,g): #BRF: x is the mission statements and g is the glossary 
    for i in range(0,g['index'].max()+1): #BRF: I added "+1" to include the last term in the glossary
        print(str(i) + ': ' + str(g.iloc[i,1]) + ' -> ' + str(g.iloc[i,2]))
        x = x.str.replace(g.iloc[i,1],g.iloc[i,2]) #BRF: replace word with fix
        df_mission['mission_corrected'] = x
    df_mission.to_csv("Mission Data_Corrected (Test).csv",sep=',',index=False,na_rep="")
    #return x
    #print(x)

df_mission['mission_prepped'] = correct_text(df_mission['mission_prepped'],df_glossary)
