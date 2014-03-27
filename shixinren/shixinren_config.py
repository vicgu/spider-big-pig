# -*- coding: utf-8 -*-
#
#FileName: shixinren_config.py
#Description:
#     Configuration file
#
#Author:  Xiaoning Liu
#Create:  2013/11/5
#

# Configurations for shixinren_sipder
DB_SOURCE = "shixinren.court"
url     = 'http://shixin.court.gov.cn/detail?id='
startId = 1
endId   = 40000
perThd  = 5000                          # Number of info every thread responsible for
tmpFol  = "shixinren_tmp"               # Temporary folder
outFol  = "."                           # Output folder
priOut  = "shixinren.csv"               # Output file for private person
comOut  = "com_shixinren.csv"           # Output file for company
faiOut  = "fail_shixinren.csv"          # Failed id list met with network error
retryTm = 10                            # Retry times when network error

priKeys = ['iname', 'caseCode', 'age', 'sexy', 'cardNum',\
           'courtName', 'areaName', 'partyTypeName', 'gistId',\
           'regDate', 'gistUnit', 'duty', 'performance',\
           'disruptTypeName', 'publishDate']    # Json keys for private person
           
comKeys = ['iname', 'caseCode', 'cardNum', 'businessEntity', 'courtName',\
           'areaName', 'partyTypeName', 'gistId', 'regDate', 'gistUnit',\
           'duty', 'performance', 'disruptTypeName', 'publishDate'
          ]                                     # Json keys for company
# Configuration part end