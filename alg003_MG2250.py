"""
Provides:
伺服阀动作过程状态分析（辊缝上升沿、下降沿），计算进出口压差指标
==============
Input Signals (3):
* 实际辊缝值：gap_act
* 无杆腔压力: pis_pressure
* 有杆腔压力: rod side

Parameter Configs (4)：
* 上升（下降）沿辊缝最小值
* 上升（下降）沿辊缝最大值
* 上升（下降）沿持续时间下限（秒）
* 上升（下降）沿辊缝值变化量下限
==============
Outputs:
指标   |  指标id
---------------------
* 上升沿压差均值：  10300
* 上升沿压差标准差：10301
* 上升沿压差最大值：10302
* 上升沿压差最小值：10302
* 下降沿压差均值：  10304
* 下降沿压差标准差：10305
* 下降沿压差最大值：10306
* 下降沿压差最小值：10307
"""

import numpy as np
from graph import Index
import com_util


class Alg003:
    def __init__(self, graph):
        self.graph = graph

    @staticmethod
    def get_fe(df, algparas):
        measdate1 = []
        avg_pressure1 = []
        std_pressure1 = []
        max_pressure1 = []
        min_pressure1 = []
        measdate2 = []
        avg_pressure2 = []
        std_pressure2 = []
        max_pressure2 = []
        min_pressure2 = []
        if not df.empty:
            idx = (df.gap_act >= algparas[0]) & (df.gap_act <= [1])
            re_iter = com_util.Reg.finditer(idx, algparas[2] * df.num_per_sec)
            for i in re_iter:
                [stidx, edidx] = i.span()
                dgap = df.gap_act[stidx] - df.gap_act[edidx-1]
                if abs(dgap) < algparas[3]:  # 开始结束时间辊缝值变化小于门限不计算指标
                    continue
                dp = df.pis_pressure[stidx:edidx] - df.rod_pressure[stidx:edidx]  # 压差
                if dgap < 0:  # 上升沿
                    avg_pressure1.append(np.mean(dp))
                    std_pressure1.append(np.std(dp))
                    max_pressure1.append(np.max(dp))
                    min_pressure1.append(np.min(dp))
                    measdate1.append(df.index[stidx])
                else:  # 下降沿
                    avg_pressure2.append(np.mean(dp))
                    std_pressure2.append(np.std(dp))
                    max_pressure2.append(np.max(dp))
                    min_pressure2.append(np.min(dp))
                    measdate2.append(df.index[stidx])

        return measdate1, avg_pressure1, std_pressure1, max_pressure1, min_pressure1,\
            measdate2, avg_pressure2, std_pressure2, max_pressure2, min_pressure2

    def execute(self):
        df = self.graph.get_data_from_api(['gap_act', 'pis_pressure', 'rod_pressure'])
        measdate1, avg_pressure1, std_pressure1, max_pressure1, min_pressure1, \
        measdate2, avg_pressure2, std_pressure2, max_pressure2, min_pressure2 \
            = self.get_fe(df, self.graph.parameter)

        for i, meastime in enumerate(measdate1):
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "10300",
                           'value1st': avg_pressure1[i], 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "10301",
                           'value1st': std_pressure1[i], 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "10302",
                           'value1st': max_pressure1[i], 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "10303",
                           'value1st': min_pressure1[i], 'indices2nd': []})
            self.graph.indices.append(index)

        for i, meastime in enumerate(measdate2):
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "10304",
                           'value1st': avg_pressure2[i], 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "10305",
                           'value1st': std_pressure2[i], 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "10306",
                           'value1st': max_pressure2[i], 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "10307",
                           'value1st': min_pressure2[i], 'indices2nd': []})
            self.graph.indices.append(index)
