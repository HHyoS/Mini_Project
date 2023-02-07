[ 설 계 ]

[ 개 요 ] 

임베디드 분야에서 직접 접근해야하는 메모리에 대한 이해는 필수적입니다.

우리가 사용하는 SSD의 동작을 분석해서, SSD에 대한 이해를 높히고 S/W적으로 구현해보고, 검증하는 쉘 프로그램을 통해

향후 취업하게 될지도 모르는 SSD에 대한 이해와 개발역량을  

[ 프로젝트 기간 ]

22.09.30 ~ 22.10.04

[ 프로젝트 인원 ]

1인 프로젝트

[ 프로젝트 구성 ] 

1. 가상 SSD 제작
    - HW 를 Software 로 구현한다
2. Test Shell Application 만들기
    - 테스트 프로그램
3. Test Script 작성하기
    - 테스트 프로그램 內 Test Code

[ Detail ]

1. SSD는 물리적인 저장장치이지만, SW적으로 구현하는 프로젝트로 설계할 예정.
2. SSD 는 파일 입출력을 통해서 간단하게 구현
3. Read/Write 기능 구현을 통해 SSD 테스트 가능

[ 필요 지식 ]

SSD 

- 저장할 수 있는 최소 공간의 사이즈는 4KB
( 한 글자 = 약 1 Byte 으로 간주했을 때 , 4,096 글자 저장 가능 공간
- 각 공간마다 LBA (Logical Block Address) 라는 주소를 가짐
- SSD 는 OS 로부터 Read / Write / Unmap 등 다양한 명령어를
전달받는다

[ 가상 SSD 스펙 ]

- Read 명령어와 Write 명령어만 존재
- LBA 단위는 4 Byte
- ( 실제로는 4KB 이지만 , 우리가 만들 최소 저장공간 사이즈는 4 Byte)
- LBA 0 ~ 99 까지 100 칸을 저장할 수 있다
- 총 400 Byte 를 저장 할 수 있는 가상 SSD 를 구현

[ 세부 규정 ]

데이터 범위

- LBA : 0 ~ 99, 10 진수
- 값 : 항상 0x 가 붙으며 10 글자로 표기한다 . ( 0x00000000 ~ 0xFFFFFFFF

Read 명령어

- ssd R [LBA]
- result.txt 에 읽은 값이 적힌다 . 기존 데이터는 사라진다
- 한번도 안적은 곳은 0x00000000 으로 읽힌다.

Write 명령어

- ssd W [LBA] [ 값]
- nand.txt 에 저장한 값이 기록된다

----------------------------------------------------------------------------------------------

 [ 정 리 ]
 
 구현해야 할 프로그램
 1) 가상 SSD
  LBA size : 4Byte ( 값은 항상 10글자로 표현 ex) 0x00000000 ~ 0xFFFFFFFF )
  총 100개의 LBA ( 0 ~ 99 )
 -> 사용할 명령어 : Write / Read
  가상 ssd 프로그램 이름 : ssd
 
 사용 가능한 명령어
   - Write : >>ssd W 주소 값 
   모니터에 출력안됨 -> nand.txt 에 저장됩니다.
   
   - Read : >> ssd R 주소
   모니터에 출력 안됨 -> result.txt 에 read한 결과 저장 ( 1줄만 표시, over write )
   기존에 저장된 값이 없으면 0x00000000

 2) Test Shell Application
  테스트 프로그램
  사용가능 명령어
   write     : write 3 0xAAAABBBB -> ssd에 명령어를 전달한다
   read      : read 3 -> ssd에 명령어를 전달한다, result.txt의 값을 화면에 출력
   exit       : shell 종료
   help      : 명령어 "사용 방법" 출력
   fullwrite : fullwrite 0xABCDASDA -> LBA 0~99 전체에 값 저장
   fullread : fullread -> LBA 0~99 전체의 값 화면에 출력

 3) Test Script
  TestApp1 : Test Shell 에서 "testapp1" 명령어 입력 시 동작
          -1 fullwrite
          -2 fullread
  TestApp2 : Test Shell 에서 "testapp2" 명령어 입력 시 동작
          -1 0~5 LBA에 0xAAAABBBB 값 총 30번 write
          -2 0~5 LBA에 0x12345678 1회 OverWrite
          -3 0~5 LBA read : 0x12345678 나옴 

유의사항
 1) 매개변수 유효성 검사 수행 : format, LBA 0~99, 0~F 숫자 범위만 허용
 2) 없는 명령어일 경우, "INVALID COMMAND" 출력, segment fault 나오면 안됨
 
 -----------------------------------------------------------------------------------------------------------------------------------------
 
 22 10 01 변경 사항

SSD와 Test Shell 코드분리

SSD의 동작은 Write와 Read뿐, Test Shell에서 입력값에 따라 SSD에 system 명령어를 통해 기능 구현

개선 사항

Test Shell의 코드의 기능 별 코드분리 예정

-------------------------------------------------------------------------------------------------------------------------------------------------------

22.09.30 ~ 22.10.04 완성!

[ 완성본..? ]

프로그램 구성

