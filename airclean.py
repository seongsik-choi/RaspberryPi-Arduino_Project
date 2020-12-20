import serial                //시리얼통신 모듈
from queue import Queue      //시스템 큐 생성 모듈
import RPi.GPIO as gpio      //GPIO 모듈
import time                  //time 모듈 내 delay()함수사용
import threading             //멀티 스레드 모듈
from RPLCD import CharLCD    //text LCD 모듈
//기본설정을 처리하는 함수생성
def settings():
	//ignore warning messages
	gpio.setwarnings(False)
	//set up pin numbers as BCM
	gpio.setmode(gpio.BCM)
        //스레드간 미세먼지 값 전달을 위한 변수
	global data1, data2
        //각각의 미세먼지 센서가 보내는 데이터를 전송할 큐를 따로 생성
	global q1, q2
	q1 = Queue()
	q2 = Queue()
//GPIO핀을 할당하는 함수생성
def allocations():
	//pin - gpio allocation
	global red, green
        //red : red LED, green : green LED
	red = 24                                      //GPIO NUMBER 24
	green = 25                                    //GPIO NUMBER 25
	gpio.setup(red, gpio.OUT)
	gpio.setup(green, gpio.OUT)
	//out2in_fan : 밖에서 안으로 공기를 보내는 환풍기
	//in2out_fan : 안에서 밖으로 공기를 보내는 환풍기
	global out2in_fan, in2out_fan
	out2in_fan = 11                               //GPIO NUMBER 11
	in2out_fan = 9                                //GPIO NUMBER 9
	gpio.setup(out2in_fan, gpio.OUT)
	gpio.setup(in2out_fan, gpio.OUT)
	//servo_in2out : in2out_fan과 함께 동작
	global servo_in2out, motor_in2out
	servo_in2out = 6                              //GPIO NUMBER 6   
	gpio.setup(servo_in2out, gpio.OUT)
	//모터의 PWM범위를 0~50Hz로 설정
	motor_in2out = gpio.PWM(servo_in2out, 50)
	//초기 모터 위치는 10으로 설정
	motor_in2out.start(10)
        //servo_out2in : out2in_fan과 함께 동작
	global servo_out2in, motor_out2in
	servo_out2in = 7                              //GPIO NUMBER 7
	gpio.setup(servo_out2in, gpio.OUT)
	motor_out2in = gpio.PWM(servo_out2in, 50)
	motor_out2in.start(10)
//미세먼지를 측정하는 스레드 함수
def measuring(q1, q2):
	print("measuring start")
	//switch값에 따라 미세먼지센서를 번갈아가며 데이터를 가져옴
	switch = 0
	//set up serial port
	//아두이노 시리얼포트 : /dev/ttyACM0
	//           통신속도 : 9600 baud
	ser = serial.Serial("/dev/ttyACM0", 9600)
	//textLCD allocation
	lcd = CharLCD(numbering_mode = gpio.BCM, cols = 16, rows = 2, pin_rs = 4, pin_e = 17, pins_data = [18, 27, 22, 23])
	lcd.clear()                                   //화면 초기화 함수
	lcd.cursor_pos = (0, 0)                       //커서 위치 설정함수
	lcd.write_string("1. ")                       //문자열을 LCD에 표시하는 함수
	lcd.cursor_pos = (0, 11)
	lcd.write_string("ug/m3")
	lcd.cursor_pos = (1, 0)
	lcd.write_string("2. ")
	lcd.cursor_pos = (1, 11)
	lcd.write_string("ug/m3")
	while True:
		try:
                        //시리얼포트에서 읽은 내용을 UTF-8로 변환하고 변수에 저장
			line = ser.readline().decode('utf-8')
			if line:
				if switch == 0:
					data1 = line
					//queue에 데이터 전송
					q1.put(data1)
					switch = 1
					print("send[1]", data1)
					lcd.clear()
					lcd.cursor_pos = (0, 0)
					lcd.write_string("<1> ")
					lcd.cursor_pos = (0, 4)
					lcd.write_string(str(data1))
					lcd.cursor_pos = (0, 11)
					lcd.write_string("ug/m3")
				else:
					data2 = line
					q2.put(data2)
					//queue에 데이터 전송
					switch = 0
					print("send[2]", data2)
					lcd.cursor_pos = (1, 0)
					lcd.write_string("<2> ")
					lcd.cursor_pos = (1, 4)
					lcd.write_string(str(data2))
					lcd.cursor_pos = (1, 11)
					lcd.write_string("ug/m3")
                //아무 키보드 키 입력시
		except KeyboardInterrupt:
			ser.close()           //시리얼 통신 종료
			q.task_done()         //queue 사용 종료
			break
