import json
import math
import random
from collections import Counter as cnt

def HangeulAlphabet(input_s):
    # If Hangeul, returns True
    # If Alphabet, returns False
    # expired but maybe next time?
    k_count = 0
    e_count = 0
    for c in input_s:
        if ord('가') <= ord(c) <= ord('힣'):
            k_count+=1
        elif ord('a') <= ord(c.lower()) <= ord('z'):
            e_count+=1
    return True if k_count>1 else False

class token:
    """
    Token.json에서 토큰을 가져온다. 토큰을 활용할 때는 token.token 형식으로 가져오면 된다.
    """
    with open('Token.json', 'r') as t:
        token = json.load(t)['token']
        
class unit:
	
	file = dict()
	
	@classmethod
	def columns(cls):
		li = []
		for a in list(cls.file.values()):
			li.extend(a)
		return li
	
	
class area(unit):
	
	file = {
		
    	'base': ['fertility', 'reserves', 'flatness'],
    	
    	'resouce': ['food', 'material', 'population', 'man_power', 'military_power'],
    	
    	'state': ['stableness', 'rank'],
    	
    	'building': ['food_storage', 'material_storage', 'government_office', 'castle', 'city_planning'],
    	
    	'policy': []
    	
    }
    
	base_dice = '1'*4 + '2'*7 + '3'*12 + '4'*17 + '5'*20 + '6'*17 + '7'*12 + '8'*7 + '9'*4
	
	# base produce, technology efficiency, culture compansation, technology compensation, defendency compensation
	base_table = {'1': [10,  0.3,  0.3,   1.5,  6],
				  '2': [17,  0.5,  0.5,   1.3,  4],
				  '3': [30,  0.75, 0.75,  1.15, 2],
				  '4': [42,  0.9,  0.9,   1.05, 1],
				  '5': [50,  1.0,  1.0,   1.0,  0],
				  '6': [59,  1.1,  1.05,  1.0,  0],
				  '7': [83,  1.25, 1.125, 1.0,  0],
				  '8': [143, 1.45, 1.225, 1.0,  0],
				  '9': [250, 1.7,  1.35,  1.0,  0],
	}
	
	base_desc = {'123': '평균이하',
				 '456': '평균',
				 '789': '펑균이상',
	}
	       

class group(unit):
	
	file = {
	
		'base': [],
		
		'info': ['technology', 'culture', 'executive_power', 'remained_time'],
		
		'resource': ['fund', 'debt'],
		
		'state' : ['belligerence']
		
	}


class Constant:
	"""
	A pile of constants
	"""
	
    # 기준 재고, 기준총가
	std_stock = 160000
	std_price_sum = 2000000
	
class Formula:
	"""
	A pile of formulas
	"""
	
	# 기준총가, 재고 -> 새로운 가격
	new_unitprice = lambda stock: round(Constant.std_price_sum / stock, 2)
	
class File:
    """
    파일 이름, 확장자, 기본적인 파일 관련 함수들 모음
    """
    
    columns = {
        # 각 파일에 들어갈 세로줄 이름 적기
        'system': ['food_stock', 'matl_stock', 'food_price', 'matl_price', 'refresh_times', 'area_number', 'group_number'],
        
        'area': area.columns(),
        
        'group': group.columns(),
        
        'area_std_r': ['area_name', 'group_ID'],
        
        'group_std_r': ['group_name', 'owner', 'higher']
        
    }

    @classmethod
    def port_key(cls, column: str):
        """
        column에 맞는 파일명과 위치를 찾는 함수

        column은 무조건 columns_translate에 번역된 명칭 중 하나일 수도 있고 영문일 수도 있음

        :param column: str
        :return: 파일명(str), 인덱스(int)
        """
        col = cls.columns
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
        if '.json' in filename:
            return filename
        else:
            return filename + '.json'

    @classmethod
    def json_detacher(cls, filename: str) -> str:
        """
        파일명의 .json을 무조건 떼는 함수

        :param filename: str
        :return: filename.json -> filename
        """
        if '.json' in filename:
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
    def modifyone(cls, ID, column, value, *arithmetic):
        """
        특정 파일의 ID의 행의 값을 value로 바꿔 write()로 덮어쓰는 함수
        
        value가 숫자인 경우에 arithmetic에 '+', '-'를 써서 산술 계산을 할 수 있다.
        
        :param filename: str
        :param ID: str
        :param column: str
        :param value: str, int, float
        :param arithmetic: '+', '-'
        :return: 내용 덮어쓰기
        """
        filename, ind = cls.port_key(column)
        load = cls.load(filename)
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
            
    

class Make(File):
    # 데이터를 생성하는 함수를 모은 클래스
    
    @classmethod
    def system_value(cls):
        """
        system의 초기값 만들기

        :return: dict {column(str) : value(int, float), ...}
        """
        price = Formula.new_unitprice(Constant.std_stock)
        value = (Constant.std_stock, Constant.std_stock, price, price, 0, 0, 0)
        rtn = dict()
        for i in range(len(value)):
            rtn.setdefault(cls.columns['system'][i], value[i])
        return rtn

    @classmethod
    def frame(cls):
        """
        전체 파일 초기화 함수

        :return: 모든 파일을 빈 껍데기로 만듦
        """
        # 파일 틀만 만들어놓기

        with open('system.json', 'w') as sys:
            json.dump(cls.system_value(), sys, indent = 2)

        with open('area.json', 'w'):
            pass

        with open('group.json', 'w'):
            pass

        with open('area_std_r.json', 'w'):
            pass

        with open('group_std_r.json', 'w'):
            pass

        cls.write('diplomacy.json', {'user' : []})

    @classmethod
    def ID(cls, which, *extra):
    	load = cls.load('system.json')
    	if which == 'area':
    		rtn = 'A' + str(load['area_number']).zfill(3)
    	if which == 'group':
    		if 'u' in extra[0]:
    			rtn = 'GU'
    		elif 'n' in extra[0]:
    			rtn = 'GN'
    		else:
    			print('fill extra with u or n')
    		rtn += str(load['group_number']).zfill(3)
    	return rtn
    	
    @classmethod
    def area(cls):
    	base = [random.choice(area.base_dice) for i in range(3)]
    	
    	mustlen = len(cls.columns['area'])
    	
    	val = []
    	
    	for i in range(mustlen):
    		val.append('')
    	
    	val[:3] = base
    	
    	num = ''
        
    	load = cls.load('system.json')
    	load['area_number'] += 1
    	with open('system.json', 'w') as file:
        	json.dump(load, file, indent=2)
        
    	num = cls.ID('area')
    	
    	cls.addwrite('area.json', num, val)