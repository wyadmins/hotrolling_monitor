"""
Provides:
马钢双仪表检测
==============
Input Signals (2):
* 仪表1信号：signal1
* 仪表2信号：signal2

Parameter Configs (5)：
*  信号类型：模拟量 -> 1 , 0/1型量 -> 2
*  模拟量聚合时间（s）
*  模拟量偏差门限（%）
*  0-1量报警点数要求
*  0-1量报警时长要求（s）

==============
Outputs:
指标   |  指标id
---------------------

"""


import numpy as np
from graph import Event


class Alarm001:
    def __init__(self, graph):
        self.graph = graph

    def get_alarm_analogs(self, p2, p3):
        """
        模拟量信号
        """
        df = self.graph.get_data_from_api(['signal1', 'signal2'])
        if not df.empty:
            df = df.resample(f'{p2}S').mean()
            r = (np.abs(df['signal1'] - df['signal2']) / np.mean(df['signal1'] + df['signal2'])) * 100   # 双仪表相对偏差（%）
            if np.any(r) > p3:
                event = Event({'assetid': self.graph.deviceid, 'meastime': df.index[0], 'level': 1, 'info': '双仪表数值不匹配'})
                self.graph.events.append(event)

    def get_alarm_logical(self, p4, p5):
        """
        0-1型信号
        """
        df = self.graph.get_data_from_api(['signal1', 'signal2'])
        if not df.empty:
            n = np.sum(np.abs(df['signal1'] - df['signal2']))
            t = n * df.dt
            if t > p4 or n > p5:
                event = Event({'assetid': self.graph.deviceid, 'meastime': df.index[0], 'level': 1, 'info': '双仪表数值不匹配'})
                self.graph.events.append(event)

    def execute(self):
        [p1, p2, p3, p4, p5] = self.graph.parameter
        if 1 == p1:
            self.get_alarm_analogs(p2, p3)   # 模拟量信号双仪表检测
        elif 2 == p1:
            self.get_alarm_logical(p4, p5)   # 0/1类型信号双仪表检测


