import subprocess
import numpy as np
import cv2
def get_screenshot():
    pipe = subprocess.Popen("adb shell screencap -p",
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, shell=True)
    image_bytes = pipe.stdout.read().replace(b'\r\r\n', b'\n')
    nparr = np.fromstring(image_bytes, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    return image

    #cv2.imshow("", image)
    #cv2.waitKey(0)
    #cv2.destroyWindow("")

