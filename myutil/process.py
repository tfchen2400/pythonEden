from multiprocessing import Process
import os
from jpype import *
import jpype

# 子进程要执行的代码
def run_proc(name):
    jvmPath = jpype.getDefaultJVMPath()
    # ext_classpath = "E:\Lib\OracleMain_ojdbc14.jar"
    ext_classpath = "E:\Lib\OraceJdbc.jar"
    jvmArg = '-Djava.class.path=' + ext_classpath
    if not jpype.isJVMStarted():
        jpype.startJVM(jvmPath, jvmArg)
        system = jpype.java.lang.System
        system.out.println('hello world!')
        oracle = jpype.JClass('snippet.OracleMain')
        oracleMain = oracle()
        res = oracleMain.runSql("jdbc:oracle:thin:@192.168.60.95:1521:wangzw", "scott", "scott", "SELECT * FROM DEPT")
        print(res)
        shutdownJVM()
        #jpype.startJVM(jvmPath, jvmArg)
    print('Run child process %s (%s)...' % (name, os.getpid()))


if __name__ == '__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')
