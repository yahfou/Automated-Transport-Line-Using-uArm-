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
* DC3V-6V Reduction Motor * 2
* SG90 Servo Motor (used for gate control) * 2

The rest of the miscellaneous details can be found in the attached document.
## Descriptions
