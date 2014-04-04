# coding=utf-8
# FileName: renrendai.py
# Description:
#           Spider
# Author:   Gu, Jianyu
# Create Date:
#           Apr 1, 2014
# Mail:     vicgu123@gmail.com
#

from renrendai_config import *
import sys, urllib2, cookielib, json, time, re
sys.path.append("../")
import db

# Login procedure
# Return: login opener
def login():
  # Create cookieJar & cookie handler
  cookieJar = cookielib.CookieJar()
  opener    = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
  
  opener.addheaders = LOGIN_HAD
  opener.open(LOGIN_URL, LOGIN_DTA)
  
  if isLogin(cookieJar) == False:
    print "-------> login failed, check your name & password in 'renrendai_config.py' file"
    exit(0)
  
  return opener
  
def isLogin(cookieJar):
  for cookie in cookieJar:
    if cookie.name == "jforumUserInfo":
      return True
  return False
  
# Get loan id list
# Return: Get Loan List ids
def getLoanlist(opener):
  loanIds = []

  # travel with loanList,  Max trying times
  for pageId in range(LOAN_LIST_BEG, LOAN_LIST_END + 1):
    # Get json
    time.sleep(VISIT_TIME)
    url = LOAN_LIST_URL + str(pageId)
    isSuccess = False
    try:
      response  = opener.open(url)
      isSuccess = True
    except:
      for i in range(MAX_RETRY_TIME):
        try:
          time.sleep(RETRY_TIME)
          response  = opener.open(url)
          isSuccess = True
          break
        except:
          continue
          
    if isSuccess == False:
      continue
      
    # Json parser
    try:
      try:
        raw_page = response.read().decode('utf-8')
      except:
        print "-------> get id try to use gbk", pageId
        raw_page = response.read().decode('gbk')
            
      jsonDict = json.loads(raw_page)
      
      for loan in jsonDict['data']['loans']:
        loanIds.append(loan[LOAN_ID_WORD])
        print "----> get", loan[LOAN_ID_WORD]
    except Exception, data:
      print "---->[Exception]", data
      print "---->[Error] Json parser error for loanPage %d" % pageId
      continue

  # return id list
  return loanIds

def saveInfoToDB(db, infoUser, infoItems, bidRecords, paybackRecords):
  try:
    personID = db.getPersonID(infoUser[0], DB_SOURCE)
    # check whether personInfo exists. if not, save it
    if personID < 0:
      columns = "nickName, updateTime, age, gender, infoSource, url"
      values = "'%s', '%s', '%s', '%s', '%s', '%s'" % (infoUser[0], str(time.time()), infoUser[4], infoUser[1], DB_SOURCE, DB_URL)
      sql = "insert into personInfo (%s) values (%s);" % (columns, values)
      personID = db.insert(sql)

    # save borrowRecords to DB
    columns = "personID, updateTime, moneyAmount, interestRate, duration, payment, infoSource, url, monthPay"
    values = "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (personID, str(time.time()), infoItems[0], infoItems[1], infoItems[2], infoItems[5], DB_SOURCE, DB_URL, infoItems[6])
    sql = "insert into borrowRecords (%s) values (%s);" % (columns, values)
    borrowID = db.insert(sql)

    # save bidRecords to DB
    columns = "borrowID, personID, bidMoney, updateTime, url, bidTime"
    for loan in bidRecords:
      bidPersonName = loan['userNickName']
      bidPersonID = db.getPersonID(bidPersonName, DB_SOURCE)
      if bidPersonID < 0:
        sql = "insert into personInfo (nickName, updateTime, infoSource, url) values ('%s', '%s', '%s', '%s');" % (bidPersonName, str(time.time()), DB_SOURCE, DB_URL)
        bidPersonID = db.insert(sql)
      values = "'%s', '%s', '%s', '%s', '%s', '%s'" % (borrowID, bidPersonID, str(loan['amount']), str(time.time()), DB_URL, loan['lendTime'])
      sql = "insert into bidRecord (%s) values (%s);" % (columns, values)
      bidID = db.insert(sql)

    # save paybackRecords to DB
    if paybackRecords == "":
      return
    columns = "borrowID, updateTime, url, state, paybackDate, paybackMoney, penalty"
    for loan in paybackRecords:
      values = "'%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (borrowID, str(time.time()), DB_URL, loan['repayType'], loan['repayTime'], str(loan['unRepaidAmount']), str(loan['unRepaidFee']))
      sql = "insert into paybackRecord (%s) values (%s);" % (columns, values)
      paybackID = db.insert(sql)

  except Exception, data:
    print "Exception:", data

