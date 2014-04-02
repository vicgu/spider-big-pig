# coding=utf-8
# FileName: renrendai_spider.py
# Description:
#           Spider
# Author:   Liu, Xiaoning
# Create Date:
#           Nov 16, 2013
# Mail:     xiaoning.liu.leon@gmail.com
#

from renrendai_config import *
import urllib2, cookielib, json, time, re, sys
# Import global scripts
sys.path.append("../")
import log, db
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
  
def addToDBOneRecord(db, item):
 # if SAVE_DB == False:
  #  return
  #print "begin db"
  personID = db.getPersonID(item[0], INFO_SOURCE)
  if personID < 0:
    sql = "insert into personInfo (nickName, infoSource, updateTime) values ('%s', '%s', '%s')" % (item[0], INFO_SOURCE, str(time.time()))
    personID = db.insert(sql)
    db.exeSql(sql)
    print "insert success"
  else:
    print "insert fail"

# Get user's info list
# Return: user's info list
def getuserinfo(opener,db):
  loanIds = []

  # travel with loanList,  Max trying times
  for pageId in range(640000,650000):#用户ID范围
    # Get html
    time.sleep(VISIT_TIME)
    url = USER_LIST_URL + str(pageId)
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
      
    # 
    try:
      try:
        raw_page = response.read().decode('utf-8')
      except:
        print "-------> get id try to use gbk", pageId
        raw_page = response.read().decode('gbk')
    except:
        pass

  #  f = open(str(pageId), 'w+')
   # f.write( raw_page.encode('utf-8'))
    #f.close()
            
    myItems = re.findall(REG_EXP.decode('utf-8'), raw_page, re.S)
    if len(myItems[0])<=0:
      continue
    else :
      print myItems[0].encode('gbk')
      addToDBOneRecord(db,myItems[0])

  # return id list
  return loanIds

# Spider entrance
def renrendaiSpider(database):
  # Login
  print "----> login"
  opener = login()
  print "----> login successfully\n"
  
  # Get user info
  print "----> getting user info"
  loanIds = getuserinfo(opener,database)
  print "----> user info getting successfully\n"
 
 
def main():
  if __name__ == "__main__":
    if SAVE_DB == False:
      log.write(INFO_SOURCE, "info", "save to db turned off")
    
    database = db.DB()
    database.open()
    print "===== renrendai spider Start ====="
    renrendaiSpider(database)
    print "===== renrendai spider End ====="
    database.close()
main()