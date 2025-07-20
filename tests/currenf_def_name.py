import inspect

def myfunction():
    print(f'Имя функции: {inspect.currentframe().f_code.co_name}')
    pass
myfunction()