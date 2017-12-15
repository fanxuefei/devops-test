import time
def timer(func):
    def deco(*args,**kwargs):
        start_time = time.time()
        func(*args,**kwargs)
        stop_time = time.time()
        print('the func run time %s' %(stop_time-start_time))
    return deco
@timer
def test1():
    time.sleep(3)
    print('in the test1')

@timer
def test2():
    time.sleep(3)
    print('in the test2')


test1()
test2()