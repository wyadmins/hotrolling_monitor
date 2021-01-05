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

from itertools import groupby
import numpy as np
from graph import Index, Event


class Alg018:
    def __init__(self, graph):
        self.graph = graph

    def get_alarm(self):
        df = self.graph.get_data_from_protobuf(['on_off', 'flow_detection'])

        if df.empty:
            return

        algparas = self.graph.parameter

        d = np.abs(df['on_off'] - df['flow_detection'])
        n_array = [len(list(v)) for k, v in groupby(d) if k == 1]
        t = max(n_array) * df.dt if n_array else 0
        index = Index({'assetid': self.graph.deviceid, 'meastime1st': df.index[0], 'feid1st': "18000",
                       'value1st': t, 'indices2nd': []})
        self.graph.indices.append(index)
        if t > algparas[0]:
            event = Event({'assetid': self.graph.deviceid, 'assetname': self.graph.devicename,
                           'aiid': self.graph.aiid,
                           'meastime': df.index[0], 'level': 1, 'info': '报警：流量保护开关检测异常！！'})
            # event = Event({'assetid': self.graph.deviceid, 'meastime': df.index[0], 'level': 1, 'info': '流量保护开关检测异常！'})
            self.graph.events.append(event)

    def execute(self):
        self.get_alarm()


