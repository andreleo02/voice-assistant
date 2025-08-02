import queue
import threading

audio_queue = queue.Queue()

audio_done_event = threading.Event()
audio_done_event.set()