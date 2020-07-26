# 프로그램 구성에 필요한 외부 모듈 가져오기
import discord
import datetime
import random
# 프로그램 구성에 필요한 내부 모듈 가져오기
import Ari_data as dt
import Ari_msg as ms

play_stopped = False
ari = discord.Client()


# 기본 함수

def solve(a, b, c, d, e, f):
    numer_f = e * c - b * f
    numer_m = a * f - d * c
    dnomi = a * e - b * d
    if dnomi == 0:
        raise ValueError()
    return numer_f // dnomi, numer_m // dnomi


admin_list = ["DRTN#8341", "Siadel#7457", "paxbun#6463"]
king_list = dt.InstantLoad('오너').convert_list()


def check_permission(author):
    name = author.name
    disc = author.discriminator
    key = name + "#" + disc
    if key in admin_list or (key in admin_list and name in king_list):
        return '관리자'
    elif name in king_list:
        return '왕'
    else:
        return '모두'


def get_channel_by_position(pos):
    for ch in ari.get_all_channels():
        if ch.position == pos and ch.type == discord.ChannelType.text:
            return ch


def parse(message):
    # !로 명령어를 선언하고, 공백과 따옴표로 명령어 나누기
    message.strip()
    if message.startswith('!'):
        message = message[1:]
        if len(message) == 0:
            return None
        if '!' in message:
            return None
        message.strip()
        # 따옴표를 사용하려면, 반드시 따옴표 안에 공백을 넣어야 함.

        # 먼저 메세지(str)를 공백을 기준으로 나눈다.
        msg = message.split()
        li = []
        # 나눈 메세지(list)를 스캔해 따옴표가 있는 메세지의 위치를
        # 새로운 리스트에 저장한다.
        for i in range(len(msg)):
            if '"' in msg[i] or "'" in msg[i]:
                li.append(i)
        li.reverse()  # 리스트를 전환한다. (역순 계산을 해야 하기 때문)

        # 따옴표가 있는 메세지의 시작점과 끝 점을 받아 공백으로 잇는다.
        # 이은 메세지를 기존의 메세지와 교체한다.
        for i in range(0, len(li), 2):
            string = ' '.join(msg[li[i + 1]:li[i] + 1])
            del msg[li[i + 1]:li[i] + 1]
            msg.insert(li[i + 1], string)

        # 양쪽의 따옴표를 제거한다.
        # 따옴표가 중간에 존재하는 경우 따옴표를 기준으로 다시 분리한다.
        for i in msg:
            ind = msg.index(i)
            if i.startswith('"') or i.startswith("'"):
                string = i[1:]
                del msg[ind]
                msg.insert(ind, string)
            i = msg[ind]
            if i.endswith('"') or i.endswith("'"):
                string = i[:-1]
                del msg[ind]
                msg.insert(ind, string)
            i = msg[ind]
            if '"' in i:
                nw = i.split('"')
                del msg[ind]
                msg.insert(ind, nw[0])
                msg.insert(ind + 1, nw[1])
            elif "'" in i:
                nw = i.split("'")
                del msg[ind]
                msg.insert(ind, nw[0])
                msg.insert(ind + 1, nw[1])

        return msg

    else:
        return None


def sorted_nati_name():
    il = dt.InstantLoad
    nati_name = il('나라').convert_list()
    nati_name.sort()
    user = il('오너').convert_list()
    user.sort()
    nati_name.extend(user)

    return nati_name


# 예외 클래스
class ArgsError(Exception):
    # 명령어 자릿수 예외
    def __init__(self, args_needed, command):
        super().__init__(f'방금 명령어는 **{args_needed}**자리야.\n**!아리 {command}** 명령어로 자세히 알아보는 건 어때?')


class MinArgsError(Exception):
    # 최소 명령어 자릿수 예외
    def __init__(self, min_args_needed, command):
        super().__init__(f'방금 명령어는 최소 **{min_args_needed}**자리야.\n"!아리 {command}" 명령어로 자세히 알아보는 건 어때?')


class PermiError(Exception):
    # 권한 예외
    def __init__(self, perm_needed, command):
        super().__init__(f'방금 명령어는 **{perm_needed}**만 쓸 수 있어.\n"!아리 {command}" 명령어로 자세히 알아보는 건 어때?')


