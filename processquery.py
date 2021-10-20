#imports
import datetime #to find the date+time
import sys # to use the system
import os

def fetchlog(): #get latest query from query.log file
    try:
        with open('query.log', 'r') as f:
            last_line = f.readlines()[-1]
            query = last_line[53:]
            return query

    except:
        print("Error Reading query.log")
        return "Error"


query = fetchlog()

if 'test' in query:
    print(f"This is a test message: {query}")

elif 'what is the time' in query or 'tell me the time' in query:
    print(datetime.datetime.now())


elif 'exit' in query or 'stop' in query:
    print("Exiting Session...")
    quit()

elif 'Error' in query:
    print("Error Has Been Returned - Not Able To Read From query.log File.")

elif 'discord' in query:
    print("Sending a message to Discord...")


elif 'open cmd' in query or 'open command prompt' in query:
    print("Opening Command Prompt")
    os.startfile("C:\WINDOWS\system32\cmd.exe")



else:
    print("Command Not Found - Sorry")