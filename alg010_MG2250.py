"""
Provides:
电机里程统计
==============
Input Signals (2):
* 实际转速：speed
* 压力控制模式：in_force_control

Parameter Configs (0)：
==============
Outputs:
指标   |  指标id
---------------------
* 电机运行总里程：11000
* 电机负载总里程：10001
* 电机空载总里程：10002
"""

import numpy as np
import scipy
from graph import Index
import com_util


class Alg010:
    def __init__(self, graph):
        self.graph = graph

    @staticmethod
    def get_fe(df):
        measdate = []
        s_total = 0
        s_in_operation = 0
        if not df.empty:
            measdate = df.index[0]   # 时间
            idx = (df.in_force_control == 1)
            re_iter = com_util.Reg.finditer(idx, 0.5*df.num_per_sec)
            s_total = scipy.trapz(np.abs(df.speed)) * df.dt  # 总里程
            for i in re_iter:
                [stidx, edidx] = i.span()
                s_in_operation += scipy.trapz(np.abs(df.speed[stidx:edidx])) * df.dt  # 负载里程

        return measdate, s_total, s_in_operation, max(0, s_total-s_in_operation)

    def execute(self):
        df = self.graph.get_data_from_api(['speed', 'in_force_control'])
        measdate, s_total, s_in_operation, s_idler = self.get_fe(df)
        if measdate:
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': measdate, 'feid1st': "11000",
                           'value1st': s_total, 'indices2nd': []})
            self.graph.indices.append(index)

            index = Index({'assetid': self.graph.deviceid, 'meastime1st': measdate, 'feid1st': "11001",
                           'value1st': s_in_operation, 'indices2nd': []})
            self.graph.indices.append(index)

            index = Index({'assetid': self.graph.deviceid, 'meastime1st': measdate, 'feid1st': "11002",
                           'value1st': s_idler, 'indices2nd': []})
            self.graph.indices.append(index)
