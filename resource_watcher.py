import os
import psutil
import time
import threading
from functools import wraps

def monitor_resources(label="", interval=0.5):
    """
    Decorator that logs CPU and memory usage while the function is executing.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            proc = psutil.Process(os.getpid())
            stop_flag = threading.Event()

            def log_usage():
                proc.cpu_percent(interval=None)
                while not stop_flag.is_set():
                    cpu = proc.cpu_percent(interval=None)
                    mem = proc.memory_info().rss / (1024 * 1024)
                    print(f"[{label}] CPU: {cpu:.2f}% | Memory: {mem:.2f} MB")
                    time.sleep(interval)

            t = threading.Thread(target=log_usage, daemon=True)
            t.start()

            try:
                return func(*args, **kwargs)
            finally:
                stop_flag.set()
                t.join()
        return wrapper
    return decorator
