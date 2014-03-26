# coding=utf-8
# FileName: renrendai_config.py
# Description:
#           Configuration variables for renrendai.com
# Author:   Liu, Xiaoning
# Create Date:
#           Nov 16, 2013
# Mail:     xiaoning.liu.leon@gmail.com
#

LOGIN_URL     = "https://www.renrendai.com/j_spring_security_check"
LOGIN_USR     = "18801970616" # Set your login name here
LOGIN_PSD     = "rrdkey110" # Set your password here
LOGIN_DTA     = "j_username=%s&j_password=%s" % (LOGIN_USR, LOGIN_PSD)
LOGIN_HAD     = [("Accept", "text/html, application/xhtml+xml, */*"), \
                 ("User-Agent", "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)"), \
                 ("Content-Type", "application/x-www-form-urlencoded"), \
                 ("Host", "www.renrendai.com")]
                 
LOAN_LIST_URL = "http://www.renrendai.com/lend/loanList!json.action?pageIndex="
LOAN_LIST_BEG = 1
LOAN_LIST_END = 1
LOAN_ID_WORD  = "loanId"

PRIVATE_URL   = "http://www.renrendai.com/lend/detailPage.action?loanId="

MAX_RETRY_TIME= 3
RETRY_TIME    = 60
VISIT_TIME    = 3

OUTPUT_FILE   = "renrendai.csv"

REG_EXP       = '用户档案.*?ID\s*?(\d*?)</span>.*?nickname-text.*?>(.*?)<.*?ui-icon-gender.*?"(.)".*?公司行业</span>.*?>(.*?)</span>.*?年龄</span>.*?>(\d*?)</span>.*?公司规模</span>.*?>(.*?)</span>.*?学历</span>.*?>(.*?)</span>.*?工作城市</span>.*?>(.*?)</span>.*?学校</span>.*?>(.*?)</span>.*?工作时间</span>.*?>(.*?)</span>.*?婚姻</span>.*?>(.*?)</span>.*?岗位职位</span>.*?>(.*?)</span>.*?收入范围</span>.*?>(.*?)</span>'

REG_TITLES    = '用户ID, 用户名, 性别, 公司行业, 年龄, 公司规模, 学历, 工作城市, 学校, 工作时间, 婚姻, 职位, 收入范围\n'