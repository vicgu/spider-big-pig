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
import sys, urllib2, urllib, cookielib, json, time, re
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
  for i in range(len(infoLoan[0])):
    print ''.join(''.join(infoLoan[0][i].split()).split(','))

def main():
  if __name__ == "__main__":
    opener = login()
    getPageInfo(opener)
    
main()
