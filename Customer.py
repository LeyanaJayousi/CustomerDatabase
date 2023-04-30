r"""
mySQL Homework
Leyana Jayousi
120200153
"""

import sqlite3 as sq
import os.path
import os

from datetime import datetime

# ---------------------------------- Funcs --------------------------------------


def prestigious(threshold):
    r""" Returns query corresponding to rows in table BRANCH where liability is greater than defined threshold.
    """
    query = f"""SELECT * FROM BRANCH WHERE liability > {threshold}"""
    return query


def mini(threshold):
    r"""
    """
    query = f"""SELECT * FROM BRANCH WHERE cash_hold < {threshold}"""
    return query


def result1(table):
    r"""
    """
    query = f"""SELECT branch_name, liability FROM ({table})"""
    return query


def result2(table_1, table_2):
    r"""
    """
    query = f"""SELECT branch_name, liability FROM ({table_1} UNION {table_2})"""
    return query


def result3():
    r"""
    """
    query = f"""SELECT * FROM CUSTOMER CROSS JOIN LOAN"""
    return query


def result4(table_1, table_2):
    query = f"""SELECT * FROM ({table_1}) as TAB INNER JOIN {table_2} ON TAB.branch_id=LOAN.branch_id"""
    return query


# ----------------------------------- Main ---------------------------------------
if os.path.exists('bank.db'):
    os.remove('bank.db')

# Question 1
db_name = "bank"
db = sq.connect(db_name + '.db')  # create connection to bank.db


# Question 2
cur = db.cursor()  # create cursor
# create tables
cur.execute("CREATE TABLE CUSTOMER(customer_id integer PRIMARY KEY, name varchar, lastname varchar, registration_date date, score integer)")
cur.execute("CREATE TABLE BRANCH(branch_id integer PRIMARY KEY, branch_name varchar, cash_hold float, foundation_date date, liability float)")
cur.execute("CREATE TABLE LOAN(loan_id integer PRIMARY KEY, amount float, branch_id integer, customer_id integer, FOREIGN KEY(branch_id) REFERENCES BRANCH(branch_id), FOREIGN KEY(customer_id) REFERENCES CUSTOMER(customer_id))")

# verification (if tables exist)
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
print('--------------- Verification (question 2) --------------------')
print(f"Table names in {db_name}:")
print([tab for (tab,) in cur.fetchall()])
print("------------------------------------------------------\n\n")


# Question 3
data_customer = [
    (1, 'Leyana', 'Jayousi', datetime.strptime(r'2018-12-01', r'%Y-%m-%d'), 49),
    (2, 'Faisal', 'Jayousi', datetime.strptime(r'2022-12-14', r'%Y-%m-%d'), 100),
    (3, 'Alfonso', 'MonteCarlo', datetime.strptime(r'2001-09-28', r'%Y-%m-%d'), 91),
    (4, 'Leonardo', 'DiCaprio', datetime.strptime(r'2008-04-28', r'%Y-%m-%d'), 85),
    (5, 'Lara', 'Croft', datetime.strptime(r'2017-04-07', r'%Y-%m-%d'), 66)
]

data_branch = [
    (10, 'Istanbul', 3001.95, datetime.strptime(r'2019-04-21', r'%Y-%m-%d'), 55.5),
    (11, 'Antalya', 8401.12, datetime.strptime(
        r'2019-04-27', r'%Y-%m-%d'), 1002.9),
    (12, 'Konya', 1951.78, datetime.strptime(r'2009-04-21', r'%Y-%m-%d'), 1700),
    (13, 'Izmir', 19008.45, datetime.strptime(
        r'2009-04-21', r'%Y-%m-%d'), 21090.41),
    (14, 'Ankara', 1578.5, datetime.strptime(r'2009-04-21', r'%Y-%m-%d'), 1)
]

data_loan = [
    (100, 45000, 10, 1),
    (101, 46000, 11, 1),
    (102, 45000, 12, 4),
    (103, 48000, 14, 5),
    (104, 45000, 13, 2),
]

# insert data into tables & commit
cur.executemany("INSERT INTO CUSTOMER VALUES(?, ?, ?, ?, ?)", data_customer)
cur.executemany("INSERT INTO BRANCH VALUES(?, ?, ?, ?, ?)", data_branch)
cur.executemany("INSERT INTO LOAN VALUES(?, ?, ?, ?)", data_loan)
db.commit()

# verification
print('--------------- Verification (question 3) --------------------')
records = cur.execute("""SELECT name from CUSTOMER""").fetchall()
print(records)
print("------------------------------------------------------\n\n")


# Question 4
query_prestigious = prestigious(1.5)
query_mini = mini(50000)
query_Result1 = result1(query_prestigious)
queryResult2 = result2(mini(50000), prestigious(1.5))
queryResult3 = result3()
queryResult4 = result4(prestigious(1.5), "LOAN")


# verification
print('--------------- Verification (question 4) --------------------')
print('\t -PRESTIGIOUS(1.5)')
print(db.execute(query_prestigious).fetchall())
print("------------------------------------------------------\n\n")
print('\n\t -MINI(50000)')
print(db.execute(query_mini).fetchall())
print("------------------------------------------------------\n\n")
print('\n\t -RESULT1')
print(db.execute(query_Result1).fetchall())
print("------------------------------------------------------\n\n")
print('\n\t -RESULT2')
print(db.execute(queryResult2).fetchall())
print("------------------------------------------------------\n\n")
print('\n\t -RESULT3')
print("------------------------------------------------------\n\n")
print(db.execute(queryResult3).fetchall())
print('\n\t -RESULT4')
print("------------------------------------------------------\n\n")
print(db.execute(queryResult4).fetchall())
print("------------------------------------------------------\n\n")


# Question 5
def question5(table, information):
    query = f"""SELECT {information} FROM (({table}) as TAB INNER JOIN LOAN ON TAB.branch_id=LOAN.branch_id) as TABB INNER JOIN CUSTOMER ON TABB.customer_id=CUSTOMER.customer_id"""
    return query


customer_info = 'name, lastname, registration_date, score, amount'
non_prestigious_query = f"""SELECT * FROM BRANCH WHERE liability <= 1.5"""
query_LOAN_NONPRES = question5(non_prestigious_query, customer_info)
print('\n\t Question 5')
print(db.execute(query_LOAN_NONPRES).fetchall())
print("------------------------------------------------------\n\n")


# Question 6
def question6(year):
    query = f"""SELECT SUM(LOAN.amount) FROM LOAN INNER JOIN BRANCH ON LOAN.branch_id=BRANCH.branch_id WHERE strftime('%Y', BRANCH.foundation_date)='{year}'"""
    return query


print('\n\t Question 6')
print(db.execute(question6(2019)).fetchall())
print("------------------------------------------------------\n\n")
