# weibo-spider
新浪微博爬虫（仅适用于爬取某条微博的评论区，爬取一级评论和二级评论）

## 运行效果
传递特定一条微博的id，即可爬取该微博的评论区，仅包含一级评论和二级评论（一般几千条可完整爬取，不会报错。更多条有可能报错，但可以保存正常的前几千条，因为已经满足我需求了，就没有优化），爬取结果会保存在csv文件中。

## 使用步骤
1. 导入相关的依赖，直接看主代码需要什么就导入什么
2. 找到要爬取的微博的id，替换main方法中对应位置的id（注意是某条博文的id，而不是用户的id）
   ![image](https://github.com/ValoraY/weibo-spider/assets/65067116/89dcbb20-5c15-4e84-9e72-520babbaf057)
4. 运行程序
