"""
Provides:
伺服阀泄漏指标，计算稳态伺服阀开口度（夹送辊/ FSB夹送辊）
==============
Input Signals (4):
* 伺服阀设定值：sv_out
* 位置设定值: value_ref
* 位置实际值：value_act
* 伺服阀前截止阀: cutoff_valve

Parameter Configs (3):
* 位置实际值给定下限
* 位置实际值给定上限
* 稳态持续时间下限(秒)
==============
Outputs:
指标   |  指标id
---------------------
* 伺服阀开口度均值：  10400
* 伺服阀开口度标准差：10401
* 伺服阀开口度最大值：10402
* 伺服阀开口度最小值：10403
====================
Author: chenqiliang
"""

import numpy as np
from graph import Index
import com_util

class Alg004_S5:
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
            idx = (df['value_act'] >= algparas[0]) & (df['value_act'] <= algparas[1]) & (df['cutoff_valve'] == 1)   # 停机伺服阀稳态开口度
            re_iter = com_util.Reg.finditer(idx, algparas[2] * df.num_per_sec)
            for i in re_iter:
                [stidx, edidx] = i.span()
                n = (edidx - stidx) // 5
                if edidx - stidx > n:
                    measdate.append(df.index[stidx + n])
                    avg_sv_out.append(np.mean(df.sv_out[stidx + n:edidx - n]))
                    std_sv_out.append(np.std(df.sv_out[stidx + n:edidx - n]))
                    max_sv_out.append(np.max(df.sv_out[stidx + n:edidx - n]))
                    min_sv_out.append(np.min(df.sv_out[stidx + n:edidx - n]))
        return measdate, avg_sv_out, std_sv_out, max_sv_out, min_sv_out

    def execute(self):
        df = self.graph.get_data_from_api(['sv_out', 'value_ref','value_act', 'cutoff_valve'])
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