//----------------------------- program start -----------------------------------
settings()
allocations()
//스레드로 동작시킬 함수 지정(타겟 - measuring함수, 매개변수 - queue 2개)
t = threading.Thread(target = measuring, args = (q1, q2))
t.start()//스레드 시작
while True:
	//data1 is dust concentration rate inside
        //queue에서 데이터 읽어옴
	data1 = q1.get()
	//시리얼통신으로 읽어온 값은 문자열이므로 실수형으로 변환
	data1 = float(data1)
	print("received[1] :", data1, "\n")
	data2 = q2.get()
	data2 = float(data2)
	print("received[2] :", data2, "\n")
        //핵심 동작은 보고서의 "4.1 제품 설계 목표"에 수록
	if data1 >= 76.0:
		gpio.output(red, True)
		gpio.output(green, False)
		if data2 >= 76.0:
			print("안 : 매우 나쁨! 밖 : 매우 나쁨!\n")
			motor_in2out.ChangeDutyCycle(10)
			motor_out2in.ChangeDutyCycle(10)
		elif 36.0 <= data2 < 76.0:
			print("안 : 매우 나쁨! 밖 : 나쁨!\n")
			motor_in2out.ChangeDutyCycle(10)
			motor_out2in.ChangeDutyCycle(10)
		elif 16.0 <= data2 < 36.0:
			print("안 : 매우 나쁨! 밖 : 보통!\n")
			motor_in2out.ChangeDutyCycle(5)
			motor_out2in.ChangeDutyCycle(5)
		else:
			print("안 : 매우 나쁨! 밖 : 좋음!\n")
			motor_in2out.ChangeDutyCycle(5)
			motor_out2in.ChangeDutyCycle(5)
	elif 76.0 > data1 >= 36.0:
		gpio.output(red, True)
		gpio.output(green, False)
		if data2 >= 76.0:
			print("안 : 나쁨! 밖 : 매우 나쁨!\n")
			motor_in2out.ChangeDutyCycle(10)
			motor_out2in.ChangeDutyCycle(10)
		elif 36.0 <= data2 < 76.0:
			print("안 : 나쁨! 밖 : 나쁨!\n")
			motor_in2out.ChangeDutyCycle(10)
			motor_out2in.ChangeDutyCycle(10)
		elif 16.0 <= data2 < 36.0:
			print("안 : 나쁨! 밖 : 보통!\n")
			motor_in2out.ChangeDutyCycle(5)
			motor_out2in.ChangeDutyCycle(5)
		else:
			print("안 : 나쁨! 밖 : 좋음!\n")
			motor_in2out.ChangeDutyCycle(5)
			motor_out2in.ChangeDutyCycle(5)
	elif 36.0 > data1 >= 16.0:
		gpio.output(red, False)
		gpio.output(green, True)
		if data2 >= 76.0:
			print("안 :보통! 밖 : 매우 나쁨!\n")
			motor_in2out.ChangeDutyCycle(10)
			motor_out2in.ChangeDutyCycle(10)
		elif 36.0 <= data2 < 76.0:
			print("안 : 보통! 밖 : 나쁨!\n")
			motor_in2out.ChangeDutyCycle(10)
			motor_out2in.ChangeDutyCycle(10)
		elif 16.0 <= data2 < 36.0:
			print("안 : 보통! 밖 : 보통!\n")
			motor_in2out.ChangeDutyCycle(10)
			motor_out2in.ChangeDutyCycle(10)
		else:
			print("안 : 보통! 밖 : 좋음!\n")
			motor_in2out.ChangeDutyCycle(5)
			motor_out2in.ChangeDutyCycle(5)
	else:
		gpio.output(red, False)
		gpio.output(green, True)
		if data2 >= 76.0:
			print("안 : 좋음! 밖 : 매우 나쁨!\n")
			motor_in2out.ChangeDutyCycle(10)
			motor_out2in.ChangeDutyCycle(10)
		elif 36.0 <= data2 < 76.0:
			print("안 : 좋음! 밖 : 나쁨!\n")
			motor_in2out.ChangeDutyCycle(10)
			motor_out2in.ChangeDutyCycle(10)
		elif 16.0 <= data2 < 36.0:
			print("안 : 좋음! 밖 : 보통!\n")
			motor_in2out.ChangeDutyCycle(10)
			motor_out2in.ChangeDutyCycle(10)
		else:
			print("안 : 좋음! 밖 : 좋음!\n")
			motor_in2out.ChangeDutyCycle(10)
			motor_out2in.ChangeDutyCycle(10)