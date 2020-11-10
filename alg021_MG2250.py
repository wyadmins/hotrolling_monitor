"""
Provides:
卷曲卷筒冲顶报警和统计，高温卷统计
==============
Input Signals (8):
* 入卷温度1: in_coil_temp1
* 入卷温度标志: in_coil_temp_flag
* 入卷温度2: in_coil_temp2
* 预涨标志位: pre_inflation
* 满涨标志位: full_inflation
* 卸卷标志位: coil_stripping
* 咬钢信号: bite_steel
* 卷径实际值（计算）: coil diameter

Parameter Configs (None)：
*
==============
Outputs:
指标   |  指标id
---------------------
* 满涨冲顶报警凑数： 21000
* 高温卷统计次数：   21001
* 高温卷时长：       21002
"""

import numpy as np
from graph import Index


class Alg021:
    def __init__(self, graph):
        self.graph = graph

    def get_alarm(self):
        df = self.graph.get_data_from_api(['in_coil_temp1', 'temp_flag', 'in_coil_temp2',
                                           'pre_inflation', 'full_inflation', 'coil_stripping',
                                           'bite_steel', 'coil diameter'])
        if df.empty:
            return

        # 卷筒冲顶报警和次数统计
        if 1 == df['pre_inflation'] and (df['coil diameter'] > 746 or df['coil diameter'] < 744):
            self.graph.set_alarm('卷筒冲顶！')

        alarm_count = 0
        if 1 == df['full_inflation'] and df['coil diameter'] > 762:
            alarm_count += 1  # 满涨报警次数统计
            self.graph.set_alarm('卷筒冲顶！')

        if 1 == df['coil_stripping'] and (df['coil diameter'] > 728 or df['coil diameter'] < 726):
            self.graph.set_alarm('卷筒冲顶！')

        # 高温卷统计
        high_temp_coil_count = 0
        high_temp_coil_duration = 0
        if 1 == df['in_coil_temp_flag']:
            avg_temp = np.mean(df['in_coil_temp1'])
            if avg_temp > 600 and 1 == df['bite_steel']:
                high_temp_coil_count = 1
                high_temp_coil_duration = df.dt * df.df.num_per_sec

        return df.index[0], alarm_count, high_temp_coil_count, high_temp_coil_duration

    def execute(self):
        meastime, alarm_count, high_temp_coil_count, high_temp_coil_duration = self.get_alarm()
        if alarm_count > 0:
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "21000",
                           'value1st': alarm_count, 'indices2nd': []})
            self.graph.indices.append(index)

        if high_temp_coil_count > 0:
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "21001",
                           'value1st': high_temp_coil_count, 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "21002",
                           'value1st': high_temp_coil_duration, 'indices2nd': []})
            self.graph.indices.append(index)

