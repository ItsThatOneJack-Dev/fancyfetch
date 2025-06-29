class Widget: # Must be named Widget.
    def __init__(self):
        # It is advised that you process your most intensive logic here.
        import platform
        #self.Value = "{{gold}}OS: {{white}}"+platform.uname().system+" "+platform.uname().version+" ("
        self.Value = f"<:gold:>OS: <:white:>{platform.uname().system} {platform.uname().version} ({platform.machine()})"
    
    def Get(self):return self.Value # Must be named Get, but may return anything that can be converted to a string.