"""
Provides:
通用传感器误信号检测
==============
Input Signals(1):
* t5

Parameter Configs(5)：
* 绝对门限上限
* 绝对门限下限
* 聚合时长
* 峰峰值报警门限
* 变换率报警门限

==============
Outputs:
指标   |  指标id
---------------------
Author: chengqiliang
"""
import pandas as pd
import numpy as np
from graph import Event


class Alg022:
    def __init__(self, graph):
        self.graph = graph

    def get_alarm(self):

        df = self.graph.get_data_from_protobuf(['d'])
        algparas = self.graph.parameter

        if df.empty:
            return
        if -1 == algparas[0] or -1 == algparas[1]:
            return

        if df['d'].max() > algparas[0] or df['d'].min() < algparas[1]:
            event = Event({'assetid': self.graph.deviceid, 'meastime': df.index[0], 'level': 1, 'info': '传感器异常！'})
            self.graph.events.append(event)

        df_rsp = df['d'].resample(f'{algparas[2]}S')
        df_p2p = (df_rsp.max() - df_rsp.min()).max()
        diff_rsp = (pd.Series(np.abs(np.diff(df['d'])), index=df.index[0:df.shape[0]-1])).resample(f'{algparas[2]}S')
        diff_max = (diff_rsp.mean()).max()

        if df_p2p > algparas[3] or diff_max > algparas[4]:
            event = Event({'assetid': self.graph.deviceid, 'meastime': df.index[0], 'level': 1, 'info': '传感器异常！'})
            self.graph.events.append(event)

    def execute(self):
        self.get_alarm()


