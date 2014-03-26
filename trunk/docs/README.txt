### Database
115.28.134.240:3306
User:pig
Password:ILikeBigPig888
DB:spider

### Python
Version: 2.7.6

### MySQLdb
Version: 1.2.4
Download: http://sourceforge.net/projects/mysql-python/
Document: http://mysql-python.sourceforge.net/MySQLdb.html#installation

### 编码规范
1. py代码文件采用utf-8 without BOM编码, 代码第一行表明“encoding=utf-8”
2. 缩进为2空格，不允许使用tab
3. 函数名开头小写，类名大写，配置变量全大写，采用驼峰式；

### 项目结构
1. 每个网站对应python代码应该至少包括2个py文件，1个为配置文件，1个为入口文件
2. 入口文件为网站中文名称小写全拼或英文名，配置文件在入口文件基础上增加”_config”后缀；
3. URL地址、URL中数字范围、网络超时、输入输出路径等参数应该配置在配置文件中；
4. db.py, config.py, log.py 为项目全局文件，分别作为数据库接口、配置文件、日志接口使用；
