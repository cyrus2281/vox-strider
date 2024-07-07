import time
import subprocess
import threading

from constants import SNAPSHOT_INTERVAL, SNAPSHOT_RESOLUTION, SNAPSHOT_ROTATION


def capture_images(file_path, size, interval, rotation=SNAPSHOT_ROTATION):
    while True:
        subprocess.run(
            f"rpicam-jpeg --output {file_path} -v 0 -n -t 1 --rotation {rotation} --width {size[0]} --height {size[1]}",
            shell=True,
        )
        time.sleep(interval)


def setup_camera(latest_image_path, size=SNAPSHOT_RESOLUTION, interval=SNAPSHOT_INTERVAL):
    camera_thread = threading.Thread(
        target=capture_images, args=(latest_image_path, size, interval)
    )
    camera_thread.daemon = True
    camera_thread.start()
    return camera_thread
