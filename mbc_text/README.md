# MBC Academy LMS Program

Python(Flask) · MySQL · 웹개발 설계 평가시험용 프로그램입니다.
회원(일반/관리자) 권한에 따라 기능이 분리하여 설계했습니다.

---

## 메인 화면
![메인화면](docs/main.png)

---

# 회원 프론트 구현

## 로그인
![로그인](docs/login.png)

## 회원가입
![회원가입](docs/join.png)

## 마이페이지
![마이페이지](docs/mypage.png)

## 회원수정
![회원수정](docs/edit.png)

---
# 관리자 페이지 프론트 구현

## 관리자 대시보드
![대시보드](docs/dashboard.png)

## 회원목록리스트 화면
![회원목록 리스트](docs/list.png)

## 회원검색 화면
![회원목록 리스트](docs/search.png)

## 회원상세보 화면
![회원목록 리스트](docs/details.png)

---

# MYSQL DB 생성 및 테이블 코드 
## DB 생성 
```
/*DB를 새로 생성한다.*/
CREATE DATABASE mbc_text 
DEFAULT CHARACTER SET utf8mb4 
/*utf8mb4 | 한글, 특수문자, 이모지까지 완전 지원*/
COLLATE utf8mb4_general_ci;
/*COLLATE | 문자열 정렬/비교 방식 지정 // general_ci | 대소문자 구분 없이 비교*/


SHOW DATABASES; /*DB 리스트 조회*/
USE mbc_text; /*mbc DB 사용*/

/*사용자 계정 생성 및 권한 부여*/
CREATE USER 'text'@'192.168.0.%' IDENTIFIED BY '1234';
/*			 ID    접속권한 PC                    pc*/

GRANT ALL PRIVILEGES ON mbc_text.* TO 'text'@'192.168.0.%';
/*권한 부여   모든권한      DB명  모든테이블ID@접속권한*/
FLUSH PRIVILEGES; 
/*즉시권한적용*/
```
## MEMBERS 테이블 생성
```
USE mbc_text;

-- 1) MEMBERS (회원)
-- ---------------------------------------
CREATE TABLE members (
  id INT AUTO_INCREMENT PRIMARY KEY,

  -- 로그인
  uid VARCHAR(50) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,

  -- 기본정보
  name VARCHAR(50) NOT NULL,
  phone VARCHAR(20) NOT NULL,
  email VARCHAR(120) NOT NULL UNIQUE,
  address VARCHAR(255) NOT NULL,
  profile_img VARCHAR(255) NULL,
  role ENUM('USER','ADMIN') NOT NULL DEFAULT 'USER',
  active BOOLEAN DEFAULT TRUE,
  created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP);
  
  ```

