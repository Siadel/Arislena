import json
import math
import random
from collections import Counter as cnt

class token:
    """
    Token.json에서 토큰을 가져온다. 토큰을 활용할 때는 token.token 형식으로 가져오면 된다.
    """
    with open('Token.json', 'r') as t:
        token = json.load(t)['token']

class Constant:
    """
    상수 모음
    """

    # 기준 재고, 기준총가
    standard_stock = 160000
    standard_price_sum = 2000000

    # 초기 구매가 비율, 초기 판매가 비율
    early_buy_price_ratio = 1
    early_sell_price_ratio = 0.6

    # 초기 주기 회복률
    early_refresh_ratio = 0.1

    # 초기 자금, 공격병 비율, 충성도
    early_capital = 10000
    early_warrior = float(0)
    early_royalty = 1000

class Formula:
    """
    계산식 모음
    """

    # 정책 점수 계산식
    # 나라 기술, 나라 문화 -> 정책 점수(기본)
    point = lambda nati_tech, nati_cult: int(nati_tech / 8) + int(nati_cult / 5)

    # 공격병 비율 보여주기 계산식
    # 공격병 비율(데이터) -> 공격병 비율(보는값)
    warrior = lambda warr: int(warr * 1000)

    # 정책을 고려한 기준 스탯 계산식
    # 초기 스탯(식량, 자재), 현재 기술 스탯, '창고' 효과 -> 기준 스탯
    stnd_stat = lambda early_rsc, tech, storage: int(
        round((early_rsc + storage) * (1 + 0.01 * tech) + 0.05 * tech, 2) * 100)

    # 정책을 고려한 리프레시 회복률 계산식 (유저 지역 기준)
    # 수도권 (기술, 문화) 스탯, '생산' 효과 -> 회복률
    # 기본 : 0.1
    restor = lambda base, metr_tech, metr_cult, produce: round(
        (base + 0.001 * metr_tech) * (1 + 0.02 * metr_cult) * (1 + produce), 4)

    # 최대 자금 계산식
    # 초기 자금, 나라 (기술, 문화) 스탯 -> 최대 자금
    max_capi = lambda nati_tech, nati_cult: int(Constant.early_capital * (1 + 0.03 * nati_tech + 0.08 * nati_cult))

    # 최저 자금 계산식
    # 최대 자금 -> 최저 자금
    # 최대 자금은 따로 계산해줘야 함
    min_capi = lambda max_capi: -1 * int(max_capi / 7.5)

    # 정책 점수를 n번 투자해야 레벨을 1 올리게 되는 식
    # 투자한 정책 점수, 1레벨 올리는 데 필요한 점수 -> 현재 레벨
    # 정책 점수를 추출했다면, 반대로 작용한다.
    lv = lambda point, require_point: math.floor(point / require_point)

    # '국내 정치(안정/방치)' 식
    # %p, 기본 감소
    # 레벨 -> 효과
    local_manage = lambda lv: -1 * round(lv * 0.04, 2)

    # '국제 외교(개입/방치)' 식
    # 레벨 -> 효과
    diplomacy_inv = lambda lv: 15 * lv
    diplomacy_ext = lambda lv: round(15 * lv - 1.5 * (lv * (lv + 1)))

    # ' ~ 창고(확장/축소)' 식
    # 레벨 -> 효과
    storage_inv = lambda lv: 100 * lv
    storage_ext = lambda lv: round((lv - 0.05 * (lv * (lv + 1))) * 100)

    # ' ~ 생산(증대/감소)' 식
    # 레벨 -> 효과
    produce_inv = lambda lv: 0.05 * lv
    produce_ext = lambda lv: round(0.05 * lv - 0.005 * (lv * (lv + 1)), 2)

    # '~ 산업(투자/축소)' 식
    # 레벨 -> 효과
    invest_inv = lambda lv: -1 * 0.05 * lv
    invest_ext = lambda lv: -1 * round(0.1 * lv - 0.01 * (lv * (lv + 1)), 2)

    # 체력, 공격력 계산식
    # 현재 (식량, 자재, 기술) 스탯, 주사위 수치(무작위), 공격병 비율 -> 체력 / 공격력
    hp = lambda food, matl, metr_tech, dice, warr: round(
        (240 * food + 90 * matl) * (1 + 0.01 * metr_tech) * (1 + 0.1 * dice) * warr)
    ap = lambda food, matl, metr_tech, dice, warr: round(
        (3 * food + 8 * matl) * (1 + 0.01 * metr_tech) * (1 + 0.3 * dice) * warr)

    # 원주민 나라 생성 기준
    # 동시충족 - 최상위
    # 개별충족 - 평균
    # 개별충족 - 최상위
    biggest = lambda _avr: round(_avr * 1.5)
    indiv_ = lambda together_: round(together_ * (4 / 3))

    # 원주민 레벨에 따라 세력이 변화하는 정도
    stat_plus = lambda lv: lv * (lv + 1)  # 시그마 2n
    belligerence_plus = lambda lv: lv * (lv + 1) * 5  # 시그마 10n
    capital_plus = lambda lv: lv * (lv + 1) * 750  # 시그마 1500n

    # 구매 가격 정하는 공식
    # 초기 구매가 비율, 초기 판매가 비율, 수도권 문화
    buy_price = lambda b_buy, b_sell, metr_cult: round(b_buy - ((b_buy - b_sell) * 0.0095 * metr_cult), 4)

    # 기술에 따른 구매량 증가율
    # 원구매량, 기술 -> 실제 구매량
    tech_efficiency = lambda metr_tech: round(1 + metr_tech * 0.03, 2)

    # 판매 가격 정하는 공식
    # 초기 구매가 비율, 초기 판매가 비율, 기술 효율, 수도권 문화
    sell_price = lambda b_buy, b_sell, tech_eff, metr_cult: round(
        int(((b_sell / tech_eff) + ((b_buy - b_sell) * 0.0004 * metr_cult)) * 10000) / 10000, 4)

    # 단가, 개수, 비율 -> 가격 공식
    price = lambda unitprice, amount, ratio: round(unitprice * amount * ratio)

    # 기준총가, 재고 -> 새로운 가격
    new_unitprice = lambda stock: round(Constant.standard_price_sum / stock, 2)

    # 최고이득문화 공식
    # 수도권 기술 -> 최고이득문화
    max_profit_cult = lambda metr_tech: int(390000 / (3922 + 4.8 * metr_tech))

    # 방어병 공식
    # 공격병 비율 -> 방어병 비율
    def_warriors = lambda warriors: 1 - warriors

    # 호전성 공식
    # 나라 (식량, 자재, 기술, 문화), 나라 기준 (식량, 자재) 스탯 -> 호전성
    @staticmethod
    def belligerence(nati_food, nati_matl, nati_tech, nati_cult, nati_stnd_food, nati_stnd_matl):
        rratio = 0.2 + (nati_food + nati_matl) / (nati_stnd_food + nati_stnd_matl) * 5
        if nati_tech == nati_cult == 0:
            tratio = 1
        else:
            tratio = 0.8 + nati_tech / (nati_tech + nati_cult) * 1.25

        return round(rratio * tratio, 2)

