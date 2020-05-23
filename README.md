# 아리슬레나 공리

## 서문

### 소개

 **아리슬레나(Arislena)**는 소규모(4명~10명 내외)의 유저가 자신만의 설정이 담긴 가상 국가를 세우고(설정은 밸런스에 영향을 미치지 않는다), 세력전, 외교, 상거래 등 컨텐츠를 통해 각자의 국가를 키워 나가는 공동 세계관 게임이다. **아리**는 아리슬레나 시스템 봇의 명칭이다.

### 상황

 2019년 말, **DRTN**을 중심으로 아리슬레나 제0시즌 개발을 시작했고, 2020년 1월 초에 제0시즌을 시작했다. 이후 2020년 1월 중순에 원작자 **DRTN**이 개발/운영에서 하차했다. **Freiyer**가 유지/보수/개발을 맡고 **Elna(Siadel)**가 디코방 운영을 맡아 2020년 2월경에 제0시즌을 마쳤다. 개발자 **Freiyer**는 아리의 코드에 한계가 많아 코드를 전면적으로 개선하려 하였지만, 시간적 여유 부족으로 인해 **Elna**가 개발을 시작하게 되었다.

 그리하여 2020년 3월부터 개발을 시작하였으나, **Elna**는 코딩을 처음부터 배워야 했으므로 작업 진척이 더뎠다. 개발 중간 약 3회의 전면적 내부 수정도 이뤄지면서 진척을 이루지 않았고, 결국 입대일인 5월 25일 이전에 개발을 완료하지 못했다.

### 따라서

 전체적인 관리자 업무 설명과, 당초 의도한 개발 방향을 설명하려고 한다.

### 효력

 코드와 설명이 서로 맞지 않는다면, 파일의 설명을 기준으로 한다.

# 디코방 운영

## 권한

 아리슬레나 디스코드 방에는 **관리자**, **개발자**, **서기**, **자문단**, **왕**이라는 권한이 존재한다. 서기와 자문단은 항상 왕을 겸하며, 개발자는 항상 관리자를 겸한다. 따라서 권한은 크게 **관리자 / 왕**으로 나뉜다. 권한을 디스코드 내에서 한 눈에 파악할 수 있게 디코방에서 **역할**을 배정해줘야 한다. 역할명과 권한명은 같다.

### 관리자

 관리자는 아리슬레나 디스코드 방의 운영을 총괄한다. 채널/카테고리 신설/유지/삭제, 게임 진행, 봇 실행/종료/유지/개발 등이 기본적인 업무다.

### 개발자

 개발자는 관리자와 권한 설정은 같으나, 주 업무가 봇과 관련한 자다. 관리자 부재 시 개발자가 관리자 일을 할 수 있다.

### 서기

 서기는 게임이 진행 중일 때 특수한 컨텐츠를 만드는 사람이다. (나라 관계도 만들기 등) 필수적인 역할은 아니다.

### 자문단

 자문단은 관리자/개발자와 협력해 게임을 이끌어나가는 사람이다. 게임 시스템에 대해 깊은 지식을 요한다. 베타 테스터 역할도 한다.

### 왕

 아리슬레나에 나라를 신청하여, 나라를 운영할 수 있는 사람이다.

### 모두 (일반)

 나라를 신청하지 않은 나머지 사람이다.

## 관리자의 주요 업무

1. 게임 운영
   정해진 시간에 `!새날`로 아리슬레나에 시간이 흐르게 해야 한다. 유저들이 전쟁/식민/지역 이름 변경 등 민원을 해오면 가능한 한 빠르게 대응해야 한다. (원칙적으로는 다음 `!새날`까지 처리하면 되지만, 편한 게임 환경 제공을 위해서다) 이외 업데이트/버그 수정 공지, 기타 공지 등 많지는 않으나 매일 1시간 정도는 투자해야 할 일이 생긴다. 일은 언제 생길지 모르니 여유 시간이 많은 사람이 하는 것이 좋다.
2. 디코방 운영
   인원 관리, 역할 관리, 홍보, 분탕/잠수 잡기 등 디코방 관리에 신경써야 한다. 이 부분은 유저 대부분이 (보기에) 온건한 편이므로 나름 안정적이다.
3. 꾸준한 규칙 성문화/엄밀화
   규칙을 완성도 있게 정리하는 것도 관리자의 몫이나, 시즌0 때와 그 이후에도 제대로 이행되지 않았다. 그러나 성문화/엄밀화를 진행한다면 비생산적인 유저/관리자 간의 게임 규칙 논쟁을 막을 수 있는 등 효과가 분명 존재한다.
