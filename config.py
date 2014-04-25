# FileName: config.py
# Description: Global environment settings, example for database connection
# Author: Xiaoning, Liu
# CreateDate: Mar 18, 2014

# SET ENV
ENV = "PROD"

DB_ADDRESS = ''
DB_USER    = ''
DB_PWD     = ''
DB_NAME    = ''
DB_CHARSET = ''
LOG_FILE   = ''

if ENV == "QA":
  DB_ADDRESS = '115.28.134.240'
  DB_USER    = 'pig'
  DB_PWD     = 'ILikeBigPig888'
  DB_NAME    = 'spider'
  DB_CHARSET = 'utf8'
  LOG_FILE   = 'spider.log'
  
if ENV == "PROD":
  DB_ADDRESS = '115.28.134.240'
  DB_USER    = 'pig'
  DB_PWD     = 'ILikeBigPig888'
  DB_NAME    = 'spider_prod'
  DB_CHARSET = 'utf8'
  LOG_FILE   = 'spider.log'