class DifferentTypeError(Exception):
    # 데이터 종류가 다른 예외
    def __init__(self):
        super().__init__('적당한 값을 안 넣었어.')


class DifferentNameError(Exception):
    # 검색한 나라 / 지역이 존재하지 않음을 알리는 오류
    def __init__(self):
        super().__init__('찾고자 하는 건 없어. 오타가 아닐까?')


class MinusError(Exception):
    # 음수 예외
    def __init__(self):
        super().__init__('음수 값을 넣을 순 없어.')


class SumError(Exception):
    # 합 예외
    def __init__(self, string, shouldbe, howmuch):
        if howmuch > shouldbe:
            super().__init__(f'{string} 합이 {shouldbe}이 돼야 해.\n{howmuch - shouldbe}만큼 빼면 되겠다.')
        if howmuch < shouldbe:
            super().__init__(f'{string} 합이 {shouldbe}이 돼야 해.\n{shouldbe - howmuch}만큼 더하면 되겠다.')


class DupliNatiError(Exception):
    def __init__(self):
        super().__init__('그 사람은 이미 나라가 있어.')


class UnknownError(Exception):
    def __init__(self):
        li = ['미안. 뭐라고?', '잘 모르겠어.', '글쎄.. 다시 말해줄래?']
        super().__init__(random.choice(li))


class UnitError(Exception):
    # 구매 시 100단위가 아닌 예외
    def __init__(self):
        super().__init__('꼭 100단위로 써 줘.')


class StopError(Exception):
    # 명령어 작동을 취소한 예외
    def __init__(self):
        super().__init__('하던 작업을 취소했어.')


class NotEnoughCapitalError(Exception):
    # 돈이 부족한 예외
    def __init__(self, howmuch):
        super().__init__(f'돈이 **{howmuch}**만큼 부족해..!')


class NotEnoughResourceError(Exception):
    # 자원이 부족한 예외
    def __init__(self, what, *howmuch):
        msg = ''
        if what == '식량' and howmuch[0] > 0:
            msg = f'식량이 **{howmuch[0]}**만큼 부족해..!'
        elif what == '자재' and howmuch[1] > 0:
            msg = f'자재가 **{howmuch[1]}**만큼 부족해..!'
        elif what == '다':
            msg = f'식량이 **{howmuch[0]}**, 자재가 **{howmuch[1]}**만큼 부족해..!'

        super().__init__(msg)


# 상위 명령어 클래스
class Command:
    # 명령어 전반에 대한 가이드 제공
    def __init__(self, name, permission, args_needed, description, ms_description):
        # 명령어의 요소
        self.name = name
        self.perm = permission
        self.args = args_needed
        self.desc = description
        self.ddesc = ms_description

    async def check(self, message, parsed, permission, args):
        # 기본적인 형식을 검사하는 함수
        try:
            if not args == self.args and self.args >= 1:  # 필요 명령어 자릿수가 1 이상일 때는 그 자릿수를 반드시 맞춰야 함
                raise ArgsError(self.args, parsed[0])
            elif self.args == 0:  # 필요 명령어 자릿수가 0일 때는 명령어 자릿수 제한 없음
                pass
            if not (permission == self.perm or self.perm == '모두' or permission == '관리자'):
                # 명령어 주체가 관리자거나, 권한을 맞추거나, 모두 권한 명령어여야 함
                raise PermiError(self.perm, parsed[0])
            await self.execute(message, parsed, permission, args)
        except ArgsError as Args:
            await message.channel.send(Args)
        except PermiError as Permi:
            await message.channel.send(Permi)
        except NotImplementedError:
            await message.channel.send('그건 아직 구현이 안 됐어.')

    async def execute(self, message, parsed, permission, args):
        # 실행 부분
        raise NotImplementedError()


# 하위 명령어 클래스 모음
# class (명령어영문명)
# super().__init__((명령어 이름), (명령어 사용 가능 권한), (명령어 자릿수), (명령어 설명), (명령어 세부 설명))

# 관리자
class Test(Command):
    def __init__(self):
        super().__init__('테스트', '관리자', 1, '코드 테스트용 명령어', '그런 거 없다')

    async def execute(self, message, parsed, permission, args):
        li = [member.display_name for member in message.guild.members if str(member.status) == 'online']
        expression = ['귀여워', '멋져', '좋아', '바보', '멍충이', '말미잘']
        li.remove('아리')
        for i in li:
            msg = str(i) + ' ' + str(random.choice(expression))
            await message.channel.send(msg)


