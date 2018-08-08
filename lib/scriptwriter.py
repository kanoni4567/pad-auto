import os.path
from lib.classifier import get_canvas_position
from lib.screen import get_screenshot

script_path = "C:\\Users\\saiyann\\PycharmProjects\\padauto\\script"
complete_path = os.path.join(script_path,"script.py")

def get_coords():
    screen = get_screenshot()
    return get_canvas_position(screen)


def write_path_script(path):
    f = open(complete_path,"w+")
    f.write("from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice\r\n")
    f.write("device = MonkeyRunner.waitForConnection()\r\n")

    xstart, xend, ystart, yend, size = get_coords()

    y, x = int((path[0][0]+1) * size - size / 2 + ystart), int((path[0][1]+1) * size - size / 2 + xstart)

    f.write("device.touch(%d,%d,MonkeyDevice.DOWN)\r\n" %(x,y))
    f.write("MonkeyRunner.sleep(0.8)\r\n")
    for p in path[1:]:
        x += p[1]*size
        y += p[0]*size
        f.write("device.touch(%d,%d,MonkeyDevice.MOVE)\r\n" %(x,y))
        f.write("MonkeyRunner.sleep(0.2)\r\n")
    f.write("device.touch(%d,%d,MonkeyDevice.UP)\r\n" % (x, y))
    f.close

if __name__ == "__main__":
    print(get_coords())