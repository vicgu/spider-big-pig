# coding=utf-8
# FileName: ppdai.py
# Description:
#           Configuration variables for ppdai.com
# Author:   Xiaoning Liu, Jianyu Gu
# Create Date:
#           May 6, 2014
# Mail:     xiaoning.liu.leon@gmail.com
#           vicgu123@gmail.com
#

LOGIN_BEFORE_URL = "http://ac.ppdai.com/login"
LOGIN_URL     = "http://ac.ppdai.com/auth/Credentials"
LOGIN_USR     = "testcase" # Set your login name here
LOGIN_PSD     = "1qazxsw2" # Set your password here
LOGIN_DTA     = {"Continue" : "http://www.ppdai.com/account",
                 "UserName" : LOGIN_USR,
                 "Password" : LOGIN_PSD}
LOGIN_HAD     = [("Accept", "text/html, application/xhtml+xml, */*"), \
                 ("User-Agent", "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)"), \
                 ("Content-Type", "application/x-www-form-urlencoded")]
                 
VISIT_TIME    = 3
MAX_RETRY_TIME= 3
LOAN_URL      = "http://www.ppdai.com/list/"
LOAN_ID_BEGIN = 123456
LOAN_ID_END   = 123456
RE_LOAN       = '金&nbsp;&nbsp;&nbsp;额.*?<span.*?;(.*?)<.*?年利率.*?<span.*?>(.*?)<.*?期&nbsp;&nbsp;&nbsp;限.*?<span.*?>(.*?)<.*?每月还款.*?;(.*?)<.*?class="user_face_name".*?href.*?>(.*?)<'
