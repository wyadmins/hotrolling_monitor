"""
Provides:
电机空载电流均值/标准差
==============
Input Signals (4):
* 钩子状态（放下状态）
* 速度给定
* 实际电流
* 实际转矩

Parameter Configs (5)：
* 空载速度给定下限
* 空载速度给定上限
* 空载持续时长下限（秒）
* 切头（秒）
* 切尾（秒）

==============
Outputs:
指标   |  指标id
---------------------
* 空载电流均值：  10100
* 空载电流标准差：10101
* 空载电流最大值：10102
* 空载电流最小值：10103
* 空载转矩均值：  10104
* 空载转矩标准差：10105
* 空载转矩最大值：10106
* 空载转矩最小值：10107
==============
Notes
1. 加入钩子信号筛选条件，适用于换辊小车
"""


import numpy as np
from graph import Index
import com_util


class Alg001_S2:
    def __init__(self, graph):
        self.graph = graph

    def get_curr_avg_and_std(self):

        df = self.graph.get_data_from_protobuf(['hook_status', 'spd_ref', 'curr_act', 'torq_act'])
        algparas = self.graph.parameter

        curr_avg = []
        curr_std = []
        curr_max = []
        curr_min = []
        torq_avg = []
        torq_std = []
        torq_max = []
        torq_min = []
        measdate = []
        if not df.empty:
            idx = (df.spd_ref >= algparas[0]) & (df.spd_ref <= algparas[1]) & (0 == df.hook_status)
            re_iter = com_util.Reg.finditer(idx, int(algparas[2] * df.num_per_sec))
            n1 = int(algparas[3] * df.num_per_sec)
            n2 = int(algparas[4] * df.num_per_sec)
            for i in re_iter:
                [stidx, edidx] = i.span()
                if edidx - stidx > 2 * n1:
                    measdate.append(df.index[stidx + n1])
                    curr_avg.append(np.mean(df.curr_act[stidx+n1: edidx-n2]))  # 切头切尾
                    curr_std.append(np.std(df.curr_act[stidx+n1: edidx-n2]))
                    curr_max.append(np.max(df.curr_act[stidx+n1: edidx-n2]))
                    curr_min.append(np.min(df.curr_act[stidx+ n1: edidx-n2]))
                    torq_avg.append(np.mean(df.torq_act[stidx+n1: edidx-n2]))  # 切头切尾
                    torq_std.append(np.std(df.torq_act[stidx+n1: edidx-n2]))
                    torq_max.append(np.max(df.torq_act[stidx+n1: edidx-n2]))
                    torq_min.append(np.min(df.torq_act[stidx+n1: edidx-n2]))

        return measdate, curr_avg, curr_std, curr_max, curr_min, \
               torq_avg, torq_std, torq_max, torq_min

    def execute(self):
        measdate, curr_avg, curr_std, curr_max, curr_min, torq_avg, torq_std, torq_max, torq_min \
            = self.get_curr_avg_and_std()
        for i, meastime in enumerate(measdate):
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "10100",
                           'value1st': curr_avg[i], 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "10101",
                           'value1st': curr_std[i], 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "10102",
                           'value1st': curr_max[i], 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "10103",
                           'value1st': curr_min[i], 'indices2nd': []})
            self.graph.indices.append(index)
            if torq_avg:
                index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "10104",
                               'value1st': torq_avg[i], 'indices2nd': []})
                self.graph.indices.append(index)
                index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "10105",
                               'value1st': torq_std[i], 'indices2nd': []})
                self.graph.indices.append(index)
                index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "10106",
                               'value1st': torq_max[i], 'indices2nd': []})
                self.graph.indices.append(index)
                index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "10107",
                               'value1st': torq_min[i], 'indices2nd': []})
                self.graph.indices.append(index)
        self.graph.set_alarm('电机卡阻特征！')


