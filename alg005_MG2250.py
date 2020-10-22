"""
Provides:
精轧机零调刚度计算
==============
Input Signals (5):
* zeroing_run:  零调标志位
* hgc_force_os: 操作侧轧制力
* hgc_pos_os:   操作侧HGC位置
* hgc_force_ds: 驱动侧轧制力
* hgc_pos_ds:   驱动侧HGC位置


Parameter Configs (3)：
* 刚度计算压力区间最小值
* 刚度计算压力区间最大值
* 刚度计算持续时长

==============
Outputs:
指标   |  指标id
---------------------
* 操作侧刚度 50000
** 操作侧分段刚度 （二次指标）
* 驱动侧刚度 50001
** 驱动侧分段刚度 （二次指标）
"""

import sys
import traceback
import numpy as np
import com_util
from graph import Index


class Alg005:
    def __init__(self, graph):
        self.graph = graph

    def regexp_monotrend(self, trend, lower_limit, upper_limit, duration, sign1):
        if sign1 == '+':
            sign1 = 1
        else:
            sign1 = -1
        idx = (trend < upper_limit) & (trend > lower_limit)
        re_iter = com_util.Reg.finditer(idx, duration)
        st = []
        ed = []
        for i in re_iter:
            [stidx, edidx] = i.span()
            if edidx - stidx < 10:
                continue
            d = trend[stidx:edidx]
            s = (np.mean(d[-5:]) - np.mean(d[:5])) / np.mean(d) > 0.1
            if sign1 == s:
                st.append(stidx)
                ed.append(edidx)
        return st, ed


    def get_stiffness(self, stidx, edidx, df):
        measdate = []
        stiffness = []
        avg_stiffness = []
        TREND_NUM = 5
        for st, ed in zip(stidx, edidx):
            force = df.hgc_force[st:ed]
            cutn = len(force) % TREND_NUM
            force = force[:len(force) - cutn]
            f = force.values.reshape((-1, TREND_NUM), order='F')
            pos = df.hgc_position[st:ed]
            pos = pos[:len(pos) - cutn]
            p = pos.values.reshape((-1, TREND_NUM), order='F')
            trend = np.abs((f[-1, :] - f[0, :]) / (p[-1, :] - p[0, :]))
            measdate.append(df.index[st])
            stiffness.append(trend.tolist())
            avg_stiffness.append(abs(force.values[-1] - force.values[0]) / abs(pos.values[-1] - pos.values[0]))
        return measdate, stiffness, avg_stiffness

    def execute(self):
        try:
            algparas = self.graph.parameter
            df = self.graph.get_data_from_api(['zeroing_run', 'hgc_force_os', 'hgc_pos_os', 'hgc_force_ds', 'hgc_pos_ds'])
            df = df[1 == df['zeroing_run']]
            if df.empty:
                return

            df2 = df[['hgc_force_os', 'hgc_pos_os']].rename(columns={'hgc_force_os': 'hgc_force', 'hgc_pos_os': 'hgc_position'})
            [stidxs, edidxs] = self.regexp_monotrend(df2['hgc_force'], algparas[0], algparas[1], algparas[2]*df.num_per_sec, '+')
            [meadate, stiffness, avg_stiffness] = self.get_stiffness(stidxs, edidxs, df2)
            for i, meastime in enumerate(meadate):
                index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "50000",
                               'value1st': avg_stiffness[i], 'indices2nd': stiffness})
                self.graph.indices.append(index)

            df3 = df[['hgc_force_ds', 'hgc_pos_ds']].rename(columns={'hgc_force_ds': 'hgc_force', 'hgc_pos_ds': 'hgc_position'})
            [stidxs, edidxs] = self.regexp_monotrend(df3['hgc_force'], algparas[0], algparas[1], algparas[2]*df.num_per_sec, '+')
            [meadate, stiffness, avg_stiffness] = self.get_stiffness(stidxs, edidxs, df3)
            for i, meastime in enumerate(meadate):
                index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "50001",
                               'value1st': avg_stiffness[i], 'indices2nd': stiffness})
                self.graph.indices.append(index)

        except Exception as _:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            errorinfo = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
            self.graph.exceptions.append(errorinfo)


