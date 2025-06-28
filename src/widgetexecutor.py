import threading as ThreadingLibrary
import time as TimeLibrary
from contextlib import contextmanager as ContextManager

@ContextManager
def Timeout(duration):
    Result = {"timedout": False}
    
    def TimeoutHandler():
        TimeLibrary.sleep(duration)
        Result["timedout"] = True
    
    Timer = ThreadingLibrary.Timer(duration, TimeoutHandler)
    Timer.start()
    
    try:
        yield Result
        Timer.cancel()
        if Result["timedout"]:
            raise TimeoutError("Timed out.")
    finally:
        Timer.cancel()

def Execute(lines):
    Code = '\n'.join(lines)
    LocalVariables = {}
    
    try:
        with Timeout(5) as TimeoutResult:
            exec(Code, {"__builtins__": __builtins__}, LocalVariables)
            if TimeoutResult['timed_out']:
                return "Widget timed out"
            return LocalVariables.get('_', str(LocalVariables))
    except TimeoutError:
        return "Widget timed out!"
    except Exception as e:
        return f"Widget error! Error: {e}"