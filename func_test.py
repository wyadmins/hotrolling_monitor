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
    x = '{"nodes": "测试测点", "algcode": "test001", "datasource": [{"parameter": [1, 1000, 5, 0, 0], "channelid":[-999]}], "indices": [], "exceptions": [], "deviceid":"sb001", "devicename":"测试设备", "starttime":"t1", "endtime":"t2"}'
    graph = Graph_test.graph_from_json(x)

    alg = Alg015(graph)
    alg.execute()

    graph.consumetime = time.time() - t1
    sys.stdout.write(str(graph.to_json()) + '\n')


if __name__ == '__main__':
    main()
