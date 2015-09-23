import requests
from bs4 import BeautifulSoup

page = requests.get('http://www.adm.uwaterloo.ca/infocour/CIR/SA/under.html').text
start = page.find('<SELECT NAME="subject"')
start = page.find('<OPTION', start)
end = page.find('</SELECT>', start)
subjects = []

for line in page[start:end].splitlines():
    gt = line.rfind('>')
    subjects.append(line[gt+1:])

page = None
for subject in ['MATH']:
    url = 'http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl'
    payload = {
            'level': 'under',
            'sess': 1159,
            'subject': subject,
            'cournum': ''
    }
    r = requests.post(url, payload).text
    page = BeautifulSoup(r)
    tables = page.prettify().split('<tr><td colspan="4"></td></tr>')
    for table in tables[:1]:
        print(table)
        
