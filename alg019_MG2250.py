"""
Provides:
保护压力开关1对多
==============
Input Signals (Optional):
* 供油压力： pressure
* 参考压力开关：s1
* 参考压力开关：s2(optional)
* 参考压力开关：s3(optional)
* 参考压力开关：s4(optional)
* 参考压力开关：s5(optional)
* 参考压力开关：s6(optional)
* 参考压力开关：s7(optional)
* 参考压力开关：s8(optional)
* 参考压力开关：s9(optional)
* 参考压力开关：s10(optional)
* 参考压力开关：s11(optional)
* 参考压力开关：s12(optional)
* 参考压力开关：s13(optional)
* 参考压力开关：s14(optional)
* 参考压力开关：s15(optional)
* 参考压力开关：s16(optional)
* 参考压力开关：s17(optional)
* 参考压力开关：s18(optional)
* 参考压力开关：s19(optional)
* 参考压力开关：s20(optional)


Parameter Configs (1)：
* 供油压力默认门限
==============
Outputs:
指标   |  指标id
---------------------

==============
Author: chengqiliang
"""


class Alg019:
    def __init__(self, graph):
        self.graph = graph

    def get_alarm(self):
        signal_num = len(self.graph.channelid)
        if 2 == signal_num:
            df = self.graph.get_data_from_api(['pressure', 's1'])
        elif 5 == signal_num:
            df = self.graph.get_data_from_api(['pressure', 's1', 's2', 's3', 's4'])
        elif 8 == signal_num:
            df = self.graph.get_data_from_api(['pressure', 's1', 's2', 's3', 's4', 's5', 's6', 's7'])
        elif 10 == signal_num:
            df = self.graph.get_data_from_api(['pressure', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9'])
        elif 11 == signal_num:
            df = self.graph.get_data_from_api(['pressure', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10'])
        elif 21 == signal_num:
            df = self.graph.get_data_from_api(['pressure', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 's10', 's11', 's12', 's13', 's14', 's15', 's16', 's17', 's18', 's19', 's20'])
        else:
            raise Exception("Exception(保护开关一对多)：输入点位数量错误!")

        if df.empty:
            return

        algparas = self.graph.parameter

        df_hp = df[df.pressure >= algparas[0]]
        df_lp = df[df.pressure < algparas[0]]

        if 2 == signal_num:
            if not ((all(df_hp.s1 == 1)) | (all(df_lp.s1 == 0))):
                self.graph.set_alarm('供油压力开关检测异常！')
        elif 5 == signal_num:
            if not ((all(df_hp.s1 == 1) & all(df_hp.s2 == 1) & all(df_hp.s3 == 1) & all(df_hp.s4 == 1)) \
                    | (all(df_lp.s1 == 0) & all(df_lp.s2 == 0) & all(df_lp.s3 == 0) & all(df_lp.s4 == 0))):
                self.graph.set_alarm('供油压力开关检测异常！')
        elif 8 == signal_num:
            if not ((all(df_hp.s1 == 1) & all(df_hp.s2 == 1) & all(df_hp.s3 == 1) & all(df_hp.s4 == 1)
                     & all(df_hp.s5 == 1) & all(df_hp.s6 == 1) & all(df_hp.s7 == 1)) \
                    | (all(df_lp.s1 == 0) & all(df_lp.s2 == 0) & all(df_lp.s3 == 0) & all(df_lp.s4 == 0)
                       & all(df_lp.s5 == 0) & all(df_lp.s6 == 0) & all(df_lp.s7 == 0))):
                self.graph.set_alarm('供油压力开关检测异常！')
        elif 10 == signal_num:
            if not ((all(df_hp.s1 == 1) & all(df_hp.s2 == 1) & all(df_hp.s3 == 1) & all(df_hp.s4 == 1) & all(df_hp.s5 == 1)
                & all(df_hp.s6 == 1) & all(df_hp.s7 == 1) & all(df_hp.s8 == 1) & all(df_hp.s9 == 1)) \
                    | (all(df_lp.s1 == 0) & all(df_lp.s2 == 0) & all(df_lp.s3 == 0) & all(df_lp.s4 == 0) & all(df_lp.s5 == 0)
                       & all(df_lp.s6 == 0) & all(df_lp.s7 == 0) & all(df_lp.s8 == 0) & all(df_lp.s9 == 0))):
                self.graph.set_alarm('供油压力开关检测异常！')
        elif 11 == signal_num:
            if not ((all(df_hp.s1 == 1) & all(df_hp.s2 == 1) & all(df_hp.s3 == 1) & all(df_hp.s4 == 1) & all(df_hp.s5 == 1)
                & all(df_hp.s6 == 1) & all(df_hp.s7 == 1) & all(df_hp.s8 == 1) & all(df_hp.s9 == 1) & all(df_hp.s10 == 1))\
                    | (all(df_lp.s1 == 0) & all(df_lp.s2 == 0) & all(df_lp.s3 == 0) & all(df_lp.s4 == 0) & all(df_lp.s5 == 0)
                       & all(df_lp.s6 == 0) & all(df_lp.s7 == 0) & all(df_lp.s8 == 0) & all(df_lp.s9 == 0) & all(df_lp.s10 == 0))):
                self.graph.set_alarm('供油压力开关检测异常！')
        elif 21 == signal_num:
            if not((all(df_hp.s1 == 1) & all(df_hp.s2 == 1) & all(df_hp.s3 == 1) & all(df_hp.s4 == 1) & all(df_hp.s5 == 1) & all(df_hp.s6 == 1) & all(df_hp.s7 == 1)
                & all(df_hp.s8 == 1) & all(df_hp.s9 == 1) & all(df_hp.s10 == 1) & all(df_hp.s11 == 1) & all(df_hp.s12 == 1) & all(df_hp.s13 == 1)
                & all(df_hp.s14 == 1) & all(df_hp.s15 == 1) & all(df_hp.s16 == 1) & all(df_hp.s17 == 1) & all(df_hp.s18 == 1) & all(df_hp.s19 == 1)
                & all(df_hp.s20 == 1)) | (all(df_lp.s1 == 0) & all(df_lp.s2 == 0) & all(df_lp.s3 == 0) & all(df_lp.s4 == 0) & all(df_lp.s5 == 0)
                                        & all(df_lp.s6 == 0) & all(df_lp.s7 == 0) & all(df_lp.s8 == 0) & all(df_lp.s9 == 0) & all(df_lp.s10 == 0)
                                        & all(df_lp.s11 == 0) & all(df_lp.s12 == 0) & all(df_lp.s13 == 0) & all(df_lp.s14 == 0) & all(df_lp.s15 == 0)
                                        & all(df_lp.s16 == 0) & all(df_lp.s17 == 0) & all(df_lp.s18 == 0) & all(df_lp.s19 == 0) & all(df_lp.s20 == 0))):
                self.graph.set_alarm('供油压力开关检测异常！')

    def execute(self):
        self.get_alarm()
