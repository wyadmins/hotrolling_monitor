import json
import requests
import pandas as pd
import com_util


class Graph:
    def __init__(self, nodes, algcode, datasource, indices, events, datasourcetimes, exceptions,
                 starttime, endtime, channelid, deviceid, devicename, aiid):
        self.nodes = nodes
        self.algcode = algcode
        self.datasource = datasource
        self.indices = indices
        self.events = events
        self.datasourcetimes = datasourcetimes
        self.exceptions = exceptions
        self.starttime = starttime
        self.endtime = endtime
        self.channelid = channelid
        self.deviceid = deviceid
        self.devicename = devicename
        self.aiid = aiid

    @staticmethod
    def graph_from_json(data):
        line = json.loads(data)
        nodes = line.get('nodes')
        events = line.get('events', [])
        indices = line.get('indices', [])
        if line.get('inputstr'):
            datasource = eval(line.get('inputstr')[0])['datasource'][0]
        else:
            datasource = line.get('datasource')[0]
        exceptions = line.get('exceptions', [])
        channelid = datasource.get('channelid')
        algcode = datasource.get('algcode')
        deviceid = datasource.get('deviceid')
        devicename = datasource.get('devicename')
        starttime = datasource.get('starttime')
        endtime = datasource.get('endtime')
        datasourcetimes = datasource.get('datasourcetimes')
        aiid = datasource.get('aiid')
        return Graph(nodes, algcode, datasource, indices, events, datasourcetimes, exceptions,
              starttime, endtime, channelid, deviceid, devicename, aiid)

    def to_json(self):
        def to_dict(value):
            return {k: v for k, v in value.__dict__.items() if
                    not str(k).startswith('_')}  # if inspect.isclass(value) else value

        return json.dumps(self, default=to_dict, ensure_ascii=False)

    def get_data_from_api(self, tags):
        url = f'http://192.168.1.15:8132/api/Values/GetTagDataGet?AssetId={self.deviceid}&AiId={self.aiid}&Start={self.starttime}&End={self.endtime}'
        r = requests.get(url)
        data = json.loads(r.json())
        df = pd.DataFrame(data['Detail']).T
        df.columns = tags
        df.set_index(pd.to_datetime(df.index), inplace=True)
        df.dt, df.num_per_sec = com_util.get_dt(df.index)
        return df

    def read_cache(self):
        url = f"http://192.168.1.15:8130/api/services/app/V1_Ai/GetAiCache?DeviceId={self.deviceid}&AlgCode={self.algcode}"
        data = requests.get(url).json()
        cache = data['data']['cache']
        return cache

    def set_cache(self, cache):
        url = 'http://192.168.1.15:8130/api/services/app/V1_Ai/CreateOrEditAiCache'
        data = '{"deviceId": "%s","algCode": "%s","cache": "%s"}' % (self.deviceid, self.algcode, cache)
        rep = requests.post(url=url, data=data, headers={'Content-Type': 'application/json'})
        return rep.ok


class Index:
    """
    指标
    """
    def __init__(self, value):
        self.assetid = value['assetid']
        self.meastime1st = value['meastime1st']
        self.feid1st = value['feid1st']
        self.value1st = value['value1st']
        self.indices2nd = value.get('indices2nd', [])


class Event:
    """
    报警事件
    """
    def __init__(self, value):
        self.assetid = value['assetid']
        self.alarm_time = value['meastime']
        self.alarm_level = value['level']
        self.alarm_info = value['info']