"""
Provides:
液位漏油特征监测
==============
Input Signals(1):
* level: 液位
* 抑制信号 (optional)

Parameter Configs(3)：
* 聚合时长(s)
* 液位下降持续时间(min)
* 液位下降程度 (%)


==============
Outputs:
指标   |  指标id
---------------------
* 液位下降程度 23000

Note:
* (1)满足液位持续下降时间和液位下降标准
* (2)存在抑制信号时,满足抑制条件
Author: wangyong
"""
from graph import Event


class Alg023:
    def __init__(self, graph):
        self.graph = graph

    def get_alarm(self):
        algparas = self.graph.parameter
        df = self.graph.get_data_from_protobuf(['liquid_level'])

        if df.empty:
            return

        resampled_level = df['liquid_level'].resample(f'{algparas[0]}S').mean()  # 原始液位趋势聚合
        max_fall = resampled_level.diff(3).rolling(int(algparas[1]*60/algparas[0])).sum().max()  # 检测窗口内液位下降最大程度
        if max_fall <= -algparas[2]:
            event = Event({'assetid': self.graph.deviceid, 'assetname': self.graph.devicename,
                           'aiid': self.graph.aiid,
                           'meastime': df.index[0], 'level': 3, 'info': '报警：液位下降异常，存在泄露异常特征！！'})
            self.graph.events.append(event)

    def execute(self):
        self.get_alarm()


