# Cardoc-api

## 1. 배경 및 공통 요구사항

<aside>
😁 **카닥에서 실제로 사용하는 프레임워크를 토대로 타이어 API를 설계 및 구현합니다.**

</aside>

- 데이터베이스 환경은 별도로 제공하지 않습니다.
 **RDB중 원하는 방식을 선택**하면 되며, sqlite3 같은 별도의 설치없이 이용 가능한 in-memory DB도 좋으며, 가능하다면 Docker로 준비하셔도 됩니다.
- 단, 결과 제출 시 README.md 파일에 실행 방법을 완벽히 서술하여 DB를 포함하여 전체적인 서버를 구동하는데 문제없도록 해야합니다.
- 데이터베이스 관련처리는 raw query가 아닌 **ORM을 이용하여 구현**합니다.
- Response Codes API를 성공적으로 호출할 경우 200번 코드를 반환하고, 그 외의 경우에는 아래의 코드로 반환합니다.

[Copy of Code](https://www.notion.so/08e67c3cdc8e471fb1aab50e5963fb05)

---

## 2. 사용자 생성 API

🎁 **요구사항**

- ID/Password로 사용자를 생성하는 API.
- 인증 토큰을 발급하고 이후의 API는 인증된 사용자만 호출할 수 있다.

```jsx
/* Request Body 예제 */

 { "id": "candycandy", "password": "ASdfdsf3232@" }
```

---

## 3. 사용자가 소유한 타이어 정보를 저장하는 API

🎁 **요구사항**

- 자동차 차종 ID(trimID)를 이용하여 사용자가 소유한 자동차 정보를 저장한다.
- 한 번에 최대 5명까지의 사용자에 대한 요청을 받을 수 있도록 해야한다. 즉 사용자 정보와 trimId 5쌍을 요청데이터로 하여금 API를 호출할 수 있다는 의미이다.

```jsx
/* Request Body 예제 */
[
  {
    "id": "candycandy",
    "trimId": 5000
  },
  {
    "id": "mylovewolkswagen",
    "trimId": 9000
  },
  {
    "id": "bmwwow",
    "trimId": 11000
  },
  {
    "id": "dreamcar",
    "trimId": 15000
  }
]
```

🔍 **상세구현 가이드**

- 자동차 정보 조회 API의 사용은 아래와 같이 5000, 9000부분에 trimId를 넘겨서 조회할 수 있다.  
 **자동차 정보 조회 API 사용 예제 →**  
  [https://dev.mycar.cardoc.co.kr/v1/trim/5000](https://dev.mycar.cardoc.co.kr/v1/trim/5000)  
 [https://dev.mycar.cardoc.co.kr/v1/trim/9000](https://dev.mycar.cardoc.co.kr/v1/trim/9000)  
    [https://dev.mycar.cardoc.co.kr/v1/trim/11000](https://dev.mycar.cardoc.co.kr/v1/trim/11000)  
  [https://dev.mycar.cardoc.co.kr/v1/trim/15000](https://dev.mycar.cardoc.co.kr/v1/trim/15000)
- 조회된 정보에서 타이어 정보는 spec → driving → frontTire/rearTire 에서 찾을 수 있다.
- 타이어 정보는 205/75R18의 포맷이 정상이다. 205는 타이어 폭을 의미하고 75R은 편평비, 그리고 마지막 18은 휠사이즈로써 {폭}/{편평비}R{18}과 같은 구조이다.
 위와 같은 형식의 데이터일 경우만 DB에 항목별로 나누어 서로다른 Column에 저장하도록 한다.

---

## 4. 사용자가 소유한 타이어 정보 조회 API

🎁 **요구사항**

- 사용자 ID를 통해서 2번 API에서 저장한 타이어 정보를 조회할 수 있어야 한다.

---
# 구현 내용
1. 배포주소:
http://118.67.143.107/  
 2. 테스트가능 주소:
http://118.67.143.107/docs
    

# 서버 구조 및 디자인 패턴에 대한 개략적인 설명

api/service/sql_app으로 레이어를 나누었습니다.
api에는 직접적인 request를 받고, response를 하는 역할을 하고
service에서는 비즈니스 로직을
sql_app에서는 db와 소통하는 역할을 맡고 있습니다.


# 구현방법
타이어 정보 저장 api의 경우,
차 정보를 수집하는 외부 api에 의존하고 있으므로, 비동기 방식으로 처리하였습니다.


# 실행방법
```shell
git clone https://github.com/Heon4856/Cardoc-api.git
```

```shell
# 루트 디렉토리에 env.py 파일안에 다음과 같은 내용 추가.
SECRET_KEY = "시크릿키"
ALGORITHM = "JWT 알고리즘 종류"
ACCESS_TOKEN_EXPIRE_MINUTES = 시간, int타입으로
```

```shell
pip install -r requirements.txt
```

```shell
uvicorn main:app --host=0.0.0.0 --port=8000
```

localhost:8000에서 확인가능 합니다.


# 레퍼런스
이 프로젝트는 원티드x위코드 백엔드 프리온보딩 과제 일환으로 카닥에서 출제한 과제를 기반으로 만들었습니다.
