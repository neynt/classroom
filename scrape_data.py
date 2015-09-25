import requests
from bs4 import BeautifulSoup
import json

def safeint(i):
    try:
        return int(i)
    except ValueError:
        return None

def getAllSubjects():
    page = requests.get('http://www.adm.uwaterloo.ca/infocour/CIR/SA/under.html').text
    start = page.find('<SELECT NAME="subject"')
    start = page.find('<OPTION', start)
    end = page.find('</SELECT>', start)
    subjects = []

    for line in page[start:end].splitlines():
        gt = line.rfind('>')
        subjects.append(line[gt+1:])

    return {subject: getSubject(subject) for subject in subjects} 

def getSubject(subject):
    print("SUBJECT", subject)
    url = 'http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl'
    payload = {
            'level': 'under',
            'sess': 1159,
            'subject': subject,
            'cournum': ''
    }
    r = requests.post(url, payload).text
    page = BeautifulSoup(r, 'html.parser')
    if not page.body.table:
        return []
    rows = page.body.table.find_all('tr')
    
    data = {}
    datas = []

    for row in rows:
        cols = row.find_all('td')
        if len(cols) == 4:
            # Subject, Catalog, Units, Title
            data["subject"] = cols[0].text.strip()
            data["number"] = safeint(cols[1].text)
            data["units"] = cols[2].text.strip()
            data["title"] = cols[3].text.strip()
        if row.table:
            srows = row.table.find_all('tr')
            for r in srows:
                cols = r.find_all('td')
                isClass = False
                try:
                    classnum = safeint(cols[0].text)
                    if classnum:
                        isClass = True
                        data["class_number"] = classnum
                        data["section"] = cols[1].text.strip()
                        data["campus"] = cols[2].text.strip()
                        data["assoc_class"] = safeint(cols[3].text)
                        data["rel_1"] = safeint(cols[4].text)
                        data["rel_2"] = safeint(cols[5].text)
                        data["enroll_cap"] = safeint(cols[6].text)
                        data["enroll_total"] = safeint(cols[7].text)
                        data["wait_cap"] = safeint(cols[8].text)
                        data["wait_total"] = safeint(cols[9].text)
                        data["time"] = cols[10].text.strip()
                        data["building"] = cols[11].text.strip()
                        data["instructor"] = cols[12].text.strip()
                    elif cols[5].text.strip() != "":
                        isClass = True
                        data["time"] = cols[5].text.strip()
                        data["building"] = cols[6].text.strip()
                        data["instructor"] = cols[7].text.strip()
                    elif cols[10].text.strip() != "":
                        isClass = True
                        data["time"] = cols[10].text.strip()
                        data["building"] = cols[11].text.strip()
                        data["instructor"] = cols[12].text.strip()
                except IndexError:
                    pass
                except ValueError:
                    pass

                if isClass:
                    datas.append(data.copy())
    return datas

def saveAllSubjects():
    m = getAllSubjects()
    for k, v in m.items():
        f = open("data/{0}.json".format(k), "w")
        f.write(json.dumps(v))
        f.close()
