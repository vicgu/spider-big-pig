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
  

def main():
  if __name__ == "__main__":
    login()
    
main()
