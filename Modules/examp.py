def powers(start=1,end=10,power=2):
    """Prints powers of integers.
    
     Keyword arguments:
     start -- integer to start on. DEFAULT = 1
     end -- integer to end on (counts in steps of 1). DEFAULT = 10
     power -- to what power to evaluate to. DEFAULT = 2"""
    print("Integers to the power of "+str(power)+" starting at "+str(start)+" and ending at "+str(end)+":")
    print("")
    for i in range(start,end+1):
        print(str(i)+" to the power of "+str(power)+" = "+str(i**(power)))
        
def hello_world():
    """Prints Hello World!"""
    print("Hello World!")