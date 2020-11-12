import pandas as pd
import numpy as np
import re
import gzip
import timeseries_pb2
import base64
from graph import Graph


def get_dt(index):
    dt = (pd.to_datetime(index[1]) - pd.to_datetime(index[0])).total_seconds()
    sec = int(np.floor(1 / dt))
    return dt, sec


def find_0_to_1(d):
    indexs = np.where(1 == np.diff(d))
    return indexs


def find_1_to_0(d):
    indexs = np.where(-1 == np.diff(d))[0]
    return indexs


def down_sample(df):
    df = df.resample('T').mean()
    return df


class Reg:
    @staticmethod
    def finditer(idx, n, flag=1):
        s = idx.astype(int)
        str1 = ''.join(str(i) for i in s)
        re_iter = re.finditer(f'{flag}{int(n),}'.replace('(', '{').replace(')', '}'), str1)
        return re_iter

    @staticmethod
    def search(idx, n, sec):
        s = idx.astype(int)
        str1 = ''.join(str(i) for i in s)
        r2 = re.search(f'1{sec,}'.replace('(', '{').replace(')', '}'), str1)
        return r2


def generate_graph(x):
    c = timeseries_pb2.KafkaAiDataDto()
    content = gzip.decompress(base64.b64decode(x))
    c.ParseFromString(content)
    graph = Graph.graph_from_protobuf(c)
    graph.data = c.Data
    return graph