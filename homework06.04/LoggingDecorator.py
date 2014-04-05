import logging


def logging_decorator(fileName):
    def inner_decorator(f):
        def wrap(*args, **kwargs):
            logger = logging.getLogger('logName')
            if not logger.hasHandlers():
                hdlr = logging.FileHandler(fileName)
                hdlr.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
                logger.addHandler(hdlr)
            logger.setLevel(logging.INFO)
            if len(args) == len(kwargs) == 0:
                logger.info('Function {0} was called'.format(f.__name__))
            elif len(kwargs) == 0:
                logger.info('Function {0} was called with args {1}'.format(f.__name__, args))
            elif len(args) == 0:
                logger.info('Function {0} was called with kwargs {1}'.format(f.__name__,
                                                                             {x[0]: x[1] for x in kwargs.items()}))
            else:
                logger.info('Function {0} was called with args {1} and kwargs {2}'.format
                            (f.__name__, args, {x[0]: x[1] for x in kwargs.items()}))
            f(*args, **kwargs)
        return wrap
    return inner_decorator


@logging_decorator('testLog.txt')
def func(arg):
    print(arg)

@logging_decorator('testLog.txt')
def awesomeFunc(arg1, arg2, arg3):
    print(arg1 + arg2 + arg3)

@logging_decorator('testLog.txt')
def freakyFunc(**kwargs):
    for x in kwargs.values():
        print(x)

if __name__ == '__main__':
    func(5)
    awesomeFunc(1, 2, 3)
    freakyFunc(b=5)