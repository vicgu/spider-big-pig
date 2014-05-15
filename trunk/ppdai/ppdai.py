# coding=utf-8
# FileName: ppdai.py
# Description:
#           Spider
# Author:   Gu, Jianyu
#           Xiaoning Liu
# Create Date:
#           Apr 1, 2014
# Mail:     vicgu123@gmail.com
#           xiaoning.liu.leon@gmail.com

from ppdai_config import *
import sys, urllib2, urllib, cookielib, time, re
sys.path.append("../")
import log, db

# Login procedure
# Return: login opener
def login():
  # Create cookieJar & cookie handler
  cookieJar = cookielib.CookieJar()
  opener    = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
  
  opener.addheaders = LOGIN_HAD
  opener.open(LOGIN_BEFORE_URL, urllib.urlencode({}))
  
  try:
    opener.open(LOGIN_URL, urllib.urlencode(LOGIN_DTA))
  except Exception as err:
    print err
  
  if isLogin(cookieJar) == False:
    print "-------> Login failed, check your name & password"
    exit(0)
  else:
    print "-------> Login success"
  
  return opener
 
def isLogin(cookieJar):
  for cookie in cookieJar:
    if cookie.name == "ppd_serName":
      return True
  return False
 
def getPageInfo(opener):
  for loanId in range(LOAN_ID_BEGIN, LOAN_ID_END + 1):
    getLoanInfo(loanId, opener)

def getLoanInfo(loanId, opener):
  url = LOAN_URL + str(loanId)
  try:
    response = opener.open(url)
  except Exception, data:
    print "[Exception]", data
    exit(0)
  try:
    pageString = response.read().decode('utf-8')
  except:
    pageString = response.read().decode('gbk')
  #print pageString
  infoLoan = re.findall(RE_LOAN.decode('utf-8'), pageString, re.S)
  infoBorrow = re.findall(RE_BORROW.decode('utf-8'), pageString, re.S)
  infoLoanList = []
  for i in range(len(infoLoan[0])):
    infoLoanList.append(''.join(''.join(infoLoan[0][i].split()).split(',')))

  database = db.DB()
  database.open()

  saveLoanInfoToDB(database, infoLoanList, infoBorrow,url)

def saveLoanInfoToDB(db, infoLoan, infoBorrow,url):
  try:
    # check whether personInfo exists. if not, save it
    personID = db.getPersonID(infoLoan[4], INFO_SOURCE)
    if personID < 0:
      sql = "insert into personInfo (nickName, infoSource, updateTime) values ('%s', '%s', '%s');" % (infoLoan[4], INFO_SOURCE, str(time.time()))
      personID = db.insert(sql)

    # save borrowRecords to DB
    columns = "personID, updateTime, moneyAmount, interestRate, duration, infoSource, url, monthPay"
    values = "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (personID, str(time.time()), infoLoan[0], infoLoan[1], infoLoan[2], INFO_SOURCE, url, infoLoan[3])
    sql = "insert into borrowRecords (%s) values (%s);" % (columns, values)
    borrowID = db.insert(sql)

    # save bidRecords to DB
    columns = "borrowID, personID, bidMoney, updateTime, url"
    for borrow in infoBorrow:
      bidPersonName = ''.join(''.join(borrow[0].split()).split(','))
      bidMoney = ''.join(''.join(borrow[2].split()).split(','))
      bidPersonID = db.getPersonID(bidPersonName, INFO_SOURCE)
      if bidPersonID < 0:
        sql = "insert into personInfo (nickName, infoSource, updateTime) values ('%s', '%s', '%s');" % (bidPersonName, INFO_SOURCE, str(time.time()))
        bidPersonID = db.insert(sql)
      values = "'%s', '%s', '%s', '%s', '%s'" % (borrowID, bidPersonID, bidMoney, str(time.time()), url)
      sql = "insert into bidRecord (%s) values (%s);" % (columns, values)
      bidID = db.insert(sql)
  except Exception, data:
    print "[Exception]", data

def ppdai_start():
    opener = login()
    getPageInfo(opener)
    
def main():
  if __name__ == "__main__":
    ppdai_start()

    
main()
