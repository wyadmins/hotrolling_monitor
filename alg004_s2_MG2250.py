"""
Provides:
伺服阀泄漏指标，计算稳态伺服阀开口度 (实现版本2)
==============
Input Signals (3):
* ???：balance_on
* ???：check_value
* 伺服阀开口度：sv_out

Parameter Configs (2)：
* 开口度计算对应balance_on：  [1,0]
* 开口度计算对应check_value： [1,0]
==============
Outputs:
指标   |  指标id
---------------------
* 伺服阀开口度均值：  10400
* 伺服阀开口度标准差：10401
* 伺服阀开口度最大值：10402
* 伺服阀开口度最小值：10403
===============
说明：
* 适用于SSP平衡系统伺服阀
"""

import numpy as np
from graph import Index
import com_util


class Alg004_S2:
    def __init__(self, graph):
        self.graph = graph

    def get_fe(self, algparas):
        df = self.graph.get_data_from_api(['balance_on', 'check_value', 'sv_out'])

        avg_sv_out = []
        std_sv_out = []
        max_sv_out = []
        min_sv_out = []
        measdate = []
        if not df.empty:
            idx = (df.balance_on == algparas[0]) & (df.check_value == algparas[1])
            re_iter = com_util.Reg.finditer(idx, 0)
            for i in re_iter:
                [stidx, edidx] = i.span()
                if edidx - stidx > 0:
                    measdate.append(df.index[stidx])
                    avg_sv_out.append(np.mean(df.sv_out[stidx: edidx]))
                    std_sv_out.append(np.std(df.sv_out[stidx: edidx]))
                    max_sv_out.append(np.max(df.sv_out[stidx: edidx]))
                    min_sv_out.append(np.min(df.sv_out[stidx: edidx]))
        return measdate, avg_sv_out, std_sv_out, max_sv_out, min_sv_out

    def execute(self):
        measdate, avg_sv_out, std_sv_out, max_sv_out, min_sv_out = self.get_fe(self.graph.parameter)
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