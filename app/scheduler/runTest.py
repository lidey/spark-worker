
from app.scheduler.schedulerTest import RunSchTest
from app.scheduler.method import runMethod
from app.scheduler.shell_scheduler import ShellScheduler

# ss = ShellScheduler()
# ss.add_job("123", "hehe")

st = RunSchTest()
st.runTest('name', '*/1')
# st.some_decorated_task();
# r = runMethod();
# r.doing();