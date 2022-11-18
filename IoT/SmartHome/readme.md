개발 목표 : 배운 iot 지식을 바탕으로 나만의 작은 Smart Home 구축해보기

개발 장비 : 
  1) 개발 보드 : Raspberry Pi 4 
  2) MCU : ESP32
  3) 시각화 도구 : Node-red
  4) IoT 서버 : AWS
  5) 통신 : Mosquitto( MQTT )
 
개발 프로세스 :

![image](https://user-images.githubusercontent.com/57944215/202660351-6b9c2818-9f22-4bbd-b2d1-be9ac8b17636.png)

이 개발에서 Smart Home 구축을 위해 다음과 같은 프로세스로 개발을 진행하였습니다.

1) Node Device(ESP32)들 과 중간 다리 역할의 게이트웨이 디바이스(Raspberry Pi 4) 그리고 AWS 까지 세단계의 IoT를 구성
2) MQTT 로 통신하여 게이트웨이로 전송하고, 그 정보를 AWS로 로깅하였습니다.
3) AWS에서는 말단 디바이스들에서 들어온 정보를 받아 외부에서도 확인할 수 있도록 하였습니다.

회로 구성

![image](https://user-images.githubusercontent.com/57944215/202661394-34218454-7f11-419d-9688-d60c4e6adec5.png)

Node-red 구성

![image](https://user-images.githubusercontent.com/57944215/202661722-3ef68b62-ad04-4b5a-8112-daeb580470ce.png)

Node-red로 구성한 Ui

![image](https://user-images.githubusercontent.com/57944215/202661836-63bb8286-f9ab-4edd-bca5-9a33b41f4738.png)

동작

1. 버튼을 눌렀을 때, led on 및 AWS로 데이터 전송

![image](https://user-images.githubusercontent.com/57944215/202662067-92110f40-8483-4806-a63a-1dc03e13a580.png)

![image](https://user-images.githubusercontent.com/57944215/202662149-4b49b025-2682-4976-a178-a57fb7cbccd6.png)

2. Node-red Ui로 led 동작 및 데이터 전송

![rn_image_picker_lib_temp_d3d37103-eedb-4ac3-9fe7-ce2a8c2cc607](https://user-images.githubusercontent.com/57944215/202662321-f4e4c23b-af91-42e4-a4df-c9d48d234f51.jpg)

3. 온.습도 센서 감지로 그래프 표현

![rn_image_picker_lib_temp_b8ea64cc-1979-4912-a475-97e03b1efcc7](https://user-images.githubusercontent.com/57944215/202662546-9e9ae0d8-9fd4-4632-9fc3-5005d9415d5a.jpg)

4. AWS 데이터 로깅 확인

![image](https://user-images.githubusercontent.com/57944215/202662767-48b53d80-9eed-4371-a7a8-0864f6b28fda.png)






