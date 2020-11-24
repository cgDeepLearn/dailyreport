#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : fetch_data.py 
# @Author : cgDeepLearn
# @Create Date : 2020/10/29-10:36 上午

import datetime
from db_interface import db_interface
import numpy as np


class FetchBasic(object):
    def __init__(self, credit_type='CreditA', report_days=7):
        """credit_type:
                CreditA - 征信源A
                CreditB - 征信源B
                CreditC - 征信源C
                CreditD - 征信源D
                ...更多
        """
        self.datas = list()
        self.report_days = report_days
        self.credit_type = credit_type
        self.credit_table = ''
        self.credit_apply_field = ''
        self.credit_data_field = ''
        self.credit_product_field = ''
        self.prepare()  # 准备

    def prepare(self):
        if self.credit_type in self.credit_table_map:
            self.credit_table = self.credit_table_map[self.credit_type]  # 数据表
            self.credit_apply_field = self.credit_apply_map[self.credit_type]  # 进件字段
            self.credit_data_field = self.credit_data_map[self.credit_type]  # 征信结果数据
            self.credit_product_field = self.credit_product_map[self.credit_type]  # 查征产品大类
        else:
            raise Exception('intput credit_type [{}] error, only support in {}'.format(
                self.credit_type, self.credit_table_map.keys()))

    @property
    def credit_type_name(self):
        name_map = {
            'CreditA': 'A征信',
            'CreditB': 'B征信',
            'CreditC': 'C征信',
            'CreditD': 'D征信',
        }
        if self.credit_type in name_map.keys():
            name = name_map[self.credit_type]
        else:
            name = self.credit_type
        return name

    @property
    def credit_table_map(self):
        """各征信对应数据表"""
        table_map = {
            'CreditA': 'credit_db_a',
            'CreditB': 'credit_db_b',
            'CreditC': 'credit_db_c',
            'CreditD': 'credit_db_d',
        }
        return table_map

    @property
    def credit_apply_map(self):
        """各征信数据表对应apply_id进件字段"""
        apply_map = {
            'CreditA': 'apply_id',
            'CreditB': 'uniq_id',
            'CreditC': 'uniq_id',
            'CreditD': 'uniq_id',
        }
        return apply_map

    @property
    def credit_product_map(self):
        """各征信数据表对应product_id字段,这是为了兼容数据表不一致的情况
        A征信有product_id字段，其他的没有 ,其他的征信源根据cache_key来看,这里使用'-1'作为缺省值"""
        apply_map = {
            'CreditA': 'product_id',
            'CreditB': '-1',  # 无
            'CreditC': '-1',  # 无
            'CreditD': '-1',  # 无
        }
        return apply_map

    @property
    def credit_data_map(self):
        """各征信数据表对应结果字段，这是为了兼容字段不一致的情况"""
        apply_map = {
            'CreditA': 'result',
            'CreditB': 'data',
            'CreditC': 'data',
            'CreditD': 'data',
        }
        return apply_map

    @property
    def query_fileds(self):
        """查询字段
        众安表有product_id"""
        fields = [self.credit_apply_field, 'status', 'method', 'cache_key']
        if self.credit_type == 'CreditA':
            fields.append('product_id')
        else:
            fields.append('-1')
        return ','.join(fields)

    def get_yestoday_data(self, include_today=False):
        datas = list()
        end_date = datetime.date.today()
        begin_date = end_date - datetime.timedelta(days=1)
        begin_date_str = datetime.datetime.strftime(begin_date, '%Y-%m-%d')
        end_date_str = datetime.datetime.strftime(end_date, '%Y-%m-%d')
        if include_today:
            end_date += datetime.timedelta(days=1)
            begin_date += datetime.timedelta(days=1)
        sql = """ SELECT {} FROM {}
        WHERE source = 1 AND created_at >= %s AND created_at < %s
        """.format(self.query_fileds, self.credit_table)
        values = [begin_date_str, end_date_str]
        for row in db_interface.db1_check.select(sql, values):
            record = [int(r) if index <= 1 else r for index, r in enumerate(row)]  # apply_id/uniq_id 和status转int
            datas.append(record)
        return datas

    def _get_range_data(self, begin_date, end_date):
        """status:
            1 - 成功
            2 - 失败(众安前置审核失败)
            3 - 查询中
            4 - 杭银失败(-400征信为空)
            5 - 中裔四要素验证失败
        """
        STATUS_SUCCESS = 1  # 查询成功
        STATUS_CreditA_FAIL = 2  # A征信查询失败
        STATUS_QUERYING = 3  # 查询中
        STATUS_CreditB_FAIL = 4  # B征信查询失败
        STATUS_CreditC_FAIL = 5  # C征信查询失败
        STATUS_CreditD_FAIL = 6  # D征信查询失败
        total_cnt = 0  # 总量
        success_cnt = 0  # 成功量
        querying_cnt = 0  # 查询中量
        fail_cnt = 0  # 失败量
        special_fail_cnt = 0  # 特殊失败量
        begin_date_str = datetime.datetime.strftime(begin_date, '%Y-%m-%d')
        sql = '''
        SELECT status, count(1) FROM {}
        where source = 1 and method regexp 'rule'  and created_at >= %s and created_at < %s
        group by status
        '''.format(self.credit_table)
        values = [begin_date, end_date]
        for row in db_interface.db1.select(sql, values):
            total_cnt += int(row[1])
            if int(row[0]) == STATUS_SUCCESS:
                success_cnt += int(row[1])
            elif int(row[0]) == STATUS_QUERYING:
                querying_cnt += int(row[1])
            else:
                fail_cnt += int(row[1])
                if self.credit_type == 'CreditA' and int(row[0]) == STATUS_CreditA_FAIL:
                    # A征信失败
                    special_fail_cnt += int(row[1])
                elif self.credit_type == 'CreditB' and int(row[0]) == STATUS_CreditB_FAIL:
                    # B征信失败
                    special_fail_cnt += int(row[1])
                elif self.credit_type == 'CreditC' and int(row[0]) == STATUS_CreditC_FAIL:
                    # C征信失败
                    special_fail_cnt += int(row[1])
                elif self.credit_type == 'CreditD' and int(row[0]) == STATUS_CreditD_FAIL:
                    # D征信失败
                    special_fail_cnt += int(row[1])
        data = [begin_date_str, self.credit_type, total_cnt, success_cnt,
                querying_cnt, fail_cnt, special_fail_cnt]
        return data

    def get_summary_data(self):
        """获取近几天的数据"""
        sum_datas = list()
        today = datetime.date.today()
        # 日期起始列表
        days_range = range(1, self.report_days + 1, 1)
        date_pairs = [(today - datetime.timedelta(days=i), today - datetime.timedelta(days=i - 1)) for i in days_range]
        for date_pair in date_pairs:
            data = self._get_range_data(date_pair[0], date_pair[1])
            sum_datas.append(data)
        return sum_datas


def get_data(credit_type='CreditA', summary=False, report_days=7, include_today=False):
    credit_fetch = FetchBasic(credit_type=credit_type, report_days=report_days)
    if summary:
        data = credit_fetch.get_summary_data()
    else:
        data = credit_fetch.get_yestoday_data(include_today=include_today)
    return data
    # data = credit_fetch.get_yestoday_data()
    # np_data = np.array(data)
    # np.save('data_save_{}'.format(credit_type), np_data)


if __name__ == '__main__':
    get_data(credit_type='CreditA', summary=True)