class ModifyOne(Command):
    def __init__(self):
        super().__init__('고치기', '관리자', 0, '데이터 하나를 강제로 고치는 명령어야.', ms.ModifyOne.desc)

    async def execute(self, message, parsed, permission, args):
        if args == 4:
            dt.File.modifyone(parsed[0], parsed[1], parsed[2], parsed[3])
        elif args == 5:
            dt.File.modifyone(parsed[0], parsed[1], parsed[2], parsed[3], parsed[4])

        # 이전, 이후 값을 embed로 출력해야 함


class Eolmana(Command):
    def __init__(self):
        super().__init__('얼마나지났어', '관리자', 1, '얼마나 지났어?', '방법 : **!얼마나지났어**\n권한 : 관리자')

    async def execute(self, message, parsed, permission, args):
        today = datetime.datetime.today()
        y = today.year
        m = today.month
        d = today.day
        howmuch = datetime.datetime(y, m, d) - datetime.datetime(2020, 3, 11)
        await message.channel.send('오늘은 개발일부터 **{}**일이 지났어.'.format(howmuch.days))


class Stop(Command):
    def __init__(self):
        super().__init__('중지', '관리자', 1, '관리자만 명령어를 쓰게 하는 명령어야.', '방법 : **!중지**\n권한 : 관리자')

    async def execute(self, message, parsed, permission, args):
        global play_stopped
        if not play_stopped:
            play_stopped = True
            await message.channel.send('타임! 지금부턴 관리자만 명령할 수 있어.')
        elif play_stopped:
            await message.channel.send('이미 중지했어.')


class Restart(Command):
    def __init__(self):
        super().__init__('재개', '관리자', 1, '다시 유저도 명령어를 쓸 수 있게 하는 명령어야.', '방법 : **!재개**\n권한 : 관리자')

    async def execute(self, message, parsed, permission, args):
        global play_stopped
        if play_stopped:
            play_stopped = False
            await message.channel.send('타임 끝! 이젠 모두 명령할 수 있어.')
        elif not play_stopped:
            await message.channel.send('이미 재개했어.')


class MakeNation(Command):
    def __init__(self):
        super().__init__('건국', '관리자', 8, '유저 나라를 만드는 명령어야.', ms.MakeNation.desc)

    async def execute(self, message, parsed, permission, args):
        try:
            area_name, nati_name, owner = parsed[1], parsed[2], parsed[3]
            food, matl, tech, cult = int(parsed[4]), int(parsed[5]), int(parsed[6]), int(parsed[7])  # 메세지는 모두 str 취급
            limit = 20  # 초기 스탯 합이 몇이어야 하는가
            hap = food + matl + tech + cult  # 입력한 초기 스탯의 합

            if owner in king_list:
                raise DupliNatiError()
            if not (food >= 0 and matl >= 0 and tech >= 0 and cult >= 0):
                raise MinusError()
            if not hap == limit:
                raise SumError('초기 스탯', limit, hap)

            dt.Make.user_nation(area_name, nati_name, owner, food, matl, tech, cult)

            # 나라정보, 지역정보, 지역기타 데이터 찾기
            ni = dt.NationInfo('나라', nati_name)
            ai = dt.AreaInfo('나라', nati_name)
            ae = dt.AreaExtra('나라', nati_name)
            nid = ni.nati_ID[0] # 나라 ID
            aid = ni.area_ID[nid][0] # 수도 ID

            # 초기 스탯, 현재 스탯, 현재 자금, 최대 자금, 최저 자금
            max_capi = dt.Formula.max_capi(ai.tech[aid], ai.cult[aid])

            emb = discord.Embed(title='새 나라가 나타났어!')
            # "!열람"과 구분할 필요성 있음 (지금은 열람 명령어를 정의하기 이전 상태)
            # 오너명, 나라명, 지역명,
            # 초기 식량, 초기 자재, 초기 기술, 초기 문화, 현재 식량, 현재 자재,
            # 현재 자금, 최대 자금, 최저 자금,
            # 가용 정책 점수
            value = ms.MakeNation.embed.format(
                ni.nati_owner[nid], ni.nati_name[nid], ai.area_name[aid],
                ae.early_food[aid], ae.early_matl[aid],
                ae.early_tech[aid], ae.early_cult[aid],
                ai.food[aid], ai.matl[aid],
                ni.capital[nid], max_capi, dt.Formula.min_capi(max_capi), ni.investable_point[nid]
            )
            emb.add_field(name='축하해! 이제 {0}도 어엿한 [왕]이 됐어!'.format(owner), value=value)
            await message.channel.send(embed=emb)
            king_list.append(owner)
        except ValueError:
            await message.channel.send('적당한 값을 안 넣었어.')
        except DupliNatiError as Dupli:
            await message.channel.send(Dupli)
        except MinusError as Minus:
            await message.channel.send(Minus)
        except SumError as Sum:
            await message.channel.send(Sum)