class File:
    """
    파일 이름, 확장자, 기본적인 파일 관련 함수들 모음
    """
    columns = {
        # 각 파일에 들어갈 세로줄 이름 적기
        'system': ['food_stock', 'matl_stock', 'food_price', 'matl_price', 'refresh_times', 'native_number'],
        'NationInfo': ['nati_name', 'nati_owner', 'capital', 'debt', 'refund_date',
                       'investable_point', 'acted_times', 'belligerence'],
        'NationPolicy': ['atk_strategy', 'def_strategy', 'territory', 'local_manage', 'metro_radius',
                         'diplomacy'],
        'NationExtra': ['origin_nati', 'origin_owner', 'user_native', 'protect_remain'],
        'AreaInfo': ['area_name', 'area_owner', 'food', 'matl', 'tech', 'cult', 'warrior', 'royalty', 'wariness', 'properties'],
        'AreaPolicy': ['food_storage', 'food_produce', 'matl_storage', 'matl_produce', 'tech_invest',
                       'cult_invest'],
        'AreaExtra': ['early_food', 'early_matl', 'early_tech', 'early_cult'],
        'area_standard_relation' : 'nati_ID',
        'nation_standard_relation' : ['area_IDs'],
        'seq': ['name', 'seq']
    }

    columns_translate = {
        # columns에 대한 한국어 번역
        'system' : ['식량재고', '자재재고', '식량가격', '자재가격', '주기횟수', '원주민번호'],
        'NationInfo' : ['나라', '오너', '자금', '빚', '상환기간', '투자점수', '정책행동', '호전성'],
        'NationPolicy' : ['공격전략', '방어전략', '영토', '내정', '수도권', '외교'],
        'NationExtra' : ['본래나라', '본래오너', '유저여부', '보호기간'],
        'AreaInfo' : ['지역', '지역오너', '식량', '자재', '기술', '문화', '공격병', '충성도', '경계도', '속성'],
        'AreaPolicy' : ['식량창고', '자재생산', '자재창고', '자재생산', '기술투자', '문화투자'],
        'AreaExtra' : ['초기식량', '초기자재', '초기기술', '초기문화'],
   }

    names = [f for f in columns]

    ext = '.json'

    # 각 파일 이름 변수화
    sys = names[0]
    NI = names[1]
    NP = names[2]
    NE = names[3]
    AI = names[4]
    AP = names[5]
    AE = names[6]
    arel = names[7]
    nrel = names[8]
    seq = names[9]
    DI = 'DiplomacyInfo'

    sysj = names[0] + ext
    NIj = names[1] + ext
    NPj = names[2] + ext
    NEj = names[3] + ext
    AIj = names[4] + ext
    APj = names[5] + ext
    AEj = names[6] + ext
    arelj = names[7] + ext
    nrelj = names[8] + ext
    seqj = names[9] + ext
    DIj = DI + ext  # 얘는 세로줄, 가로줄이 모두 가변적이라 특별하게 다뤄야 할듯.

    @classmethod
    def port_key(cls, column: str):
        """
        column에 맞는 파일명과 위치를 찾는 함수

        column은 무조건 columns_translate에 번역된 명칭 중 하나여야 함

        :param column: str
        :return: 파일명(str), 인덱스(int)
        """
        col = cls.columns_translate
        for f in col:
            if column in col[f]:
                for c in col[f]:
                    if column == c:
                        return f, col[f].index(c)

    @classmethod
    def json_attacher(cls, filename: str) -> str:
        """
        파일명에 무조건 .json을 붙이는 함수

        :param filename: str
        :return: filename.json
        """
        if cls.ext in filename:
            return filename
        else:
            return filename + cls.ext

    @classmethod
    def json_detacher(cls, filename: str) -> str:
        """
        파일명의 .json을 무조건 떼는 함수

        :param filename: str
        :return: filename.json -> filename
        """
        if cls.ext in filename:
            return filename[:-5]
        else:
            return filename
            
    @classmethod
    def load(cls, filename: str):
        """
        해당 파일의 전체 정보를 불러오는 함수

        :param filename: str
        :return: dict {ID(str) : values(list), ...}
        """
        filename = cls.json_attacher(filename)
        try:
            with open(filename, 'r') as file:
                load = json.load(file)
        except json.decoder.JSONDecodeError:
            load = dict()
        return load

    @classmethod
    def write(cls, filename: str, data: dict):
        """
        해당 파일에 정보를 덮어쓰는 함수

        :param filename: str
        :param data: dict
        :return: 내용 덮어쓰기
        """
        filename = cls.json_attacher(filename)
        with open(filename, 'w') as file:
            json.dump(data, file, indent = 2)

    @classmethod
    def modifyone(cls, filename: str, ID: str, column: str, value: [str, int, float], *arithmetic: str):
        """
        특정 파일의 ID의 행의 값을 value로 바꿔 write()로 덮어쓰는 함수
        
        column은 한국어 번역명이어야 한다.
        
        value가 숫자인 경우에 arithmetic에 '+', '-'를 써서 산술 계산을 할 수 있다.
        
        :param filename: str
        :param ID: str
        :param column: str
        :param value: str, int, float
        :param arithmetic: '+', '-'
        :return: 내용 덮어쓰기
        """
        filename = cls.json_detacher(filename)
        load = cls.load(filename)
        ind = cls.columns_translate[filename].index(column)
        if len(arithmetic) != 0:
            arth = arithmetic[0]
            replace = load[ID][ind]
            if arth == '+':
                replace += value
            elif arth == '-':
                replace -= value
        else:
            replace = value
        del load[ID][ind]
        load[ID].insert(ind, replace)

        cls.write(filename, load)

    @classmethod
    def updatewrite(cls, filename, key, value):
        filename = cls.json_attacher(filename)
        load = cls.load(filename)
        load.update({key : value})

        cls.write(filename, load)

