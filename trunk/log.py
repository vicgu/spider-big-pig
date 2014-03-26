# FileName: log.py
# Description: General log functions
# Author: Xiaoning, Liu
# CreateDate: Mar 18, 2014

# TODO:
# 1. Try to deal with the con

import os, config, time
  
def write(app, type, msg):
  try:
    logFile = open(config.LOG_FILE, "a")
  except:
    timeStr = time.strftime('%Y-%m-%d %H::%M::%S',time.localtime(time.time()))
    fileTimeStr = time.strftime('%Y%m%d_%H%M%S_',time.localtime(time.time()))
    randomFile = fileTimeStr + config.LOG_FILE
    
    print "[%s ERROR, %s] Cannot open log file %s, try to create another log file %s" % (timeStr, app, config.LOG_FILE, randomFile)
    try:
      logFile = open(randomFile, 'a')
    except:
      timeStr = time.strftime('%Y-%m-%d %H::%M::%S',time.localtime(time.time()))
      print "[%s ERROR, %s] Cannot open log file %s, failed to log" % (timeStr, app, randomFile)
      return
        
  timeStr = time.strftime('%Y-%m-%d %H::%M::%S',time.localtime(time.time()))
  log = "[%s %s, %s] %s\n" % (timeStr, type, app, msg)
  logFile.write(log)
  
  logFile.close()
  
def main():
  if __name__ == "__main__":
    write('log', 'INFO', 'TRY TO TEST THE LOG SYSTEM')
    
    for i in range(10):
      sql = "insert into personInfo (name) values ('sadf%s')" % str(i)
      print "sql: ", sql
    write('log', 'INFO', 'SEEMS VERY GOOD')
  
main()