class Colonize(Command):
    def __init__(self):
        super().__init__('식민', '관리자', 3, '지역을 나라의 식민지로 만드는 명령어야.', ms.Colonize.desc)

    async def execute(self, message, parsed, permission, args):
        domi_nati = parsed[1]
        colo_area = parsed[2]
        try:
            if not domi_nati in dt.InstantLoad('나라').convert_list():
                raise DifferentNameError()
            if not colo_area in dt.InstantLoad('지역').convert_list():
                raise DifferentNameError()
            result = dt.Politic.colonize(domi_nati, colo_area)
            emb = discord.Embed(title='{}의 {} 식민 완료!'.format(domi_nati, colo_area))
            emb.add_field(name='변화한 점', value=ms.Colonize.embed.format(
                result[0][1], result[1][1],
                result[0][2], result[1][2],
                result[0][3], result[1][3]
            ))
            await message.channel.send(embed=emb)
        except DifferentNameError as dif:
            await message.channel.send(dif)


class Transfer(Command):
    def __init__(self):
        super().__init__('편입', '관리자', 3, '원주민 지역을 충성스러운 식민지로 만드는 명령어야.', ms.Transfer.desc)
       
    async def execute(self, message, parsed, permission, args):
    	pass


class Merge(Command):
    def __init__(self):
        super().__init__('병합', '관리자', 3, '식민지나 편입지를 수도권으로 만드는 명령어야.', ms.Merge.desc)

    async def execute(self, message, parsed, permission, args):
    	pass

class Expel(Command):
    def __init__(self):
        super().__init__('추방', '관리자', 2, '식민지, 편입지, 병합지를 버리는 명령어야.', ms.Expel.desc)

    async def execute(self, message, parsed, permission, args):
    	pass

class Refresh(Command):
    def __init__(self):
        super().__init__('새날', '관리자', 0, '아리슬레나의 시간을 흐르게 하는 명령어야.', ms.Refresh.desc)

    async def execute(self, message, parsed, permission, args):
        if args == 1:
            dt.refresh()
            today = datetime.datetime.today()
            y = today.year
            m = today.month
            d = today.day
            times = Read.system()['refresh_times']
            await message.channel.send('{}년 {}월 {}일 제 {}주기 실행 완료!'.format(y, m, d, times))
        elif args == 2:
            howmany = int(parsed[1])
            for i in range(howmany - 1):
                Arislena.refresh()


# 왕
class CurrentStats:
	pass

class SetWarrior(Command):
    def __init__(self):
        super().__init__('공격병', '왕', 0, '자기 지역의 공격병 비율을 변경하는 명령어야.', ms.SetWarrior.desc)

    async def execute(self, message, parsed, permission, args):
        try:
            nati_name = dt.Load(message.author).nati_name
            area_names = dt.Read.my_area_names(nati_name)

            if args == 2:

                warr = int(parsed[1])
                if warr < 0 or warr > 1000:
                    raise Exception()
                for area_name in area_names:
                    changed = dt.Politic.change_warriors(area_name, warr)

                await message.channel.send('공격병 비율 : {} 조정 완료!'.format(changed))

            elif args >= 3:
                li = parsed[2:]
                warr = int(li.pop())
                for i in li:
                    if not i in area_names:
                        raise DifferentNameError()
                    else:
                        pass

                for area_name in area_names:
                    changed = Politic.change_warriors(area_name, warr)

                    await message.channel.send('{}의 공격병 비율 : {} 조정 완료!'.format(area_name, changed))

        except DifferentNameError as dif:
            await message.channel.send(dif)


