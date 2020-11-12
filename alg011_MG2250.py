"""
Provides:
启机次数统计
==============
Input Signals (1):
* 启停标志位（0-1序列）：drive_run

Parameter Configs (1)：
* 启机标志位 [0, 1]
==============
Outputs:
指标   |  指标id
---------------------
* 启机次数：  11100
* 运行时长：  11101
* 停机时长：  11102
"""

import numpy as np
from graph import Index


class Alg011:
    def __init__(self, graph):
        self.graph = graph

    @staticmethod
    def get_fe(df, algparas):
        measdate = []
        switch_nums = 0
        run_time = 0
        stop_time = 0
        if not df.empty:
            measdate = df.index[0]
            if algparas == 0:  # 启机状态标志为0
                n = sum(-1 == np.diff(df.drive_run))   # 启机次数
                n_run = sum(df.drive_run == 0)
            else:
                n = sum(1 == np.diff(df.drive_run))
                n_run = sum(df.drive_run == 1)
            run_time = n_run * df.dt  # 运行时长
            stop_time = (df.shape[0] - n_run) * df.dt  # 停机时长
            if n > 0:
                switch_nums = n
        return measdate, switch_nums, run_time, stop_time

    def execute(self):
        df = self.graph.get_data_from_protobuf(['drive_run'])
        measdate, switch_nums, run_time, stop_time = self.get_fe(df, self.graph.parameter)
        if measdate:
            if switch_nums > 0:
                index = Index({'assetid': self.graph.deviceid, 'meastime1st': measdate, 'feid1st': "11100",
                               'value1st': float(switch_nums), 'indices2nd': []})
                self.graph.indices.append(index)
            if run_time > 0:
                index = Index({'assetid': self.graph.deviceid, 'meastime1st': measdate, 'feid1st': "11101",
                               'value1st': float(run_time), 'indices2nd': []})
                self.graph.indices.append(index)
            if stop_time > 0:
                index = Index({'assetid': self.graph.deviceid, 'meastime1st': measdate, 'feid1st': "11102",
                               'value1st': float(stop_time), 'indices2nd': []})
                self.graph.indices.append(index)