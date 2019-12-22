# Spiders

随便写的爬虫

## zhihu

爬取知乎follow（关注）关系，用于构建社交关系网络拓扑

- crawl.py          爬虫
- install.sh        安装环境
- zhihu_follow.sql  爬取的75w条无重复数据

## dl_movie

爬取电影网站的电影下载链接，参见 (https://github.com/cckuailong/DLMovies)

- getMovie.py   爬虫
- handle.py     处理爬取的数据为mysql load data infile的格式
- mv_info.sql   爬好的数据

## ol_movie

爬取电影网站的电影在线观看链接

- getMovie_pc.py    爬虫，根据PC端网页编写
- getMovie_mb.py    爬虫，根据mobile（手机）端网页编写
- handle.py         处理爬取的数据为mysql load data infile的格式

## scada

抓取scada默认密码，形成markdown形式表格

- scada.html    网页信息
- handle.py     爬取处理html
- table.md      生成的markdown形式表格