class Price(Command):
    def __init__(self):
        super().__init__('가격', '왕', 0, '각종 가격 정보를 알려주는 명령어야.\n!아리, 가격 필수!', ms.Price.desc)

    async def execute(self, message, parsed, permission, args):
        embed = discord.Embed(title='가격 정보')

        store = Read.system()
        embed.add_field(name='상점 가격 정보', value=ms.PriceEmbed().format(
            round(Constant.buy_price_ratio * 100), round(Constant.sell_price_ratio * 100),
            store['food_stock'], store['matl_stock'],
            store['food_price'], store['matl_price']
        ))

        await message.channel.send(embed=embed)


class Buy(Command):
    def __init__(self):
        super().__init__('구매', '왕', 4, '자금을 써서 소유한 지역 하나의 스탯을 얻는 명령어야.', ms.Buy.desc)

    async def execute(self, message, parsed, permission, args):
        try:
            # 정보 모으기
            nati_name = Load(message.author).nati_name
            area_names = Read.my_area_names(nati_name)
            area_name = parsed[1]

            if not area_name in area_names:
                raise DifferentNameError()

            metr_tech = Calc.metr_stat(nati_name)[0]
            metr_cult = Calc.metr_stat(nati_name)[1]
            if metr_cult > Formula.max_profit_cult(metr_tech):  # 최고이득문화
                metr_cult = Formula.max_profit_cult(metr_tech)

            buy_food, buy_matl = int(parsed[2]), int(parsed[3])
            nati_id = Read.ID('나라', nati_name)[0]
            area_id = Read.ID('지역', area_name)[0]
            stnd_sum = Constant.standard_price_sum
            prot = Read.choose('나라', nati_name, 'NationExtra')['NationExtra'][3]

            capi = Read.choose('나라', nati_name, 'NationInfo')['NationInfo'][1]
            ratio = Formula.buy_price(Constant.buy_price_ratio, Constant.sell_price_ratio, metr_cult)
            food_unitprice, matl_unitprice = Read.system()['food_price'], Read.system()['matl_price']
            food_unitprice = max(food_unitprice, 4)  # 최소가 정하기
            matl_unitprice = max(matl_unitprice, 4)
            food_price = Formula.price(food_unitprice, buy_food, ratio)
            matl_price = Formula.price(matl_unitprice, buy_matl, ratio)
            S = food_price + matl_price

            tech_eff = Formula.tech_efficiency(metr_tech)
            food = int(buy_food * tech_eff)
            matl = int(buy_matl * tech_eff)

            if not buy_food % 100 == 0 or not buy_matl % 100 == 0:
                raise UnitError()
            if buy_food < 0 or buy_matl < 0:
                raise MinusError()
            if capi < S:
                raise NotEnoughCapitalError(S - capi)

            embed = discord.Embed(title='초세계 상점 이용 고마워!')
            embed.description = (ms.BuyEmbed()[0].format(S, food, matl))

            # 확인 구하기
            await message.channel.send(embed=embed)
            await message.channel.send('예상 결과야. 이대로 진행할래?\n진행하려면 **그래**라고 해.')
            if prot > 0:
                await message.channel.send('구매 진행하면 보호가 풀린다는 점 꼭 고려해!')

            def pred(m):
                return m.author == message.author and m.channel == message.channel

            msg = await ari.wait_for('message', check=pred)

            if msg.content == '그래':
                pass
            else:
                raise StopError()

            # 자금 지불
            capital_result = Arislena.modify('NationInfo', 'capital', 'ID', nati_id, '정수', '산술', -S)
            # 자원 제공
            food_result = Arislena.modify('AreaInfo', 'food', 'ID', area_id, '정수', '산술', food)
            matl_result = Arislena.modify('AreaInfo', 'matl', 'ID', area_id, '정수', '산술', matl)
            # 재고 변동
            food_stock = Arislena.modify('System', 'Value', 'ID', 'food_stock', '정수', '산술', -food)
            matl_stock = Arislena.modify('System', 'Value', 'ID', 'matl_stock', '정수', '산술', -matl)
            # 단가 변동
            new_food_unitprice = Arislena.modify('System', 'Value', 'ID', 'food_price', '실수', '고정',
                                                 Formula.new_unitprice(stnd_sum, food_stock[1]))
            new_matl_unitprice = Arislena.modify('System', 'Value', 'ID', 'matl_price', '실수', '고정',
                                                 Formula.new_unitprice(stnd_sum, matl_stock[1]))
            # 보호 0으로 변경
            if prot > 0:
                new_prot = Arislena.modify('NationExtra', 'prot_date', 'ID', nati_id, '정수', '고정', 0)
            # 첨부물 제작
            embed.add_field(name='결제 전',
                            value=ms.BuyEmbed()[1].format(capital_result[0], food_result[0], matl_result[0]))
            embed.add_field(name='결제 후',
                            value=ms.BuyEmbed()[2].format(capital_result[1], food_result[1], matl_result[1]))

            await message.channel.send(embed=embed)

        except DifferentNameError as dif:
            await message.channel.send(dif)
        except UnitError as un:
            await message.channel.send(un)
        except StopError as st:
            await message.channel.send(st)
        except MinusError as mn:
            await message.channel.send(mn)
        except NotEnoughCapitalError as n:
            await message.channel.send(n)


