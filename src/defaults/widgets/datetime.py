class Widget: # Must be named Widget.
    def __init__(self):
        # It is advised that you process your most intensive logic here.
        import time
        self.Value = time.ctime()
    
    def Get(self):return self.Value # Must be named Get, but may return anything that can be converted to a string.