[Test shell]

  목적 : 가상 ssd를 테스트하는 Test shell
  
  기능 : 
    (1) read IDX : read IDX 명령어를 ssd에 전달 
    (2) fullread : 가상 SSD의 값을 읽어 저장된 모든 값을들 화면에 표시
    (3) write IDX Address : write IDX Address 명령어를 ssd에 전달
    (4) fullwrite Address : 가상 SSD에 모든 위치에 Address값을 저장하도록 명령어 전달
    (5) help : Test Shell의 간략한 명령어 사용법 출력
    (6) test FileName : FileName으로 입력된 테스트 파일을 읽어 SSD테스트 실행
    (7) exit : shell 종료
    --------------------------------------------------------
    * 명령어는 read, fullread, write, fullwrite, help, test, exit
      입력값은 IDX, Address, FileName
 
  파일 구성 :
    shell.c verification.c verification.h run.c run.h
    
  기능 별 출력 :
    (1) read IDX : result.txt 파일 출력
    (2) fullread : 화면 출력
    (3) write IDX Address : nand.txt에 값 작성
    (4) fullwrite Address : nand.txt에 값 작성
    (5) help : 화면 출력
    (6) test FileName : 입력된 파일 내용을 바탕으로 위의 (1) ~ (5) 기능 실행
    (7) exit : program exit! 라는 화면출력후 shell 종료
  
  
소스코드 파일 별 역할 :
  1) shell.c
    shell의 입력을 다른 함수로 전달하는 코드, 입력받은 값을 바탕으로 Invaild() 함수를 실행하여
    정해진 입력값에 맞는 명령어인지 확인하고, 명령어를 SSD에 전달 or 실행하는 역할
  2) verification.c
    Invaild 함수가 존재하는 코드. 
    (1) nand.txt가 존재하는지 확인하고 없다면 생성 (2) 입력받은 값이 옳은 명령어인지 확인  
  3) test.c
    test 명령어를 입력받았을 경우 실행되는 코드. 입력받은 파일의 끝까지 탐색하며 명령어를 수행
    사용자의 입력에 따라 명령어를 생략하기도 함
  4) run.c
    test.c 에서 읽은 test파일의 내용을 실행시키는 코드. shell.c와 마찬가지로 명령어를 확인하고
    수행하는 역할
  5) ssd.c
    가상 SSD를 구현한 코드. (1) write (2) read 두가지 기능만 존재하며 
    가상 SSD는 nand.txt 파일을 통해서 구현.
    인덱스는 0 ~ 99 까지 총 100개, 100줄이 존재하며 
    write IDX Address 수행 시 nand.txt의 IDX번쨰 줄에 Address값을 입력
    read IDX 수행 시, nand.txt의 IDX번쨰 줄의 값을 읽어 result.txt 생성
    
[ 가상 SSD ]

  목적 : 물리적인 SSD가 아닌 가상 SSD를 구현하여 SSD 동작 테스트
  
  기능 :
    (1) read IDX : 입력받은 IDX값을 result.txt 로 출력
    (2) write IDX Address : IDX번째 위치에 Address 주소 작성

  파일 구성 :
    ssd.c
    
[ 실행 방법 ]
  실행 환경 : Ubuntu 20.04 권장(개발환경)
  필요 파일 : 
    공통파일 : MakeFile
    Test Shell : run.c run.h shell.c test.c verification.c verification.h
    가상 SSD : ssd.c
  출력 파일 :
    nand.txt result.txt
  
  실행 순서
    1) 필요한 파일들을 모두 다운 후 cmd 실행하여 다운받은 위치로 이동.
    2) make  입력
      -make 입력 시 run.o test.o verification.o ssd.o tShell ssd 파일 생성
    3) ./tShell 입력으로 쉘 실행
    4) 위에 명시된 명령어 실행
    5) exit 입력으로 프로그램 종료
    6) make clear 입력으로 2)에서 생성된 모든 파일 삭제
    
[ 실행 화면 ]

1. make 실행

![초기화면](https://user-images.githubusercontent.com/57944215/193822639-9fcb7515-37bd-419b-8857-4f183f781dd4.PNG)

2. help

![tshell_help](https://user-images.githubusercontent.com/57944215/193822929-f28ad1cb-edcd-4973-9d1c-4a82b672224d.PNG)

3. fullread

![fullread](https://user-images.githubusercontent.com/57944215/193822981-c96f7c67-8935-40f4-93d4-c1360ac206d0.PNG)

4. write 후 fullread

![write_fullread](https://user-images.githubusercontent.com/57944215/193823027-f6291b21-3f58-476a-9b4a-05d84427cfc2.PNG)

5. fullwrite 후 fullread

![fullwrite_fullread](https://user-images.githubusercontent.com/57944215/193823075-5ca397fc-1c0f-4596-893c-9bb4fe1944c6.PNG)

6. test 명령어로 test파일 실행

![test](https://user-images.githubusercontent.com/57944215/193823132-f6cfb9cc-d629-44e6-ab64-a07d2fd92d21.PNG)

7. exit 실행

![exit](https://user-images.githubusercontent.com/57944215/193823177-f36d04ba-7b71-4111-b8fe-76518aea2f88.PNG)

8. make clear 입력

![clear](https://user-images.githubusercontent.com/57944215/193823231-5e96075f-033e-4b31-85d3-1de1be9b8e0d.PNG)

--------------------------------------------------------------------------------------------------------

이상으로 가상 SSD 미니프로젝트 설명을 마치겠습니다.

만약 궁금한점이 있으시다면 gytkd33@naver.com 으로 메일 보내주시면 최대한 빠르게 답변해드릴 수 있도록

하겠습니다.
