from honglingchuangtou_config import *
import urllib2, re, sys, JSspider, time

# Import global scripts
sys.path.append("../")
import log, db


###################################################
# For Ongoing Borrowing
###################################################

def onGoingSpider(database):
  # Create output file
  outputFile = open(ONGOING_OUT_FILE, "w+")
  
  # Generate titles
  for title in ONGOINT_TIT:
    outputFile.write(title.decode('utf-8').encode('gbk') + ',\t')
  outputFile.write('\n')
  
  # Get all pages
  for pageId in range(1, ONGOING_RAN + 1):
    outputFile.write(onGoingOnePage(database, pageId).encode('gbk'))
    
  # Regular Expression Deal
  # Output
  outputFile.close()

def onGoingOnePage(db, pageId):
  # Access to web page
  # string page = onGoingOnePageSpider, return "" meansing failure
  pageStr = onGoingOnePageSpider(pageId)
  
  # Regular the page
  return onGoingOnePageReg(db, pageStr)
 
def onGoingOnePageSpider(pageId):
  # return one page content
  url = ONGOING_URL + str(pageId)
  isFail = False
  
  try:
    response = urllib2.urlopen(url)
  except:
    for i in range(MAX_RETRY):
      time.sleep(RET_TIME)
      try:
        response = urllib2.urlopen(url)
        isFail = False
        break
      except:
        isFail = True
        continue

  if isFail == True:
    return ""
    
  try:
    raw_page = response.read().decode('utf-8')
  except:
    raw_page = response.read().decode('gbk')
   
  return raw_page
    
def onGoingOnePageReg(db, pageStr):
  # return one line in final result
  unicodePageStr = pageStr # using unicode in python, transfering from utf-8 to unicode
  unicodeReg     = ONGOING_REG.decode("utf-8")

  myItems = re.findall(unicodeReg, unicodePageStr, re.S)
  
  res = ""

  for item in myItems:
    onGoingToDBOneRecord(db, item)
    for i in range(len(ONGOINT_TIT)):
      tmp = item[i].replace(',', ' ')
      tmp = tmp.replace('\n', ' ')
      res = res + tmp + ','  + '\t'
    
    res = res + "\n"

  
  return res

###################################################
# For Finish Borrowing
###################################################

def finsihSpider(db):
  # Create output file
  outputFile = open(FINISH_OUT_FILE, "w+")
  
  # Generate titles
  for title in FINISH_TIT:
    outputFile.write(title.decode('utf-8').encode('gbk') + ',\t')
  outputFile.write('\n')
  
  # Get all pages
  for pageId in range(1, FINISH_RAN + 1):
    outputFile.write(finishOnePage(db, pageId).encode('gbk'))
    
  # Regular Expression Deal
  # Output
  outputFile.close()

def finishOnePage(db, pageId):
  # Access to web page
  # string page = onGoingOnePageSpider, return "" meansing failure
  pageStr = finishOnePageSpider(pageId)
  
  # Regular the page
  return finishOnePageReg(db, pageStr)
  
def finishOnePageSpider(pageId):
  # return one page content
  url = FINISH_URL + str(pageId)
  isFail = False
  
  try:
    response = urllib2.urlopen(url)
  except:
    for i in range(MAX_RETRY):
      time.sleep(RET_TIME)
      try:
        response = urllib2.urlopen(url)
        isFail = False
        break
      except:
        isFail = True
        continue

  if isFail == True:
    return ""
    
  try:
    raw_page = response.read().decode('utf-8')
  except:
    raw_page = response.read().decode('gbk')
   
  return raw_page

def finishOnePageReg(db, pageStr):
  # return one line in final result
  unicodePageStr = pageStr # using unicode in python, transfering from utf-8 to unicode
  unicodeReg     = FINISH_REG.decode("utf-8")

  myItems = re.findall(unicodeReg, unicodePageStr, re.S)
  
  res = ""

  for item in myItems:
    finishToDBOneRecord(db, item)
    for i in range(len(FINISH_TIT)):
      tmp = item[i].replace(',', ' ')
      tmp = tmp.replace('\n', ' ')
      res = res + tmp + ','  + '\t'
    
    res = res + "\n"

  return res

def finishToDBOneRecord(db, item):
  if SAVE_DB == False:
    return

  personID = db.getPersonID(item[0], INFO_SOURCE)
  if personID < 0:
    sql = "insert into personInfo (nickName, infoSource, updateTime) values ('%s', '%s', '%s')" % (item[0], INFO_SOURCE, str(time.time()))
    personID = db.insert(sql)
  
  columns = "personID, updateTime, startTime, hasFinish, moneyAmount, interestRate, infoSource, duration, payment, bidding"
  values = "%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(personID), str(time.time()), item[1], "y", item[2], item[3], INFO_SOURCE, item[6], item[7], item[5])
  sql = "insert into borrowRecords (%s) values (%s)" % (columns, values)
  db.exeSql(sql)

def onGoingToDBOneRecord(db, item):
  if SAVE_DB == False:
    return

  personID = db.getPersonID(item[0], INFO_SOURCE)
  if personID < 0:
    sql = "insert into personInfo (nickName, infoSource, updateTime) values ('%s', '%s', '%s')" % (item[0], INFO_SOURCE, str(time.time()))
    personID = db.insert(sql)
  
  columns = "personID, updateTime, startTime, hasFinish, moneyAmount, interestRate, infoSource, duration, payment, bidding"
  values = "%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (str(personID), str(time.time()), item[2], "n", item[3], item[4], INFO_SOURCE, item[8], item[9], item[6])
  sql = "insert into borrowRecords (%s) values (%s)" % (columns, values)
  db.exeSql(sql)
 
def main():
  if __name__ == "__main__": 
    # JSspider.JSspider("black.csv")
    if SAVE_DB == False:
      log.write(INFO_SOURCE, "info", "save to db turned off")
    
    database = db.DB()
    database.open()
    
    onGoingSpider(database)
    finsihSpider(database)
    
    database.close()
    
main()