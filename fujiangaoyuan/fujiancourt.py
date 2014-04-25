# coding=utf-8
# FileName: fujiancourt.py
# Description:
# Author:   Liu, Xiaoning
# Create Date:
#           Nov 23, 2013
# Mail:     xiaoning.liu.leon@gmail.com
#

from fujiancourt_config import *
import urllib2, json, time, sys

reload(sys)
sys.setdefaultencoding( "utf-8" )
sys.path.append("../")
import db, log

def getPriInfoById(db, itemId):
  url = ITEM_URL + itemId 
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
  
  infoStr = ""
  
  try:
    jsonDict = json.loads(raw_page)
    saveToDB(db, jsonDict['data'])
    for item in ITEM_TIT:
      itemStr = str(jsonDict['data'][item])
      itemStr = itemStr.replace(',', ' ')
      itemStr = itemStr.replace('\r\n', ' ')
      infoStr = infoStr + itemStr.encode('gbk') + ','
  except Exception as e:
    print "[JSON Error]", e
    return ""
    
  return infoStr + '\n'

def saveToDB(db, data):
  # check whether exist
  sql = "select dishonestID from dishonestRecords where performCaseNum = '%s'" % (data['num'])
  res =  db.select(sql)
  if (len(res) == 1):
    sql = "update dishonestRecords set performBasis = '%s', filingTime = '%s', performCourt = '%s', publishTime = '%s', updateTime = '%s', province = '%s', fulfilled = '%s', unfulfilled = '%s', dishonestAct = '%s', performBasisUnit = '%s', obligations = '%s' where performCaseNum = '%s'" % (
      data['wh'], data['time'], data['court'], data['fbsj'], str(time.time()), data['sf'], data['ylxqk'], data['wlxqk'], data['sxqx'], data['zcyjdw'], data['sxfyws'], data['num']
    )
    db.exeSql(sql)
    return
  
  personID = db.getPersonID(data['name'], DB_SOURCE)
  if personID < 0:
    sql = "insert into personInfo (nickName, name, infoSource, updateTime, age, gender, IDnumber) values ('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (data['name'], data['name'], DB_SOURCE, str(time.time()), data['age'], data['gender'], data['idNum'])
    personID = db.insert(sql)
    
  sql = '''insert into dishonestRecords
            (performBasis, personID, performCaseNum, filingTime, performCourt, publishTime, updateTime, province, fulfilled, unfulfilled, dishonestAct, performBasisUnit, obligations)
          values 
            ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')''' % (
            data['wh'], str(personID), data['num'], data['time'], data['court'], data['fbsj'], str(time.time()), data['sf'], data['ylxqk'], data['wlxqk'], data['sxqx'], data['zcyjdw'], data['sxfyws']
          )
          
  db.exeSql(sql)
  
def getPriInfo(outputFile, db, itemIds):
  for item in ITEM_TIT:
    outputFile.write(item.encode('gbk') + ',')
  outputFile.write('\n')
  
  for id in itemIds:
    print "Getting", id
    outputFile.write(getPriInfoById(db, id))

def getListByPage(pageID):
  itemIds = []
  
  
  url = LIST_URL + str(pageID)
  # Get Json Page
  try:
    response  = urllib2.urlopen(url)
  except:
    for i in range(MAX_RETRY):
      time.sleep(RET_TIME)
      try:
        response  = urllib2.urlopen(url)
        break
      except:
        if i == RET_TIME - 1 :
          print "[Network Error] cannot get people list"
          return []
        else:
          continue
  
  # Json decode
  try:
    raw_page = response.read().decode('utf-8')
  except:
    raw_page = response.read().decode('gbk')
    
  # Get list
  try:
    jsonDict = json.loads(raw_page)
    for item in jsonDict['data']['list']:
      itemIds.append(item['id'])   
      print item['id']
  except Exception as e:
    print "[JSON Error]", e
    return []
    
  print "Get list finished, total", len(itemIds)
  return itemIds

def getList():
  itemIDs = []
  for i in range(1, TOTAL_LIST_PAGE + 1):
    itemIDs += getListByPage(i)
  
  tmpIDfile = open('id.txt', 'w+')
  for id in itemIDs:
    tmpIDfile.write(id + '\n')
  tmpIDfile.close()
  
  return itemIDs
  
def fujiancourt():
  print "----> getting item ids"
  itemIds = getList()
  print "----> get item ids successfully"
  
  database = db.DB()
  database.open()
  
  print "----> getting private info"
  outputFile = open(OUT_FILE, "w+")
  getPriInfo(outputFile, database, itemIds)
  print "----> getting successfully\n"
  
  database.close()
  
  outputFile.close()

def fujiancourt_start():
    print "===== Fu Jian court spider Start ====="
    fujiancourt()
    print "===== Fu Jian court spider End ====="
    
def main():
  if __name__ == "__main__":
    fujiancourt_start()

    
main()