4. 꾸준한 개발
   뭐든지 정지하면 더 이상 가치를 잃는 법이다. 끊임없이 개선점을 찾고 업데이트를 진행해야 한다.

## 자문단의 주요 업무

1. 개발 자문
   아리슬레나 개발 상황에 귀를 기울여야 하며, 전체적인 규칙을 상당히 깊게 숙지하고 있어야 한다. 적극적으로 의견을 내어 개발에 간접적으로 참여해야 한다. 시스템의 헛점을 밝혀내 보안 이슈를 만드는 것도 중요하다.
2. 신규 인원 교육, 분위기 조성
   꾸준한 접속을 통해 분위기를 조성하면 좋다. 또한 분쟁이 일어나지 않도록 관리해야 하며, 만약 분쟁이 일어나면 신속하고 정확하게 분쟁을 종료하고 유의미한 결론이 나도록 상황을 이끌어야 한다. 신규 인원이 들어오면 잘 적응할 수 있게 교육을 해주는 것도 꼭 필요하다.
3. 자문단은 반드시 왕 중에서 뽑는다.

## 서기의 주요 업무

1. 콘텐츠 제작, 역사 기록
   아리가 제공하는 것 외의 콘텐츠를 만들거나, 지나간 역사를 기록하는 일이 주된다. 가급적이면 콘텐츠는 매일 업데이트되는 것으로 하면 좋다.
2. 서기는 자문단을 반드시 겸직한다.

# 개발

## 개념

- **지역, 나라, 오너**

  아리슬레나는 자연의 물리 법칙 위에 세운 곳이 아니다.

  지역은 하나의 점으로 표현할 수 있다. 
  또, 지역은 아리슬레나에서 가장 기초적인 영토 단위다. 

  나라는 지역을 모은 집합이다. 
  모든 지역은 항상 어느 나라와 연관이 있어야 한다. 
  나라는 지역이 없어도 되지만, 지역은 나라가 없으면 안 된다.

  오너는 **지역 오너와 나라 오너**로 분리할 수 있다.
  **지역 오너**는 지역에 대한 권한이 있는 유저며,
  **나라 오너**는 나라에 대한 권한이 있는 유저다.
  한 나라 내에서 나라 오너와 지역 오너가 같은 게 일반적이지만, 다를 수도 있다.

  - **수도**

    나라를 만들 때 생성되는 지역이다. 

  - **식민, 식민지**

    식민은 한 나라가 다른 지역을 자신의 범위에 넣는 행위다. 이렇게 얻은 지역을 식민지라 한다. 식민지는 충성도에 따라 반란을 할 수 있다.

  - **편입, 편입지**

    편입은 한 원주민 나라가 유저 나라에게 자발적으로 식민되는 행위다. (조건을 충족하면 원주민 나라에서 요청을 한다.) 이렇게 얻은 지역을 편입지라 한다.

  - **병합, 병합지**

    병합은 식민지를 수도권에 편입하여 정치적 안정성을 꾀하는 행위다. 이렇게 얻은 지역을 병합지라 한다.

  - **추방**

    추방은 식민지나 병합지를 자신 나라에서 퇴출시켜 원주민으로 만드는 행위다.

  - **유저, 원주민**

    유저는 사람이며, 원주민은 아리슬레나의 NPC를 일컫는다.

    원주민은 유저보다 수치 스펙이 더 높다. 원주민이 유저만큼 전략을 짜지는 못하지만, 유저와 비슷한 AI를 만드는 것이 목표다. 예를 들면 유저가 원주민을 공격하면 해당 원주민이 해당 유저에게 반격하며, 해당 원주민과 교류하고 있는 원주민도 해당 유저를 공격할 수 있다. 원주민은 제한적으로 외교의 대상이 될 수 있다.

- 유형자원

  직접적인 스펙(국력)과 관련이 있는 스탯이다. **구매**, **판매**, **수출**할 수 있다.

  - **식량**

    식량 생산량, 저장량, 식량 관련 노하우 등 식량/자연과 관련한 스탯이다. 식량이 높을수록 풍요롭고, 낮을 수록 척박한 이미지다.

  - **자재**

    자원 생산량, 저장량, 공업력 등 지하자원과 관련한 스탯이다. 자재가 높을수록 도시적이고, 낮을수록 시골스러운 이미지다.