class Make(File):
    # 데이터를 생성하는 함수를 모은 클래스

    # 나라를 만들 때 넣는 기본값
    early_warr = Constant.early_warrior
    royalty = Constant.early_royalty

    @classmethod
    def defi_id(cls, filename: str):
        """
        해당 파일이 대표 ID값이 있는 파일(NationInfo, AreaInfo)이냐 아니냐를 판단하는 함수

        :param filename: str
        :return: True, False
        """
        filename = cls.json_detacher(filename)
        if filename in ['NationInfo', 'AreaInfo']:
            return True
        else:
            return False

    @classmethod
    def seq_value(cls):
        """
        seq의 초기값 만들기

        :return: dict {filename(str) : 1, ...}
        """
        rtn = dict()
        for c in cls.columns:
            if cls.defi_id(c):
                rtn.setdefault(c, 1)
            else:
                pass
        return rtn

    @classmethod
    def system_value(cls):
        """
        system의 초기값 만들기

        :return: dict {column(str) : value(int, float), ...}
        """
        price = Formula.new_unitprice(Constant.standard_stock)
        value = (Constant.standard_stock, Constant.standard_stock, price, price, 0, 0)
        rtn = dict()
        for i in range(len(value)):
            rtn.setdefault(cls.columns[cls.sys][i], value[i])
        return rtn

    @classmethod
    def frame(cls):
        """
        전체 파일 초기화 함수

        :return: 모든 파일을 빈 껍데기로 만듦
        """
        # 파일 틀만 만들어놓기
        # 최초 1회만 작동
        with open(cls.seqj, 'w') as seq:
            json.dump(cls.seq_value(), seq, indent = 2)

        with open(cls.sysj, 'w') as sys:
            json.dump(cls.system_value(), sys, indent = 2)

        with open(cls.NIj, 'w'):
            pass

        with open(cls.NPj, 'w'):
            pass

        with open(cls.NEj, 'w'):
            pass

        with open(cls.AIj, 'w'):
            pass

        with open(cls.APj, 'w'):
            pass

        with open(cls.AEj, 'w'):
            pass

        with open(cls.arelj, 'w'):
            pass

        with open(cls.nrelj, 'w'):
            pass

        cls.write(cls.DIj, {'user' : []})

    @classmethod
    def addwrite(cls, filename: str, key: str, value):
        """
        {key : value} 딕셔너리 하나를 파일에 더하는 함수

        :param filename: str
        :param key: str
        :param value: 보통은 list
        :return: 파일 저장
        """
        filename = cls.json_attacher(filename)
        load = cls.load(filename)
        load.setdefault(key, value)

        cls.write(filename, load)

    @classmethod
    def fill(cls, filename: str, *values):
        """
        특정 파일에 데이터(values)를 리스트 형식으로 묶어 넣는 함수

        addwrite()를 활용함

        :param filename: str
        :param values: str, int, float
        :return: 파일 저장
        """
        filename = cls.json_detacher(filename)
        seqload = cls.load(cls.seqj)
        num = ''
        if 'Nation' in filename or filename == cls.nrel:
            num = seqload[cls.NI]
        elif 'Area' in filename or filename == cls.arel:
            num = seqload[cls.AI]

        li = []
        if filename == cls.arel:
            cls.addwrite(filename, num, *values)
        elif filename == cls.nrel:
            cls.addwrite(filename, num, list(values))
        else:
            for i in range(len(cls.columns[filename])):
                li.append(values[i])

            cls.addwrite(filename, num, li) # num(ID)이 key가 되고, li(데이터)가 value가 되는 방식.

    @classmethod
    def seq_plus(cls, filename):
        filename = cls.json_detacher(filename)
        with open(cls.seqj, 'r') as seq:
            load = json.load(seq)
            load[filename] += 1
        with open(cls.seqj, 'w') as seq:
            json.dump(load, seq, indent=2)

    @classmethod
    def user_nation(cls, area_name: str, nati_name: str, owner: str, early_food: int, early_matl: int, early_tech: int, early_cult: int):
        """유저 나라 데이터를 생성하는 함수"""
        food, matl = Formula.stnd_stat(early_food, early_tech, 0), Formula.stnd_stat(early_matl, early_tech, 0)
        nati_id, area_id = cls.load(cls.seq)[cls.NI], cls.load(cls.seq)[cls.AI]
        # 나라명, 오너명, 초기 자금, 빚, 남은상환기간, 가용점수, 행동횟수, 호전성
        cls.fill(cls.NI, nati_name, owner, Constant.early_capital, 0, 0, Formula.point(early_tech, early_cult), 0,
                 Formula.belligerence(food, matl, early_tech, early_cult, food, matl))
        cls.fill(cls.NP, 0, 0, 0, 0, 0, 0) # 전부 기본값 0
        cls.fill(cls.NE, nati_name, owner, True, 7) # 나라명, 오너명, 유저, 보호 일수
        # 지역명, 기준 (식량, 자재) 스탯, 기술, 문화, 공격병, 충성도, 경계도, 지역속성
        cls.fill(cls.AI, area_name, owner, food, matl, early_tech, early_cult, 0, 1000, 0, '수도')
        cls.fill(cls.AP, 0, 0, 0, 0, 0, 0) # 전부 기본값 0
        cls.fill(cls.AE, early_food, early_matl, early_tech, early_cult) # 초기 스탯
        # 지역 기준 관계 파일
        cls.fill(cls.arel, str(nati_id))
        # 나라 기준 관계 파일
        cls.fill(cls.nrel, str(area_id))
        # 외교 파일
        load_di = cls.load(cls.DIj)
        load_di['user'].append(str(nati_id))
        cls.write(cls.DIj, load_di)

        for c in [cls.NI, cls.AI]:
            cls.seq_plus(c)

