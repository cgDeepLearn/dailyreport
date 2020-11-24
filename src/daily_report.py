#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : daily_report.py 
# @Author : cgDeepLearn
# @Create Date : 2020/11/2-2:48 下午


import datetime
from utils.sendmail import send_mail
from fetch_data import get_data
from utils.get_html import GetHtml
from collections import OrderedDict
import numpy as np
import pandas as pd
import config
from gen_img import GenIMG

status_map = {
        0: '查询准备中',
        1: '成功',
        2: 'A失败',
        3: '查询中',
        4: 'B失败',
        5: 'C失败',
        6: 'D失败',
        # ...更多
    }


def cachekey_to_product(s):
    product_key = s['cache_key'].replace('_rule_model', '').replace('_rule', '')
    product_map = {
        'product1': '产品1',
        'product2': '产品2',
        'product3': '产品3',
        'product4': '产品4',
        'product5': '产品5',
        'product6': '产品6',
        'product7': '产品7',
        'product8': '产品8',
    }
    if product_key in product_map.keys():
        product_name = product_map[product_key]
    else:
        product_name = product_key
    return product_name


def status_to_code(s):
    if s['status'] in status_map.keys():
        code = status_map[s['status']]
    else:
        code = s['status']
    return code


class Report(object):
    def __init__(self, report_name):
        self.report_name = report_name
        self.report_date = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
        self.html = GetHtml()
        self.images = list()
    
    def get_apollo_config(self):
        email_configs = config.email_configs
        basic_email_tos = email_configs['email_to'].split(',')
        final_credit_email_users = list(set(basic_email_tos + email_configs['credit_email_to'].split(',')))
        credit_emails = ['{}@xxx.com'.format(name) for name in final_credit_email_users if name != '']
        email_configs.update({'credit_emails': credit_emails})
        return email_configs

    def gen_report(self):
        """need to be implement"""
        datas = list()
        table_name = '表名'
        header = '表头'
        self.html.add_table(table_name, header, datas)
        return self.html.output_html()

    def send_report(self, report):
        title = '{}-{}'.format(self.report_name, self.report_date)
        apollo_config = self.get_apollo_config()
        email_to = apollo_config['credit_emails']
        send_mail(email_to, title, report)


class CreditSumReport(Report):
    def __init__(self):
        self.report_name = '查征概要报表'
        super(CreditSumReport, self).__init__(self.report_name)

    def df_to_img(self, img_name, df, summary=False):
        gen_image = GenIMG(img_name=img_name, pd_data=df)
        img_file = gen_image.process(sum=summary)
        self.images.append(img_file)
        self.html.add_img(img_name)

    def gen_report(self):
        """获取数据生成报表"""
        credit_name_map = OrderedDict()
        credit_name_map['za'] = '众安'
        credit_name_map['CreditA'] = 'A征信'
        credit_name_map['CreditB'] = 'B征信'
        credit_name_map['CreditC'] = 'C征信'
        credit_name_map['CreditD'] = 'D征信'
        credit_special_fail_map = {
            'CreditA': 'A征信特殊失败',
            'CreditB': 'B征信特殊失败',
            'CreditC': 'C征信特殊失败',
            'CreditD': 'D征信特殊失败',
        }
        all_sum_datas = list()
        for credit_type, credit_name in credit_name_map.items():
            sum_data = get_data(credit_type=credit_type, summary=True, report_days=7)
            all_sum_datas.extend(sum_data)  # 添加到汇总数据
            table_name = '{} 近7日查征概要'.format(credit_name)
            header = ['', '征信源', '日查询总量', '查询成功量', '在查询中量', '查询失败总量', '特殊失败量']
            header[-1] = credit_special_fail_map.get(credit_type, '特殊失败量')
            self.html.add_table(table_name, header, sum_data)
            # 单个数据源分析
            pd_data = pd.DataFrame(
                np.array(sum_data),
                columns=['date', 'credit_type', 'total', 'success', 'querying', 'fail', 'special_fail'])
            pd_data = pd_data.set_index(['date']).drop(labels=['credit_type'], axis=1).sort_index(ascending=True)
            pd_data = pd_data.apply(pd.to_numeric)  # 转换为数字类型
            self.df_to_img(img_name=credit_type, df=pd_data)  # 生成图片并添加到mail中

        # 汇总数据
        all_sum_datas_pd = pd.DataFrame(np.array(all_sum_datas), columns=['date', 'credit_type', 'total', 'success', 'querying', 'fail', 'special_fail'])
        all_sum_count_pd = all_sum_datas_pd.set_index(['date', 'credit_type']).apply(pd.to_numeric)  # 重新索引
        all_sum_count_goupby_date = all_sum_count_pd.groupby('date').sum()  # 聚合汇总
        self.df_to_img(img_name='sum', df=all_sum_count_goupby_date, summary=True)  # 生成图片

        return self.html.output_html()

    def send_report(self, report):
        title = '{}-{}'.format(self.report_name, self.report_date)
        apollo_config = self.get_apollo_config()
        email_to = apollo_config['credit_emails']
        send_mail(email_to, title, report, images=self.images)