- 무형자원

  유형자원의 효율을 높이거나 외교/행정을 할 수 있게 해주거나 영토를 넓히는 유틸리티 스탯이다. **구매**, **판매**, **수출**할 수 없다. **승리**하는 데 중요한 역할을 한다.

  - **기술**

    자원 가공 기술, 인프라, 전쟁술 등 기술적인 것과 관련한 스탯이다. (문화와 비교해서) 기술이 높을수록 공격적이고 선제적인 이미지다. 유형자원 효율/양, HP/AP, 호전성 등에 보너스가 있지만, 외교가 약점이다.

  - **문화**

    법, 제도, 예술, 유흥, 사상 등 문화적인 것과 관련한 스탯이다. (기술과 비교해서) 문화가 높을수록 방어적이고 소극적인 이미지다. 외교, 정책, 유형자원 생산량 등에 보너스가 있다.
  
- 스탯 분류

  "자원"에는 식량, 자재, 기술, 문화를 대입할 수 있다.

  - **수도권, 수도권 자원**

    수도와 병합지를 수도권이라고 하고, 수도권 자원은 수도권의 자원에 대해 각각 총합을 매긴 것이다.

  - **나라 자원**

    나라(수도, 병합지, 식민지, 편입지)의 자원에 대해 각각 총합을 매긴 것이다.

  - **국제 자원**

    모든 지역의 자원에 대해 각각 총합을 매긴 것이다.

- 경제 관련

  - **자금**

    시작 시 10000을 지급받는다. 수도권 기술/문화에 따라 보유할 수 있는 최대 자금이 늘어나고, 최저 자금(음수)도 늘어난다. 빚 상환 등으로 인해 자금이 음수가 될 수 있는데, 이 음수 자금이 최저 자금 미만이 되면 지역을 매각해야 한다. 매각할 지역이 없으면 패배하고, 수도가 경매로 팔린다.

  - **대출**

    `!대출` 명령어로 급전을 마련할 수 있다. 수도권 기술, 문화 합에 따라 대출받을 수 있는 자금 규모가 늘어난다. 대출에는 대출액을 기준으로 한 단계(~5000, ~15000, ~45000)가 있으며, 각 단계마다 요구하는 수도권 기술, 문화 합, 

  - **빚**

    대출

  - **남은 상환 기간**

- 내정 관련

  - **투자 점수**
  - **정책 행동**
  - **충성도**

- 외교 관련

  - **호전성**
  - **호감도**

## 전체적인 파일 구조

 파일은 크게 **코드 파일**과 **데이터 파일**로 나뉜다. 코드 파일은 말 그대로 python 코드 파일이고, 데이터 파일은 json으로 각종 데이터를 담는다.

### 코드 파일

- **Ari_data.py**

  이 파일은 **기본 상수, 계산 공식, 데이터 파일 정의, 데이터 생성/삭제/수정, 데이터 검색, 데이터 카테고리화** 등 계산, 데이터와 관련한 모든 클래스와 함수가 들어 있는 파일이다. 사실상 아리의 전신이라고 할 수 있다. 이 파일에서 기본적인 작업을 완료한 후, **Ari_slena** 파일에서 그것을 절차에 따라 실행하거나 결과를 보기 좋게 embed(첨부물) 형식으로 디코방에 출력하는 게 의도한 개발 방향이다.

- **Ari_slena.py**

  아리의 본체가 되는 파일이다. 이 파일을 실행하면 봇이 켜진다. Ari_data와 후술할 Ari_msg를 모듈로서 import한다. **해당 파일에서만 쓰는 특수 함수, 오류 클래스, 명령어 클래스, 봇 실행부(@ari.event)**가 들어 있다.
  Ari_data는 `from Ari_data import *`로 import했기 때문에, `Ari_data.~~`처럼 클래스나 인스턴스를 참조하지 않는다.

- **Ari_msg.py**

 **Ari_slena에서 쓸 첨부물/일반 메세지**를 모아둔 파일이다. (Ari_slena의 명령어).(용도) 형식으로 이름을 정했으며, 그러한 형식이면 해당 str을 바로 가져올 수 있다.

### 데이터 파일

- **Token.json**

  토큰 정보를 저장한 파일이다. Ari_slena에서 봇의 토큰을 가져올 때만 쓰이며, 웬만해서는 내용을 바꿀 일이 없을 것이다.

- **system.json**

  시스템 정보를 저장하는 파일이다. 저장하는 정보는
  
  1. 식량 재고(food_stock)
  2. 자재 재고(matl_stock)
  3. 식량 가격(food_price)
  4. 자재 가격(matl_price)
  5. 새날 실행 횟수(refresh_times)
  6. 다음 원주민 번호(native_number)
  
  다. **다음 원주민 번호**는 후술할 seq와 기능이 동일하다.

- **seq.json**

  Sqlite3의 sequence table에서 영향을 받았다. Area계, Nation계 파일의 다음 row 번호를 저장하는 파일이다.