class Sell(Command):
    def __init__(self):
        super().__init__('판매', '왕', 4, '소유한 지역 하나의 스탯을 대가로 자금을 얻는 명령어야.', ms.Sell())

    async def execute(self, message, parsed, permission, args):
        try:
            # 정보 모으기
            nati_name = Load(message.author).nati_name  # 나라 이름
            area_names = Read.my_area_names(nati_name)  # 나라의 지역 이름
            area_name = parsed[1]  # 입력 지역명

            if not area_name in area_names:  # 입력 지역명이 데이터와 맞는지 체크
                raise DifferentNameError()

            now_stat = Read.choose('지역', area_name, 'AreaInfo')['AreaInfo']  # 현재 스탯
            now_food, now_matl = now_stat[1], now_stat[2]  # 현재 식량, 자재 스탯
            metr_tech = Calc.metr_stat(nati_name)[0]  # 수도권 기술 스탯
            metr_cult = Calc.metr_stat(nati_name)[1]  # 수도권 문화 스탯
            if metr_cult > Formula.max_profit_cult(metr_tech):  # 최고이득문화
                metr_cult = Formula.max_profit_cult(metr_tech)

            sell_food, sell_matl = int(parsed[2]), int(parsed[3])  # 입력 판매 자원량
            nati_id = Read.ID('나라', nati_name)[0]  # 나라 id
            area_id = Read.ID('지역', area_name)[0]  # 지역 id
            stnd_sum = Constant.standard_price_sum
            capi = Read.choose('나라', nati_name, 'NationInfo')['NationInfo'][1]
            prot = Read.choose('나라', nati_name, 'NationExtra')['NationExtra'][3]
            max_capi = Calc.min_max_capi(nati_name)[1]  # 최대 자금

            tech_eff = Formula.tech_efficiency(metr_tech)
            ratio = Formula.sell_price(Constant.buy_price_ratio, Constant.sell_price_ratio, tech_eff, metr_cult)
            food_unitprice, matl_unitprice = Read.system()['food_price'], Read.system()['matl_price']
            food_price = Formula.price(food_unitprice, sell_food, ratio)
            matl_price = Formula.price(matl_unitprice, sell_matl, ratio)
            S = food_price + matl_price

            if sell_food < 0 or sell_matl < 0:
                raise MinusError()
            if now_food < sell_food and now_matl < sell_matl:
                raise NotEnoughResourceError('다', sell_food - now_food, sell_matl - now_matl)
            if now_food < sell_food:
                raise NotEnoughResourceError('식량', sell_food - now_food, sell_matl - now_matl)
            if now_matl < sell_matl:
                raise NotEnoughResourceError('자재', sell_food - now_food, sell_matl - now_matl)

            embed = discord.Embed(title='초세계 상점 이용 고마워!')
            embed.description = (ms.SellEmbed()[0].format(S, sell_food, sell_matl))

            # 확인 구하기
            await message.channel.send(embed=embed)
            await message.channel.send('예상 결과야. 이대로 진행할래?\n진행하려면 **그래**라고 해.')
            if prot > 0:
                await message.channel.send('구매 진행하면 보호가 풀린다는 점 꼭 고려해!')
            if capi + S > max_capi:
                await message.channel.send('이대로 구매를 진행하면 최대 자금에 막히는데, 그래도 괜찮아?')

            def pred(m):
                return m.author == message.author and m.channel == message.channel

            msg = await ari.wait_for('message', check=pred)

            if msg.content == '그래':
                pass
            else:
                raise StopError()

            # 자원 지불
            food_result = Arislena.modify('AreaInfo', 'food', 'ID', area_id, '정수', '산술', -sell_food)
            matl_result = Arislena.modify('AreaInfo', 'matl', 'ID', area_id, '정수', '산술', -sell_matl)
            # 자금 제공
            if capi + S > max_capi:
                S = max_capi - capi
            capital_result = Arislena.modify('NationInfo', 'capital', 'ID', nati_id, '정수', '산술', S)
            # 재고 변동
            food_stock = Arislena.modify('System', 'Value', 'ID', 'food_stock', '정수', '산술', sell_food)
            matl_stock = Arislena.modify('System', 'Value', 'ID', 'matl_stock', '정수', '산술', sell_matl)
            # 단가 변동
            new_food_unitprice = Arislena.modify('System', 'Value', 'ID', 'food_price', '실수', '고정',
                                                 Formula.new_unitprice(stnd_sum, food_stock[1]))
            new_matl_unitprice = Arislena.modify('System', 'Value', 'ID', 'matl_price', '실수', '고정',
                                                 Formula.new_unitprice(stnd_sum, matl_stock[1]))
            # 보호 0으로 변경
            if prot > 0:
                new_prot = Arislena.modify('NationExtra', 'prot_date', 'ID', nati_id, '정수', '고정', 0)
            # 첨부물 제작
            embed.add_field(name='결제 전',
                            value=ms.BuyEmbed()[1].format(capital_result[0], food_result[0], matl_result[0]))
            embed.add_field(name='결제 후',
                            value=ms.BuyEmbed()[2].format(capital_result[1], food_result[1], matl_result[1]))

            await message.channel.send(embed=embed)

        except DifferentNameError as dif:
            await message.channel.send(dif)
        except MinusError as mn:
            await message.channel.send(mn)
        except NotEnoughResourceError as r:
            await message.channel.send(r)
        except StopError as st:
            await message.channel.send(st)


