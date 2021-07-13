start = 0
from datetime import datetime as dt
def dtn():
    """Sets start variable to the current date and time
    
    IMPORTANT: must define global start variable before using"""
    global start
    start = dt.now()
    
def end():
    """Using in conjunction with dtn() function, returns the time taken between dtn() and this function being called"""
    return str(dt.now()-start)

def gen_end():
    """Generic function that gives a string telling how long it has been since dtn() was called. Can be used instead of end()"""
    stop = end()
    print("Completed in :"+stop)