- **Area계**

  Area로 시작하며, 지역 정보만 저장하는 파일이다. 

- **Nation계**

  Nation으로 시작하며, 나라 정보만 저장하는 파일이다.

- **Info형**

  Info로 끝나며, 자주 참조하는 정보를 저장하는 파일이다.

  - AreaInfo : 지역명, 지역오너명, 현재 식량, 현재 자재, 현재 기술, 현재 문화, 공격병비율, 충성도, 지역속성

  - NationInfo : 나라명, 오너명, 현재 자금, 현재 빚, 남은 상환 기간, 가용 정책 점수, 금일 행동 횟수, 호전성 수치

- **Policy형**

  Policy로 끝나며, 각 정책에 투자한 점수를 저장하는 파일이다.

  - AreaPolicy, NationPolicy : 각각 6개의 투자 카테고리가 있다.

- **Extra형**

  Extra로 끝나며, 자주 참조하지 않는 정보/Info와 분리해야 하는 정보 등을 저장하는 파일이다.

  - AreaExtra : 초기 식량/자재/기술/문화 스탯

  - NationExtra : 초기 나라명/오너명, 유저 여부, 보호 잔여일

- `_standatd_relation`형

  `_standard_relation`으로 끝나며, 지역/나라를 기준으로 한 포함 관계를 저장하는 파일이다.

  - `area_standard_relation` : 지역 ID : 나라 ID 1:1 대응 파일이다. str : str 형식으로 저장한다. 모든 지역은 어떤 나라와 반드시 소유 관계를 맺어야 한다. 그게 아니라면, 삭제해야 한다.

  - `nation_standard_relation` : 나라 ID : 지역 ID 1:다 대응 파일이다. str : list 형식으로 저장한다. 나라는 지역을 여러 개 소유할 수 있으며, 지역을 하나도 소유하지 않을 수도 있다.

## 아리(봇)의 말투

 기본적으로 반말체다. 이는 예전에 시행한 투표로 공인된 바 있다. 지향해도 되고 안 지향해도 되지만, 디테일한 컨셉을 말하자면 **친한 여자 친구** 정도라고 말할 수 있다. 부담스럽다면 **비서 말투에 반말만 끼얹으면** 된다.

 유저별로 아리의 말투를 다르게 하는 **코스튬**이 논의된 바 있지만, 구현 부담 때문에 우선순위에서 밀렸다.

## 명령어

 모든 아리슬레나 구성원은 봇(명칭 : 아리)에 명령어로 명령을 내려 특정 행동을 수행할 수 있다. 명령어의 권한은 **관리자**, **왕**, **모두**로 나뉜다. 관리자는 왕, 모두의 상위 권한이며 왕은 모두의 상위 권한이다. 디스코드 역할과 짝짓자면 **관리자 - 관리자/개발자, 왕 - 왕/자문단/서기, 모두 - 일반(역할이 없는 유저)** 이 된다.

### 양식

1. 모든 명령어는 `!`로 시작하며, ` `(공백) 또는 `'' / ""`(따옴표)로 구분한다. 

   `!명령어 인자1 인자2 인자3` 과 같이 구분한다.

2. 따옴표 안에는 항상 공백이 있어야 한다. 즉,
   `!명령어 '공백이 들어간 말'`은 유효하지만,
   `!명령어 '공백없는말'`은 유효하지 않다.

3. 따옴표는 항상 `'`로 시작해 `'`로 끝나거나, `"`로 시작해 `"`로 끝나야 한다.

4. 명령어를 작성할 때, 괄호`()`는 반드시 포함해야 할 인자고, 대괄호`[]`는 포함해도 되고 안 해도 되는 인자다.

5. `, ...`은 인자 여러 개를 쓸 수 있다는 의미다.

### 작동

```python
File : Ari_slena

@ari.event
async def on_message

class Command
```

부분을 참조

### 전체 목록 (계획상)

- 구현 안 된 명령어는 **두껍게**, 덜 구현된 명령어는 *기울이기*

- 관리자 명령어
  1. 테스트 - 그저 테스트. 원하는 테스트 코드를 집어넣으면 된다. 현재 코드는 스텔로 디스코드의 **품평회**의 전신이 되는 코드 중 일부다.
  2. 얼마나지났어 - 개발을 본격적으로 시작한 날짜인 2020년 3월 11일부터 오늘까지 며칠이 지났는지를 출력하는 명령어다.
  3. 수정 - 긴급하게 어느 값을 수정해야 할 일이 있을 때 쓰는 명령어. modifyone() 함수와 사용법이 같다.
  4. 중지 -
  5. 재개 -
  6. 건국 -
  7. **식민**
  8. **편입**
  9. **병합**
  10. **추방**
  11. *새날*
      1. 자원 회복
      2. 원주민 생성
      3. **호감도 조정**
      4. **호감도에 따른 이 날의 원주민의 행동 양식 정의**
      5. **재해**
      6. 지역 자동 매각
  12. **세부열람**
  13. **경매**
      1. **추가**
      2. 