class Read(File):

    @classmethod
    def one(cls, filename):
        pr = cls.load(filename)
        print(pr)

    @classmethod
    def many(cls, *filenames):
        for f in filenames:
            print(cls.load(f))

class Search(File):
    def __init__(self, searchkey, searchvalue, *condition):
        # searchvalue가 str일 경우, *condition은 불필요함
        # searchvalue가 int나 float일 경우, *condition으로 검색 범위를 조절할 수 있음
        self.searchkey = searchkey
        self.searchvalue = searchvalue
        self.condition = condition

        self.area_ID, self.nati_ID = self.return_ID()

    def return_ID(self):
        """
        해당 파일의 모든 데이터를 불러온 다음, 조건에 맞춘 ID를 list나 dict로 반환하는 함수

        이 때 ID는 str임

        :return: 지역 ID, 나라 ID
        """
        filename, ind = self.port_key(self.searchkey)
        load = self.load(filename)
        area_ID = []
        nati_ID = []
        rtn_c = []

        def conditionclause(prt):
            if 'Nation' in filename:
                nati_ID.append(prt)
            elif 'Area' in filename:
                area_ID.append(prt)

        if type(self.searchvalue) == str:
            for ID in load:
                if self.searchvalue == load[ID][ind]:
                   conditionclause(ID)

        elif type(self.searchvalue) in [int, float]:
            cnd = self.condition

            if len(cnd) > 0:
                if cnd[0] == '이상':
                    for ID in load:
                        if load[ID][ind] >= self.searchvalue:
                            conditionclause(ID)
                elif cnd[0] == '이하':
                    for ID in load:
                        if load[ID][ind] <= self.searchvalue:
                            conditionclause(ID)
                elif cnd[0] == '초과':
                    for ID in load:
                        if load[ID][ind] > self.searchvalue:
                            conditionclause(ID)
                elif cnd[0] == '미만':
                    for ID in load:
                        if load[ID][ind] < self.searchvalue:
                            conditionclause(ID)

                if len(cnd) == 3:
                    scn_value = cnd[1]
                    scn_cnd = cnd[2]
                    li = []
                    if 'Nation' in filename:
                        li = nati_ID
                    elif 'Area' in filename:
                        li = area_ID
                    if scn_cnd == '이상':
                        for ID in li:
                            if load[ID][ind] >= scn_value:
                                rtn_c.append(ID)
                    elif scn_cnd == '이하':
                        for ID in li:
                            if load[ID][ind] <= scn_value:
                                rtn_c.append(ID)
                    elif scn_cnd == '초과':
                        for ID in li:
                            if load[ID][ind] > scn_value:
                                rtn_c.append(ID)
                    elif scn_cnd == '미만':
                        for ID in li:
                            if load[ID][ind] < scn_value:
                                rtn_c.append(ID)

            else:
                for ID in load:
                    if load[ID][ind] == self.searchvalue:
                        conditionclause(ID)

        if len(rtn_c) != 0:
            if 'Nation' in filename:
                nati_ID = rtn_c
            elif 'Area' in filename:
                area_ID = rtn_c

        if 'Nation' in filename:
            area_ID = dict()
            nrel = self.load(self.nrel)
            for ID in nati_ID:
                area_ID.setdefault(ID, nrel[ID])
        elif 'Area' in filename:
            nati_ID = dict()
            arel = self.load(self.arel)
            for ID in area_ID:
                nati_ID.setdefault(ID, arel[ID])

        return area_ID, nati_ID

    def convert_to_list(self, ID):
        """
        ID가 dict면 list로 바꾸고, 아니면 그대로 반환하는 함수
        
        :param ID: dict or list
        :return: list
        """
        if type(ID) == dict:
            if ID == self.area_ID: # 나라 기준 rel
                rli = []
                for I in ID:
                    if type(ID[I]) == list:
                        rli.extend(ID[I])
                    else:
                        rli.append(ID[I])
                ID = rli
            elif ID == self.nati_ID: # 지역 기준 rel
                rli = []
                for I in ID:
                    if type(ID[I]) == list:
                        rli.extend(ID[I])
                    else:
                        rli.append(ID[I])
                ID = list(dict(cnt(rli)).keys())
        return ID

    def search_parse(self, filename, ID):
        """
        :param filename: str
        :param ID: dict or list -> list
        :return: list contains dict
        """
        filename = self.json_detacher(filename)
        ID = self.convert_to_list(ID)

        data = self.load(filename)
        li = []
        collen = len(self.columns[filename])
        for c in range(collen):
            li.append(dict())
        for i in ID:
            for c in range(collen):
                li[c].setdefault(i, data[i][c])
        return li

