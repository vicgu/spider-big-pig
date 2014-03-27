# coding=utf-8
# FileName: fujiancourt_config.py
# Description:
#           Spider
# Author:   Liu, Xiaoning
# Create Date:
#           Nov 23, 2013
# Mail:     xiaoning.liu.leon@gmail.com
#

LIST_RAN = 29641
LIST_ONE_SIZE = 3000
TOTAL_LIST_PAGE = LIST_RAN / LIST_ONE_SIZE + 1
LIST_URL = "http://www.fjcourt.gov.cn/Ajax/Page/zxgsAjax.ashx?act=getzxgslist&pageSize=%d&pageIndex=" % LIST_ONE_SIZE
ITEM_URL = "http://www.fjcourt.gov.cn/Ajax/Page/zxgsAjax.ashx?act=getcasedetail&id="
ITEM_TIT = ["id", "court", "idNum", "name", "num", "sf", "sxqx", "wh", "ywqk"]
MAX_RETRY= 3
RET_TIME = 2
OUT_FILE = "fujiancourt.csv"

DB_SOURCE= "fujiancourt"