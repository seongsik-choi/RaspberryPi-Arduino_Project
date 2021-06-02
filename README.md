# RaspberryPi-Arduino_Project

## 미세먼지 키트와, 라즈베리파이, 아두이노를 이용한 공기정화 시스템

**1) Project Subject**
  - UART통신의 개념을 이해하고, 아두이노와 라즈베리파이간의 시리얼통신이 가능하도록 동작  
  - C언어, 파이썬을 사용하여 라즈베리파이 활용, 부속 모듈(Text Lcd, LED, 서보모터 등)의 사용법을 이해 및 활용  
  - 미세먼지 키트를 활용하여 서보모터 및 환풍기 동작을 구동  
  - 미세먼지 수치의 변화를 확인하고 설계 작품을 통하여 공기를 정화  
  - 팀 프로젝트를 통하여, 협업과 역할분담, 설계과정을 진행하여 원하는 작품의 완성이 최종 목적  
 
**2) Main Function**
  - 미세먼지 모듈을 사용하여 공기 속 미세먼지를 PM 1.0 단위로 감지  
  - 수치에 따라 환풍기 및 창문을 동작시켜 미세먼지 수치를 실시간으로 떨어뜨림  
  - 외.내부의 미세먼지 수치에 따라 창문 기능을 하는 서보모터와 LED의 색상이 다르게 동작하도록 프로그래밍  

내부 미세먼지 농도(ug/m³) | 외부 미세먼지 농도(ug/m³) | 창문 개폐 | LED 점등
-- | -- | -- | --
0~15 | 0~15 | 닫힘 | GREEN
0~15 | 16~35 | 닫힘 | GREEN
0~15 | 36~75 | 닫힘 | GREEN
0~15 | 76~ | 닫힘 | GREEN
16~35 | 0~15 | 열림 | GREEN
16~35 | 16~35 | 닫힘 | GREEN
16~35 | 36~75 | 닫힘 | GREEN
16~35 | 76~ | 닫힘 | GREEN
36~75 | 0~15 | 열림 | RED
36~75 | 16~35 | 열림 | RED
36~75 | 36~75 | 닫힘 | RED
36~75 | 76~ | 닫힘 | RED
76~ | 0~15 | 열림 | RED
76~ | 16~35 | 열림 | RED
76~ | 36~75 | 닫힘 | RED
76~ | 76~ | 닫힘 | RED

 **3) Technology**
  - O/S : Raspbian OS, Arduino
  - Language : c, python
  - Technology : UART Serial
  - Tools : Raspberry pi 3b+, Arduino, Embedded module
---

**4) Flow Chart**

![image](https://user-images.githubusercontent.com/76051264/102713824-238d5480-430e-11eb-89bd-adbf5c3521bf.png)  
---

**5) Function Diagram**
  -  All)  
![image](https://user-images.githubusercontent.com/76051264/102713811-08224980-430e-11eb-98f4-9b99b3f0515d.png)  

  - Detail)  
![image](https://user-images.githubusercontent.com/76051264/102713812-0a84a380-430e-11eb-9163-76980f6a9b71.png)  
----

**6) External Design**

![image](https://user-images.githubusercontent.com/76051264/102713846-40298c80-430e-11eb-9d35-2daf7abc952b.png)  
----

**7) Acrtion**

![image](https://user-images.githubusercontent.com/76051264/102713895-9696cb00-430e-11eb-9466-34b7e8fe031c.png)
- 내부 미세먼지를 1번으로 하여 TEXT LCD 첫 번째 줄에 출력에 성공
- 외부 미세먼지를 2번으로 하여 TEXT LCD 두 번째 줄에 출력에 성공
- 미세먼지 농도에 따른 창문 및 환풍기 동작을 성공
