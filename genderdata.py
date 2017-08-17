from leGenderary import leGenderary as lg
import pandas as pd 
import openpyxl

options = { 'male'          : 'male', 
            'female'        : 'female',
            'androgynous'   : 'androgynous',
            'unknown'       : 'unknown',
            'maleConfirm'   : 'male needs confirmation',
            'femaleConfirm' : 'female needs confirmation',
            'dict1'         : 'dictionaries/dict1.txt',
            'dict2'         : 'dictionaries/dict2.txt',
            'customDict'    : 'dictionaries/customDict.txt',
            'bingAPIKey'    : 'ABC123478ZML'
          }

gender = lg(options)

dforig = pd.read_csv('employees2017.csv', parse_dates=True)
dforig.drop(dforig.columns[8], axis=1, inplace=True)
dforig['First Name'] = dforig['First Name'].astype(str)

#dfslice = dforig.head(n=30)
phoneticguess=[]
dictionaryguess=[]
followupflag=[]

for row in dforig['First Name']:
	
	dguess = gender.determineFromDictionary(row)
	print row + " " + dguess
	dictionaryguess.append(dguess)
	
	pguess = gender.determineFromPhonetic(row)
	print row + " " + gender.determineFromPhonetic(row)
	phoneticguess.append(pguess)
	
	guesses = [dguess, pguess]	
	if set(['male','female']).issubset(set(guesses)):
		followupflag.append('x')
	else:
		followupflag.append('')

#gpetersguess=[]
#for row in dforig['First Name']:
#	print row + " " + gender.determineFromGPeters(row)
#	gpetersguess.append(
#		gender.determineFromGPeters(row)
#		)

dforig['dictionaryguess'] = dictionaryguess
dforig['phoneticguess'] = phoneticguess
#dforig['gpetersguess'] = gpetersguess
dforig['followupflag'] = followupflag

#print dforig
writer = pd.ExcelWriter("employees2017gender.xlsx")
dforig.to_excel(writer,"fortableau")
writer.save()