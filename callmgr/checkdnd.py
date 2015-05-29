import MySQLdb
import datetime
import os
import requests
import xml.etree.ElementTree as ET

from settings import dbhost,dbuser,dbpasswd,sid,token

def main():
  todaydate=datetime.date.today().strftime("%d%B%Y")
  db = MySQLdb.connect(host=dbhost, user=dbuser, passwd=dbpasswd, charset='utf8')
  cur=db.cursor()
  db.autocommit(True)
  query="SET NAMES utf8"
  cur.execute(query)
  query="use libtech"
  cur.execute(query)
  query="select phone from addressbook where dnd='unknown'"
  cur.execute(query)
  results = cur.fetchall()
  for row in results:
    phone=row[0]
    #print phone
    url = 'https://%s:%s@twilix.exotel.in/v1/Accounts/%s/Numbers/%s' % (sid, token, sid, phone)
    r = requests.get(url)
    #print r.content
    root = ET.fromstring(r.content)
    for number in root.findall('Numbers'):
      PhoneNumber = number.find('PhoneNumber').text
      Circle = number.find('Circle').text
      CircleName = number.find('CircleName').text
      Type = number.find('Type').text
      Operator = number.find('Operator').text
      OperatorName = number.find('OperatorName').text
      DND = number.find('DND').text
      query="update addressbook set dnd='"+DND.lower()+"',circle='"+Circle+"',operatorName='"+OperatorName+"' where phone='"+phone+"';"
      cur.execute(query)
    #print '\n'


 
if __name__ == '__main__':
  main()
