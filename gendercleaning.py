import pandas as pd 
import openpyxl
import xlrd
import unicodecsv as csv
from leGenderary import leGenderary as lg

options = { 'male'          : 'male', 
            'female'        : 'female',
            'androgynous'   : 'androgynous',
            'unknown'       : 'unknown',
            'maleConfirm'   : 'male needs confirmation',
            'femaleConfirm' : 'female needs confirmation',
            'dict1'         : 'LeGenderary/dictionaries/dict1.txt',
            'dict2'         : 'LeGenderary/dictionaries/dict2.txt',
            'customDict'    : 'LeGenderary/dictionaries/customDict.txt',
            'bingAPIKey'    : 'ABC123478ZML'
          }

gender = lg(options)

# Function to onvert Excel data to csv and encode it in UTF-8 because these special characters will give us text trouble later
def csv_from_excel(xlsxfile):

    wb = xlrd.open_workbook(xlsxfile)
    sh = wb.sheet_by_name('fortableau')
    csv_file = open('employees2017gender.csv', 'wb')
    wr = csv.writer(csv_file, quoting=csv.QUOTE_ALL, encoding='utf-8')

    for rownum in xrange(sh.nrows):
        wr.writerow(sh.row_values(rownum))

    csv_file.close()

#Converting our excel file that was the result of the genderdata.py script
csv_from_excel('employees2017gender.xlsx')

df = pd.read_csv('employees2017gender.csv', parse_dates=True)
df.rename(columns = 
	{'First Name':'firstname', 
	'Last Name' : 'lastname', 
	'Type Appt':'typeappt',
	'Position Title':'postitle',
	'Hire Date':'hiredate'
	}, inplace=True)
df['firstname'] = df['firstname'].astype(str)

#Create empty list for a variable that will be the ultimate choice of gender for each record
genderdecide = []

maleresult = [['male','unknown'],['male','androgynous'],['unknown','male'],['androgynous','male']]
femaleresult = [['female','unknown'],['female','androgynous'],['unknown','female'],['androgynous','female']]

#Decide gender for cases where the genderdata.py script returned ambiguous (but one-gender) results.
for index, row in df.iterrows():
	dictguess = row['dictionaryguess']
	phonguess = row['phoneticguess']

	guesses = [dictguess,phonguess]

	if dictguess==phonguess and dictguess != 'unknown' and dictguess != 'androgynous':
		genderdecide.append(dictguess)

	elif guesses in maleresult:
		genderdecide.append('male')
	elif guesses in femaleresult:
		genderdecide.append('female')	
	else:
		genderdecide.append("")
		df.set_value(index, 'followupflag', "x")

# Append gender decision column to DataFrame
df['genderdecide']=genderdecide

# Go through list of first names, and rerun dictionary/phonetic lookup for those which have middle initials
for index, row in df.iterrows():
	if row['followupflag'] == "x":
		firstname = row['firstname'].lower()
		firstnametrim = row['firstname'].lower().split(' ',1)[0]
		
		if firstname != firstnametrim:
			dguess = gender.determineFromDictionary(firstnametrim)
			df.set_value(index,'dictionaryguess', dguess)

			pguess = gender.determineFromPhonetic(firstnametrim)
			df.set_value(index,'phoneticguess', pguess)

			guesses = [dguess, pguess]	
			print guesses

			if set(['male','female']).issubset(set(guesses)):
				df.set_value(index, 'followupflag','x')
			
			elif dguess==pguess and dictguess != 'unknown' and dictguess != 'androgynous':
				df.set_value(index,'genderdecide', dguess)
				df.set_value(index,'followupflag',"0")

			elif guesses in maleresult:
				df.set_value(index,'genderdecide', 'male')
				df.set_value(index,'followupflag',"0")
			
			elif guesses in femaleresult:
				df.set_value(index,'genderdecide', 'female')	
				df.set_value(index,'followupflag',"0")

			else:
				df.set_value(index,'followupflag', "x")

csvoutput = "employees2017gendercleaned.csv"
df.to_csv(csvoutput, encoding='utf-8')

#print df.head(50)

#dng = df[['firstname','dictionaryguess', 'phoneticguess','followupflag','genderdecide']]


#print hn.head(50)
#print dng.sample(n=50)
#print dng.count()


