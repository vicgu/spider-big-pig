# coding=utf-8
# FileName: renrendai_config.py
# Description:
#           Configuration variables for renrendai.com
# Author:   Gu, Jianyu
# Create Date:
#           Apr 1, 2014
# Mail:     vicgu123@gmail.com
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

FM_PLAN_URL   = "http://www.renrendai.com/financeplan/listPlan!detailPlan.action?financePlanId="
FM_PLAN_JOIN_URL = "http://www.renrendai.com/financeplan/getFinancePlanLenders.action?financePlanStr="
FM_PLAN_BEG   = 56
FM_PLAN_END   = 56

DB_SOURCE     = "renrendai"
DB_URL        = "www.renrendai.com"

PRIVATE_URL   = "http://www.renrendai.com/lend/detailPage.action?loanId="

BID_RECORD_URL= "http://www.renrendai.com/lend/getborrowerandlenderinfo.action?id=lenderRecords&loanId="
PAYBACK_RECORD_URL= "http://www.renrendai.com/lend/getborrowerandlenderinfo.action?id=repayDetail&loanId="

MAX_RETRY_TIME= 3
RETRY_TIME    = 60
VISIT_TIME    = 3

OUTPUT_FILE   = "renrendai.csv"

RE_FMPLAN     = '计划金额.*?<em.*?>(.*?)<.*?预期收益.*?data-value=\"(.*?)\".*?计划状态.*?<span.*?>(.*?)<.*?锁定期限.*?<em.*?>(.*?)<.*?锁定结束.*?<span.*?>(.*?)<.*?剩余金额.*?<em.*?>(.*?)<'
RE_USER       = '用户名.*?<em.*?title=\"(.*?)\".*?title=\"(.*?)\".*?公司行业.*?<span.*?>(.*?)<.*?收入范围.*?<span.*?>(.*?)<.*?年&nbsp;&nbsp;&nbsp;&nbsp;龄.*?<span.*?>(.*?)<.*?公司规模.*?<span.*?>(.*?)<.*?学&nbsp;&nbsp;&nbsp;&nbsp;历.*?<span.*?>(.*?)<.*?岗位职位.*?<span.*?>(.*?)<.*?学&nbsp;&nbsp;&nbsp;&nbsp;校.*?title=\"(.*?)\".*?工作城市.*?<span.*?>(.*?)<.*?婚&nbsp;&nbsp;&nbsp;&nbsp;姻.*?<span.*?>(.*?)<.*?工作时间.*?<span.*?>(.*?)<'
RE_READY      = '标的总额.*?<em.*?>(.*?)<.*?年利率.*?<em.*?>(.*?)<.*?还款期限.*?<em.*?>(.*?)<.*?保障方式.*?<span.*?>(.*?)<.*?提前还款费率.*?<em.*?>(.*?)<.*?还款方式.*?<span.*?>(.*?)<.*?月还本息.*?<em.*?>(.*?)<'
RE_REPAYING   = '标的总额.*?<em.*?>(.*?)<.*?年利率.*?<em.*?>(.*?)<.*?还款期限.*?<em.*?>(.*?)<.*?保障方式.*?<span.*?>(.*?)<.*?提前还款费率.*?<em.*?>(.*?)<.*?还款方式.*?<span.*?>(.*?)<.*?月还本息.*?<em.*?>(.*?)<.*?待还本息.*?<span.*?>(.*?)<.*?剩余期数.*?<span.*?>(.*?)<.*?下一合约还款日.*?<span.*?>(.*?)<'
REG_EXP       = '用户档案.*?ID\s*?(\d*?)</span>.*?nickname-text.*?>(.*?)<.*?ui-icon-gender.*?"(.)".*?公司行业</span>.*?>(.*?)</span>.*?年龄</span>.*?>(\d*?)</span>.*?公司规模</span>.*?>(.*?)</span>.*?学历</span>.*?>(.*?)</span>.*?工作城市</span>.*?>(.*?)</span>.*?学校</span>.*?>(.*?)</span>.*?工作时间</span>.*?>(.*?)</span>.*?婚姻</span>.*?>(.*?)</span>.*?岗位职位</span>.*?>(.*?)</span>.*?收入范围</span>.*?>(.*?)</span>'

RE_TITLES     = ''
REG_TITLES    = '用户ID, 用户名, 性别, 公司行业, 年龄, 公司规模, 学历, 工作城市, 学校, 工作时间, 婚姻, 职位, 收入范围\n'
