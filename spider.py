# FileName: spider.py
# Description: Main entrance for all websites spider
# Author: Xiaoning Liu
# CreateDate: Mar 19, 2014
# Mail: xiaoning.liu.leon@gmail.com

import log, sys
sys.path.append("./yirendai")
sys.path.append("./shixinren")
sys.path.append("./honglingchuangtou")
sys.path.append("./fujiancourt")
sys.path.append("./renrendai")
sys.path.append("./ppdai")

import yirendai
import shixinren
import honglingchuangtou
import fujiancourt
import renrendai
import ppdai

def main():
  if __name__ == "__main__":
    log.write("spider", "info", "Spider starts...")
    # Below are all the entrance for different websites
    
    print "\n---------- yirendai ----------\n"
    print "Begin search for yirendai..."
    yirendai.yirendai_start()
    print "Finish search for yirendai..."
    
    print "\n---------- shixinren ----------\n"
    print "Begin search for yirendai..."
    shixinren.shixinren_start()
    print "Finish search for yirendai..."
    
    print "\n---------- honglingchuangtou ----------\n"
    print "Begin search for honglingchuangtou..."
    honglingchuangtou.honglingchuangtou_start()
    print "Finish search for honglingchuangtou..."
    
    print "\n---------- fujiancourt ----------\n"
    print "Begin search for fujiancourt..."
    fujiancourt.fujiancourt_start()
    print "Finish search for fujiancourt..."
    
    print "\n---------- renrendai ----------\n"
    print "Begin search for renrendai..."
    renrendai.renrendai_start()
    print "Finish search for renrendai..."
    
    print "\n---------- ppdai ----------\n"
    print "Begin search for ppdai..."
    ppdai.ppdai_start()
    print "Finish search for ppdai..."
    
main()