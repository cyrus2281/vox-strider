from camera.camera import setup_camera
from server.http_server import start_http_server
from robot.loop import loop

def main():
    camera = setup_camera()
    command_queue = start_http_server(camera)
    loop(command_queue)

if __name__ == "__main__":
    main()