from sql_operations import sql_operations
import datetime
from helper import helper
import csv

db_ops = sql_operations()

def checkID(testID):
    # finding ID in databse and whether ID is valid
    query = "SELECT DISTINCT teachID FROM teachers;"
    TIDS = db_ops.single_attribute(query)
    if testID in TIDS:
        return True
    else:
        return False

#print all options for user and return their choice
def userOptions():
    print('''
    Select from the following menu options:\n
    1) SEE MY TIME
    2) SEE MY ROSTER
    3) SEE MY PAY
    4) SEE MY INFO
    5) EXIT
    ''')
    return helper.get_choice([1, 2, 3, 4, 5])

# prints time menu options for the user
def timeOptions():
    print('''
    Select from the following time options:\n
    1) ENTER HOURS
    2) SEE PREVIOUS HOURS
    3) DELETE HOURS
    4) GO BACK
    ''')
    return helper.get_choice([1, 2, 3, 4])

# prints pay menu options
def payOptions():
    print('''
    Select from the following pay options:\n
    1) CALCULATE NEXT PAY
    2) EXPORT NEXT PAY
    3) GO BACK
    ''')
    return helper.get_choice([1, 2, 3])  

# prints menu options
def infoOptions():
    print('''
    Select from the following info options:\n
    1) PRINT MY INFO
    2) UPDATE MY SCHOOL NAME
    3) GO BACK
    ''')
    return helper.get_choice([1, 2, 3])

# updates the hours of a entry
def updateTime(userID):
    # print("UPDATE TIME\n")
    done = False
    while (done == False):
        # getting input
        year = input("Enter the year: ")
        month = input("Enter the month: ")
        day = input("Enter the day: ")
        # time must be in these ranges or else program will break
        timeInHr = input("Enter a timeIn(0-24 HOUR): ")
        timeInMin = input("Enter a timeIn(0-59 MINUTE): ")
        timeOutHr = input("Enter a timeOut(0-24, HOUR): ")
        timeOutMin = input("Enter a timeOut(0-59 MINUTE): ")
        print("Is this correct?\n")
        print(f"Date: {month}/{day}/{year}\n")
        print(f"Time In: {timeInHr}:{timeInMin} Time Out: {timeOutHr}:{timeOutMin}")
        choice = input("ENTER YES OR NO: ")
        if choice.lower() == "yes" or choice.lower() == "y":
            done = True
        else:
            continue
        
        # query with aggregate
        maxIdQuery = '''
        SELECT MAX(timesheetID)
        FROM timesheets;
        '''
        try:
            maxId = db_ops.single_record(maxIdQuery)
            maxId = maxId + 1
        except:
            print("FAILED")

        query = '''
        INSERT INTO entry (timeIn, timeOut, timesheetID)
        VALUES (%s,%s,%s)
        '''

        # changing to datetime
        dateIn = datetime.datetime(int(year), int(month), int(day), int(timeInHr), int(timeInMin), 0)
        dateIn.strftime('%Y-%M-%D %H:%M:%S')
        dateOut = datetime.datetime(int(year), int(month), int(day), int(timeOutHr), int(timeOutMin), 0)
        dateOut.strftime('%Y-%M-%D %H:%M:%S')

        vals = [(dateIn, dateOut, maxId)]

        try:
            db_ops.bulk_insert(query,vals)
            print("Hours added successfully!")
        except:
            print("Failed to add in hours.")
        
        query2 = f'''
        SELECT entryID 
        FROM entry 
        WHERE timesheetID={maxId}
        '''

        # updating record
        try:
            entryyID = db_ops.single_record(query2)
        except:
            print("FAILED")

        query3 = '''
        INSERT INTO timesheets (teachID, entryID, timesheetID)
        VALUES (%s,%s,%s)
        '''

        vals2 = [(userID, entryyID, maxId)]

        try:
            db_ops.bulk_insert(query3, vals2)
        except:
            print("Failed to add to timesheets.")

# prints previous hours 
def seeTime(userID):
    query1 = f'''
    SELECT timesheets.timesheetID, entry.timeOut, entry.timeIn
    FROM (entry INNER JOIN timesheets ON entry.entryID = timesheets.entryID) INNER JOIN teachers ON timesheets.teachID = teachers.teachID
    WHERE teachers.teachID = {userID}
    '''
    resultingDates = db_ops.bulk_query(query1)
    for x in resultingDates:
        print(f'TIMESHEET ID: {x[0]} \nTIME IN: {x[2]} \nTIME OUT: {x[1]} \n')

# deletes entry based on timesheet ID
def deleteTime(userID):
    while(True):
        tID = input("Enter the timesheet ID you wish to delete: ")

        queryy = '''
        SELECT DISTINCT timesheetID 
        from timesheets
        '''

        tIDs = db_ops.single_attribute(queryy)
        
        if int(tID) in tIDs:
            pass
        else:
            print("Please try again with a valid timesheet ID.")
            continue

        
        print(f"Timesheet ID: {tID}\n")
        choice = input("Please confirm that this is correct ID you wish to delete (yes/no)?\n")
        if choice.lower() == "yes" or choice.lower() == "y":
            # initially a transaction but couldn't get to work without errors
            query = f'''
            DELETE FROM entry
            WHERE timesheetID = {tID};
            '''

            query2 = f'''
            DELETE FROM timesheets
            WHERE timesheetID = {tID};
            '''
            db_ops.insert(query2)

            try:
                db_ops.insert(query)
                print('DELETED SUCCESSFULLY. COMMITED.')
                break
            except:
                print("DELETE FAILED.")
                break
        else:
            print("Aborted.")
            break     
        
