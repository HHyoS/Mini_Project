[ 프로그램 개발 동기 ]

최근 대선, 코로나, 우크라이나 전쟁 등 다양한 이슈가 발생하고 있는데, 네이버에 실시간 검색어가 막히면서 최근에 어떤 이슈가 많이 발생하고 있는지 시각화해서 보여주면 좋겠다 락 생각 하였습니다.

지금까지 익힌 vue.js와 웹관련 기술, 그리고 네이버 디벨로퍼(https://developers.naver.com/main/) 의 	데이터랩 (검색어트렌드) api를 사용하면 특정 검색어를 기준으로 연관 검색를 묶을 수 있고, 그를 통해 시각적으로 표현하는 저만의 실시간 검색순위를 만들기로 했습니다.

[ 기술 스택 ]

FrontEnd :  Vue.js

BackEnd :  express(Node.js)

개발환경 : Visual studio code


[ 개발 설계 ]

1. naver datalab api 를 활용해서 data 를 시각화한다.
  A. API 서버 구축하기
    i. express 서버에서 naver datalab api 를 가져온다.
    ii. api 를 axios 로 가져와서 리턴해주는 프로젝트를 생성한다.
  B. Vue.js 로 visualizing
    i. axios 로 express 단에 요청을 보낸다.
    ii. 응답 값을 chart 화 시킨다.(https://www.chartjs.org/ 의 charjs를 사용하여)
    


    


