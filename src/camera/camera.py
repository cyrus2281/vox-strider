import time
import subprocess
import threading


def capture_images(file_path, size, interval):
    while True:
        subprocess.run(
            f"rpicam-jpeg --output {file_path} -v 0 -n -t 1 --rotation 180 --width {size[0]} --height {size[1]}",
            shell=True,
        )
        time.sleep(interval)


def setup_camera(latest_image_path, size=(720, 480), interval=0.5):
    camera_thread = threading.Thread(
        target=capture_images, args=(latest_image_path, size, interval)
    )
    camera_thread.daemon = True
    camera_thread.start()
    return camera_thread
