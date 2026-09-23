import os
import json
from bs4 import BeautifulSoup

# Dictionary of all the quests by level
questsDict = {}

for levelPage in os.listdir('.\\LvLFiles'):
    # Get the current level and create a dictionary for it
    currentLevel = int(levelPage.split('_')[1].split('.')[0])
    questsDict[currentLevel] = []

    # Open the file
    with open(f'LvLFiles\\{levelPage}', 'r', encoding='utf-8') as htmlFile:
        unparsedHTML = htmlFile.read()
    # Create a soup of it
    soup = BeautifulSoup(unparsedHTML, 'html.parser')

    # Find the quests in the page
    sortedSoup = soup.select('td div a')

    # Loop through the quests and grab the text
    for quest in sortedSoup:
        questsDict[currentLevel].append(quest.text.replace('\t', '').replace('\n', ''))


with open('AllQuests.json', 'w') as jsonFile:
    json.dump(questsDict, jsonFile, indent=4)