class Develop(Command):
    def __init__(self):
        super().__init__('발전', '왕', 4, '자금을 써서 소유한 지역 하나의 기술/문화를 올리는 명령어야.', ms.Develop())

    async def execute(self, message, parsed, permission, args):
        try:
            # 정보 모으기
            nati_name = Load(message.author).nati_name  # 나라 이름
            area_names = Read.my_area_names(nati_name)  # 나라의 지역 이름
            area_name = parsed[1]  # 입력 지역명

            if not area_name in area_names:  # 입력 지역명이 데이터와 맞는지 체크
                raise DifferentNameError()

            area_info = Read.choose('지역', area_name, 'AreaInfo')['AreaInfo']
            now_tech = area_info[3]
            now_cult = area_info[4]
        except:
            pass


class Policy(Command):
    pass


# 모두
class Ari(Command):
    def __init__(self):
        super().__init__('아리', '모두', 0, '명령어를 설명하는 명령어야.', ms.Ari.desc)

    async def execute(self, message, parsed, permission, args):

        if args == 1:
            li = list(comm_dict.keys())
            li_perm = []
            li_desc = []
            for i in li:
                li_perm.append(comm_dict[i].perm)
                li_desc.append(comm_dict[i].desc)
            n = (len(li) - 1) // 9 + 1
            for i in range(n):
                emb = discord.Embed(title="아리슬레나 명령어 목록 ({0}/{1})".format(i + 1, n), color=0x0000b7)
                if len(li) > 9:
                    for j in range(9):
                        emb.add_field(name=li[j], value=li_desc[j] + "\n" + '권한: ' + li_perm[j])
                    await message.channel.send(embed=emb)
                    del li[0:9]
                    del li_desc[0:9]
                    del li_perm[0:9]
                elif len(li) <= 9:
                    for j in range(len(li)):
                        emb.add_field(name=li[j], value=li_desc[j] + "\n" + '권한: ' + li_perm[j])
                    await message.channel.send(embed=emb)
        else:
            li = list(comm_dict.keys())
            task = ['안녕', '잘 가', '알려줘']
            hello = ['안녕!', '반가워!', '오늘 하루도 힘내!', '아리슬레나에 어서 와!', '{0}, 잘 왔어.'.format(message.author.name),
                     '오늘도 좋은 날이야.']
            bye = ['안녕~', '다음에 또 봐~', '또 와줘!', '잘 가!', '{0}, 또 보자~'.format(message.author.name)]

            if parsed[1] in li:
                emb = discord.Embed(title='{}? 설명해줄게!'.format(parsed[1]), color=0x0000b7)
                emb.description = (comm_dict[parsed[1]].desc + '\n' + comm_dict[parsed[1]].ddesc)
                await message.channel.send(embed=emb)
            elif parsed[1] in task:
                if parsed[1] == '안녕':
                    await message.channel.send(random.choice(hello))
                elif parsed[1] == '잘 가':
                    await message.channel.send(random.choice(bye))
                elif parsed[1] == '알려줘':
                    emb = discord.Embed(title='안녕? 난 아리라고 해!', color=0x0000b7)
                    emb.description = ms.ari.helpme_desc
                    emb.add_field(name='이 다음에 하게 될 것:', value=ms.ari.helpme_helpyou, inline=False)
                    await message.channel.send(embed=emb)

