import sys
import traceback
import time
from com_util import generate_graph
from datetime import datetime
from alg001_MG2250 import Alg001
from alg001_s2_MG2250 import Alg001_S2
from alg003_MG2250 import Alg003
from alg004_MG2250 import Alg004
from alg004_s2_MG2250 import Alg004_S2
from alg004_s3_MG2250 import Alg004_S3
from alg004_s4_MG2250 import Alg004_S4
from alg004_s5_MG2250 import Alg004_S5
from alg004_s6_MG2250 import Alg004_S6
from alg004_s7_MG2250 import Alg004_S7
from alg004_s8_MG2250 import Alg004_S8
from alg005_MG2250 import Alg005
from alg010_MG2250 import Alg010
from alg011_MG2250 import Alg011
from alg014_MG2250 import Alg014
from alg015_MG2250 import Alg015
from alg016_MG2250 import Alg016
from alg017_MG2250 import Alg017
from alg018_MG2250 import Alg018
from alg019_MG2250 import Alg019
from alg021_MG2250 import Alg021


def main():
    t1 = time.time()
    for x in sys.stdin:
        try:
            graph = generate_graph(x)
            algcode = graph.algcode

            if algcode == 'alg001':    # 电机卡阻
                alg = Alg001(graph)
            elif algcode == 'alg001_s2_MG2250':    # 电机卡阻s2
                alg = Alg001_S2(graph)
            elif algcode == 'alg003_MG2250':  # 伺服阀动作过程压差指标
                alg = Alg003(graph)
            elif algcode == 'alg004_MG2250':  # 伺服阀稳态过程开口度
                alg = Alg004(graph)
            elif algcode == 'alg004_s2_MG2250':  # 伺服阀稳态过程开口度s2
                alg = Alg004_S2(graph)
            elif algcode == 'alg004_s3_MG2250':
                alg = Alg004_S3
            elif algcode == 'alg004_s4_MG2250':
                alg = Alg004_S4
            elif algcode == 'alg004_s5_MG2250':
                alg = Alg004_S5
            elif algcode == 'alg004_s6_MG2250':
                alg = Alg004_S6
            elif algcode == 'alg004_s7_MG2250':
                alg = Alg004_S7
            elif algcode == 'alg004_s8_MG2250':
                alg = Alg004_S8
            elif algcode == 'alg005_MG2250':
                alg = Alg005(graph)
            elif algcode == 'alg010_MG2250':
                alg = Alg010(graph)
            elif algcode == 'alg011_MG2250':
                alg = Alg011(graph)
            elif algcode == 'alg014_MG2250':
                alg = Alg014(graph)
            elif algcode == 'alg015_MG2250':
                alg = Alg015(graph)
            elif algcode == 'alg016_MG2250':
                alg = Alg016(graph)
            elif algcode == 'alg017_MG2250':
                alg = Alg017(graph)
            elif algcode == 'alg018_MG2250':
                alg = Alg018(graph)
            elif algcode == 'alg019_MG2250':
                alg = Alg019(graph)
            elif algcode == 'alg021_MG2250':
                alg = Alg021(graph)
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
