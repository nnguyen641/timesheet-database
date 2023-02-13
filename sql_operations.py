# module defines operations to use with sql database - adapted from Sierra Clibourne's SQLLite db_operations
import mysql.connector
import time
import datetime

class sql_operations():
    def __init__(self):
        try:
            global mydb
            # REPLACE THE PASSWORD WITH YOUR ROOT SQL PASSWORD
            mydb = mysql.connector.connect(host="localhost", user="root", password="monSQL92610@",
                                           auth_plugin='mysql_native_password', database='teacher_timesheet')

            # create cursor obj to interact with mySQL
            self.cursor = mydb.cursor()

            # create teacher timesheet schema
            # self.cursor.execute("CREATE SCHEMA teacher_timesheet")
            # self.cursor.execute("SHOW DATABASES")
            # for x in self.cursor:
            #     print(x)

            # print("SQL CONNECTION SUCCESSFUL.\n")
        except:
            print("SQL CONNECTION FAILED.\n")

    # function for bulk inserting records
    def bulk_insert(self, query, records):
        self.cursor.executemany(query, records)
        mydb.commit()
        #print("query executed..")
    
    # function for inserting one record
    def insert(self, query):
        self.cursor.execute(query)
        mydb.commit()
        #print("query executed..")
    
    # function to return a single value from table
    def single_record(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()[0]

    # function to return a single record from table
    def single_row(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchone()

    # function to return a single attribute values from table
    def single_attribute(self, query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        try:
            results.remove(None)
        except:
            pass
        return results

    # SELECT with named placeholders
    def name_placeholder_query(self, query, dictionary):
        self.cursor.execute(query, dictionary)
        results = self.cursor.fetchall()
        results = [i[0] for i in results]
        return results
    
    def bulk_query(self, query):
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        return results
    
    # Used to add testing data to database
    def add(self):
        # sql1 = "INSERT INTO rides (userID, driverID, pickupLoc, dropLoc, RideRating) VALUES (%s, %s, %s, %s, %s)"

        # vals = [
        #     ("222", "333", "Coruscant", "Alderaan", "5"),
        #     ("444", "666", "Raada", "Hoth", "3"),
        #     ("555", "333", "Tatooine", "Death Star", "4")
        # ]

        # sql1 = "INSERT INTO teachers (teachID, locID, FirstName, LastName) VALUES (%s, %s, %s, %s)"

        # vals = [
        #     ("1", "2", "Nathan", "Nguyen"),
        #     ("2", "2", "John", "Dang"),
        #     ("3", "1", "Gage", "Banzon"),
        #     ("4", "3", "Olivia", "Chilvers")
        # ]

        # sql2 = "INSERT INTO schools (locID, Name) VALUES (%s, %s)"

        # vals2 = [
        #     ("1", "Beacon Park"),
        #     ("2", "Brywood"),
        #     ("3", "Stonecreek"),
        # ]

        sql3 = "INSERT INTO timesheets (teachID, entryID, timesheetID) VALUES (%s, %s, %s)"

        vals3 = [
            ("1", "1", "1"),
            ("2", "2", "2"),
            ("3", "3", "3"),
            ("4", "4", "4")
        ]

        # sql4 = "INSERT INTO entry (entryID, timeIn, timeOut, timesheetID) VALUES (%s, %s, %s, %s)"

        # date1 = datetime.datetime(2022, 7, 13, 7, 12, 0)
        # date1.strftime('%Y-%M-%D %H:%M:%S')
        # date2 = datetime.datetime(2022, 7, 13, 7, 20, 0)
        # date2.strftime('%Y-%M-%D %H:%M:%S')
        # date3 = datetime.datetime(2022, 7, 14, 7, 0, 0)
        # date3.strftime('%Y-%M-%D %H:%M:%S')
        # date4 = datetime.datetime(2022, 7, 17, 7, 30, 0)
        # date4.strftime('%Y-%M-%D %H:%M:%S')

        # date5 = datetime.datetime(2022, 7, 13, 15, 15, 0)
        # date5.strftime('%Y-%M-%D %H:%M:%S')
        # date6 = datetime.datetime(2022, 7, 13, 15, 13, 0)
        # date6.strftime('%Y-%M-%D %H:%M:%S')
        # date7 = datetime.datetime(2022, 7, 14, 15, 4, 0)
        # date7.strftime('%Y-%M-%D %H:%M:%S')
        # date8 = datetime.datetime(2022, 7, 17, 15, 30, 0)
        # date8.strftime('%Y-%M-%D %H:%M:%S')

        # vals4 = [
        #     ("1", date1, date5, "1"),
        #     ("2", date2, date6, "2"),
        #     ("3", date3, date7, "3"),
        #     ("4", date4, date8, "4")
        # ]

        # sql5 = "INSERT INTO students (studID, grade, teachID, FirstName, LastName) VALUES (%s, %s, %s, %s, %s)"

        # vals5 = [
        #     ("1", "5", "1", "Adrian", "Atlas"),
        #     ("2", "5", "1", "Britney", "Book"),
        #     ("3", "5", "1", "Chloe", "Claus"),
        #     ("4", "5", "1", "Darian", "Deck"),
        #     ("5", "5", "1", "Edward", "Edison"),
        #     ("6", "6", "2", "Felicity", "Farm"),
        #     ("7", "6", "2", "George", "Gold"),
        #     ("8", "6", "2", "Heather", "Hill"),
        #     ("9", "6", "2", "Isabelle", "Isotope"),
        #     ("10", "6", "2", "Jason", "Jack"),
        #     ("11", "3", "3", "Keath", "King"),
        #     ("12", "3", "3", "Lily", "Lover"),
        #     ("13", "3", "3", "Monique", "Monty"),
        #     ("14", "3", "3", "Nicholas", "Nelson"),
        #     ("15", "4", "4", "Opal", "Owen"),
        #     ("16", "4", "4", "Patrick", "Pill"),
        #     ("17", "4", "4", "Quirin", "Quill"),
        #     ("18", "4", "4", "Rachel", "Rome"),
        #     ("19", "4", "4", "Seth", "Soap"),
        #     ("20", "4", "4", "Trevor", "Trick")
        # ]

        # self.cursor.executemany(sql1, vals)
        # mydb.commit()
        # print("query executed...")
        # self.cursor.executemany(sql2, vals2)
        # mydb.commit()
        # print("query executed...")
        self.cursor.executemany(sql3, vals3)
        mydb.commit()
        print("query executed...")
        # self.cursor.executemany(sql4, vals4)
        # mydb.commit()
        # print("query executed...")
        # self.cursor.executemany(sql5, vals5)
        # mydb.commit()
        # print("query executed...")

        

    # Creates timesheets table 
    def create_timesheets_table(self):
        query = '''
            CREATE TABLE timesheets(
                teachID VARCHAR(20) NOT NULL,
                entryID INT NOT NULL,
                timesheetID INT NOT NULL PRIMARY KEY
            );
            '''
        self.cursor.execute(query)
        print('Table Created')
    
    # Creates entry table
    def create_entry_table(self):
        query = '''
            CREATE TABLE entry(
                entryID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                timeOut DATETIME NOT NULL,
                timeIn DATETIME NOT NULL,
                timesheetID INT NOT NULL
            );
            '''
        self.cursor.execute(query)
        print('Table Created')

    # Create teachers table
    def create_teachers_table(self):
        query = '''
            CREATE TABLE teachers(
                teachID VARCHAR(20) NOT NULL PRIMARY KEY,
                locID INT NOT NULL,
                FirstName VARCHAR(20) NOT NULL,
                LastName VARCHAR(20) NOT NULL
            );
            '''
        self.cursor.execute(query)
        print('Table Created')

    # Create teachers table
    def create_schools_table(self):
        query = '''
            CREATE TABLE schools(
                locID INT NOT NULL PRIMARY KEY,
                Name VARCHAR(20) NOT NULL
            );
            '''
        self.cursor.execute(query)
        print('Table Created')
    
     # Create teachers table
    def create_students_table(self):
        query = '''
            CREATE TABLE students(
                studID VARCHAR(20) NOT NULL PRIMARY KEY,
                grade INT NOT NULL,
                teachID INT NOT NULL,
                FirstName VARCHAR(20),
                LastName VARCHAR(20) NOT NULL
            );
            '''
        self.cursor.execute(query)
        print('Table Created')

    # close connection
    def destructor(self):
        try:
            mydb.close()
        except:
            print("CLOSE CONNECTION FAILED.")

