"""
Provides:
伺服阀零偏
==============
Input Signals (2):
* 信号设定：sv_ref
* 信号反馈：sv_act

Parameter Configs (2)：
*  稳态时间持续时长（s）
*  模拟量偏差门限（%）

==============
Outputs:
指标   |  指标id
---------------------
伺服阀零偏 16000
"""


import numpy as np
from graph import Event, Index
import com_util


class Alg016:
    def __init__(self, graph):
        self.graph = graph

    def get_alarm(self):
        """
        模拟量信号
        """
        df = self.graph.get_data_from_api(['sv_ref', 'sv_act'])
        if df.empty:
            return
        algparas = self.graph.parameter
        idx = np.diff(df['sv_ref'])
        re_iter = com_util.Reg.finditer(idx, algparas[0]*df.num_per_sec, flag=0)
        avg = 0
        r = 0
        for i in re_iter:
            [stidx, edidx] = i.span()
            n = (edidx - stidx) // 5
            avg_ref = np.mean(df['sv_ref'][stidx + n:edidx - n])
            avg_act = np.mean(df['sv_act'][stidx + n:edidx - n])
            if abs(avg_ref) >= avg:
                avg = np.mean(df['sv_ref'][stidx + n:edidx - n])
                r = np.abs(avg_ref - avg_act) / avg_ref * 100
        if r > algparas[1]:
            event = Event({'assetid': self.graph.deviceid, 'meastime': df.index[0], 'level': 1, 'info': '伺服阀零偏报警'})
            self.graph.events.append(event)

            index = Index({'assetid': self.graph.deviceid, 'meastime1st': df.index[0], 'feid1st': "16000",
                           'value1st': r, 'indices2nd': []})
            self.graph.indices.append(index)

    def execute(self):
        self.get_alarm()


