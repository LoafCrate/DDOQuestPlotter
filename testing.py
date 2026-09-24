from bs4 import BeautifulSoup

with open('Temp\\Level_01.html', 'r', encoding='utf-8') as htmlFile:
    unparsedHTML = htmlFile.read()

soup = BeautifulSoup(unparsedHTML, 'html.parser')

def fixCharacter(text):
    fixedText = "".join(char for char in text if char.isalnum() or char.isspace() or char == '—')

    fixedText = fixedText.replace('—', '0')
    fixedText = fixedText.replace('\n', '')
    fixedText = fixedText.replace('\t', '')
    if fixedText.isdigit():
        int(fixedText)

    return fixedText


# Find the two tables in the webpage, and pick the quest table
try:
    findTables = soup.find_all('tbody')[1]
    # Find the rows in the table
    findRows = findTables.select('tr')

    for row in findRows[:-1]:
        # Find all the cells in the row we're on
        cells = row.select('td')

        # Select the correct cells
        Name    = fixCharacter(cells[0].text)   # Name of the quest
        Pack    = fixCharacter(cells[3].text)
        Casual  = fixCharacter(cells[6].text)   # Casual Difficulty
        Normal  = fixCharacter(cells[7].text)   # Normal Difficulty
        Hard    = fixCharacter(cells[8].text)   # Hard Difficulty
        Elite   = fixCharacter(cells[9].text)  # Elite Difficulty

        print(Name)
        print(Casual)
        print(Normal)
        print(Hard)
        print(Elite)

# Skip the file if there is an index error
except IndexError:
    pass