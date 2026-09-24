import os
import json
import sqlite3
from pathlib import Path
from bs4 import BeautifulSoup

# Dictionary of all the quests by level
questsDict = {}

# Initilize DB connection
database = sqlite3.connect("quests.db")
dbCursor = database.cursor()

# Check if we have the table we're looking for, if not, create it
master = dbCursor.execute("SELECT name FROM sqlite_master")
if(Path('.\\quests.db').is_file() == False):
    dbCursor.execute("CREATE TABLE quests(name TEXT, level INTEGER, casual_EXP INTEGER, normal_EXP INTEGER, hard_EXP INTEGER, elite_EXP INTEGER)")
if(master.fetchone() == None):
    dbCursor.execute("CREATE TABLE quests(name TEXT, level INTEGER, casual_EXP INTEGER, normal_EXP INTEGER, hard_EXP INTEGER, elite_EXP INTEGER)")
else:
    # If the database already exists, clear it so we don't dupe data
    dbCursor.execute("DELETE FROM quests")


def fixCharacter(text):
    fixedText = "".join(char for char in text if char.isalnum() or char.isspace() or char == '—')

    fixedText = fixedText.replace('—', '0')
    fixedText = fixedText.replace('\n', '')
    fixedText = fixedText.replace('\t', '')
    if fixedText.isdigit():
        int(fixedText)

    return fixedText

for levelPage in os.listdir('.\\Temp'):
    # Get the current level and create a dictionary for it
    currentLevel = int(levelPage.split('_')[1].split('.')[0])
    questsDict[currentLevel] = []

    # Open the file
    with open(f'Temp\\{levelPage}', 'r', encoding='utf-8') as htmlFile:
        unparsedHTML = htmlFile.read()
    # Create a soup of it
    soup = BeautifulSoup(unparsedHTML, 'html.parser')

    # Find the two tables in the webpage, and pick the quest table
    try:
        findTables = soup.find_all('tbody')[1]
        # Find the rows in the table
        findRows = findTables.select('tr')

        for row in findRows[:-1]:
            # Find all the cells in the row we're on
            cells = row.select('td')
            if(cells == []):
                continue

            # Select the correct cells
            Name    = fixCharacter(cells[0].text)   # Name of the quest
            Casual  = fixCharacter(cells[6].text)   # Casual Difficulty
            Normal  = fixCharacter(cells[7].text)   # Normal Difficulty
            Hard    = fixCharacter(cells[8].text)   # Hard   Difficulty
            Elite   = fixCharacter(cells[9].text)   # Elite  Difficulty

            # Add the info to the database
            dbCursor.execute(f"INSERT INTO quests VALUES ((?), (?), (?), (?), (?), (?))", (Name, currentLevel, Casual, Normal, Hard, Elite))

    # Skip the file if there is an index error
    except IndexError:
        pass

    # Commits all our data to the DB
    database.commit()