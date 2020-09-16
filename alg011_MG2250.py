"""
Provides:
电机启机次数统计
==============
Input Signals (1):
* 启停标志位（0-1序列）：drive_run

Parameter Configs (1)：
* 启机标志位
==============
Outputs:
指标   |  指标id
---------------------
* 启机次数：  11107
"""

import numpy as np
from graph import Index


class Alg011:
    def __init__(self, graph):
        self.graph = graph

    @staticmethod
    def get_fe(df, algparas):
        measdate = []
        switch_nums = []
        if not df.empty:
            if algparas == 0:
                n = sum(np.diff(df.drive_run) == -1)  # 启机状态为0
            else:
                n = sum(np.diff(df.drive_run) == 1)
            if n > 0:
                switch_nums.append(n)
                measdate.append(df.index[0])
        return measdate, switch_nums

    def execute(self):
        df = self.graph.get_data_from_api(['drive_run'])
        measdate, switch_nums = self.get_fe(df, self.graph.parameter)
        for t, v in zip(measdate, switch_nums):
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': t, 'feid1st': "11107",
                           'value1st': float(v), 'indices2nd': []})
            self.graph.indices.append(index)
