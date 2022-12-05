
• 백엔드
  - AWS를 사용한 Ubuntu 환경의 서버
• 프론트엔드
  - Vue.js 활용

프로젝트 명세서

개요 : AWS 기반 웹 프로젝트

DB 서버 : 3306 포트

Backend 서버 : 8080 포트

Frontend 서버 : 80포트 (Nginx)

API 명세서 - menus

- menus
    - GET /api/menus
        - 메뉴 전체 조회
        - GET /api/menus
            - 메뉴 일부 조회
    - Post /api/menus
        - 메뉴 등록
    - PATCH /api/menus/:id
        - 메뉴 수정
    - POST /api/menus/:id/image
        - 메뉴 이미지 수정
    - DELETE /api/menus/:id
        - 메뉴 삭제

API 명세서 - orders

- orders
    - GET /api/orders
        - 주문 전체 조회
    - GET /api/orders/:id
        - 주문 내역 조회
    - POST /api/orders
        - 주문 하기
    - PATCH /api/orders/:id
        - 주문 수정하기
    - DELETE /api/orders/:id
        - 주문 삭제하기

라우터 설계

메뉴 ( 관리자만 설정 가능)

/admin/menus

 메뉴 전체 조회(api.menus.findAll)

/admin/menus/register

메뉴 등록

/admin/menus/register/:id

메뉴 수정

id에 해당하는 메뉴를 수정

/admin/menus/:id

메뉴 상세 조회

주문

/orders

주문 전체 조회

/orders/register

주문 등록

/orders/register/:id

주문 수정

/orders/:id

주문 상세조회


메인 화면

![메인](https://user-images.githubusercontent.com/57944215/205580018-7959369f-8768-425a-b362-327e0ded7a77.GIF)

관리자 페이지

![관리자페이지](https://user-images.githubusercontent.com/57944215/205580042-67045ec2-fe86-43be-a434-f35e6ef64a3a.GIF)

주문 목록

![주문 목록](https://user-images.githubusercontent.com/57944215/205580197-63a3423f-781b-4844-800e-14f38d12c8c1.GIF)

메뉴 목록/수정(메뉴 클릭 시 수정화면 존재)

![메뉴목록](https://user-images.githubusercontent.com/57944215/205580103-101d5bde-2a51-47ce-8dd5-2ba3441eb757.GIF)

메뉴 추가

![메뉴추가](https://user-images.githubusercontent.com/57944215/205580112-29f6330f-c649-4023-a8ad-2871bddc2716.GIF)

