#encoding=utf-8
# FileName: db.py
# Description: DB interfaces used by spider
# Author: Xiaoning, Liu
# CreateDate: Mar 18, 2014

import config, log
import MySQLdb

class DB:
  def __init__(self):
    self.opened = False
    
  def open(self):
    try:
      self.conn = MySQLdb.connect(host=config.DB_ADDRESS,
        user=config.DB_USER, passwd=config.DB_PWD,
        db=config.DB_NAME, charset=config.DB_CHARSET)
      self.cursor = self.conn.cursor()
      self.opened = True
      return True
    except Exception as e:
      log.write('db', 'error', 'Cannot connect to database, exception: %s' % e)
      return False
    
  def ping(self):
    if self.conn.ping() == False:
      self.close()
      self.open()
  
  def close(self):
    if self.opened == True:
      try:
        self.cursor.close()
        self.conn.close()
        return True
      except Exception as e:
        log.write('db', 'error', 'Cannot close connection, exception: %s' % e)
        return False
    return True
  
  # Return the number of line has affected, -1 means error
  def exeSql(self, sql):
    try:
      self.ping()
      n = self.cursor.execute(sql)
      self.conn.commit()
      return n
    except Exception as e:
      log.write('db', 'error', 'exeSql() Cannot execute sql, exception: %s' % e)
      return -1
  
  # Return personID
  def getPersonID(self, nickName, source):
    self.ping()
    sql = "select personID from personInfo where nickName = '%s' and infoSource = '%s'" % (nickName, source)
    res = self.select(sql)
    if len(res) == 0:
      return -1
    else:
      return int(res[-1][0])
  
  # Return the generated id, -1 means error
  def insert(self, sql):
    try:
      self.ping()
      self.cursor.execute(sql)
      n = int(self.conn.insert_id())
      self.conn.commit()
      return n
    except Exception as e:
      log.write('db', 'error', 'insert() Cannot execute sql, exception: %s' % e)
      return -1
  
  # Return all the values selected
  def select(self, sql):
    try:
      self.ping()
      self.cursor.execute(sql)
      self.conn.commit()
      return self.cursor.fetchall()
    except Exception as e:
      log.write('db', 'error', 'select() Cannot execute sql, exception: %s' % e)
      return -1

def main():
   if __name__ == "__main__":
    print "Database test"
    db = DB()
    db.open()
    
    res = db.select("select personID, name from personInfo")
    print type(res)
    print res
    
    for i in range(len(res)):
      print res[i][0], res[i][1]
    
    '''
    for i in range(10):
      sql = "insert into personInfo (name) values ('sadf%s')" % str(i)
      print "exeSql:", sql
      print db.exeSql(sql)
    
    for i in range(10, 20):
      sql = "insert into personInfo (name) values ('sadf%s')" % str(i)
      print "insert:", sql
      print db.insert(sql)   
    '''
    
    db.close()
 
main()