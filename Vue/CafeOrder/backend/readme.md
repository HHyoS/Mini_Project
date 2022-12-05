주문관리 웹앱 BackEnd 구현 코드입니다.


서버 : AWS Ubuntu에서 Node 사용

Database : mysql


환경 세팅 :

1. AWS 접속
2. sudo apt update
3. sudo apt install mysql-server
    - mysql —version 으로 버전확인
4. sudo mysql
5. ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password by 'mynewpassword';
6. exit
7. sudo mysql_secure_installation
8. 비밀번호 입력 - mynewpassword 
9. 순서대로 - n n y y y y
10. mysql -u root -p
11. mynewpassword 입력
12. CREATE USER ‘유저이름’@’localhost’ IDENTIFIED BY ‘비밀번호’;
    
    ex) CREATE USER ‘test’@’localhost’ IDENTIFIED BY ‘ttest’;
    
13. GRANT ALL PRIVILEGES ON *.* TO '유저이름'@'localhost';
14. CREATE USER '유저이름'@'%' IDENTIFIED BY '비밀번호';
15. GRANT ALL PRIVILEGES ON * .* TO '유저이름'@'%';
16. FLUSH PRIVILEGES;
17.  exit 입력 → 로그인하기 시작
18.   mysql -u 유저아이디 -p
    
    ex) mysql -u test -p
    
19. 비밀번호 입력
    
    ex) ttest    엔터
    
20. CREATE DATABASE DB이름 CHARACTER SET utf8 COLLATE utf8_general_ci;
21. SHOW DATABASES; → 데이터베이스 확인
22. USE DB이름;
23. DB에 데이터넣기

CREATE TABLE `menus` (
`menu_id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
`menu_name` VARCHAR(20) NOT NULL,
`menu_description` TEXT NOT NULL,
`menu_img_link` TEXT NOT NULL
) default character set utf8 collate utf8_general_ci;

INSERT INTO `menus`
(`menu_name`, `menu_description`, `menu_img_link`)
VALUES
("아이스 아메리카노", "여름엔 아아가 진리", "/menus/ice-americano.jpg");

INSERT INTO `menus`
(`menu_name`, `menu_description`, `menu_img_link`)
VALUES
("카페라떼", "Latte is horse", "/menus/cafe-latte.jpg");

INSERT INTO `menus`
(`menu_name`, `menu_description`, `menu_img_link`)
VALUES
("복숭아 아이스티", "내 입안 복숭아향 가득", "/menus/peach-icetea.jpg");

1. SELECT * FROM menus; → 데이터베이스 데이터 확인
2. sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf
3. bind-address 127.0.0.1을 0.0.0.0 으로 수정
4. 컨트롤 + o  → 엔터 로 저장 → 컨트롤 + x 로 파일종료 
5. sudo service mysql restart

------------------------------------------------------------------------------------------------------------------------------------------------------------------

환경 설정 이후 sudo node index.js 로 BackEnd 

