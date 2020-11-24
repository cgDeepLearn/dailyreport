#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File : gen_img.py 
# @Author : cgDeepLearn
# @Create Date : 2020/11/4-11:18 上午

import matplotlib as mpl
# mpl.rcParams['font.sans-serif'] = ['SimHei']
# mpl.rcParams['font.serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
mpl.use('Agg')

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

CUR_PATH = os.path.dirname(os.path.abspath(__file__))
IMG_PATH = os.path.join(os.path.dirname(CUR_PATH), "files")


class GenIMG(object):
    def __init__(self, img_name, pd_data):
        self.img_name = img_name
        self.pd_data = pd_data

    def process(self, sum=False):
        kind = 'line'
        title = 'query {} info'.format(self.img_name)
        if sum:
            kind = 'bar'
            title = 'all credit summary info'
        axes_subplot = self.pd_data.plot(kind=kind)
        plt.title(title)
        plt.xlabel("date")
        plt.ylabel("num")
        plt.legend(loc="best")
        plt.grid(True)
        full_path_filename = os.path.join(IMG_PATH, '{}.png'.format(self.img_name))
        plt.savefig(full_path_filename)
        return full_path_filename
