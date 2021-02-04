"""
Provides:
马钢双仪表检测
==============
Input Signals (2):
* 仪表1信号：signal1
* 仪表2信号：signal2

Parameter Configs (4)：
*  信号类型：模拟量 -> 1 , 0/1型量 -> 2
*  模拟量偏差计算门限
*  模拟量偏差门限（%）
*  0-1量报警时长要求（s）

==============
Outputs:

指标   |  指标id
---------------------
*  双仪表相对偏差：  15000
*  双仪表绝对偏差：  15001
"""

from itertools import groupby
import numpy as np
import com_util
from graph import Event, Index


class Alg015:
    def __init__(self, graph):
        self.graph = graph

    def get_alarm_analogs(self, p2, p3):
        """
        模拟量信号
        """
        df = self.graph.get_data_from_protobuf(['signal1', 'signal2'])

        if not df.empty:
            idx = df['signal1'] > p2
            re_iter = com_util.Reg.finditer(idx, 2 * df.num_per_sec)
            for i in re_iter:
                [stidx, edidx] = i.span()
                n = (edidx - stidx) // 5  # 切头尾
                bias = np.abs(np.mean(df.signal1[stidx+n:edidx-n]) - np.mean(df.signal2[stidx+n:edidx-n]))
                r = bias / np.mean(df.signal1[stidx+n:edidx-n]) * 100  # 双仪表相对偏差（%）

                index = Index({'assetid': self.graph.deviceid, 'meastime1st': df.index[0], 'feid1st': "15000",
                               'value1st': r, 'indices2nd': []})
                self.graph.indices.append(index)

                index = Index({'assetid': self.graph.deviceid, 'meastime1st': df.index[0], 'feid1st': "15001",
                               'value1st': bias, 'indices2nd': []})
                self.graph.indices.append(index)

                self.graph.set_alarm('双仪表数值不匹配！')

                # if r > p3:
                #     event = Event({'assetid': self.graph.deviceid, 'assetname': self.graph.devicename,
                #                    'aiid': self.graph.aiid,
                #                    'meastime': df.index[0], 'level': 1, 'info': '双仪表数值不匹配！'})
                #     self.graph.events.append(event)

    def get_alarm_logical(self, p4):
        """
        0-1型信号
        """
        df = self.graph.get_data_from_protobuf(['signal1', 'signal2'])
        if not df.empty:
            d = np.abs(df['signal1'] - df['signal2'])
            n_array = [len(list(v)) for k, v in groupby(d) if k == 1]
            t = max(n_array) * df.dt if n_array else 0
            if t > p4:
                event = Event({'assetid': self.graph.deviceid, 'assetname': self.graph.devicename,
                               'aiid': self.graph.aiid,
                               'meastime': df.index[0], 'level': 1, 'info': '双仪表数值不匹配！'})
                self.graph.events.append(event)

    def execute(self):
        [p1, p2, p3, p4] = self.graph.parameter
        if 1 == p1:
            self.get_alarm_analogs(p2, p3)   # 模拟量信号双仪表检测
        elif 2 == p1:
            self.get_alarm_logical(p4)   # 0/1类型信号双仪表检测


