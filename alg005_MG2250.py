"""
Provides:
精轧机零调刚度计算
==============
Input Signals (3):
* hgc_force: 压力
* hgc_pos:   操作侧位置
* zero_run:  零调标志位

Parameter Configs (3)：
* 刚度计算压力区间最小值
* 刚度计算压力区间最大值
* 刚度计算持续时长

==============
Outputs:
指标   |  指标id
---------------------
* 空载电流均值：  10100
* 空载电流标准差：10101
* 空载电流最大值：10102
* 空载电流最小值：10103
* 空载转矩均值：  10104
* 空载转矩标准差：10105
* 空载转矩最大值：10106
* 空载转矩最小值：10107
"""

import sys
import traceback
import numpy as np
import com_util
from graph import Index


class Alg001:
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
            df = self.graph.get_data_from_api(['hgc_force', 'hgc_pos', 'zero_run'])
            df = df[1 == df['zeroing_run']]
            if df.empty:
                return
            [stidxs, edidxs] = self.regexp_monotrend(df['hgc_force'], algparas[0], algparas[1], algparas[2]*df.num_per_sec, '+')
            [meadate, stiffness, avg_stiffness] = self.get_stiffness(stidxs, edidxs, df)
            for i, meastime in enumerate(meadate):
                index = Index({'assetid': self.graph.deviceid, 'meastime1st': meastime, 'feid1st': "50000",
                               'value1st': avg_stiffness[i], 'indices2nd': stiffness})
                self.graph.indices.append(index)
        except Exception as _:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            errorinfo = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
            self.graph.exceptions.append(errorinfo)


