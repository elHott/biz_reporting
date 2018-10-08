

import sqlite3

print('Create database')
# create a database to hold the PCN data

conn = sqlite3.connect('PCN_db.sqlite')
cur = conn.cursor()

# create table from MS People data dump
cur.execute('DROP TABLE IF EXISTS MSP_PCNs')

cur.execute('''
CREATE TABLE MSP_PCNs ('Level 2 Mgr' TEXT, 'Level 3 Mgr' TEXT,
    'Func Exec' TEXT, 'Cost Center' TEXT, 'COGS Opex' TEXT, Email TEXT,
      PCN INTEGER, 'Open Pos Ind' TEXT,
      'Future start' TEXT, 'On Leave' TEXT, MSPeople TEXT)''')

fname = input('Enter MSPeople file name: ')
# shortcut for easy testing file entry
if len(fname) < 1:
    fname = '2018.09.28-MSP_ELH-copy.txt'
fh = open(fname)
lst = list()
count = 0

for line in fh:
    if line.startswith('Y'):
        pieces = line.split('\t')
        # problem: title field can have a comma in it, as does the requistion location col AA
        # using tab (\t) as delimiter seems to work
        reports_to_level_2 = pieces[1]
        reports_to_level_3 = pieces[2]
        func_exec_summary = pieces[6]
        cost_center = pieces[9]
        cogs_opex = pieces[10]
        email = pieces[11]
        position_number = pieces[12]
        open_position_ind = pieces[17]
        future_start_date = pieces[18]
        on_leave = pieces[31]
        count = count + 1

        cur.execute('''INSERT INTO MSP_PCNs ('Level 2 Mgr', 'Level 3 Mgr',
            'Func Exec', 'Cost Center', 'COGS Opex', Email, PCN,
            'Open Pos Ind', 'Future start', 'On Leave', MSPeople)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1)''', (reports_to_level_2,
            reports_to_level_3, func_exec_summary, cost_center, cogs_opex,
            email, position_number, open_position_ind, future_start_date, on_leave,))

        # checkpoint for testing
        # if count == 12: break
    else: continue

# then put stuff in DB
conn.commit()

print("There were", count, "lines in the file with Y as the first character.")

# create table from admins spreadsheets data dump
conn = sqlite3.connect('PCN_db.sqlite')
cur = conn.cursor()

# create table from admin's spreadsheets data dump
cur.execute('DROP TABLE IF EXISTS Admins_PCNs')

cur.execute('''
CREATE TABLE Admins_PCNs ('New Hire Name' TEXT, 'Direct' TEXT,
      PCN INTEGER, 'Start Date' TEXT, 'Soure Tab' TEXT, Disposition TEXT)''')

# when creating file add Source Tab column followed by Disposition column
fname = input('Enter Admins PCN list file name: ')
# shortcut for easy testing file entry
if len(fname) < 1:
    fname = 'Admins_PCN_List.txt'
fh2 = open(fname)
lst2 = list()
count2 = 0


for line in fh2:
    if not line.startswith('Industry'):
        pieces2 = line.split('\t')
        # problem: title field can have a comma in it, as does the requistion location col AA
        # using tab (\t) as delimiter seems to work
        new_hire = pieces2[0]
        start_date = pieces2[1]
        position_number2 = pieces2[2]
        direct = pieces2[7]
        tab = pieces2[12]
        disposition = pieces2[13]
        count2 = count2 + 1

        cur.execute('''INSERT INTO Admins_PCNs ('New Hire Name', 'Direct',
            PCN, 'Start Date', 'Soure Tab', Disposition)
            VALUES (?, ?, ?, ?, ?, ?)''', (new_hire, direct, position_number2,
            start_date, tab, disposition))

        # checkpoint for testing
        # if count == 12: break
    else: continue

# then put stuff in DB
conn.commit()

print("There were", count2, "lines in the file pulled from admin's spreadsheets.")


# create table from Temp PCN data from recruiting (ENG PCN Report)
conn = sqlite3.connect('PCN_db.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Recruiting_PCNs')

cur.execute('''
CREATE TABLE Recruiting_PCNs (PCN INTEGER, 'Prim Recruiter' TEXT, 'Req status' TEXT,
        'Furthest Status' TEXT, 'Open Pos Ind' TEXT, 'Start Date' TEXT)''')

# when creating file advisable to sort by Func Exec Summary before dumping
fname = input('Enter Recruiting Temp PCN list file name: ')
# shortcut for easy testing file entry
if len(fname) < 1:
    fname = 'Eng_PCN_dump.txt'
fh3 = open(fname)
lst3 = list()
count3 = 0

for line in fh3:
    if not line.startswith('Position'):
        pieces3 = line.split('\t')
        # problem: title field can have a comma in it, as does the requistion location col AA
        # using tab (\t) as delimiter seems to work
        position_number3 = pieces3[0]
        open_pos = pieces3[24]
        recruiter = pieces3[26]
        req_status = pieces3[34]
        furthest_status = pieces3[43]
        start_date3 = pieces3[45]
        count3 = count3 + 1

        cur.execute('''INSERT INTO Recruiting_PCNs (PCN, 'Prim Recruiter',
            'Req status', 'Furthest Status','Open Pos Ind', 'Start Date')
            VALUES (?, ?, ?, ?, ?, ?)''', (position_number3,  recruiter, req_status,
            furthest_status, open_pos, start_date3))

        # checkpoint for testing
        # if count == 12: break
    else: continue

# then put stuff in DB
conn.commit()

print("There were", count3, "lines in the file from recruiting.")

# Now write the queries to isolate those PCNs which are candidates to be closed


