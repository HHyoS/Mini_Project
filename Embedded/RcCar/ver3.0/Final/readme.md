ver2 대비 변경사항


ver2 

구성 : rc카 ( RPi 4 + Motor Hat )

동작 : 키보드를 통한 이동

통신 : MobaXterm 을 사용하여 RPi 4를 직접 조작

ver 3

구성 : 
  본체 : ver2 Rc카
  
  센서 및 장치 : 
      Pi Camera v2, 초음파 센서, 부저
     
  통신 : Rc카 본체 < - > Aws DB Server < - > PyQt
         Pyqt에서 Ui를 통해 동작을 입력하면 Aws DB서버로 명령어가 전달되고, 해당 명령어를 RC카 본체에서 읽어 동작을 수행
         
  동작 : Aws DB서버를 통한 수동조작 + Open Cv 를 사용한 Line Trace 자율주행
  
        자율주행 중 초음파센서에 설정한 값 이상으로 물체가 가까이 붙으면 주행을 정지하며 부저를 울리고, 수동조작으로 변경
        
        수동 조작 중 초음파 센서에 물체가 다가오면 부저만 울리고 차는 정지하지 않음
        
        


https://user-images.githubusercontent.com/57944215/204087921-69a872ee-ab2f-4c1e-894c-7f36dc149400.mp4



RC카 항공샷 

![KakaoTalk_20221124_181054249](https://user-images.githubusercontent.com/57944215/203786095-228f7710-0fbd-413a-ba61-04f8da8adb00.jpg)


RC카 정면샷

![KakaoTalk_20221124_181054249_01](https://user-images.githubusercontent.com/57944215/203786114-68ed40ff-3e32-41c9-9334-d4a2ab8fd95b.jpg)

프로젝트 완성기념 한컷

![KakaoTalk_20221124_181054249_02](https://user-images.githubusercontent.com/57944215/203786147-4e29c784-d11e-4c83-8dee-07745fa5c909.jpg)



----------------------------------------------------------------------------------------------------------------------------------------------------------------

23.01.23 App.py 코드 리팩토링

##객체지향에 대해 공부하던 중 구현했었던 LineTracing RC카 코드를 객체지향적으로 수정 가능할 것이라고 생각되어 리팩토링 진행

변경사항

    1. 전역 함수와 전역변수로 선언하고 사용하던 Motor Driver와 센서의 동작을 Car 클래스와 LineTracing 클래스 객체지향적으로 수정
    2. Car 클래스는 기본적인 주행기능을 담당, LineTracing 클래스는 Car 클래스를 상속받고 센서와 LineTracing 주행기능을 담당
    3. 전역 변수로 사용하던 변수들을 클래스의 내부의 변수로 사용하고, 사용할 때 Get().. Change() 함수를 사용하여 접근하도록 하여 직접접근
    4. DB에만 사용하는 함수와 변수를 담는 DB클래스를 생성하여 객체로 사용하도록 수정
