"""
Provides:
伺服阀泄漏指标，计算稳态伺服阀开口度（AWC）
==============
Input Signals :
* 上侧伺服阀开口度：sv_out_up
* 上侧实际辊缝值：gap_act_up
* 上侧伺服阀前截止阀: cutoff_valve_up
* 下侧伺服阀开口度：sv_out_down
* 下侧实际辊缝值：gap_act_down
* 下侧伺服阀前截止阀: cutoff_valve_down


Parameter Configs ：
* 稳态持续时间下限(秒)
* 稳态窗口变异系数门限：范围（0-5）
* 伺服阀前截止阀指标（1）


==============
Outputs:
指标   |  指标id
---------------------
* 上侧伺服阀开口度均值：  10400
* 上侧伺服阀开口度标准差：10401
* 上侧伺服阀开口度最大值：10402
* 上侧伺服阀开口度最小值：10403
* 下侧伺服阀开口度均值：  10404
* 下侧伺服阀开口度标准差：10405
* 下侧伺服阀开口度最大值：10406
* 下侧伺服阀开口度最小值：10407
====================
Author: chenqiliang
"""

import numpy as np
from graph import Index
import com_util


class Alg004_S5:
    def __init__(self, graph):
        self.graph = graph

    @staticmethod
    def get_fe(df, algparas):
        avg_sv_out_up = []
        std_sv_out_up = []
        max_sv_out_up = []
        min_sv_out_up = []
        measdate_up = []
        avg_sv_out_down = []
        std_sv_out_down = []
        max_sv_out_down = []
        min_sv_out_down = []
        measdate_down = []
        if not df.empty:
            rolling1 = df['gap_act_up'].rolling(int(algparas[0] * df.num_per_sec), center=True)
            roll_cv1 = np.abs(rolling1.std() / rolling1.mean())   # 计算窗口变异系数
            idx1 = (roll_cv1 < (algparas[1] / 100)) & (df['cutoff_valve_up'] == algparas[2])
            re_iter = com_util.Reg.finditer(idx1, algparas[0] * df.num_per_sec)
            for i in re_iter:
                [stidx, edidx] = i.span()
                n = (edidx - stidx) // 5
                if edidx - stidx > n:
                    measdate_up.append(df.index[stidx + n])
                    avg_sv_out_up.append(np.mean(df.sv_out_up[stidx + n:edidx - n]))
                    std_sv_out_up.append(np.std(df.sv_out_up[stidx + n:edidx - n]))
                    max_sv_out_up.append(np.max(df.sv_out_up[stidx + n:edidx - n]))
                    min_sv_out_up.append(np.min(df.sv_out_up[stidx + n:edidx - n]))

            rolling2 = df['gap_act_down'].rolling(int(algparas[0] * df.num_per_sec), center=True)
            roll_cv2 = np.abs(rolling2.std() / rolling2.mean())   # 计算窗口变异系数
            idx2 = (roll_cv2 < (algparas[1] / 100)) & (df['cutoff_valve_down'] == algparas[2])
            re_iter = com_util.Reg.finditer(idx2, algparas[0] * df.num_per_sec)
            for i in re_iter:
                [stidx, edidx] = i.span()
                n = (edidx - stidx) // 5
                if edidx - stidx > n:
                    measdate_down.append(df.index[stidx + n])
                    avg_sv_out_down.append(np.mean(df.sv_out_down[stidx + n:edidx - n]))
                    std_sv_out_down.append(np.std(df.sv_out_down[stidx + n:edidx - n]))
                    max_sv_out_down.append(np.max(df.sv_out_down[stidx + n:edidx - n]))
                    min_sv_out_down.append(np.min(df.sv_out_down[stidx + n:edidx - n]))
        return measdate_up, avg_sv_out_up, std_sv_out_up, max_sv_out_up, min_sv_out_up, \
               measdate_down, avg_sv_out_down, std_sv_out_down, max_sv_out_down, min_sv_out_down,

    def execute(self):
        df = self.graph.get_data_from_api(['sv_out_up', 'gap_act_up', 'cutoff_valve_up', 'sv_out_down', 'gap_act_down', 'cutoff_valve_down'])
        measdate_up, avg_sv_out_up, std_sv_out_up, max_sv_out_up, min_sv_out_up, \
        measdate_down, avg_sv_out_down, std_sv_out_down, max_sv_out_down, min_sv_out_down, = self.get_fe(df, self.graph.parameter)
        for i, meastime_up in enumerate(measdate_up):
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime_up, 'feid1st': "10400",
                           'value1st': avg_sv_out_up[i], 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime_up, 'feid1st': "10401",
                           'value1st': std_sv_out_up[i], 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime_up, 'feid1st': "10402",
                           'value1st': max_sv_out_up[i], 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime_up, 'feid1st': "10403",
                           'value1st': min_sv_out_up[i], 'indices2nd': []})
            self.graph.indices.append(index)

        for i, meastime_down in enumerate(measdate_down):
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime_down, 'feid1st': "10400",
                           'value1st': avg_sv_out_down[i], 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime_down, 'feid1st': "10401",
                           'value1st': std_sv_out_down[i], 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime_down, 'feid1st': "10402",
                           'value1st': max_sv_out_down[i], 'indices2nd': []})
            self.graph.indices.append(index)
            index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime_down, 'feid1st': "10403",
                           'value1st': min_sv_out_down[i], 'indices2nd': []})
            self.graph.indices.append(index)
        self.graph.set_alarm('伺服阀稳态开口度异常！')