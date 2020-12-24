"""
Provides:
卷曲卷筒冲顶报警和统计，高温卷统计
==============
Input Signals(4):
* 入卷温度:     in_coil_temp
* 满涨标志位:   full_inflation
* 咬钢信号:     bite_steel
* 卷径实际值:   coil_diameter

Parameter Configs (1)：
* 满涨卷径统计切头时长(秒)
==============
Outputs(4):
指标   |  指标id
---------------------
* 满涨卷径最大值：21000
* 满涨卷径平均值：21001
* 高温卷次数：    21002
* 高温卷时长：    21003
"""

import numpy as np
from graph import Index


class Alg021:
    def __init__(self, graph):
        self.graph = graph

    def get_alarm(self):
        df = self.graph.get_data_from_protobuf(['in_coil_temp', 'full_inflation', 'bite_steel', 'coil_diameter'])

        if df.empty:
            return

        # 满涨卷径统计
        n = self.graph.parameter[0]
        full_inflation = df.coil_diameter[1 == df.full_inflation]
        if full_inflation.empty:
            max_coil_diameter = np.nan
            avg_coil_diameter = np.nan
        else:
            max_coil_diameter = full_inflation[: n * df.num_per_sec].max()
            avg_coil_diameter = full_inflation[: n * df.num_per_sec].mean()

        # 高温卷统计
        avg_temp = np.mean(df['in_coil_temp'][1 == df['bite_steel']])   # 温度均值
        if avg_temp > 600:
            high_temp_coil_count = 1
            high_temp_coil_duration = df.dt * sum(1 == df['bite_steel'])
        else:
            high_temp_coil_count = 0
            high_temp_coil_duration = 0

        return df.index[0], max_coil_diameter, avg_coil_diameter, high_temp_coil_count, high_temp_coil_duration

    def execute(self):
        meastime, max_coil_diameter, avg_coil_diameter, high_temp_coil_count, high_temp_coil_duration = self.get_alarm()

        if not np.isnan(max_coil_diameter) and not np.isnan(max_coil_diameter):
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "21000",
                           'value1st': max_coil_diameter, 'indices2nd': []})
            self.graph.indices.append(index)

            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "21001",
                           'value1st': avg_coil_diameter, 'indices2nd': []})
            self.graph.indices.append(index)

        if high_temp_coil_count > 0:
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "21002",
                           'value1st': high_temp_coil_count, 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "21003",
                           'value1st': high_temp_coil_duration, 'indices2nd': []})
            self.graph.indices.append(index)

