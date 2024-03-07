# Automated Transport Line (Using uArm)
Welcome to my senior project. This marks my first attempt at using image processing for task execution. While relatively simple, it should be sufficient for the task environment. :)
## Introduction
In this project, we utilized the uArm Swift Pro robotic arm to accomplish the gripping of various-shaped building blocks. Subsequently, we employed an Arduino Uno-controlled autonomous transport vehicle to transport the building blocks to another robotic arm for unloading. Throughout this process, a Raspberry Pi was employed for image recognition and control of the robotic arm's gripping actions. Additionally, we controlled a gate to ensure the transport vehicle could stop at the unloading point.
## Requirements
### Software
* opencv-python 3.4.6
* RPi.GPIO
* random
* uarm.wrapper
* time
* [uArm-Python-SDK](https://github.com/uArm-Developer/uArm-Python-SDK/tree/2.0)
### Hardware
* uArm Swift Pro * 2
* Raspberry Pi 3 Model B+ * 2
* Arduino Uno
* Logitech C270 Webcam * 2
* L298N
* HC-SR04 * 3
* DC3V-6V Reduction Motor * 2
* TCR5000 * 2
* SG90 Servo Motor (used for gate control) * 2

The rest of the miscellaneous details can be found in the attached document.
## Descriptions

The workflow of this project is as follows:

![Overview_Diagram](image/Overview_Diagram.png)

1. AGV starts and moves forward after confirming no obstacles ahead.
2. Loading area gate detects AGV and lowers the gate to stop the AGV.
3. Image recognition identifies items in the loading area. The robotic arm loads goods onto the AGV and raises the gate for AGV to proceed.
4. Unloading area gate detects AGV and lowers the gate to stop the AGV.
5. Image recognition identifies items on the AGV platform. The robotic arm picks up the goods and unloads them in the unloading area, raising the gate for AGV to move forward.
