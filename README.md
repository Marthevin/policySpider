Policy Spider : a python based tool for scrawling policies on Chinese State's Council Lawsuit Office
====================================================================================================


What is policySpider?
----------------------

pilicySpider is a tool for school academics in China who lack policy data for further research. This little
tool provides both single-thread mode as well as multi-thread mode. It uses basic python package urllib, urllib2
for connection with website, a third-party package bs4-BeautifulSoup for extracting web elements, and pymysql to
store the data into databases.

Requirements
------------
* python 2.7
* MySQL 5.6
* bs4
* lxml

How to Use it
-------------
All global vars are defined at the beginning of the programs. All you need to do is to replace the URL,HEADERS,
POST_DICT for web request, and for simple, the mysql connection parameters.This is only designed for scrawling
policy in China States Council Lawsuit Office(http://search.chinalaw.gov.cn/search2.html). And if you want to get policies of your interest, you can design
your particular keywords. Just run it to see what will happen in your mysql database.And then gradually modify
the programming for your own use...

Notice
--------------
This project will be uodated later. I will appreciate it if anyone can give some productive advice for me.And if 
this little project does do some good for you, PLEASE DO NOT HESITATE TO GIVE YOUR STAR FOR ME. THX.

