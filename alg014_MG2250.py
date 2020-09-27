"""
Provides:
F1-F7精轧机黏铁检测
==============
Input Signals (5):
* os_lc
* os_pt
* ds_lc
* ds_pt
* agc_active

Parameter Configs (1)：
* 抛钢后持续时长（秒）

==============
Outputs:
指标   |  指标id
---------------------
* 抛钢后OS_LC压力均值：  14000
* 抛钢后OS_LC压力标准差：14001
* 抛钢后OS_LC压力最大值：14002
* 抛钢后OS_LC压力最小值：14003

* 抛钢后OS_PT压力均值：  14004
* 抛钢后OS_PT压力标准差：14005
* 抛钢后OS_PT压力最大值：14006
* 抛钢后OS_PT压力最小值：14007

* 抛钢后DS_LC压力均值：  14008
* 抛钢后DS_LC压力标准差：14009
* 抛钢后DS_LC压力最大值：14010
* 抛钢后DS_LC压力最小值：14011

* 抛钢后DS_PT压力均值：  14012
* 抛钢后DS_PT压力标准差：14013
* 抛钢后DS_PT压力最大值：14014
* 抛钢后DS_PT压力最小值：14015
"""


import numpy as np
from graph import Index
from com_util import find_1_to_0


class Alg014:
    def __init__(self, graph):
        self.graph = graph

    def get_fe(self, df):
        duration = self.graph.parameter[0]
        std_force = []
        avg_force = []
        max_force = []
        min_force = []
        measdate = []
        if not df.empty:
            indexs = find_1_to_0(df['agc_active'])
            for i in indexs:
                std_force = np.std(df['force'][i: i+duration*df.num_per_sec])
                avg_force = np.mean(df['force'][i:i+duration*df.num_per_sec])
                max_force = np.max(df['force'][i: i+duration*df.num_per_sec])
                min_force = np.min(df['force'][i: i+duration*df.num_per_sec])
                measdate.append(df.index[i])
        return measdate, std_force, avg_force, max_force, min_force

    def execute(self):
        df = self.graph.get_data_from_api(['os_lc', 'os_pt', 'ds_lc', 'ds_pt', 'agc_active'])

        df['force'] = df['os_lc']
        measdate, std_force, avg_force, max_force, min_force = self.get_fe(df)
        if measdate:
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': measdate, 'feid1st': str(14000),
                           'value1st':  std_force, 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': measdate, 'feid1st': str(14001),
                           'value1st':  avg_force, 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': measdate, 'feid1st': str(14002),
                           'value1st':  max_force, 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': measdate, 'feid1st': str(14003),
                           'value1st':  min_force, 'indices2nd': []})
            self.graph.indices.append(index)

        df['force'] = df['os_pt']
        measdate, std_force, avg_force, max_force, min_force = self.get_fe(df)
        if measdate:
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': measdate, 'feid1st': str(14004),
                           'value1st':  std_force, 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': measdate, 'feid1st': str(14005),
                           'value1st':  avg_force, 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': measdate, 'feid1st': str(14006),
                           'value1st':  max_force, 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': measdate, 'feid1st': str(14007),
                           'value1st':  min_force, 'indices2nd': []})
            self.graph.indices.append(index)

        df['force'] = df['ds_lc']
        if measdate:
            measdate, std_force, avg_force, max_force, min_force = self.get_fe(df)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': measdate, 'feid1st': str(14008),
                           'value1st':  std_force, 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': measdate, 'feid1st': str(14009),
                           'value1st':  avg_force, 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': measdate, 'feid1st': str(14010),
                           'value1st':  max_force, 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': measdate, 'feid1st': str(14011),
                           'value1st':  min_force, 'indices2nd': []})
            self.graph.indices.append(index)

        df['force'] = df['ds_pt']
        if measdate:
            measdate, std_force, avg_force, max_force, min_force = self.get_fe(df)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': measdate, 'feid1st': str(14012),
                           'value1st':  std_force, 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': measdate, 'feid1st': str(14013),
                           'value1st':  avg_force, 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': measdate, 'feid1st': str(14014),
                           'value1st':  max_force, 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': measdate, 'feid1st': str(14015),
                           'value1st':  min_force, 'indices2nd': []})
            self.graph.indices.append(index)
