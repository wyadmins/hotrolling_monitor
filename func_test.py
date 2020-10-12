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

def main():
    t1 = time.time()
    x = '{"nodes": "测试测点", "algcode": "test001", "datasource": [{"parameter": [10, 5, 1], "channelid":[-999]}], "indices": [], "exceptions": [], "deviceid":"sb001", "devicename":"测试设备", "starttime":"t1", "endtime":"t2"}'
    try:
        graph = Graph_test.graph_from_json(x)

        alg = Alg016(graph)
        alg.execute()

        graph.consumetime = time.time() - t1
        sys.stdout.write(str(graph.to_json()) + '\n')
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        errorinfo = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
        error = dict(exceptiontype=str(exc_value), time=str(datetime.now()), exception=errorinfo,
                     runningtime=str(time.time() - t1))
        if 'graph' in locals():
            graph.exceptions.append(error)
            graph.inputstr = [x]
        graph.consumetime = time.time() - t1
        sys.stdout.write(str(graph.to_json()) + '\n')


if __name__ == '__main__':
    main()
