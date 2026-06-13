import sys
import os

SDK_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "pynaoqi-python2.7-2.8.6.23-win64-vs2015-20191127_152649", "lib")
if SDK_PATH not in sys.path:
    sys.path.append(SDK_PATH)
if SDK_PATH not in os.environ['PATH']:
    os.environ['PATH'] = SDK_PATH + os.pathsep + os.environ['PATH']

from naoqi import ALProxy

ROBOT_IP = "169.254.80.144"
PORT = 9559

modules = ["ALMotion", "ALTextToSpeech", "ALMemory", "ALBehaviorManager", "ALVideoDevice", "ALFaceDetection", "ALAutonomousLife", "ALBasicAwareness"]

out_file = "naoqi_methods_dump.txt"

with open(out_file, "w") as f:
    for mod_name in modules:
        f.write("=== " + mod_name + " ===\n")
        try:
            proxy = ALProxy(mod_name, ROBOT_IP, PORT)
            methods = proxy.getMethodList()
            for m in methods:
                f.write("- " + str(m) + "\n")
        except Exception as e:
            f.write("Error connecting to " + mod_name + ": " + str(e) + "\n")
        f.write("\n")

print("Successfully wrote methods to " + out_file)
