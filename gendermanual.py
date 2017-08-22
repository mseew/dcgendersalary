import pandas as pd 
import openpyxl
import unicodecsv as csv

inputfile = 'employees2017gendercleaned.csv'
outputfile = 'employees2017gendercleanedmanual.csv'

df = pd.read_csv(inputfile)
df['firstname'] = df['firstname'].astype(str) 

#Show names that have totally ambiguous/unknown results, based on the followupflag
def showhardnames():
	hardnames = []
	for index, row in df.iterrows():
		if row['followupflag'] == "x":
			hardnames.append(row['firstname'])

	hn = pd.Series(hardnames)
	dfhn = pd.DataFrame({'names':hn.values})
	namefreq = dfhn['names'].value_counts().index.tolist()

	for item in namefreq:
		print item

#Show the names frequency based on followupflag
def showhardfreq():
	print df[df['followupflag']=="x"].firstname.value_counts()

def percentgendered():
	totalgendered = df.genderdecide.count()
	totalnames = df.firstname.count()
	percent = float(totalgendered)/float(totalnames)*100
	print str(percent) + " Percent Gendered"

# Set value of gender decision column for certain common names missed/miscoded by the dictionaries, ex. John returns female
for index, row in df.iterrows():
	firstname = row['firstname'].lower().split(' ',1)[0]
	if firstname in [x.lower() for x in ['John','james', 'william', 'charles','ryan', 'aaron', 'samuel', 'maurice', 'carl', 'carlos', 'Kyle', 'Troy', 'Alan', 'Jamal', 'Allen', 'Leroy', 'Joel', 'Christian', 'Russell', 'Lee', 'Duane', 'Mario','Leon','Julius','Jay','Vernon','Glenn','Fred','Ali','Johnnie','Felix','Jimmy','Julian','Johnny','Neil','Karl','Delonte','Gabriel','Marquis','Francisco','Ray','Julio','Jon','Neal','Lance','Jimmie','Gordon','Cecil','Malik','Glen','Angelo','Cody','Morris','Gene','Raul','Archie','Lamar','Ben','Delante','Danny','Bobby','Joe','Lionel','Marlon','Marques','Myron','Shane','Jamaal', 'Van', 'Cyril','Andy', 'Max', 'Loren','Emil','Elias','Vernard','Denis','Reginal', 'Karim','Anil','Dane','Kareem','Reza','Dino','Shayne','Rico','Carlo','Noel','Yared','Rohan','Jamil','Carroll','Amos','Brady','Fritz','Mike']]:
		df.set_value(index, 'followupflag', '0')
		df.set_value(index, 'genderdecide', 'male')
	elif firstname in [x.lower() for x in ['Karen', 'Nicole', 'Patricia', 'Sharon', 'Danielle', 'Erica', 'Paula', 'Erin', 'Tanya', 'Carol', 'Michele', 'Erika','Ruth', 'Tina', 'Claudia', 'Kristen', 'Grace', 'Toni','Marian','Nadine','Vivian','Belinda','Ericka','Vicki','Nichole','Benita','Bonita','Demetria','Stella','Martina','Tiffani','Raven','Meredith','Eugenia','Octavia','Alfreda','Bianca','Angie','Sonja','Chante','Nichelle','Jelani','Danyelle','Faye','Precious','Luz','Brittani','Tenika','Shanay','Andira','Billie','Doreen','Gia','Justine','Christie','Kari','Ivy','Antonia','Keyonna','Nneka','Trenita','Shawnte','Tiarra','Beth','Georgia','Jo','Becky','Keia','Daniela','Nikkia','Shaniqua','Chantise','Darnice','Regina M','Lovely','Blessilda','Towanna','Kamisha','Guadalupe','Christy','Haley','Burnetta','Bridgit']]:
		df.set_value(index, 'followupflag', '0')
		df.set_value(index,'genderdecide', 'female')

df.to_csv(outputfile, encoding='utf-8')
percentgendered()