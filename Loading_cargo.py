import RPi.GPIO as GPIO
import time, random
from uarm.wrapper import SwiftAPI 
from cv2 import cv2

swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'}, cmd_pend_size = 2)
swift.waiting_ready()
device_info = swift.get_device_info()
firmware_version = device_info['firmware_version']
if firmware_version and not firmware_version.startswith(('0.', '1.', '2.', '3.')):
    swift.set_speed_factor(0.00005)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

trig , echo = 25, 8
motor_pin, PWM_FREQ, STEP = 17, 50, 90

GPIO.setup(trig, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)
GPIO.setup(motor_pin, GPIO.OUT)

pwm = GPIO.PWM(motor_pin, PWM_FREQ)
pwm.start(90)

def angle_to_duty_cycle(angle = 0):
    duty_cycle = (0.05 * PWM_FREQ) + (0.19 * PWM_FREQ * angle / 180)
    return duty_cycle

def get_distance():
    GPIO.output(trig, False)
    time.sleep(0.0005)
    GPIO.output(trig, True)
    time.sleep(0.001)
    GPIO.output(trig, False)
    while GPIO.input(echo) == 0:
        start = time.time()
    while GPIO.input(echo) == 1:
        end = time.time()
    return (end - start) * 17150

swift.set_position(x = 110, y = 0, z = 20, speed = 9e7)
time.sleep(3)   

while True:
    
    if 4 < get_distance() <= 20:
    
        dc = angle_to_duty_cycle(0) #          
        pwm.ChangeDutyCycle(dc)
        time.sleep(5)
 
        cap  = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read() 
            cv2.imshow("capture", frame)
            if cv2.waitKey(5000):
                cv2.imwrite("image.jpg", frame)
                break
        cap.release()
        cv2.destroyWindow("capture")
   
        image = cv2.imread("image.jpg")
        white_board = cv2.imread("white_board.jpg")    # 去背景用圖片，可自行更換
        diff = cv2.absdiff(white_board, image)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        ret, th1 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        blur = cv2.GaussianBlur(th1, (11, 11), 0)
        Canny = cv2.Canny(blur, 50, 150)
        _, find_contours, hierarchy = cv2.findContours(Canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  
        image_contours = cv2.drawContours(image, find_contours, -1, (0, 0, 255), 1)

        cv2.imshow("image_contours", image_contours)
        cv2.waitKey(5000)
        cv2.destroyWindow("image_contours")

        p = 1
        for contours1, contours2 in zip (range(len(find_contours)), find_contours):
            epsilon = 0.025 * cv2.arcLength(find_contours[contours1], True)
            approx = cv2.approxPolyDP(find_contours[contours1], epsilon, True)
            corners = len(approx) 
            
            if corners == 3:
                shape_type = "triangle" 
            elif 4 <= corners <= 6:
                shape_type = "rectangle"
            elif 7 <= corners <= 15:
                shape_type = "round"
            else:
                shape_type = "無法辨識"  
                
            M = cv2.moments(contours2)
            if M["m00"] == 0:
                M["m00"] = 1  
                
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            x, y, w, h = cv2.boundingRect(contours2) # 將輪廓分解為識別物件的左上角座標和寬、高
            cv2.circle(image_contours, (cx, cy), 3, (0, 255, 0), -1)
            cv2.putText(image, str(p), (x - 10, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2) # 給識別物件寫上標號 # 加減 10 是調整字元位置
            cv2.putText(image, str(shape_type), (x + 20, y + 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2) # 給識別物件寫上 shape_type # 加減10是調整字元位置
            p += 1
            print("形狀: %s, 鏡頭內中心座標: (%d px , %d px), 絕對座標: (%d , %d)"% 
                 (shape_type, cx, cy, round(cy * 0.25363 + 135, 3), round(cx * 0.25455 - 67, 3)))
            
        cv2.imshow("image_ci1rcle_contours", image_contours)
        cv2.waitKey(5000)
        cv2.destroyWindow("image_ci1rcle_contours")
          
        def repeat_action():
             random_value = random.random() * 10
             swift.set_position(y = 200 + random_value, speed = 9e7) # 移動到放置點Y
             time.sleep(3)       
             swift.set_position(z = 150, speed = 9e7) # 下降放置
             time.sleep(3)  
             print(swift.set_gripper(catch = False)) # 夾子打開
             time.sleep(3)   
             swift.set_position(z = 160, speed = 9e7) # 提高
             time.sleep(3)             
             swift.set_position(y = 0, speed = 9e7) # 手臂原點
             time.sleep(3)          
             swift.set_position(z = 70, speed = 9e7) # 手臂原點
             time.sleep(3)          
             swift.set_position(z = 50, speed = 9e7) # 手臂原點
             time.sleep(3)         
             swift.set_position(z = 20, speed = 9e7) # 手臂原點
             time.sleep(3)     
             swift.set_position(x = 110, speed = 9e7) # 手臂原點
             time.sleep(3)    
             
        A = [cv2.moments(contours) for contours in find_contours]
        cx = [int(M["m10"] / M["m00"]) for M in A]
        cy = [int(M["m01"] / M["m00"]) for M in A]
        
        for contours1 in range(len(find_contours)): # i:第幾個物體 # contours1:第幾個輪廓
            
            speed = 9e7   # x=110~260, y=300(左)~-300(右), z=20~170
            swift.set_position(y = cy * -0.260245 + 86, speed = 9e7) # 移動到物體Y,可自行更改座標差異值
            time.sleep(3)
            swift.set_position(z = 10, speed = 9e7) # 下降物體到一半高
            time.sleep(3)
            swift.set_position(x = cx * 0.2022 + 163, speed = 9e7) # 移動到物體X,可自行更改座標差異值
            time.sleep(3)
    
            print(swift.set_gripper(catch = True)) # 移動到物體中心點  # 物體夾取 # TIMEOUT:中心點不在輪廓內
            time.sleep(3)
            swift.set_position(z = 160, speed = 9e7) # 提高  
            time.sleep(3)
            
            epsilon = 0.09 * cv2.arcLength(find_contours[contours1], True)
            approx = cv2.approxPolyDP(find_contours[contours1], epsilon, True)
            corners = len(approx) 
            
            if corners == 3: # shape_type = "三角形"
                swift.set_position(x = 185, speed = 9e7) # 移動到放置點X
                time.sleep(3)
                repeat_action()
            elif corners == 4: # shape_type = "矩形" 
                swift.set_position(x = 175, speed = 9e7) # 移動到放置點X
                time.sleep(3)
                repeat_action()
            elif 5 <= corners <= 15: # shape_type = "圓形"
                swift.set_position(x = 165, speed = 9e7) # 移動到放置點X
                time.sleep(3)
                repeat_action()
            else: # shape_type = "無法辨識"
                swift.set_position(x = 155, speed = 9e7) # 移動到放置點X
                time.sleep(3)
                repeat_action()

        dc = angle_to_duty_cycle(90)          
        pwm.ChangeDutyCycle(dc)
        time.sleep(5)

    else:
        print("沒有車子經過")

