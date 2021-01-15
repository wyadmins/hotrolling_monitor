"""
Provides:
液位漏油特征监测
==============
Input Signals(1):
* level: 液位
* 抑制信号

Parameter Configs(3)：
* 聚合时长(s)
* 液位下降持续时间(min)
* 液位下降程度 (mm)


==============
Outputs:
指标   |  指标id
---------------------


Note:
* (1)满足液位持续下降时间和液位下降标准
* (2)存在抑制信号时,满足抑制条件
* 直接报警
Author: wangyong
"""
import pandas as pd
import numpy as np
from graph import Event


class Alg023:
    def __init__(self, graph):
        self.graph = graph

    def get_alarm(self):
        algparas = self.graph.parameter
        df = self.graph.get_data_from_protobuf(['liquid_level'])

        if df.empty:
            return

        resampled_level = df['liquid_level'].resample(f'{algparas[0]}S').mean()  # 原始趋势聚合
        max_fall  = resampled_level.diff().rolling(algparas[1]).sum()  # 检测液位下降最大程度
        if max_fall >= algparas[2]:
            event = Event({'assetid': self.graph.deviceid, 'assetname': self.graph.devicename,
                           'aiid': self.graph.aiid,
                           'meastime': df.index[0], 'level': 1, 'info': '报警：液位下降异常，存在泄露异常特征！！'})
            self.graph.events.append(event)

    def execute(self):
        self.get_alarm()


