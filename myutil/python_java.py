from jpype import *
import jpype

jvmPath = jpype.getDefaultJVMPath()
# ext_classpath = "E:\Lib\OracleMain_ojdbc14.jar"
ext_classpath = "C:\cygwin64\home\tfchen\gitRes\pythonEden\dcap_db\oraclelink\OracleMain_ojdbc8.jar"
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
    jpype.startJVM(jvmPath, jvmArg)