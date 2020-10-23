import requests
import json
import pandas as pd
import numpy as np
import re


def get_data_from_api(guid, st, ed):
    if isinstance(guid, str):
        url = f'http://192.168.1.15:8131/api/Values?tagid={guid}&Start={st}&End={ed}'
    elif isinstance(guid, list) and 1 == len(guid):
        url = f'http://192.168.1.15:8131/api/Values?tagid={guid[0]}&Start={st}&End={ed}'
    else:
        raise Exception("guid numbers > 1 !")
    # url = f'http://127.0.0.1:8130/api/Values?tagid={guid}&Start={st}&End={ed}'
    r = requests.get(url)
    data = pd.Series(json.loads(r.json()))
    return data


def get_data_from_api_v2(assetid, aiid, st, ed, tags):
    url = f'http://192.168.1.87:8132/api/Values/GetTagDataGet?AssetId={assetid}&AiId={aiid}&Start={st}&End={ed}'
    r = requests.get(url)
    data = pd.Series(json.loads(r.json()))
    df = pd.DataFrame(data['Result']['Detail']).T
    df.columns = tags
    return df


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