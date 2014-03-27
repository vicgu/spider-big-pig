# -*- coding: utf-8 -*-
#
#FileName: yirendai_spider.js
#Description:
#     This is the web spider for yirendai.com
#
#Author:  Xiaoning Liu
#Create:  2013/10/31
#

import urllib2
import re
import sys, time

sys.path.append("../")
import log, db

url     = "http://www.yirendai.com/BorrowDetailInfoAction/changeforwordPage.action?applyId="
startId = 1
endId   = 24000
regexp  = '借款人：(.*?)\s*?</p>.*?性别：</strong>(.*?)</td>.*?<td class="pb5"><strong>最高学历：</strong>(.*?)</td>.*?<strong>现居城市：</strong>(.*?)</td>.*?婚姻状况：</strong>(.*?)</td>.*?月平均收入.*?<span>\s*(.*?)\s*?</span>.*?年收入.*?<span>\s*(.*?)\s*?</span>.*?房产状况.*?<span>(.*?)</span>.*?额度.*?<span>(.*?)</span>'
output  = "yirendai.txt"
DB_SOURCE = "yirendai"

def yirendai_spider(db, url, startId, endId, regexp):
  # Open output file
  try:
    outfile = open(output, 'a')
  except:
    print "yirendai.com creating output file error"
    return
  
  # Get Next Page
  print "Getting pages, please waite..."
  for i in range(startId, endId + 1):
    if i % 100 == 0:
      print "-----> dealing %d / %d" % (i, endId)

    try:
      response = urllib2.urlopen(url + str(i))
    except:
      print "Skip for error:", (url + str(i))
      continue
  
    raw_page = response.read()
    unicode_page = raw_page.decode('utf-8', 'ignore')
    uniregexp    = regexp.decode('utf-8')
  
    infoItems = re.findall(uniregexp, unicode_page, re.S)
    for item in infoItems:
        saveToDB(db, item)
        outfile.write( item[0].encode('gbk')  + '\t' + \
                       item[1].encode('gbk')  + "\t" + \
                       item[2].encode('gbk')  + "\t" + \
                       item[3].encode('gbk')  + "\t" + \
                       item[4].encode('gbk')  + "\t" + \
                       item[5].encode('gbk')  + "\t" + \
                       item[6].encode('gbk')  + "\t" + \
                       item[7].encode('gbk')  + "\t" + \
                       item[8].encode('gbk')  + '\n')

  # Close file
  outfile.close()

def saveToDB(db, item):
  # Check whether person existing in db
  personID = db.getPersonID(item[0], DB_SOURCE)
  if personID > 0:
    # update information
    return
  
  # Insert into database
  columns = "nickName, gender, education, currentLiveplcae, marriage, monthIncome, house, creditMax, updateTime, infoSource"
  values  = "'%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s'" % (item[0], item[1], item[2], item[3], item[4], item[5], item[7], item[8], str(time.time()), DB_SOURCE)
  sql = "insert into personInfo (%s) values (%s)" % (columns, values)
  db.exeSql(sql)
  
def main():
  if __name__ == "__main__":
    
    database = db.DB()
    database.open()
    
    i = startId
    while i <= endId:
      print "Searching from %d to %d" % (i, i+999)

      yirendai_spider(database, url, i, i+999, regexp)
      i = i + 1000

    print "Finished"

    database.close()

main()