class NationInfo(Search):
    def __init__(self, searchkey, searchvalue, *condition):
        super().__init__(searchkey, searchvalue, *condition)

        self.nati_name, self.nati_owner, self.capital, self.debt, self.refund_date, self.investable_point, self.acted_times, self.belligerence = self.search_parse('NationInfo', self.nati_ID)

class NationPolicy(Search):
    def __init__(self, searchkey, searchvalue, *condition):
        super().__init__(searchkey, searchvalue, *condition)

        self.atk_strategy, self.def_strategy, self.territory, self.local_manage, self.metro_radius, self.diplomacy = self.search_parse('NationPolicy', self.nati_ID)

class NationExtra(Search):
    def __init__(self, searchkey, searchvalue, *condition):
        super().__init__(searchkey, searchvalue, *condition)

        self.origin_nati, self.origin_owner, self.user_native, self.protect_remain = self.search_parse('NationExtra', self.nati_ID)

class AreaInfo(Search):
    def __init__(self, searchkey, searchvalue, *condition):
        super().__init__(searchkey, searchvalue, *condition)

        self.area_name, self.area_owner, self.food, self.matl, self.tech, self.cult, self.warrior, self.royalty, self.properties = self.search_parse('AreaInfo', self.area_ID)

class AreaPolicy(Search):
    def __init__(self, searchkey, searchvalue, *condition):
        super().__init__(searchkey, searchvalue, *condition)

        self.food_storage, self.food_produce, self.matl_storage, self.matl_produce, self.tech_invest, self.cult_invest = self.search_parse('AreaPolicy', self.area_ID)

