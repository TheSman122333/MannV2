import threading

recognizer_event = threading.Event()
recognizer_event.set()

finger_mouse_event = threading.Event()
finger_mouse_event.clear() 