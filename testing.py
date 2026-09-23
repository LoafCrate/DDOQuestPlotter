from bs4 import BeautifulSoup

with open('LvLFiles\\Level_1.html', 'r', encoding='utf-8') as htmlFile:
    unparsedHTML = htmlFile.read()


target_classes = {'wikitable', 'sortable', 'striped', 'jquery-tablesorter'}
soup = BeautifulSoup(unparsedHTML, 'html.parser')
semiSortedSoup = soup.find_all("table")[1]
moreSortedSoup = soup.select('td div a')

for quest in moreSortedSoup:
    print(quest.text)