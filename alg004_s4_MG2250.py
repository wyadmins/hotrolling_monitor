"""
Provides:
伺服阀泄漏指标，计算稳态伺服阀开口度 (活套)
==============
Input Signals (5):
* 伺服阀A设定值：a_ref
* 伺服阀A前截止阀：a_cutoff_valve
* 伺服阀B设定值：b_ref
* 伺服阀B前截止阀：b_cutoff_valve
* 位置实际值：value_act

Parameter Configs (3)：
* 实际位置值给定下限
* 实际位置值给定上限
* 稳态时长下限（s）
==============
Outputs:
指标   |  指标id
---------------------
* 伺服阀开口度均值：  10400
* 伺服阀开口度标准差：10401
* 伺服阀开口度最大值：10402
* 伺服阀开口度最小值：10403
====================
Author: chengqiliang
"""

import numpy as np
from graph import Index
import com_util

class Alg004_S4:
    def __init__(self, graph):
        self.graph = graph

    @staticmethod
    def get_fe(df,  algparas):
        avg_sv_out = []
        std_sv_out = []
        max_sv_out = []
        min_sv_out = []
        measdate = []
        if not df.empty:
            idx1 = (df['a_cutoff_valve'] == 1) & (df['b_cutoff_valve'] == 0) & (df['value_act'] > algparas[0]) & (df['value_act'] < algparas[1])
            re_iter = com_util.Reg.finditer(idx1, algparas[2] * df.num_per_sec)
            for i in re_iter:
                [stidx, edidx] = i.span()
                n = (edidx - stidx) // 5
                measdate.append(df.index[stidx + n])
                avg_sv_out.append(np.mean(df.a_ref[stidx+n: edidx-n]))
                std_sv_out.append(np.std(df.a_ref[stidx + n: edidx - n]))
                max_sv_out.append(np.max(df.a_ref[stidx + n: edidx - n]))
                min_sv_out.append(np.min(df.a_ref[stidx + n: edidx - n]))
            idx2 = (df['b_cutoff_valve'] == 1) & (df['a_cutoff_valve'] == 0) & (df['value_act'] > algparas[0]) & (df['value_act'] < algparas[1])
            re_iter = com_util.Reg.finditer(idx2, algparas[2] * df.num_per_sec)
            for i in re_iter:
                [stidx, edidx] = i.span()
                n = (edidx - stidx) // 5
                measdate.append(df.index[stidx + n])
                avg_sv_out.append(np.mean(df.a_ref[stidx+n: edidx-n]))
                std_sv_out.append(np.std(df.a_ref[stidx + n: edidx - n]))
                max_sv_out.append(np.max(df.a_ref[stidx + n: edidx - n]))
                min_sv_out.append(np.min(df.a_ref[stidx + n: edidx - n]))
        return measdate, avg_sv_out, std_sv_out, max_sv_out, min_sv_out

    def execute(self):
        df = self.graph.get_data_from_api(['a_ref', 'a_cutoff_valve', 'b_ref', 'b_cutoff_valve', 'value_act'])
        measdate, avg_sv_out, std_sv_out, max_sv_out, min_sv_out = self.get_fe(df, self.graph.parameter)
        for i, meastime in enumerate(measdate):
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "10400",
                           'value1st': avg_sv_out[i], 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "10401",
                           'value1st': std_sv_out[i], 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "10402",
                           'value1st': max_sv_out[i], 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "10403",
                           'value1st': min_sv_out[i], 'indices2nd': []})
            self.graph.indices.append(index)
        self.graph.set_alarm('伺服阀稳态开口度异常！')
