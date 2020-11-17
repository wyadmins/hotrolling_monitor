"""
Provides:
伺服阀泄漏指标，计算稳态伺服阀开口度 (F1-F7 AGC)
==============
Input Signals:
* 伺服阀A设定值：a_ref
* 伺服阀A前截止阀：a_cutoff_valve
* 伺服阀B设定值：b_ref
* 伺服阀B前截止阀：b_cutoff_valve
* 位置实际值：value_act
* 参考咬钢信号：single

Parameter Configs：
* 稳态时长下限（s）
* 稳态窗口变异系数门限：范围（0-5）
==============
Outputs:
指标   |  指标id
---------------------
伺服阀设定均值 13500
====================
Author: chenqiliang
"""

import numpy as np
from graph import Index
import com_util

class Alg035:
    def __init__(self, graph):
        self.graph = graph

    def get_alarm(self):
        df = self.graph.get_data_from_api(['a_ref', 'a_cutoff_valve', 'b_ref', 'b_cutoff_valve', 'value_act', 'single'])

        algparas = self.graph.parameter

        measdate = []
        curr_avga = []
        curr_avgb = []

        if df.empty:
            return

        rolling = df['value_act'].rolling(int(algparas[0] * df.num_per_sec), center=True)
        roll_cv = np.abs(rolling.std() / rolling.mean())   # 计算窗口变异系数
        idx = (roll_cv < (algparas[1] / 100)) & (df['a_cutoff_valve'] == 1) & (df['b_cutoff_valve'] == 1) & (df['single'] == 0)

        re_iter = com_util.Reg.finditer(idx, algparas[0] * df.num_per_sec)
        for i in re_iter:
            [stidx, edidx] = i.span()
            n = (edidx - stidx) // 5
            measdate.append(df.index[stidx + n])
            curr_avga.append(np.mean(df.a_ref[stidx + n: edidx - n]))
            curr_avgb.append(np.mean(df.b_ref[stidx + n: edidx - n]))



        value_avg = np.mean(curr_avga) + np.mean(curr_avgb)

        index = Index({'assetid': self.graph.deviceid, 'meastime1st': df.index[0], 'feid1st': "13500",
                       'value1st': value_avg, 'indices2nd': []})
        self.graph.indices.append(index)

    def execute(self):
        self.get_alarm()