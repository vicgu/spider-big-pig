# coding=utf-8
# FileName: fujiancourt_config.py
# Description:
#           Spider
# Author:   Liu, Xiaoning
# Create Date:
#           Nov 23, 2013
# Mail:     xiaoning.liu.leon@gmail.com
#

INFO_SOURCE = "honglingchuangtou"
SAVE_DB    = False

FINISH_RAN = 100
FINISH_OUT_FILE = "finishborrowing.csv"
FINISH_URL = "http://www.my089.com/Loan/Succeed.aspx?pid="
FINISH_REG = '借款用户.*?>(.*?)</a>.*?发布时间：(.*?)</dd>.*?<dt>(.*?)</dt>.*?<dd>.*?>(.*?)</span>.*?奖励：(.*?)</dd>.*?已完成(.*?)</dd>.*?<dd>.*?</dd>.*?<dd>(.*?)</dd>.*?<dd>(.*?)</dd>'
FINISH_TIT = ["借款用户", "发布时间", "金额", "利率", "奖励", "已完成", "期限", "还款方式"]

ONGOING_RAN = 4
ONGOING_OUT_FILE = "ongoingborrowing.csv"
ONGOING_URL = "http://www.my089.com/Loan/default.aspx?pid="
ONGOING_REG = '借款用户.*?>(.*?)</a>.*?所属客服：(.*?)</dd>.*?发布时间：(.*?)</dd>.*?<dt>(.*?)</dt>.*?利率.*?>(.*?)</span>.*?<dd>奖励：(.*?)</dd>.*?已完成(.*?)</dd>.*?剩余时间：(.*?)</dd>.*?<dd>(.*?)</dd>.*?<dd>(.*?)</dd>'
ONGOINT_TIT = ["借款用户", "所属客服", "发布时间", "金额", "利率", "奖励", "已完成", "剩余时间", "期限", "还款方式"]

MAX_RETRY= 3
RET_TIME = 2