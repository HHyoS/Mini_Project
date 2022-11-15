저장 DB : FireBase

사용 보드 : ESP32-s

사용 IDE : Arduino IDE

IDE 옵션 : 

    1. Board -> Node32s
    
    2. 스케치 - 라이브러리 포함하기 - 라이브러리 관리, "Firebase ESP32 Client"
    
    3. 에러발생 폴더 제거
    
![캡처](https://user-images.githubusercontent.com/57944215/201855922-c05b4ca6-a57d-4222-acf7-c4f81482663f.PNG)


구현 내용 :

    DHT11 센서 데이터와 FireBase Db를 연결하여 Json 타입으로 현재 온도,습도 측정 데이터를 전송하기
    
    
    
 
 
전송 데이터 : 
    
![전송 데이터](https://user-images.githubusercontent.com/57944215/201854526-c4c43200-cc71-4977-8bb6-27b360cd6656.PNG)


전송 받은 데이터 :

![전송받은 데이터](https://user-images.githubusercontent.com/57944215/201854558-3e281390-cd40-4fa3-90bc-e9db8050fd08.PNG)

회로 사진

![rn_image_picker_lib_temp_8382f4b9-ab6f-4627-b21e-e6fb97125ec3](https://user-images.githubusercontent.com/57944215/201854688-3d6eec51-202d-4cda-b9ae-de4bc01c68dc.jpg)
