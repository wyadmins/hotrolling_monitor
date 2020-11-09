import sys
import traceback
import time
from datetime import datetime
from graph import Graph
from graph import Graph_test
from alg001_MG2250 import Alg001
from alg003_MG2250 import Alg003
from alg004_MG2250 import Alg004
from alg016_MG2250 import Alg016
from alg015_MG2250 import Alg015


def main():
    t1 = time.time()
    x = '{"nodes": "测试测点", "algcode": "test001", "datasource": [{"parameter": [3930,3930,10,2,2], "deviceid":"xxx", "channelid":[-999], "alarm_configs":{"10100":[10,1]}}],"indices": [], "exceptions": [], "deviceid":"sb001", "devicename":"测试设备", "starttime":"t1", "endtime":"t2"}'
    graph = Graph_test.graph_from_json(x)

    alg = Alg001(graph)
    alg.execute()

    graph.consumetime = time.time() - t1
    sys.stdout.write(str(graph.to_json()) + '\n')


if __name__ == '__main__':
    main()
