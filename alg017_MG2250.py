"""
Provides:
减压阀漂移，计算稳态工况减压阀压力均值
==============
Input Signals (4):
* 减压阀压力：pressure
* 参考信号位：s1
* 参考信号位：s2
* 参考信号位：s3

Parameter Configs (4)：
* 参考信号位s1稳态窗口时长（s）
* 参考信号s2稳态选取标志：[0, 1]
* 参考信号s3稳态选取标志：[0, 1]
* 稳态窗口变异系数门限：范围（0-0.5），用于参考信号位s1，大于该值则数据包不包含稳态工况

==============
Outputs:
指标   |  指标id
---------------------
减压阀压力均值 17000
"""


import numpy as np
import pandas as pd
from graph import Index


class Alg016:
    def __init__(self, graph):
        self.graph = graph

    def get_alarm(self):
        df = self.graph.get_data_from_api(['pressure', 's1', 's2', 's3'])
        if df.empty:
            return

        algparas = self.graph.parameter

        rolling = df['s1'].rolling(algparas[0] * df.dt)
        roll_cv = np.abs(rolling.std() / rolling.mean())   # 计算窗口变异系数
        idx1 = roll_cv < algparas[1]
        if not idx1:
            return

        idx2 = pd.Series((df['s2'] == algparas[2]) & (df['s3'] == algparas[3]))\
            .rolling(algparas[0] * df.dt, center=True).min()   # 满足

        min_cv = roll_cv[idx1 & idx2].min()

        if np.isnan(min_cv):   # 数据包不包含稳态工况
            return

        stidx = roll_cv[idx1 & idx2].argmin() - int(np.floor(algparas[0] * df.dt / 2))
        edidx = roll_cv[idx1 & idx2].argmin() + int(np.ceil(algparas[0] * df.dt / 2))

        n = (edidx - stidx) // 5  # 对稳态段切头切尾
        avg_pressure = np.mean(df['pressure'][stidx + n:edidx - n])

        index = Index({'assetid': self.graph.deviceid, 'meastime1st': df.index[0], 'feid1st': "17000",
                       'value1st': avg_pressure, 'indices2nd': []})
        self.graph.indices.append(index)

    def execute(self):
        self.get_alarm()


