"""
Provides:
保护流量开关
==============
Input Signals (Optional):
* 开关： on_off
* 流量检测： flow_detection

Parameter Configs (Optional)：
* 异常时长报警门限


==============
Outputs:
指标   |  指标id
---------------------
"""

import numpy as np


class Alg018:
    def __init__(self, graph):
        self.graph = graph

    def get_alarm(self):
        df = self.graph.get_data_from_api(['on_off', 'flow_detection'])

        if df.empty:
            return

        algparas = self.graph.parameter

        diff = np.abs(df['on_off'] - df['flow_detection'])
        if np.sum(diff) * df.dt > algparas[0]:
            self.graph.set_alarm('流量保护开关检测异常！')


    def execute(self):
        self.get_alarm()