class AreaExtra(Search):
    def __init__(self, searchkey, searchvalue, *condition):
        super().__init__(searchkey, searchvalue, *condition)

        self.early_food, self.early_matl, self.early_tech, self.early_cult = self.search_parse('AreaExtra', self.area_ID)

class Calculate(Search):
    """NationInfo ~ AreaExtra에서 가져온 데이터를 이용해 새로운 데이터를 만들거나, 계산하는 클래스"""

    def __init__(self, searchkey, searchvalue, *condition):
        super().__init__(searchkey, searchvalue, *condition)

        self.nati_ID_list = self.convert_to_list(self.nati_ID)
        self.area_ID_dict = self.convert_to_dict()

    def convert_to_dict(self):
        load = self.load('nation_standard_relation.json')
        di = dict()
        for i in self.nati_ID_list:
            di.setdefault(i, load[i])
        return di

    def parse_as_column(self, area_ID: dict, column: str):
        filename, ind = self.port_key(column)
        li = []
        for ID in area_ID:
            li.append(self.search_parse(filename, area_ID[ID]))

        rtn = []
        for l in li:
            rtn.append(l[ind])

        return rtn

    def arrange_add(self, column: str):
        li = []
        for d in self.parse_as_column(self.area_ID_dict, column):
            li.append(0)
            for i in d.values():
                li[-1] += i

        di = dict()
        n = 0
        for ID in self.nati_ID_list:
            di.setdefault(ID, li[n])
            n += 1

        return di

