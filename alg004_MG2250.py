"""
Provides:
伺服阀泄漏指标，计算稳态伺服阀开口度
==============
Input Signals (4):
* 实际辊缝值：    gap_act
* 速度给定值:     speed_ref
* 伺服阀开口度：  sv_out
* 伺服阀前截止阀: cutoff_valve

Parameter Configs (4)：
* 实际辊缝给定下限
* 实际辊缝给定上限
* 稳态持续时间下限(秒)
* 标志值
==============
Outputs:
指标   |  指标id
---------------------
* 伺服阀开口度均值：  10400
* 伺服阀开口度标准差：10401
* 伺服阀开口度最大值：10402
* 伺服阀开口度最小值：10403
==============
Notes：
标志值对于助卷辊为停机信号，对于卷曲夹送辊为位置给定值
==============
Author: wangyong
"""

import numpy as np
from graph import Index
import com_util


class Alg004:
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
            idx = (df.gap_act >= algparas[0]) & (df.gap_act <= algparas[1]) \
                  & (df.speed_ref == algparas[3]) & (df.cutoff_valve == 1)   # 停机伺服阀稳态开口度
            n = algparas[2] * df.num_per_sec
            re_iter = com_util.Reg.finditer(idx, n)
            for i in re_iter:
                [stidx, edidx] = i.span()
                if edidx - stidx > n:
                    measdate.append(df.index[stidx + int(n/5)])
                    avg_sv_out.append(np.mean(df.sv_out[stidx+int(n/5):edidx-int(n/5)]))
                    std_sv_out.append(np.std(df.sv_out[stidx+int(n/5):edidx-int(n/5)]))
                    max_sv_out.append(np.max(df.sv_out[stidx+int(n/5):edidx-int(n/5)]))
                    min_sv_out.append(np.min(df.sv_out[stidx+int(n/5):edidx-int(n/5)]))
        return measdate, avg_sv_out, std_sv_out, max_sv_out, min_sv_out

    def execute(self):
        df = self.graph.get_data_from_protobuf(['gap_act', 'speed_ref', 'sv_out', 'cutoff_valve'])
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
        self.graph.set_alarm('液压传动系统参数值异常，存在泄露异常特征！')