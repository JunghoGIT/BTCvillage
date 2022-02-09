# BTC village



## 개요



### 비트코인 실시간 가격 정보와 모의 투자 서비스



![사용예시](\사용예시.gif)



[http://btc-village.com/](http://btc-village.com/)



### 개발 인원 : 1명



### 사용 기술 스택



- Front
  - HTML, CSS, javascript
  - jquery, ajax
  - bootstrap
- back
  - python
  - Django
  - AWS rds (Mysql)
- Devops 
  - Nginx
  - uwsgi
  - Github
  - AWS EC2(ubuntu)



## 상세 개발 내용





- django FBV 방식으로 모의 투자, 게시판 서비스 구현
- 비동기 방식으로 open api 사용
- django serializer를 사용하여 queryset을 json 직렬화 하는 api 설계
- python 스크립트 파일을 django 프로젝트에 추가, 백그라운드로 실행하여 data 수집 및 모의 투자 주문 체결 관리
- AWS EC2 (ubuntu)를 사용하여 iaas 모델로 배포
- AWS rds (Mysql) DB 사용
- Nginx와 uwsgi로 서버 구축
