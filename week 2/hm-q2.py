import math
import os
import random
import re
import sys





class OperatorNotRecognizedError(Exception):
    pass

class NegativeInputError(Exception):
    pass
   
class NegativeOutputError(Exception):
    pass
  
class NonIntegerInputError(Exception):
    pass
  
        
class OutputTooLargeError(Exception):
    pass

        

def pocket_calculator(x, operator, y):
    ops = {'+':(lambda x,y:x+y),'-':(lambda x,y:x-y),'x':(lambda x,y:x*y),'/':(lambda x,y:x/y)}
    m = [operator == i for i in ['-','+','x','/']]
    try:

        if True not in m:
            raise OperatorNotRecognizedError
            
        if ('.' in x or '.' in y):
            raise NonIntegerInputError
            
        x = int(x)
        y = int(y)
         
        if x <0 or y < 0:
            raise NegativeInputError
        if y == 0:
            return 0
        result = math.trunc(ops[operator] (x,y))
        
        if result < 0:
            raise NegativeOutputError
            
        if result > 9999999:
            raise OutputTooLargeError
                
    except OperatorNotRecognizedError:
        return 'OperatorNotRecognized'
    
    except ValueError:
        return 'InputNotANumber'

    except NegativeInputError:
        return 'NegativeInput'
        
    except NegativeOutputError:
        return 'NegativeOutput'
        
    except NonIntegerInputError:
        return 'NonIntegerInput'
        
    except OutputTooLargeError:
        return 'OutputTooLarge'
    return result


if __name__ == '__main__':


    x = '0'

    operator = '/'
    
    y = '1'

    result = pocket_calculator(x, operator, y)
    print(result)
