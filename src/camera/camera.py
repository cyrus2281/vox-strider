import time
import threading
from picamera import PiCamera

# pip install picamera

def take_photo(camera, image_path, interval):
    while True:
        camera.capture(image_path)
        time.sleep(interval)
        
def setup_camera(latest_image_path, interval=0.5):
    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera_thread = threading.Thread(target=take_photo, args=(camera, latest_image_path, interval))
    camera_thread.daemon = True
    camera_thread.start()
    return camera_thread
    