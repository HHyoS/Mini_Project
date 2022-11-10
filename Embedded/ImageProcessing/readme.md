개발 환경 : 
  window - pycham
  Raspberry Pi OS - Thonny Python IDE

장비 : Raspberry pi 4 [라즈베리파이 본체] + Raspberry Pi Camera Module 2

라이브러리 : PySide2 + cv2

설계 : 

  UI : PySide2 Designer를 사용하여 UI를 구성
  
  기능 : 사용자의 시작버튼 clicked가 감지되면 화면에 카메라에서 들어오는 이미지를 바탕으로 이미지 프로세싱이 완료된 화면표시
    1) 카메라에 찍힌 원본화면 표시
    2) Canny 알고리즘을 이용하여 이미지의 테두리를 프로세싱하여 화면에 표시
    3) 흑백화면
    4) 뿌연화면
    
    
    
진행 사항 :

    22-11-10 : 원본화면과 Canny 알고리즘으로 프로세싱된 화면표시 성공 / 흑백화면, 
    
