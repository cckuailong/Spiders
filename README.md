# Spiders

随便写的爬虫

## zhihu

爬取知乎follow（关注）关系，用于构建社交关系网络拓扑

- crawl.py          爬虫
- install.sh        安装环境
- zhihu_follow.sql  爬取的75w条无重复数据

## movie

爬取电影网站的电影下载链接，参见（https://github.com/cckuailong/DLMovies）

- getMovie.py   爬虫
- handle.py     处理爬取的数据为mysql load data infile的格式
- mv_info.sql   爬好的数据
