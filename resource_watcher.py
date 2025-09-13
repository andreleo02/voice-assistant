import os
import psutil
import time
import threading
from functools import wraps
from statistics import mean

def monitor_resources(label="", interval=0.5):
    """
    Decorator that samples CPU% and RAM while the function runs,
    then prints AVG/PEAK CPU, AVG/PEAK RAM, and elapsed time.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            proc = psutil.Process(os.getpid())
            stop_flag = threading.Event()
            cpu_samples, mem_samples = [], []

            def sampler():
                proc.cpu_percent(interval=None)
                while not stop_flag.is_set():
                    cpu_samples.append(proc.cpu_percent(interval=None))
                    mem_samples.append(proc.memory_info().rss / (1024 * 1024))
                    time.sleep(interval)

            t = threading.Thread(target=sampler, daemon=True)
            t.start()
            try:
                return func(*args, **kwargs)
            finally:
                stop_flag.set()
                t.join()
                avg_cpu = mean(cpu_samples) if cpu_samples else 0.0
                peak_cpu = max(cpu_samples) if cpu_samples else 0.0
                avg_mem = mean(mem_samples) if mem_samples else 0.0
                peak_mem = max(mem_samples) if mem_samples else 0.0
                print(
                    f"[{label}] "
                    f"CPU avg/peak: {avg_cpu:.2f}% / {peak_cpu:.2f}% | "
                    f"RAM avg/peak: {avg_mem:.2f} MB / {peak_mem:.2f} MB"
                )
        return wrapper
    return decorator
