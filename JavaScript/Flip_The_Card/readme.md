# [Web] 카드 뒤집기 게임 설계

작성일시: 2022년 8월 10일 오전 10:51

카드 뒤집기 게임 설계

 0. 뒤집혀진 카드에서 같은 모양을 갖는 쌍을 모두 맞추어 모든 카드 쌍을 완성키시는 게임.

1. HTML 각각을, 하드코딩. 그리드 사용
2. 각각의 영역을 div 로 잡아서 onclick 부여 (파라미터 받기)
3. 12개의 배열안에 객체, 
4. cardArray 만듦

```jsx
{
name: String, 카드에 들어갈 동물 이름.
나중에 이걸로 맞췄는지 판단.
img: String, 이미지의 경로,
id: String, DOM 에 부여될 아이디. ex) 1-4
done: Boolean, 맞췄는지 판단
}
```

---

## 사용 변수

| 변수명 | 타입 | 역할 |
| --- | --- | --- |
| gameDOM | Array | 파싱한 돔 정보를 gameDOM 빈 배열에 집어넣음: querySelectorAll |
| clickCount | Number | 처음엔 0 클릭 횟수. <br>2회가 되면 뒤집은 카드가 같은 카드인지 확인 후, 같을 경우cardArray의 done 속성을 true로 바꿈.<br> 아닐경우 다시 ? 모양 카드로 뒤집기 |
| clickFirst | Number | 처음엔 -1<br>첫번째 클릭 위치 |
| clickSecond  | Number | 처음엔 -1<br>두번째 클릭 위치 |

---

## 사용 함수

| 함수명 | 동작 |
| --- | --- |
| getGameDOM() | DOM 정보를 미리 파싱,<br>(열 두개의 DOM 정보를 모두) |
| setIDtoCardArray() | cardArray 에 DOM 위치에 알맞는 id 부여(랜덤 위치 만들기) |
| createBoard() | 물음표로 가득 찬 게임판 생성 |
| flip() | 1.뒤집기. done 이 true 일 때는 실행 안됨.<br>2. setClickHistory(location) 실행해서 첫번째 클릭인지 두번째 클릭인지 판단<br>3. 물음표를 그림으로 뒤집음<br>4. 만약, 클릭카운트가 2이면, isCorrect() 실행해서 맞았는지 틀렸는지 판단<br>5. 이후, clickFirst, clickSecond 둘 다 -1 로 초기화 |
| setClickHistory(location) | 첫번째 클릭인지 두번째 클릭인지 판단해 클릭 데이터 저장<br>즉, 0, 1, 2, 3, ... 11 이 들어감. |
| isCorrect() | 1. 일치하는지 판별<br>2. 만약 클릭했던 두 개의 그림이 일치하면 done 을 true 로 바꿔서<br>3. flip 이 작동 안되게 처리<br>4. 두 개의 그림이 일치하면backFlip() 실행 |
| backFlip()  | backFlip() 틀렸을 때 다시 뒤집음. 0.5초 딜레이 줌. |

----------------------------------------------------------------------------------------------------------------------------------------------------------------------
22.08.12 버전 1 개발완료!
( 추가 예정 기능 - 1.점수 기능, 2. 사진들이 현재는 하드코딩 되어있는데, 판의 크기에 따라 사진의 크기조절 되도록 하기 )

초기 화면

![image](https://user-images.githubusercontent.com/57944215/184265999-486a282b-a046-4e4b-a583-3b69b0d8f6dd.png)



게임 진행 중 화면

![image](https://user-images.githubusercontent.com/57944215/184266057-b87fb5fe-b19d-42be-a68c-d7a9be25bf9d.png)

같은 사진을 찾아낸 강아지 사진은 유지되고, 한 번 클릭한 상태인 악어사진은 보이는중,

![image](https://user-images.githubusercontent.com/57944215/184266162-342d0bbd-31df-4fa2-9707-62ca06c3cf49.png)

다른 사진을 고른 현재의 상태에서는

![image](https://user-images.githubusercontent.com/57944215/184266213-d11fe62a-2257-41bb-83fe-832ff75fc2de.png)

다시 원래대로 돌아옴

--------------------------------------------------------------------------------------------------------------------------------------------------------------------

2022-08-13 카드 뒤집기ver 2.0 

추가된 기능 :

    1. 사용자가 UX 개선을 위해 게임창의 위치를 화면 정중앙에 배치
    2. 게임 판의 사이즈 증가 및 이후 게임판 크기 조절시 자동으로 이미지 사이즈가 조절 되도록 코드 구현
    3. 게임의 느낌을 살리기 위해 같은 쌍 선택시 +5, 실패시 -3점의 점수 할당
    4. 게임 종료 후 얻은 점수 alet 메세지로 사용자에게 보여줌
    


개선 후 이미지

(1) 게임판 위치 조정 및 (2) 게임판의 크기 조절

![image](https://user-images.githubusercontent.com/57944215/184493889-1c34878b-9fd2-4f67-b9b8-3eba11f5034c.png)

(3) 카드 맞추기 점수 배정

 1] 카드 쌍을 못맞추고 3번 실패시 ( -3점 * 3 = -9점)
 
 ![image](https://user-images.githubusercontent.com/57944215/184494060-451b7abc-c630-42db-b056-40bb448c4594.png)


 2] 3번 실패후 한번 성공시 ( -9 + 5 = 4점)
 
 ![image](https://user-images.githubusercontent.com/57944215/184494008-ff365c20-4af9-4cde-8d82-e107452ee7f7.png)


(4) 게임 종료 후 점수 표시

![image](https://user-images.githubusercontent.com/57944215/184493967-21943d08-6abe-4ba2-b2b3-78afdc39e2d8.png)



