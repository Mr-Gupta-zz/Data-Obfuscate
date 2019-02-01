import json
from pprint import pprint

file_name = raw_input("Enter the full file location from the current directory:\n")
#loading data to be obfuscated
with open(file_name) as f:
    data = json.load(f)

PII = ['Name', 'Address', 'SSN', 'Phone', 'Email', 'UserName']

#loading fake data from csv
import csv
ifile = open('FakeNames.csv', 'rb')
reader = csv.reader(ifile)

#mainting lists of the different fields
f_names = []
f_addresses = []
f_ssns = []
f_phones = []
f_email = []
f_users = []

#populating lists
line_count = 0
for row in reader:
	if line_count > 60:
		break
	elif line_count == 0:
		header = row
	else:
		f_names.append(row[0])
		f_addresses.append(row[1])
		f_email.append(row[2])
		f_users.append(row[3])
		f_phones.append(row[4])
		f_ssns.append(row[5])

	line_count += 1

#counters to move ahead in the lists
#to maintain entropy
name_count = 0
add_count = 0
ssn_count = 0
phone_count = 0
email_count = 0
user_count = 0

#maps to cross-reference same names
name_map = {}
user_map = {}
email_map = {}

#new json
obfus_data = []

#starting obfuscation
for ent in data:
	'''
	As names can have same first name and different last names
	I jave mapped every first name in the original data to a 
	particular fake name from the fake name list
	This way we can maintain data integrity
	'''
	#first_name = ent['Name'].split(' ')[0]
	if ent['Name'] in name_map:
		ent['Name'] = name_map[ent['Name']]
	else:
		name_map[ent['Name']] = f_names[name_count]
		ent['Name'] = f_names[name_count]
		name_count += 1


	ent['Address'] = f_addresses[add_count]
	#incrementing these counts mean moving to a new value in the lists
	add_count += 1 

	ent['SSN'] = f_ssns[ssn_count]
	ssn_count += 1
	
	#obfuscating just the last 7 digits. 
	phone_num = ent['Phone'][:4]
	phone_num += f_phones[phone_count][4:]
	ent['Phone'] = phone_num
	phone_count += 1

	if ent['Email'] in email_map:
		ent['Email'] = email_map[ent['Email']]
	else:
		email_map[ent['Email']] = f_email[email_count]
		ent['Email'] = f_email[email_count]
		email_count += 1

	if ent['UserName'] in user_map:
		ent['UserName'] = user_map[ent['UserName']]
	else:
		user_map[ent['UserName']] = f_users[user_count]
		ent['UserName'] = f_users[user_count]
		user_count += 1

	#adding the new data entry to our json
	obfus_data.append(ent)

#writing json to a file
with open('obfuscation.json', 'w') as outfile:
    json.dump(obfus_data, outfile, indent=4,
                      separators=(',', ': '), ensure_ascii=False)


print("File written as 'obfuscation.json")






