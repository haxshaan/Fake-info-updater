import requests
from bs4 import BeautifulSoup
import csv
from random import randint
import MySQLdb
from time import sleep


url = 'http://fakenametool.com/generator/random/en_IN/india'

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:56.0) Gecko/20100101 Firefox/56.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'close',
    'Upgrade-Insecure-Requests': '1'
}

pinfile = open('pincodes.csv', 'r')

totalrow = sum(1 for row in pinfile)

reader = csv.reader(pinfile)

db = MySQLdb.connect(host='5.104.230.133',
                     user='trickfor_FAKE',
                     passwd='2480539',
                     db='trickfor_FAKE')

cur = db.cursor()


def csv_values():
    randrow = randint(1, totalrow)
    pinfile.seek(0)

    for i, row in enumerate(reader):
        if i == randrow:
            return [row[-1], row[-2]]


def number_generator():
    series = randint(7, 9)
    return str(series) + str(randint(110, 999)) + str(randint(110, 999)) + str(randint(110, 999))

n = int(input("Enter the number of entries to add: "))

while n:

    resp = requests.get(url, headers=header)

    data = resp.text

    soup = BeautifulSoup(data, "html5lib")

    info = soup.find('div', {'class': 'col-lg-10'})

    final = dict()

    final['name'] = info.find('h3').text

    # Now lets get the State and City from csv file
    local_list = csv_values()
    final['city'] = local_list[1]
    final['state'] = local_list[0]

    def email_generator():
        raw_email = str(final['name']).split(' ')
        return ''.join(raw_email).lower() + str(randint(10, 999)) + '@gmail.com'

    final['email'] = email_generator()

    ran_mobile = number_generator()

    final['mobile'] = ran_mobile

    # address = str(info.find('p', {'class': 'lead'}).text)
    # pin_code = str(address.rsplit(' ', maxsplit=1)[1])

    print('Inserting these values into Database :', final)

    sql1 = ("INSERT INTO info "
            "(name, email, pass, city, state) "
            "VALUES(%s, %s, %s, %s, %s)")

    val = (final['name'], final['email'], final['mobile'], final['city'], final['state'])

    cur.execute(sql1, val)

    db.commit()

    n -= 1

    sleep(0.5)


cur.close()
db.close()
