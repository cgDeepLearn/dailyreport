# dailyreport
generate daily report by python and send  email 
根据数据定时生成每日报表并发送邮件

## 1. 获取数据
    - 示例从db1/db2提取近几天或者前一天的数据，
    - 并将数据转换成`numpy` data
    
## 2. pandas解析提取数据
    - 根据数据性质和需要 利用pandas进行转换,生成基本的DataFrame或者时间序列
    - 利用pandas清理冗余数据、填充缺失数据
    - 对DataFrame 调整index和columns或者生成新的列或者多重索引
    
    
## 3. 分析汇总数据
    - 利用pandas对DataFrame进行聚合分析
    - 转换轴、聚合计算、汇总，生产数据
    - 利用matplotlib对聚合汇总数据生成相应的图片(柱状图、折线图、饼图等)
    
## 4. 发送邮件
    - 配置邮件格式、收发人、连接等
    - 对分析汇总的数据、图片、附件填充到邮件
   
## 5. 配置定时任务
    - 测试手动运行情况 (`python daily_report.py`)
    - 配置crontab定时任务


