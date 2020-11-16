"""
Provides:
伺服阀泄漏指标，计算稳态伺服阀开口度 (活套)
==============
Input Signals:
* 伺服阀A设定值：a_ref
* 伺服阀A前截止阀：a_cutoff_valve
* 伺服阀B设定值：b_ref
* 伺服阀B前截止阀：b_cutoff_valve
* 位置实际值：value_act

Parameter Configs：
* 实际位置值给定下限
* 实际位置值给定上限
* 稳态时长下限（s）
==============
Outputs:
指标   |  指标id
---------------------
伺服阀设定均值 13100
====================
Author: chenqiliang
"""

import numpy as np
from graph import Index
import com_util

class Alg031:
    def __init__(self, graph):
        self.graph = graph

    def get_alarm(self):
        df = self.graph.get_data_from_api(['a_ref', 'a_cutoff_valve', 'b_ref', 'b_cutoff_valve', 'value_act'])

        algparas = self.graph.parameter

        measdate = []
        curr_avg = []

        if df.empty:
            return

        idx1 = (df['a_cutoff_valve'] == 1) & (df['value_act'] > algparas[0]) & (df['value_act'] < algparas[1])
        re_iter = com_util.Reg.finditer(idx1, algparas[2] * df.num_per_sec)
        for i in re_iter:
            [stidx, edidx] = i.span()
            n = (edidx - stidx) // 5
            measdate.append(df.index[stidx + n])
            curr_avg.append(np.mean(df.a_ref[stidx+n: edidx-n]))


        idx2 = (df['b_cutoff_valve'] == 1) & (df['value_act'] > algparas[0]) & (df['value_act'] < algparas[1])
        re_iter = com_util.Reg.finditer(idx2, algparas[2] * df.num_per_sec)
        for i in re_iter:
            [stidx, edidx] = i.span()
            n = (edidx - stidx) // 5
            measdate.append(df.index[stidx + n])
            curr_avg.append(np.mean(df.b_ref[stidx+n: edidx-n]))
        value_avg = np.mean(curr_avg)

        index = Index({'assetid': self.graph.deviceid, 'meastime1st': df.index[0], 'feid1st': "13100",
                       'value1st': value_avg, 'indices2nd': []})
        self.graph.indices.append(index)

    def execute(self):
        self.get_alarm()