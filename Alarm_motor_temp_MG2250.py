"""
Provides:
主电机温度报警
==============
Input Signals (7):
* 冷却系统进口温度：temp_in
* 冷却系统出口温度：temp_out
* 定子A项温度：A
* 定子B项温度：B
* 定子C项温度：C
* 前轴承温度：temp_bearing_front
* 后轴承温度：temp_bearing_rear

Parameter Configs (7)：
# 冷却系统报警参数
    * 进出口温升报警门限（低于该门限报警）
    * 三相温度触发进出口温升报警门限
# 定子温度报警
    * AB定子温差报警门限
    * AC定子温差报警门限
    * BC定子温差报警门限
    * 定子绝对温度报警门限
# 轴承温度报警门限
    * 轴承绝对温度报警门限

==============
Outputs:
指标   |  指标id
---------------------

"""

import numpy as np
from graph import Event


class Alarm_temp_predict:

    def __init__(self, graph):
        self.graph = graph

    def main_motor_temperature_detect(self, df, para):
        """
        主电机系统温度异常判断规则
        """
        if not df.empty:
            df = df.resample('T').mean()
            dT = df['temp_out'] - df['temp_in']

            # 进出口温升小于*，同时三项温度大于* => 冷却系统效果不好
            if np.any((dT < para[0]) & ((df['A'] > para[1]) | (df['B'] > para[1]) | (df['C'] > para[1]))):
                event = Event({'assetid': self.graph.deviceid, 'meastime': df.index[0], 'level': 1, 'info': '冷却系统进出口温度异常！'})
                self.graph.events.append(event)

            # 三项温度温差大于*，且绝对温度大于* => 定子温度异常
            if np.any((((df['A'] - df['B']) > para[2]) & ((df['A'] > para[1]) & (df['B'] > para[1]))) |
                      (((df['A'] - df['C']) > para[3]) & ((df['A'] > para[1]) & (df['C'] > para[1]))) |
                      (((df['B'] - df['C']) > para[4]) & ((df['B'] > para[1]) & (df['C'] > para[1])))
                      ):
                event = Event({'assetid': self.graph.deviceid, 'meastime': df.index[0], 'level': 1, 'info': '电子定子温度异常！'})
                self.graph.events.append(event)

            # 三相温度大于* => 定子温度异常
            if np.any((df['A'] > para[5]) | (df['B'] > para[5]) | (df['C'] > para[5])):
                event = Event({'assetid': self.graph.deviceid, 'meastime': df.index[0], 'level': 1, 'info': '电机定子温度异常！'})
                self.graph.events.append(event)

            # 轴承绝对温度大于* => 轴承温度异常
            if np.any((df['temp_bearing_front'] > para[6]) | (df['temp_bearing_rear'] > para[6])):
                event = Event({'assetid': self.graph.deviceid, 'meastime': df.index[0], 'level': 1, 'info': '电机轴承温度异常！'})
                self.graph.events.append(event)

    def execute(self):
        df = self.graph.get_data_from_protobuf(['temp_in', 'temp_out', 'A', 'B', 'C',
                                           'temp_bearing_front', 'temp_bearing_rear'])
        paras = self.graph.parameter

        self.main_motor_temperature_detect(df, paras)
