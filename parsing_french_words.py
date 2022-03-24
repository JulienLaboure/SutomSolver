from requests import get
from bs4 import BeautifulSoup

first_page = "https://www.listesdemots.net/touslesmots.htm"
page = "https://www.listesdemots.net/touslesmotspage{}.htm"

first_result = get(first_page)
soup = BeautifulSoup(first_result.text, 'html.parser')
words = soup.find('span', {'class', 'mot'}).text.split()
for i in range(2, 918):
    result = get(page.format(i))
    print(i, result)
    soup = BeautifulSoup(result.text, 'html.parser')
    words += soup.find('span', {'class', 'mot'}).text.split()
with open('result.txt', 'w') as result_file:
    result_file.write(' '.join(words))
    result_file.write('\n')
