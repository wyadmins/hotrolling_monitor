import sys
import traceback
import time
from datetime import datetime
from graph import Graph
from alg001_MG2250 import Alg001




def main():
    t1 = time.time()
    for x in sys.stdin:
        try:
            graph = Graph.graph_from_json(x)
            algcode = graph.algcode

            if algcode == 'alg001':  # 电机卡阻
                alg = Alg001(graph)



            else:
                raise Exception("Algorithm not registered !")

            if algcode is not None:
                alg.execute()
            else:
                raise Exception("Algorithm not registered !")
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
