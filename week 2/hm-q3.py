import random

random.seed(0)
class MyPerfTime:
    elapsed_time=0
    @staticmethod
    def time():
        number=random.randrange(1, 10)
        MyPerfTime.elapsed_time+=number 
        return MyPerfTime.elapsed_time-number # return last point of elapsed_time

#%%

# Create the decorator here
def timer(func):
    tm = MyPerfTime()
    def wrapper(*args,**kargs):
        print("Testing the performance of '{0}'".format(func.__name__))
        t1 = tm.time()
        result = func(*args,**kargs)
        t2 = tm.time()
        t = t2 - t1
        print("Finished '{0}' in {1:.4f} secs".format(func.__name__,t))
        return  result
    return wrapper
#%%



@timer # the thing I need to write
def function_to_be_tested():
    res=[]
    for i in range(8):
        res.append(str(i))
    return ' '.join(res)

@timer
def second_function_to_be_tested():
    res=[]
    for i in range(12):
        res.append(str(i))
    return ' '.join(res)
#%%
print(function_to_be_tested())
print(second_function_to_be_tested())

# Testing the performance of 'function_to_be_tested'
# Finished 'function_to_be_tested' in 7.0000 secs
# 0 1 2 3 4 5 6 7
# Testing the performance of 'second_function_to_be_tested'
# Finished 'second_function_to_be_tested' in 1.0000 secs
# 0 1 2 3 4 5 6 7 8 9 10 11

