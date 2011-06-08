主程序：book.py

此程序用来将几大门户网站读书频道的书籍扒下来保存为单独的txt文档。
以书名作为txt的文件名，文档正文以UTF-8编码保存。

支援平台：
Windows/Linux/Mac
Python 2.6

使用方法：
一. Windows用户
确定已经安装Python 2.6。
1. 打开CMD窗口，切换至book.py的存放目录。
2. 执行python book.py
3. 在接下来打印的URL:后面粘上你要下载书籍的网址。如： http://book.qq.com/xxxx/xxx/index.shtml
二. Linux/Mac用户
1. 打开终端，切换至book.py所在目录
2. 给程序赋予可执行权限 chmod +x book.py
3. 执行程序 ./book.py
4. 在接下来打印的URL:后面粘上你要下载书籍的网址。如： http://book.qq.com/xxxx/xxx/index.shtml


目前支持的网站有：
1. 腾讯读书  http://book.qq.com
2. 网易读书  http://book.163.com
3. 搜狐读书  http://book.sohu.com
4. 新浪读书  http://book.sina.com.cn
5. 痞客邦    http://blog.pixnet.net
6. 中时部落格  http://blog.chinatimes.com


附例：
sample_Irish_caffee.txt 是使用本程序扒取下来的一个范本，《愛爾蘭咖啡》by 痞子蔡
文章地址： http://jht.pixnet.net/blog/category/632799

Project Home: http://pagebrin.com/projects/getbook

====待完成====