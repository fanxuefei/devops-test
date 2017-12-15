import time
def test(func):
    start_time = time.time()
    func()
    stop_time = time.time()
    print("the func run time %s" %(stop_time-start_time))
    return func
@test
def bar():
    time.sleep(3)
    print(" in the bar")



bar()