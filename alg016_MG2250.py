"""
Provides:
伺服阀零偏
==============
Input Signals (2):
* 信号设定：signal_ref
* 信号反馈：signal_act

Parameter Configs (2)：
*  信号聚合时间（s）
*  模拟量偏差门限（%）

==============
Outputs:
指标   |  指标id
---------------------

"""


import numpy as np
from graph import Event


class Alg016:
    def __init__(self, graph):
        self.graph = graph

    def get_alarm(self):
        """
        模拟量信号
        """
        df = self.graph.get_data_from_api(['signal_ref', 'signal_act'])
        algparas = self.graph.parameter
        if not df.empty:
            df = df.resample(f'{algparas[0]}S').mean()
            r = (np.abs(df.sv_act - df.sv_ref) / np.mean(df.sv_act + df.sv_ref)) * 100   # 伺服阀相对偏差（%）
            if np.any(r > algparas[1]):
                event = Event({'assetid': self.graph.deviceid, 'meastime': df.index[0], 'level': 1, 'info': '伺服阀零偏报警'})
                self.graph.events.append(event)

    def execute(self):
        self.get_alarm()