class NationStats(Calculate):
    def __init__(self, searchkey, searchvalue, *condition):
        super().__init__(searchkey, searchvalue, *condition)

        self.nati_food = self.arrange_add('식량')
        self.nati_matl = self.arrange_add('자재')
        self.nati_tech = self.arrange_add('기술')
        self.nati_cult = self.arrange_add('문화')

class ShowArea(Search):
    def __init__(self, searchkey, searchvalue, *condition):
        super().__init__(searchkey, searchvalue, *condition)

    def show(self):
        pass

class InstantLoad(File):
    """특정 정보를 바로바로 반환하는 함수를 담은 클래스"""

    def __init__(self, column):
        """
        절대 영문자를 써넣지 마시오

        :param column: str
        """
        self.column = column

    def certain_data(self):
        """
        모든 ID에 대한 특정 데이터를 ID를 key로 한 딕셔너리로 반환하는 함수

        :return: dict {ID(str) : value(str, int, float)...}
        """
        filename, ind = self.port_key(self.column)
        load = self.load(filename)
        di = dict()
        for l in load:
            di.setdefault(l, load[l][ind])
        return di

    def convert_list(self):
        """
        certain_data에서 만든 dict를 list로 변환하는 함수

        :return: list [value(str, int, float)...]
        """
        di = self.certain_data()
        li = []
        for d in di:
            li.append(di[d])
        return li



class Delete(Search):
    """지역이나 나라를 삭제하는 함수를 모은 클래스"""

    def __init__(self, searchkey, searchvalue, *condition):
        super().__init__(searchkey, searchvalue, *condition)

    @classmethod
    def deleteone(cls, filename, ID):
        filename = cls.json_attacher(filename)
        load = cls.load(filename)
        del load[ID]
        cls.write(filename, load)

    @classmethod
    def deleteareainnrel(cls, nati_ID, area_ID):
        load = cls.load(cls.nrel)
        load[nati_ID].remove(area_ID)
        cls.write(cls.nrel, load)

    @classmethod
    def deleteDIuser(cls, ID):
        load = cls.load(cls.DI)
        load['user'].remove(ID)
        cls.write(cls.DI, load)

    def area(self):
        # 일단 검색된 지역을 지우고
        # 그 지역이 수도라면 해당 지역의 나라를 리스트에 저장하고
        # 저장한 리스트(나라 ID)를 가지고 나라를 삭제하기
        nID = []
        area_ID = self.convert_to_list(self.area_ID)
        for ID in area_ID:
            properties = AreaInfo(self.searchkey, self.searchvalue, *self.condition).properties
            arel = self.load(self.arel)
            nati_ID = arel[ID]

            self.deleteone(self.AE, ID)
            self.deleteone(self.AP, ID)
            self.deleteone(self.AI, ID)
            self.deleteareainnrel(nati_ID, ID)
            self.deleteone(self.arel, ID)

            if properties[ID] == '수도':
                nID.append(nati_ID)

        if len(nID) != 0:
            for ID in nID:
                self.deln(ID)

    def deln(self, ID):
        arealist = self.load(self.nrel)[ID]
        self.deleteone(self.NE, ID)
        self.deleteone(self.NP, ID)
        self.deleteone(self.NI, ID)
        self.deleteone(self.nrel, ID)
        self.deleteDIuser(ID)
        for aID in arealist:
            self.deleteone(self.AE, aID)
            self.deleteone(self.AP, aID)
            self.deleteone(self.AI, aID)
            self.deleteone(self.arel, aID)

    def nation(self):
        for ID in self.convert_to_list(self.nati_ID):
            self.deln(ID)