# prints time options
def timeMenu(userID):
    match timeOptions():
        case 1:
            updateTime(userID)
        case 2:
            seeTime(userID)
        case 3:
            deleteTime(userID)
        case 4:
            print("EXITING TIME MENU....\n")

# prints roster options
def studMenu(userID):
    query1 = f'''
    SELECT FirstName,LastName,grade,(SELECT teachers.LastName FROM teachers where teachID = {userID}) 
    FROM students
    WHERE teachID = {userID}
    '''
    resultingName = db_ops.bulk_query(query1)
    print(f"\n{resultingName[0][3]}'s Roster:")
    for x in resultingName:
        print(f'Student Name: {x[0]} {x[1]}, Grade {x[2]}')

# calculates predicted next pay given pay rate
def calculatePay(userID):
    payRate = input("Enter your pay rate per hour: ")

    query = f'''
    SELECT *
    FROM (entry INNER JOIN timesheets ON entry.entryID = timesheets.entryID) INNER JOIN teachers ON timesheets.teachID = teachers.teachID
    WHERE teachers.teachID = {userID}
    '''

    nextPay = 0

    resultingDates = db_ops.bulk_query(query)
    for x in resultingDates:
        currHour = x[1]-x[2]
        nextPay = nextPay + (int(payRate) * (currHour.seconds / 60 / 60) )
    
    print(f'Calculated Pay (Dollars): {round(nextPay,2)}\n')

# exports all hours + expected pay to a CSV file
def exportHours(userID):
    payRate = input("Enter your pay rate per hour: ")
    fileName = input("Enter the filename with .csv at end: ")

    f = open(fileName, 'w')
    writer = csv.writer(f)

    query = f'''
    SELECT entry.timeIn, entry.timeOut, teachers.FirstName, teachers.LastName
    FROM (entry INNER JOIN timesheets ON entry.entryID = timesheets.entryID) INNER JOIN teachers ON timesheets.teachID = teachers.teachID
    WHERE teachers.teachID = {userID}
    '''

    nextPay = 0

    resultingDates = db_ops.bulk_query(query)

    header1 = [f'NAME:{resultingDates[0][2]} {resultingDates[0][3]}']
    writer.writerow(header1)
    header2 = ["TIME IN", "TIME OUT"]
    writer.writerow(header2)

    for x in resultingDates:
        currHour = x[1]-x[0]
        nextPay = nextPay + (int(payRate) * (currHour.seconds / 60 / 60))
        blank = []
        blank.append(x[0])
        blank.append(x[1])
        writer.writerow(blank)
    
    header3 = [f"CURRENT EXPECTED PAY: {round(nextPay,2)}"]
    writer.writerow(header3)
    f.close()
    
# prints pay menu options
def payMenu(userID):
    match payOptions():
        case 1:
            calculatePay(userID)
        case 2:
            exportHours(userID)
        case 3:
            print("EXITING PAY MENU....\n")

# retrives and prints personal info about the user
def printInfo(userID):
    # ------ View Created Here ------
    # query1 = f'''
    # CREATE VIEW infoV AS
    # SELECT schools.Name, teachers.FirstName, teachers.LastName, teachers.teachID 
    # FROM teachers 
    # INNER JOIN schools ON teachers.locID = schools.locID;
    # '''

    # db_ops.insert(query1)

    query2 = f'''
    SELECT * 
    FROM infoV
    WHERE teachID = {userID}
    '''

    resultingTeach = db_ops.bulk_query(query2)
    for x in resultingTeach:
        print(f'Name: {x[1]} {x[2]} \nSchool Site: {x[0]}\n')

# Allows user to update their school name
def updateSchool(userID):
    schoolName = input("Enter a new school name: ")
    print(f"NEW SCHOOL NAME: {schoolName}\n")
    choice = input("Please confirm that this is correct school name you wish to update (yes/no)?\n")
    if choice.lower() == "yes" or choice.lower() == "y":
        try:
            locIDQ = f'''
            SELECT locID
            FROM teachers
            WHERE teachID={userID}
            '''
            locID = db_ops.single_record(locIDQ)

            query = f'''
            UPDATE schools
            SET Name = \'{schoolName}\'
            WHERE locID = {int(locID)}
            '''
            db_ops.insert(query)
            print("UPDATE SUCCESSFUL.")
        except:
            print("UPDATE FAILED. PLEASE TRY AGAIN.")
    else:
        print("Aborted. Returning to main menu.")

# prints info menu options
def infoMenu(userID):
    match infoOptions():
        case 1:
            printInfo(userID)
        case 2:
            updateSchool(userID)
        case 3:
            print("EXITING INFO MENU....\n")

# main loop
def main():
    print("Welcome to Teacher Timesheet App! \n")
    userID = input("ENTER YOUR ID NUMBER TO LOG IN: ")

    validID = checkID(userID)

    # ID check
    while (validID != True):
        print("Invalid ID. Please try again!\n")
        userID = input("ENTER YOUR ID NUMBER TO LOG IN: ")
        validID = checkID(userID)
    
    # allow user to repeatedly interface with the application until they quit
    while(validID == True):
        match userOptions():
            case 1:
                timeMenu(userID)
            case 2:
                studMenu(userID)
            case 3:
                payMenu(userID)
            case 4:
                infoMenu(userID)
            case 5:
                print("Goodbye.")
                break

main()
db_ops.destructor()
