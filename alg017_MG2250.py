"""
Provides:
减压阀漂移，计算稳态工况减压阀压力均值
==============
Input Signals (Optional):
* 减压阀压力：pressure
* 参考信号位：s1
* 参考信号位：s2
* 参考信号位：s3 (optional)
* 参考信号位：s4 (optional)

Parameter Configs (Optional)：
* 参考信号位s1稳态窗口时长（s）
* 稳态窗口变异系数门限：范围（0-0.5），用于参考信号位s1，大于该值则数据包不包含稳态工况
* 参考信号s2稳态选取标志：[0, 1]
* 参考信号s3稳态选取标志：[0, 1] (optional)
* 参考信号s4稳态选取标志：[0, 1] (optional)


==============
Outputs:
指标   |  指标id
---------------------
减压阀压力均值 17000
"""

import numpy as np
import pandas as pd
from graph import Index


class Alg017:
    def __init__(self, graph):
        self.graph = graph

    def get_alarm(self):
        signal_num = len(self.graph.channelid)
        if 3 == signal_num:
            df = self.graph.get_data_from_protobuf(['pressure', 's1', 's2'])
        elif 4 == signal_num:
            df = self.graph.get_data_from_protobuf(['pressure', 's1', 's2', 's3'])
        elif 5 == signal_num:
            df = self.graph.get_data_from_protobuf(['pressure', 's1', 's2', 's3', 's4'])
        else:
            raise Exception("Exception(减压阀漂移策略)：输入点位数量错误!")

        if df.empty:
            return

        algparas = self.graph.parameter

        rolling = df['s1'].rolling(int(algparas[0] * df.num_per_sec), center=True)
        roll_cv = np.abs(rolling.std() / rolling.mean())   # 计算窗口变异系数
        idx1 = roll_cv < algparas[1]/100

        if len(idx1) < 1:
            return

        if 3 == signal_num:
            idx2 = pd.Series(df['s2'] == algparas[2])\
                .rolling(int(algparas[0] * df.num_per_sec), center=True).min()
        elif 4 == signal_num:
            idx2 = pd.Series((df['s2'] == algparas[2]) & (df['s3'] == algparas[3])) \
                .rolling(int(algparas[0] * df.num_per_sec), center=True).min()
        elif 5 == signal_num:
            idx2 = pd.Series((df['s2'] == algparas[2]) & (df['s3'] == algparas[3]) & (df['s4'] == algparas[4])) \
                .rolling(int(algparas[0] * df.num_per_sec), center=True).min()

        min_cv = roll_cv[idx1 & idx2].min()

        if np.isnan(min_cv):   # 数据包不包含稳态工况
            return
        stidx = np.where(roll_cv.index == roll_cv[idx1 & idx2].argmin(skipna=True))[0][0]
        # stidx = roll_cv[idx1 & idx2].argmin()
        edidx = stidx + int(np.ceil(algparas[0] * df.num_per_sec))

        n = (edidx - stidx) // 5  # 对稳态段切头尾
        avg_pressure = np.mean(df['pressure'][stidx + n:edidx - n])

        index = Index({'assetid': self.graph.deviceid, 'meastime1st': df.index[0], 'feid1st': "17000",
                       'value1st': avg_pressure, 'indices2nd': []})
        self.graph.indices.append(index)

    def execute(self):
        self.get_alarm()