class Politic:

    @staticmethod
    def colonize(domi_nati, colo_area):
        # 지배국, 피지배 지역(식민지)을 인자로 받음
        # 나라 id, 나라명, 나라 오너, 속성(AreaInfo), 충성도(AreaInfo), 자금(NationInfo) 변경
        f = File()
        dn = Search('나라', domi_nati)
        ca = NationInfo('지역', colo_area)

        dn_nID = dn.nati_ID[0]
        dn_area = dn.area_ID[dn_nID]
        ca_aID = ca.area_ID[0]
        ca_nID = ca.nati_ID[ca_aID]
        ca_n_area = f.load('nation_standard_relation.json')[ca_nID]

        dn_area.extend(ca.area_ID)
        ca_n_area.remove(ca_aID)

        f.updatewrite(f.arel, ca_aID, dn_nID)
        f.updatewrite(f.nrel, dn_nID, dn_area)
        f.updatewrite(f.nrel, ca_nID, ca_n_area)

        f.modifyone('NationInfo.json', dn_nID, '자금', ca.capital[ca_nID], '+')
        f.modifyone('NationInfo.json', ca_nID, '자금', 0)
        f.modifyone('AreaInfo.json', ca_aID, '속성', '식민지')
        f.modifyone('AreaInfo.json', ca_aID, '충성도', 0)

def native_generator():
    # 원주민 생성 함수

    # 유저 평균 (기술 + 문화) 스탯과 최상위 기술 + 문화 도출해내기
    nati_names = InstantLoad('나라').convert_list()
    li_stat = []
    sum_stat = 0

    whole_tech = InstantLoad('기술').convert_list()
    whole_cult = InstantLoad('문화').convert_list()

    for d in range(len(whole_tech)):
        stat = whole_tech[d] + whole_cult[d]
        sum_stat += stat
        li_stat.append(stat)

    avr = round(sum_stat / len(nati_names))
    biggest = max(li_stat)

    # 원주민 나라 생성 시 총 기준 스탯 설정의 기준을 계산하기
    # 기준(tog_avr)을 정하면 알아서 계산해줌
    tog_avr = 15
    tog_biggest = Formula.biggest(tog_avr)
    indiv_avr = Formula.indiv_(tog_avr)
    indiv_biggest = Formula.indiv_(Formula.biggest(tog_avr))

    standard = {}
    standard.setdefault('1t', (tog_avr, tog_biggest))
    standard.setdefault('1i', (indiv_avr, indiv_biggest))

    for i in range(3):
        tog_avr = round(tog_avr * 1.5)
        tog_biggest = Formula.biggest(tog_avr)
        indiv_avr = Formula.indiv_(tog_avr)
        indiv_biggest = Formula.indiv_(Formula.biggest(tog_avr))
        standard.setdefault('{}t'.format(i + 2), (tog_avr, tog_biggest))
        standard.setdefault('{}i'.format(i + 2), (indiv_avr, indiv_biggest))

    def a_b(num):
        if num == 0:
            return (avr < standard['1t'][0] or biggest < standard['1t'][1]) and (
                        avr < standard['1i'][0] and biggest < standard['1i'][1])
        elif num >= 1:
            return (avr >= standard['{}t'.format(num)][0] and biggest >= standard['{}t'.format(num)][1]) or (
                        avr >= standard['{}i'.format(num)][0] or biggest >= standard['{}i'.format(num)][1])

    # 원주민이 몇 단계인지 계산하기
    lv = 0
    for i in range(5):
        if a_b(i):
            lv = i
        else:
            pass

    stat_plus = Formula.stat_plus(lv)
    belg_plus = Formula.belligerence_plus(lv)
    capi_plus = Formula.capital_plus(lv)

    # 기본 스탯 정보
    # 몰빵 확률이 높음 (더 정확한 랜덤을 위한 코드 개선 환영)
    def partition(number: int, space: int):
        rtn = []

        if space < 1:
            return None
        elif space >= 1:
            li = ['*' for stars in range(number)]
            for ii in range(space - 1):
                li.insert(random.randint(0, len(li)), '|')

            star = 0
            for s in li:
                if s == '|':
                    rtn.append(star)
                    star = 0
                else:
                    star += 1
            rtn.append(star)

        return rtn

    base = partition(24, 4)
    random.shuffle(base)

    # 스탯 더하기
    for i in range(len(base)):
        j = base.pop(i)
        j += stat_plus
        base.insert(0, j)

    # 호전성 더하기

    # 자금 더하기
    capi = Constant.early_capital + capi_plus

    return {'stat' : base, 'belg' : belg_plus, 'capi' : capi}