- 왕 명령어
  1. *현황*
     1. **나라**
     2. **지역**
     3. **외교**
  2. 공격병
  3. 가격
  4. **구매**
  5. **판매**
  6. **발전**
  7. **정책**
     1. **투자**
     2. **추출**
     3. **취소**
  8. **수출**
  9. **송금**
- 모두 명령어
  1. 아리
  2. *열람*
     1. **나라**
     2. **지역**

## 건국

 유저는 **#나라신청**에 양식에 맞춰 나라를 신청할 수 있다. 유저가 신청을 하면 관리자는 명령어를 이용해 유저의 나라를 데이터에 추가한다.

### 양식

 ```
!건국 (지역명) (나라명) (오너명) (초기 식량) (초기 자재) (초기 기술) (초기 문화)
 ```

### 권한

 관리자만 쓸 수 있다.

### 작동

 파일 Ari_data의 클래스 Make의 classmethod 함수 user_nation() 참조

 파일 Ari_slena의 클래스 MakeNation 참조

### 조건

1. `(지역명) (나라명) (오너명)`은 다른 지역명/나라명/오너명과 겹치지 않아야 한다.

2. `(초기 식량) (초기 자재) (초기 기술) (초기 문화)`는 숫자여야 하며, 총합이 20이어야 한다.

### 주의 사항

1. 오너명은 디스코드 유저 닉네임`Blabla#IJKL의 Blabla` 부분이다. 방에서 표기되는 닉네임과는 관련이 없다. 방에서 닉네임을 바꿔도 상관이 없지만, 유저 닉네임을 바꾸면 봇이 다른 유저로 취급한다.
2. 테스트를 이유로 나라를 건국할 때, 지역명/나라명/오너명 중 하나라도 기존 지역명/나라명/오너명과 겹치지 않아야 한다. 나중에 해당 나라를 삭제할 때 큰 문제가 따른다.

## 중지, 재개

 **중지**는 모든 명령어 사용 권한을 **관리자**로 높이는 명령어다. (= 관리자 외에는 명령어를 쓸 수 없다.) **재개**는 그렇게 변경된 권한을 원 상태로 돌린다.

### 양식 (중지)

```
!중지
```

### 양식 (재개)

```
!재개
```

### 권한

 관리자만 쓸 수 있다.

### 작동

 파일 Ari_slena의 class Stop과 Restart 참조

## 식민, 편입, 병합, 추방

 식민 : 제 0시즌의 **소유권이전**을 계승한 명령어다.

 편입 : 원주민 외교라는 개념이 생기면서 도입된 새 식민 방식이다. 지역이 식민지가 되어도 충성도를 그대로 유지한다.

 병합 : 제 0시즌의 **병합**을 계승한 명령어다.

 추방 : 수도가 아닌 휘하 지역을 원주민 지역으로 격하하는 명령어다.

### 양식

### 권한

 관리자만 쓸 수 있다.

### 작동

 유저가 원하는 지역의 식민/편입/병합/추방을 먼저 요청해야 할 수 있다.

##  새날

 제 0시즌의 **리프레시**를 계승한 명령어다.

### 양식

```
!새날
```

### 권한

 관리자만 쓸 수 있다.

### 작동

 미구현

### 주의 사항

1. 정해진 시간에만 써야 한다. 테스트 목적이 아니고서는 정해진 시간에 써야 정상적인 게임 운영이 가능하다.

## 아리

 시즌 0의 명령어 **도움/설명**을 계승한 명령어다. 명령어 전체 일람을 출력하기도 하고, 대략적인 신입 안내, 간단한 인사 등이 가능하다. 사용법에 따라 결과가 갈린다.

### 양식



## 열람

 시즌 0의 명령어 **열람**을 계승한 명령어다. 검색 분류와 검색어를 이용해 원하는 지역/나라의 대략적인 정보를 열람할 수 있다.

### 양식

```
!열람 [(검색 분류) (검색어)]
```



## 공격병 설정

 자신 나라의 특정 지역, 혹은 모든 지역의 공격병 수치(0 ~ 1000)를 지정하는 명령어다.

### 양식

```
!공격병 [(검색 분류) (검색어, ...)] 
```



### 권한



### 작동



