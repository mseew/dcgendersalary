import pandas as pd 
import openpyxl

df = pd.read_excel('employees2017gender.xlsx', parse_dates=True)
df.rename(columns = 
	{'First Name':'firstname', 
	'Last Name' : 'lastname', 
	'Type Appt':'typeappt',
	'Position Title':'postitle',
	'Hire Date':'hiredate'
	}, inplace=True)
df['firstname'] = df['firstname']
genderdecide = []

for index, row in df.iterrows():
	dictguess = row['dictionaryguess']
	phonguess = row['phoneticguess']
	maleresult = [['male','unknown'],['male','androgynous'],['unknown','male'],['androgynous','male']]
	femaleresult = [['female','unknown'],['female','androgynous'],['unknown','female'],['androgynous','female']]
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

df['genderdecide']=genderdecide

for index, row in df.iterrows():
	firstname = str(row['firstname']).decode('utf-8').lower()
	if firstname in [x.lower() for x in ['John','james', 'william', 'charles','ryan', 'aaron', 'samuel', 'maurice', 'carl', 'carlos', 'Kyle', 'Troy', 'Alan', 'Jamal', 'Allen', 'Leroy', 'Joel', 'Christian', 'Russell', 'Lee', 'Duane', 'Mario','Leon','Julius','Jay','Vernon','Glenn','Fred','Ali','Johnnie','Felix','Jimmy','Julian','Johnny','Neil','Karl','Delonte','Gabriel','Marquis','Francisco','Ray','Julio','Jon','Neal','Lance','Jimmie','Gordon','Cecil','Malik','Glen','Angelo','Cody','Morris','Gene','Raul','Archie','Lamar','Ben','Delante','Danny','Bobby','Joe','Lionel','Marlon','Marques','Myron','']]:
		df.set_value(index, 'followupflag', '0')
		df.set_value(index, 'genderdecide', 'male')
	elif firstname in [x.lower() for x in ['Karen', 'Nicole', 'Patricia', 'Sharon', 'Danielle', 'Erica', 'Paula', 'Erin', 'Tanya', 'Carol', 'Michele', 'Erika','Ruth', 'Tina', 'Claudia', 'Kristen', 'Grace', 'Toni','Marian','Nadine','Vivian','Belinda','Ericka','Vicki','Nichole','Benita','Bonita','Demetria','Stella']]:
		df.set_value(index, 'followupflag', '0')
		df.set_value(index,'genderdecide', 'female')

#print df.head(50)

#dng = df[['firstname','dictionaryguess', 'phoneticguess','followupflag','genderdecide']]
hardnames = []
for index, row in df.iterrows():
	if row['followupflag'] == "x":
		hardnames.append(row['firstname'])

hn = pd.Series(hardnames)
dfhn = pd.DataFrame({'names':hn.values})
namefreq = dfhn['names'].value_counts().index.tolist()
for item in namefreq:
	print item
#print hn.head(50)
#print dng.sample(n=50)
#print dng.count()



