"""
Provides:
伺服阀零偏
==============
Input Signals (2):
* 信号设定：sv_ref
* 信号反馈：sv_act

Parameter Configs (3)：
* 稳态窗口时长（s）
* 稳态窗口变异系数门限：0-0.5， 大于该值则数据包不包含稳态工况
* 偏差报警门限（%）

==============
Outputs:
指标   |  指标id
---------------------
伺服阀零偏 16000
"""


import numpy as np
import pandas as pd
from graph import Event, Index


class Alg016:
    def __init__(self, graph):
        self.graph = graph

    def get_alarm(self):
        df = self.graph.get_data_from_protobuf(['sv_ref', 'sv_act'])
        if df.empty:
            return
        algparas = self.graph.parameter

        if np.all(df['sv_ref'] == 0):
            return
        rolling = df['sv_ref'].rolling(int(algparas[0] / df.dt))
        roll_cv = np.abs(rolling.std() / rolling.mean())   # 计算参考值窗口变异系数

        min_cv = roll_cv.min()
        if min_cv > algparas[1]:   # 数据包不包含稳态工况
            return

        stidx = roll_cv.idxmin() - pd.Timedelta(algparas[0]/2, unit='s')
        edidx = roll_cv.idxmin() + pd.Timedelta(algparas[0]/2, unit='s')

        n = (edidx - stidx) // 5  # 对稳态段切头切尾
        avg_ref = np.mean(df['sv_ref'][stidx + n:edidx - n])
        avg_act = np.mean(df['sv_act'][stidx + n:edidx - n])

        r = np.abs(avg_ref - avg_act)  # 计算稳态工况设定值与实际值偏差

        index = Index({'assetid': self.graph.deviceid, 'meastime1st': df.index[0], 'feid1st': "16000",
                       'value1st': r, 'indices2nd': []})
        self.graph.indices.append(index)

        if r > algparas[2]:
            event = Event({'assetid': self.graph.deviceid, 'assetname': self.graph.devicename,
                           'aiid': self.graph.aiid,
                           'meastime': df.index[0], 'level': 1, 'info': '报警：伺服阀零偏异常！'})
            self.graph.events.append(event)

    def execute(self):
        self.get_alarm()


