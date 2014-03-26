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
import urllib2, cookielib, json, time, re

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
  
  try:
    pageString = response.read().decode('utf-8')
  except:
    print "-------> try to use gbk to parser loan id page"
    pageString = response.read().decode('gbk')    
  print "----------> private page parser successfully", loanId
  
  # print string to a file for debugging
  tmpFile = open(str(loanId) + ".txt", "w+")
  tmpFile.write(pageString.encode('utf-8'))
  tmpFile.close()
  
  uniregexp = REG_EXP.decode('utf-8')
  infoItems = re.findall(uniregexp, pageString, re.S)
  print "----------> private page regular parser successfully", loanId
  
  infoString = ""
  for item in infoItems:
    infoString = item[0].encode('gbk')  + ',' + \
                 item[1].encode('gbk')  + "," + \
                 item[2].encode('gbk')  + "," + \
                 item[3].encode('gbk')  + "," + \
                 item[4].encode('gbk')  + "," + \
                 item[5].encode('gbk')  + ',' + \
                 item[6].encode('gbk')  + "," + \
                 item[7].encode('gbk')  + "," + \
                 item[8].encode('gbk')  + "," + \
                 item[9].encode('gbk')  + "," + \
                 item[10].encode('gbk') + "," + \
                 item[11].encode('gbk') + "," + \
                 item[12].encode('gbk') + '\n'
  
  return infoString
  
def getPriInfo(outputFile, opener, loanIds):
  # Write output file title
  outputFile.write(REG_TITLES.decode('utf-8').encode('gbk'))
  
  # Loop with loan id list getting private info
  i = 0
  while i < len(loanIds):
    i = i + 1
    
    time.sleep(VISIT_TIME)
    print "-------> try to get loan id", loanIds[i]
    priInfo = getPriInfoById(loanIds[i], opener)    
    print "-------> success to get loan id", loanIds[i]
    
    if len(priInfo) > 0:
      outputFile.write(priInfo)
      print priInfo
    else:
      print "Fresh too quick, retry after", RETRY_TIME
      time.sleep(RETRY_TIME)
      if i > 0:
        i = i - 1

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