def getPriInfoById(loanId, opener):
  url = PRIVATE_URL + str(loanId)

  isFail = False
  try:
    response = opener.open(url)
  except:
    for i in range(MAX_RETRY_TIME):
      try:
        print "-------> retry", loanId
        time.sleep(RETRY_TIME)
        response = opener.open(url)
        isFail = False
        break
      except:
        isFail = True
        continue

  if isFail == True:
    return ""
  
  print "----------> private get successfully", loanId
  
  database = db.DB()
  database.open()

  try:
    pageString = response.read().decode('utf-8')
  except:
    print "-------> try to use gbk to parser loan id page"
    pageString = response.read().decode('gbk')    
  print "----------> private page parser successfully", loanId

  # print string to a file for debugging
  #tmpFile = open(str(loanId) + ".txt", "w+")
  #tmpFile.write(pageString.encode('utf-8'))
  #tmpFile.close()

  # check if READY or REPAYING
  if pageString.find("class=\"READY\"") >= 0:
    uniregexp = RE_READY.decode('utf-8')
  elif pageString.find("class=\"REPAYING\"") >= 0:
    uniregexp = RE_REPAYING.decode('utf-8')
  elif pageString.find("class=\"OPEN\"") >= 0:
    print "----------> Loan is not completed."
    uniregexp = RE_READY.decode('utf-8')
  else:
    print "Error! Loan state is unrecognized."
    exit(1)
  
#  uniregexp = REG_EXP.decode('utf-8')
  # get userInfo & borrowRecords
  infoUser = re.findall(RE_USER.decode('utf-8'), pageString, re.S)
  infoItems = re.findall(uniregexp, pageString, re.S)
  print "----------> private page regular parser successfully", loanId

  infoString = ""
  for i in range(len(infoUser[0])):
    infoString += infoUser[0][i].encode('gbk') + ','
  infoString = infoString[:-1] + '\n'
  for i in range(len(infoItems[0])):
    infoString += infoItems[0][i].encode('gbk') + ','
  infoString = infoString[:-1] + '\n'

  # get bidRecord
  url = BID_RECORD_URL + str(loanId)
  isSuccess = False
  try:
    response = opener.open(url)
    isSuccess = True
  except:
    for i in range(MAX_RETRY_TIME):
      try:
        time.sleep(RETRY_TIME)
        response = opener.open(url)
        isSuccess = True
        break
      except:
        continue
  if isSuccess == False:
    print "----------> Cannot get bid record from ID " + str(loanId)
  try:
    try:
      raw_page = response.read().decode('utf-8')
    except:
      raw_page = response.read().decode('gbk')
    bidDict = json.loads(raw_page)
    for loan in bidDict['data']['lenderRecords']:
      infoString += loan['userNickName'].encode('gbk') + ','
      infoString += str(loan['amount']).encode('gbk') + ','
      infoString += loan['lendTime'].encode('gbk') + '\n'
  except Exception, data:
    print "---------->[Exception]", data
    print "---------->[Error] Json parser error getting bidRecord for loanId %d" % loanId

  # get paybackRecord
  paybackDict = {'data': {'phases': ""}}
  if pageString.find("class=\"REPAYING\"") >= 0:
    url = PAYBACK_RECORD_URL + str(loanId)
    isSuccess = False
    try:
      response = opener.open(url)
      isSuccess = True
    except:
      for i in range(MAX_RETRY_TIME):
        try:
          time.sleep(RETRY_TIME)
          response = opener.open(url)
          isSuccess = True
          break
        except:
          continue
    if isSuccess == False:
      print "----------> Cannot get payback record from ID " + str(loanId)
    try:
      try:
        raw_page = response.read().decode('utf-8')
      except:
        raw_page = response.read().decode('gbk')
      paybackDict = json.loads(raw_page)
      for loan in paybackDict['data']['phases']:
        infoString += loan['repayTime'].encode('gbk') + ','
        infoString += loan['repayType'].encode('gbk') + ','
        infoString += str(loan['unRepaidAmount']).encode('gbk') + ','
        infoString += str(loan['unRepaidFee']).encode('gbk') + '\n'
    except Exception, data:
      print "---------->[Exception]", data
      print "---------->[Error] Json parser error getting paybackRecord for loanId %d" % loanId
  
  saveInfoToDB(database, infoUser[0], infoItems[0], bidDict['data']['lenderRecords'], paybackDict['data']['phases'])

  database.close()

  return infoString
  
def getPriInfo(outputFile, opener, loanIds):
  # Write output file title
  outputFile.write(RE_TITLES.decode('utf-8').encode('gbk'))
  
  # Loop with loan id list getting private info
  i = 0
  while i < len(loanIds):
    time.sleep(VISIT_TIME)
    print "-------> try to get loan id", loanIds[i]
    priInfo = getPriInfoById(loanIds[i], opener)    
    print "-------> success to get loan id", loanIds[i]
    
    if len(priInfo) > 0:
      outputFile.write(priInfo)
      i += 1
      #print priInfo
    else:
      print "Fresh too quick, retry after", RETRY_TIME
      time.sleep(RETRY_TIME)

# Spider entrance
def renrendaiSpider():
  # Login
  print "----> login"
  opener = login()
  print "----> login successfully\n"
  
  # Get loan list
  print "----> getting loan ids"
  loanIds = getLoanlist(opener)
  print "----> loan ids getting successfully\n"
  
  # Get loan list
  print "----> getting private info"
  outputFile = open(OUTPUT_FILE, "w+")
  getPriInfo(outputFile, opener, loanIds)
  outputFile.close()
  print "----> getting successfully\n"  
 
def main():
  if __name__ == "__main__":
    print "===== renrendai spider Start ====="
    renrendaiSpider()
    print "===== renrendai spider End ====="
    
main()