class Show(Command):
    def __init__(self):
        super().__init__('열람', '모두', 0, '검색어와 검색값에 해당하는 나라나 지역 정보를 열람하는 명령어야.', )

    async def execute(self, message, parsed, permission, args):
        pass

# 커맨드 사전
# 커맨드 이름 : 실행
comm_dict = {Command.name: Command for Command in [
    # 테스트 명령어(관리자)
    Test(), ModifyOne(), Eolmana(),
    # 관리자 명령어
    Stop(), Restart(), MakeNation(),
    Colonize(), Transfer(), Merge(),
    Expel(), Refresh(),
    # 왕 명령어
    CurrentStats(), SetWarrior(), Price(),
    Buy(), Sell(),
    # 모두 명령어
    Ari(), Show()
]}


@ari.event
async def on_ready():
    game = discord.Game("아리슬레나의 신 노릇")
    await ari.change_presence(status=discord.Status.online, activity=game)


@ari.event
async def on_member_update(before, after):
    if before.display_name != after.display_name:
        for m in ari.get_all_members():
            if m.display_name == after.display_name and m != after:
                await after.create_dm()
                await after.dm_channel.send("아리슬레나 내부에 중복되는 닉네임이 있습니다. 닉네임 변경이 취소됩니다.")
                await after.edit(nick=before.display_name)


@ari.event
async def on_message(message):
    global play_stopped

    name = message.author.name
    disc = message.author.discriminator
    key = name + "#" + disc
    current_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    p = parse(message.content)
    # 유저가 치는 채팅을 인식해서 나눠 p에 할당하는데,
    # 형식상 알맞지 않은 채팅(!로 시작하지 않음)이면 None을 반환한다.

    if p is not None: # 명령어가 형식상 적절할 경우
        try:
            if play_stopped and not check_permission(message.author) == '관리자':
                # '중지'되어 있으면, 관리자가 아닌 사람이 명령어를 치면 로그를 콘솔에 출력하고 await 이하를 디코에 출력한다.
                print(current_time, key, check_permission(message.author), message.content, "CANCELED!", sep="\t")
                await message.channel.send('지금은 관리자만 명령할 수 있어.')
                return
            else:
                # 명령어 상위 클래스인 Command의 check을 통해 유효성을 검사하고 명령어를 실행한다.
                await comm_dict[p[0]].check(message, p, check_permission(message.author), len(p))
                print(current_time, key, check_permission(message.author), len(p), message.content, sep="\t") # 로그 콘솔 출력
        except KeyError: # 명령어가 옳지 않으면 오류 메세지를 출력한다.
            await message.channel.send('{0} 같은 명령어는 없어. "!아리"로 명령어를 검색해 봐.'.format(p[1]))

token = dt.token.token

ari.run(token)
