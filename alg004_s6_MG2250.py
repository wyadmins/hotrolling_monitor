"""
Provides:
伺服阀泄漏指标，计算稳态伺服阀开口度（AWC/AGC/支撑辊）
==============
Input Signals (Optional]):
* 伺服阀开口度：sv_out
* 实际辊缝值：gap_act
* 伺服阀前截止阀: cutoff_valve
* 参考咬钢信号：single (optional)

Parameter Configs (Optional)：
* 稳态持续时间下限(秒)
* 稳态窗口变异系数门限：范围（0-5）
* 伺服阀前截止阀指标（1）
* 咬钢信号：[0, 1] (optional)
==============
Outputs:
指标   |  指标id
---------------------
* 伺服阀开口度均值：  13300
====================
Author: chenqiliang
"""

import numpy as np
from graph import Index
import pandas as pd

class Alg004_S6:
    def __init__(self, graph):
        self.graph = graph

    def get_alarm(self):
        signal_num = len(self.graph.channelid)
        if 3 == signal_num:
            df = self.graph.get_data_from_api(['sv_out', 'gap_act', 'cutoff_valve'])
        elif 4 == signal_num:
            df = self.graph.get_data_from_api(['sv_out', 'gap_act', 'cutoff_valve', 'single'])
        else:
            raise Exception("Exception(减压阀漂移策略)：输入点位数量错误!")
        algparas = self.graph.parameter
        if df.empty:
            return
        rolling = df['gap_act'].rolling(int(algparas[0] * df.num_per_sec), center=True)
        roll_cv = np.abs(rolling.std() / rolling.mean())   # 计算窗口变异系数
        idx1 = roll_cv < algparas[1]
        if len(idx1) < 1:
            return

        if 3 == signal_num:
            idx2 = pd.Series(df['cutoff_valve'] == algparas[2]) \
                .rolling(int(algparas[0] * df.num_per_sec), center=True).min()
        elif 4 == signal_num:
            idx2 = pd.Series((df['cutoff_valve'] == algparas[2]) & (df['single'] == algparas[3])) \
                .rolling(int(algparas[0] * df.num_per_sec), center=True).min()

        min_cv = roll_cv[idx1 & idx2].min()

        if np.isnan(min_cv):  # 数据包不包含稳态工况
            return

        stidx = roll_cv[idx1 & idx2].argmin()
        edidx = stidx + int(np.ceil(algparas[0] * df.num_per_sec))

        n = (edidx - stidx) // 5  # 对稳态段切头尾
        avg_pressure = np.mean(df['sv_out'][stidx + n:edidx - n])

        index = Index({'assetid': self.graph.deviceid, 'meastime1st': df.index[0], 'feid1st': "13300",
                       'value1st': avg_pressure, 'indices2nd': []})
        self.graph.indices.append(index)

    def execute(self):
        self.get_alarm()