import sys
import time
import traceback
from graph import Graph
# from alarm001_MG2250 import Alarm001


def main():
    t1 = time.time()
    for x in sys.stdin:
        try:
            graph = Graph.graph_from_json(x)
            algcode = graph.algcode

            if algcode == 'alarm001':  # 助卷辊电机卡阻
                # alg = Alarm001(graph)
                pass
            sys.stdout.write(str(graph.to_json()))
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            errorinfo = repr(traceback.format_exception(exc_type, exc_value, exc_traceback))
            sys.stdout.write(errorinfo)


if __name__ == '__main__':
    main()