class CreditDetailReport(Report):
    def __init__(self):
        self.report_name = '昨日查征详细报表'
        super(CreditDetailReport, self).__init__(self.report_name)

    def gen_report(self, include_today=False):
        credit_name_map = OrderedDict()
        credit_name_map['CreditA'] = 'A征信'
        credit_name_map['CreditB'] = 'B征信'
        credit_name_map['CreditC'] = 'C征信'
        credit_name_map['CreditD'] = 'D征信'
        credit_special_fail_map = {
            'CreditA': 'A征信特殊失败',
            'CreditB': 'B征信特殊失败',
            'CreditC': 'C征信特殊失败',
            'CreditD': 'D征信特殊失败',
        }
        all_yestoday_data = list()
        for credit_type, credit_name in credit_name_map.iteritems():
            print credit_type
            credit_data = get_data(credit_type=credit_type, include_today=include_today)
            if not credit_data:
                continue
            all_yestoday_data.extend(credit_data)
            pd_data = pd.DataFrame(np.array(credit_data),
                                   columns=['apply_id', 'status', 'method', 'cache_key', 'product_id'])
            pd_data['status'] = pd_data['status'].apply(int)
            rule_df = pd_data[pd_data['method'].str.contains('rule')]  # 规则
            model_df = pd_data[pd_data['method'].str.contains('rule')]  # 模型
            rule_df['product_name'] = rule_df.apply(cachekey_to_product, axis=1)
            count_df = rule_df[['product_name', 'status']]
            groupby_product = count_df.groupby(['product_name', 'status']).size()
            product_status_count = groupby_product.unstack(level=1, fill_value=0)  # status unstack到列
            col_name = sorted(product_status_count.columns.tolist())
            col_name_str = [status_map[col] for col in col_name]

            product_status_count['query_total'] = product_status_count.sum(axis=1)
            col_name.insert(0, 'query_total')
            col_name_str.insert(0, '请求')
            sum_data = [product_status_count.sum(axis=0)[col] for col in col_name]
            sum_info = ['合计'] + sum_data
            product_status_count['product_name'] = product_status_count.index
            col_name.insert(0, 'product_name')
            col_name_str.insert(0, '产品')

            table_data_df = product_status_count.reindex(columns=col_name)
            table_datas = table_data_df.values.tolist()
            table_datas.append(sum_info)
            table_name = '{} 查征明细'.format(credit_name)
            header = col_name_str
            self.html.add_table(table_name, header, table_datas)
        return self.html.output_html()

    def send_report(self, report):
        title = '{}-{}'.format(self.report_name, self.report_date)
        apollo_config = self.get_apollo_config()
        email_to = apollo_config['credit_emails']
        send_mail(email_to, title, report, images=self.images)
        

if __name__ == '__main__':

    # 概要
    credit_summary = CreditSumReport()
    summary_report = credit_summary.gen_report()  # 生成报表
    credit_summary.send_report(summary_report)  # 发送报表

    # 细分
    credit_detail = CreditDetailReport()
    yestoday_detail_report = credit_detail.gen_report()

    # 今天截止到现在的情况
    today_detail_report = credit_detail.gen_report(include_today=True)
    credit_detail.send_report(yestoday_detail_report)
    credit_detail.send_report(today_detail_report)


