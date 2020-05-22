import asyncio
import discord
import random
import math
import datetime
from shutil import copyfile

is_play_stopped = False
ari = discord.Client()

def strip(s):
    return s.lstrip().rstrip()

def parse_internal(s):
    s = strip(s)
    if len(s) == 0:
        return None
    q = ''
    t = 0
    r = []
    for i in range(len(s)):
        if s[i] == '\'' or s[i] == '\"':
            if len(q) != 0:
                if q == s[i]:
                    r.append(s[t: i])
                    t = i+1
                    q = ''
            else:
                new = strip(s[t: i])
                if len(new) != 0:
                    r.append(new)
                t = i+1
                q = s[i]
        elif len(q) == 0 and s[i].isspace():
            new = strip(s[t: i])
            if len(new) != 0:
                r.append(new)
            t = i+1
    if len(q) != 0:
        raise ValueError()
    new = strip(s[t:])
    if len(new) != 0:
        r.append(new)
    return r

def parse(s):
    if len(s) == 0:
        return None
    s = strip(s)
    if s[0].startswith('%') or s[0].startswith(' % '):
        return parse_internal(s[1:])
    else:
        return None

def approxiDiv(a, b):
    numor = int(a)
    dinomi = int(b)
    if dinomi == 0:
        raise ValueError()
    numor *= 100
    integer = numor // dinomi // 100
    approx = numor // dinomi
    integ =""
    if integer < 0:
        integer += 1
        approx += 1
        if integer == 0:
    	    integ += "-"
    approx = abs(approx)
    approx %= 100
    integ += "{0}".format(integer)
    if approx == 0:
        deci = "00"
    elif approx < 10:
        deci = "0{0}".format(approx)
    else:
        deci = "{0}".format(approx)
    result = integ + "." + deci
    return result

def randomcatch(list):
    index = random.randint(0, len(list) - 1)
    return list[index]

def decode(string):
    line = string.split("\n")
    piece = []
    for l in range(len(line)):
        piece.append(line[l].split("/"))
    return piece

def encode(data_cooked):
    return "\n".join(["/".join(d) for d in data_cooked])

def get_line(string, n):
    d = decode(string)
    return d[n]

def get_category(string, n):
    d = decode(string)
    category = []
    for l in range(len(d)):
        category.append(d[l][n])
    return category

def coord_change(string, coord, value):
    d = decode(string)
    for c in coord:
        d[c[0]][c[1]] = value
    return d

def delete_line(string, numlist):
    d = decode(string)
    rest = []
    for l in range(len(d)):
        if l not in numlist:
            rest.append(d[l])
    return rest

def unit_calc(list):
    f = int(list[0])
    m = int(list[1])
    t = int(list[2])
    unit_hp = (90000 + 240 * f + 90 * m)
    unit_ap = (3000 + 3 * f + 8 * m)
    return (unit_hp, unit_ap)

def simulate(type, a_hp, a_ap, b_hp, b_ap):
    a_min = 5
    a_range = 6
    b_min = 5
    b_range = 6
    if type == 2:
        a_min -= 2
        a_range -= 2
    a_dice = a_min + random.randint(0, a_range-1)
    b_dice = b_min + random.randint(0, b_range-1)
    a_damage = b_ap * b_dice
    b_damage = a_ap * a_dice
    a_newhp = a_hp - a_damage
    b_newhp = b_hp - b_damage
    a_newap = a_ap * a_newhp // a_hp
    b_newap = b_ap * b_newhp // b_hp
    a_damgrate = approxiDiv(a_damage, a_hp)
    b_damgrate = approxiDiv(b_damage, b_hp)
    a_report = " 측 "
    b_report = " 측 "
    victory = 0
    if a_newhp > 0 and b_newhp > 0:
        a_report += "손실율: " + a_damgrate
        b_report += "손실율: " + b_damgrate
    elif a_newhp <= 0 and b_newhp >0:
        a_report += "전멸"
        a_newhp = 0
        a_newap = 0
        b_report += "손실율: " + b_damgrate
        victory += 2
    elif a_newhp > 0:
        a_report += "손실율: " + a_damgrate
        b_report += "전멸"
        b_newhp = 0
        b_newap = 0
        victory += 1
    else:
        a_report += "전멸"
        b_report += "전멸"
        a_newhp = 0
        a_newap = 0
        b_newhp = 0
        b_newap = 0
    return (a_newhp, a_newap, b_newhp, b_newap, a_damage, b_damage, a_report, b_report, victory)

def solve(a, b, c, d, e, f):
    numer_f = e * c - b * f
    numer_m = a * f - d * c
    dnomi = a * e - b * d
    if dnomi == 0:
        raise ValueError()
    return (numer_f // dnomi , numer_m // dnomi)

def battle(type, a_data, b_data, name):
    a_hp = 0
    b_hp = 0
    a_ap = 0
    b_ap = 0
    a_fullhp = []
    b_fullhp = []
    a_fullap = []
    b_fullap = []
    a_realhp = []
    b_realhp = []
    a_realap = []
    b_realap = []
    a_rate = []
    b_rate = []
    for a in a_data:
        a_rate.append(a[3])
        calca = unit_calc([a[0], a[1], a[2]])
        a_fullhp.append(calca[0] * 1000)
        a_fullap.append(calca[1] * 1000)
        a_realhp.append(calca[0] * a[3])
        a_realap.append(calca[1] * a[3])
        a_hp += calca[0] * a[3]
        a_ap += calca[1] * a[3]
    for b in b_data:
        b_rate.append(b[3])
        calcb = unit_calc([b[0], b[1], b[2]])
        b_fullhp.append(calcb[0] * 1000)
        b_fullap.append(calcb[1] * 1000)
        b_realhp.append(calcb[0] * b[3])
        b_realap.append(calcb[1] * b[3])
        b_hp += calcb[0] * b[3]
        b_ap += calcb[1] * b[3]
    if min(a_hp, b_hp) <= 0:
        a_result = a_data
        b_result = b_data
        if a_hp > 0:
            report = name[0] + " 측 손실율: 0.00\n" + name[1] + "측 전멸"
        elif b_hp > 0:
            report = name[0] + " 측 전멸\n" + name[1] + " 측 손실율: 0.00"
        else:
            report = name[0] + " 측 전멸\n" + name[1] + " 측 전멸"
    else:
        a_result = []
        b_result = []
        a_unitsize = 0
        b_unitsize = 0
        simul = simulate(type, a_hp, a_ap, b_hp, b_ap)
        for a in a_rate:
            a_unitsize += a
        for b in b_rate:
            b_unitsize += b
        for a in range(len(a_data)):
            a_tech = a_data[a][2]
            a_newrealhp = max(a_realhp[a] - simul[4] * a_rate[a] // a_unitsize, 0)
            a_newfullhp = max(a_fullhp[a] - simul[4] * a_rate[a] // a_unitsize, a_fullhp[a] - a_realhp[a])
            a_newfullap  = a_fullap[a] * a_newfullhp // a_fullhp[a]
            if a_newfullhp == 0:
                a_newrate = 0
            else:
                a_newrate = 1000 * a_newrealhp // a_newfullhp
            solution = solve(240000, 90000, a_newfullhp - 90000000, 3000, 8000, a_newfullap - 3000000)
            a_newfood = solution[0]
            a_newmaterial = solution[1]
            a_result.append((a_newfood, a_newmaterial, a_tech, a_newrate))
        for b in range(len(b_data)):
            b_tech = b_data[b][2]
            b_newrealhp = max(b_realhp[b] - simul[5] * b_rate[b] // b_unitsize, 0)
            if type == 2:
                b_newfullhp = max(b_fullhp[b] - simul[5], 0)
                b_newfullap = b_fullap[b] * b_newfullhp // b_fullhp[b]
                b_newrate = 0
            else:
                b_newfullhp = max(b_fullhp[b] - simul[5] * b_rate[b] // b_unitsize, b_fullhp[b] - b_realhp[b])
                b_newfullap  = b_fullap[b] * b_newfullhp // b_fullhp[b]
                if b_newfullhp == 0:
                    b_newrate = 0
                else:
                    b_newrate = 1000 * b_newrealhp // b_newfullhp
            solution = solve(240000, 90000, b_newfullhp - 90000000, 3000, 8000, b_newfullap - 3000000)
            b_newfood = solution[0]
            b_newmaterial = solution[1]
            b_result.append((b_newfood, b_newmaterial, b_tech, b_newrate))
        report = name[0] + simul[6] + '\n' + name[1] + simul[7]
        v = simul[8]
        if v > 0:
            report += '\n' + name[v-1] + " 측 승리"
    return (a_result, b_result, report)
    
def nationtechlist(string):
    d = decode(string)
    namelist = get_category(string, 2)
    nameset = set()
    for n in namelist:
        if not n.startswith('-') and n != "원주민":
            nameset.add(n)
    result = []
    for nm in nameset:
        technic = 0
        for l in range(len(namelist)):
            if namelist[l] == nm:
                technic += int(d[l][5])
        result.append((nm, technic))
    return result
    
def attacklog(string):
    result = ""
    for s in range(len(string)-1):
        result += string[s+1]
    result += "F"
    return result
    
def total_economy(string, nation):
    d = decode(string)
    nationlist = get_category(string, 2)
    e = 0
    for n in range(len(nationlist)):
        if nationlist[n] == nation:
            e += int(d[n][7])
    return e
    
def get_price(string, f, m, t, techcount):
    d = decode(string)
    food = int(d[2][0]) * f
    material = int(d[2][1]) * m
    tech = (1250 + 125 * techcount) * t
    price = food + material + tech
    return price
    
def pricontrol(prime, v1, v2, v3):
    p = prime * (1000 + 3 * v1 + 10 * v2 + 30 * v3) // 1000
    return max(p, 400)
    
def native_assult(nationt, nativet):
    lot = max(0, nationt - 20)
    space = max(1, 100 - 2 * nativet)
    cast = random.randint(0, space)
    return (cast < lot)
    
def simplerepay(d, i, day):
    return (d + i * (day - 1)) // day 

def compoundrepay(d, i, day):
    if day == 1:
        return d
    else:
        return (i * (10 + i) ** (day - 1) * d) // (10 * (10 + i) ** (day - 1) - 10 ** day)

admin_list = ["DRTN#8341", "Siadel#7457", "Freiyer#6463"]

def is_admin(author):
    name = author.name
    disc = author.discriminator
    key = name + "#" + disc
    return key in admin_list

def get_channel_by_position(pos):
    for ch in ari.get_all_channels():
        if ch.position == pos and ch.type == discord.ChannelType.text:
            return ch

costume_list = []
DefaultCOSTUME = ["%", "?", ["아리시스와 인사해요!", "아리시스에게 고마움을 표해요!", "누군가의 욕설에 대해 아리시스에게 알려주어요!", "아리시스가 새로운 유저들을 위해 설명해줘요!", "아리시스가 아무말을 해요!", "아리시스가 주사위를 특정 횟수만큼 굴려요!", "아리시스가 소숫점 아래 두 자리까지 나눗셈을 해요!", "아리시스가 데이터를 공개해줘요!", "아리시스가 전쟁을 처리해요!", "아리시스가 반란을 처리해요!", "아리시스가 새로운 지역을 추가해요!", "아리시스가 지역을 없애버려요!", "아리시스가 특정 나라의 보호 여부를 바꿔요!", "아리시스가 특정한 지역을 다른 나라의 소유로 바꿔요!", "아리시스가 두 지역을 합쳐요!", "아리시스가 원주민을 생성해요!", "아리시스가 턴과 관련된 시스템들을 모두 작동시켜요!", "아리시스가 파는 스탯들을 사요!", "아리시스가 스탯들을 가져가고 돈을 줘요!", "아리시스가 돈을 빌려줘요!", "아리시스가 상환 업무를 처리해요!", "아리시스가 한 지역의 스텟을 다른 지역에 옮겨줘요!", "아리시스가 한 나라의 돈을 다른 나라에 옮겨줘요!", "아리시스가 공격병 비율을 바꾸는 작업을 해요!"], ["인사드립니다!", "염려해주신 덕분에 오늘도 무탈합니다.", "반갑습니다!", "오? 제가 여기있는 건 어떻게 아셨죠?", "안녕하세요!", "저는 안녕합니다!", "에… 저를 찾으셨나요?"], ["도움이 되었다면야!", "그리 말해주셔서 기뻐요!", "대단한 일도 아닌데요, 뭘.", "태어나길 잘했나봐요!", "친절하신 분이시네요!", "저야말로 늘 감사합니다!", "별 말씀을!"], ["감정을 낭비하지 말아주세요!", "그게 당신의 진심은 아니라고 믿어요.", "그러지 마시고 뭔가 드시고 오세요."], ["Arislena에 어서오세요~\n방금 들어오신 당신을 위해 직접 안내해드리겠습니다!", "Arislena에 오신 것을 환영합니다!\n방금 들어오신 당신을 위해 직접 안내해드리겠습니다!", "이런 곳까지 와주신 것에 감사드립니다~!\n방금 들어오신 당신을 위해 직접 안내해드리겠습니다!"], "아래의 형식에 맞춰주세요!", "아래의 범위를 지켜주세요!", "권한이 부족하여 실행할 수 없습니다.", "해당 데이터를 찾을 수 없습니다.", ["해당되는 명령어가 존재하지 않습니다."], ["처리를 완료하였습니다."], "이용해주셔서 감사합니다!", "이용해주셔서 감사합니다!", "이용 가능한 금액이 충분하지 않습니다.", "이용해주셔서 감사합니다!", "현재 해당 지역에 채무가 남아있어 대출이 불가능합니다.", "납부하신 금액이 확인되었습니다!", "무사히 전송되었습니다!", "보유 스탯이 충분하지 않습니다.", "무사히 전송되었습니다!"]
costume_list.append(DefaultCOSTUME)
DRTN8341COSTUME = ["DRTN", "8341", ["인사......", "고마워하는 거..... 받아줄게......", "누가 욕하면, 이걸로 알려 줘.......", "새로운 유저... 환영해야 하는데......", "졸려서...... 나도 몰라...... :zzz:", "주사위... 던지는 거야......", "나눗셈... 귀찮아......", "(:point_right::page_facing_up:)", "싸우는 거....... 인데, 처리하기, 엄청 귀찮아......", "왜......? 반란이라도 일으키려고......?", "그냥... 지역을 추가하는 거야......", "그 지역도... 편히 쉬게 해줄게......", "보호 여부... 변경......", "지역 소속... 변경......", "두 지역을...... 하나로 합치는 거야......", "힘들게 만드는 거니까...... 너무 괴롭히면 안 돼......?", "(:point_right::watch:)", "물건..... 뭐 살 거야......?", "스탯 필요 없으면... 뭐......", "돈 빌려줄 테니까...... 열심히 해......", "이걸로...... 돈 갚으면, 돼......", "물건... 보내줄게......", "어디다가... 부치고, 싶어......?", "공격병 비율...... 얼마면, 좋겠어......?"], ["너구나......", "깨우지 마...... :zzz:", ":zzz:...... 음냐", "그래... 너도 잘 자...... :crescent_moon:", "흐아아암...... :sparkles:", "오늘도 활기차보이네......"], ["그래......", "뭐... 고마운가보네......", "그럼, 나 좀 잘 테니까... 건들지 말아줘...... :crescent_moon:", "흐아아암...... :sparkles:"], [":zzz:......! 누구야......?", "너 때문에, 잠이 다 깨져버렸으니까...... 책임져...... :anger:", "조용히 해......", "흐아아암...... :sparkles:"], ["어서 와......\n안내해줄게......", "Arislena에 와줘서 고마워......\n안내해줄게......", "여기는, 처음이지......?\n안내해줄게......"], "이거... 여기 오류......", "흐에에..... 범위 틀렸잖아......", "이 명령어... 너는 못 쓰잖아......", "그런 데이터...... 못 찾겠어......", ["......?", "잘 못 들었어......", "무슨 소리야......?"], ["여기......", "이걸로, 됐지......?", "휴식 시간......:zzz:", "흐아아암...... :sparkles:", "(:sleeping_accommodation::zzz:)"], "여기...... 잘 써야 해......", "이정도 금액이면...... 충분하지......?", "너, 돈 모자라잖아......?", "꼭, 갚아야 해...... 알았지......?", "아직, 다 안 갚았으면서......", "갚아줘서...... 고마워.", "운반하기... 귀찮은데......", "스탯... 그만큼 안 갖고, 있잖아......?", "(:atm::money_with_wings:)"]
costume_list.append(DRTN8341COSTUME)
Siadel7457COSTUME = ["Siadel", "7457", [":sparkling_heart: 오늘의 티으라스카는 나로 시작하는 게 어때?", ":heart: 고마워할 구석이 있다는 건 살아있는 사람으로서 축복이야:star2:", ":broken_heart: 누구인가? 신성한 대화방에서 감히 욕을 지껄여!", ":sparkling_heart: 사람이 새로 들어왔는데, 그냥 가만히 있기?", ":star: Khic mi qathr fa ja.\n(아무 말이나 하게 돼)", ":heart: 널 어느 때보다도 더 열렬히 기도, 기도하게 해줄게!:notes:", ":star: 넌 이런 거 못 하지? 난 무려 소수점 두 자리까지 나눗셈이 돼☆", ":heart: 앞으로 네 친구가 될 분들이셔~", ":star: 전쟁! 파괴! 가질 수 없다면 부셔버리겠어♡", ":fist: 난 이 오너 반댈세! 자유를 위하여!", ":star: 새로운 지역은 언제나 환영이야!", ":negative_squared_cross_mark: 우리 지역이가 먼지가 됐어. X라도 눌러서 조이를 표해 보자.", ":sparkles: ｢진짜｣ 세상으로 나갈 준비가 됐어?", ":arrow_right: 경술국치의 악몽이 떠오르는구나!!", ":earth_asia: 결국 저를 무릎꿇이셨군요. 우리 애들, 책임져주세요!", ":heart: 원주민 받아라!", ":repeat: 턴종 누르고 빨리빨리 진행합시다!", ":moneybag::arrow_right::muscle: 자자, 오세요! 돈 놓고 스탯 먹기~", ":muscle::arrow_right::moneybag: 자, 이번에는 스탯 놓고 돈 먹기~", ":money_with_wings: 대출은 깔끔하게, 미래도 말끔하게!", ":ballot_box_with_check: 네가 돈을 안 갚으면, 마 그 때는 깡패가 되는 거야!", ":muscle::arrow_right: 계약에 따라, 스탯 이동!", ":moneybag::arrow_right: 계약에 따라, 자금 이동!", ":crossed_swords: 병력을 얼마나 데리고 다닐지 정해봐~"], ["안냥!", "안냥~☆", "안녕~", "안녕~☆", "그래 안녕!", "오늘 하루는 어땠어?", "왜애~♡", "누구, 저요?", "캬캬캬! 걸렸구나! 정보 채널에다 설정 500자 이상 쓰기! 안 쓰면 밴이얌~", "Si Siadel khathf ja.\n(시아델 반가워!)", "네모네모 멈뭄미 저주! 넌 미제부터 7분 돔만 돔그라미를 못 쓴다!", "나, 강림.", "오늘은 기분이 좋나 보네? 그럼 오늘은 어디를 털어볼까?", "오늘은 좋은 일이 있을 거야♡"], ["오늘은 기쁜 날이얌!", "고마우니까 오늘은 때려도 봐주면서 때리는 건 어떨까?", "고마워? 나도 고마워♡", "내가 있으니까 좋지?", "알면 잘 해~", "글케 고마운고마? ㅋㅋㅋㅋㅋㅋㅋㅋㅋㅋ", "Si thwi ruh ja~.\n(나도 기분 좋아~)"], ["욕하면 미워!", "너 원래 그런 애 아니었잖아.. 변해버린 거얌?", "오늘 무슨 일 있었어? 안아줄까?", "T le mi fa thaf na.\n(말을 멈춰.)", "그렇게 심한 말을 하다니! 나 삐졌어ㅠㅠㅠ", "나도 너 미워ㅠㅠㅠㅠ\n너랑 말 안 할 거야잉ㅠㅠ", "원주민이라도 작살내면서 화 좀 푸는 게 어떠니..?"], ["안냥! 난 아리라고 해! 앞으로 네 비서이자 심판이 될 몸이야!", "너, 강림.", "신참이네! 노래 한 곡 뽑아 봐!", "Si khac ja!\n(안녕, 처음 보네!)", "설정놀이 세상에 온 걸 환영해!", "고인물한테 박터지게 깨질 준비는 됐니♡?", "★☆★☆★☆★☆(대충 환영하는 말)☆★☆★☆★☆"], "밑에 잘 읽고 형식 맞춰서 다시 해주면 좋겠넹:star:", "밑에 잘 읽고 범위 맞춰서 다시 해주면 좋겠넹:star:", "핫! 어쩌지? 메롱! 넌 못 쓴대!!ㅋㅋㅋㅋㅋㅋㅋ", "그런 건 없는뎅? 자나 깨나 오타 조심!", ["왜? 더 궁금한 거 있어?", "잘 모르겠는뎅?", "못 알아듣겠는뎅, 혹시 그거 라녀얌?"], ["주문하신 거 나왔습니당~", "여기 바라던 거!", "이 몸께 감사하라! 나 없으면 안 될 일이지!", "요청 사항 배달 완료!", "Gaj~\n(네~)"], "우리 단골이네?ㅎㅎ 이용 고마워:heart:", "이용 고마워:heart: 돈은 계좌에 있을 거야.", "어, 혹시 너 빈털털이야? 저런:star:", "안 갚으면 알지? 나 돈 문제는 엄격해~!", "너무 욕심이 많은 거 아냐? 다른 거래방식을 택해 보렴~", "좋아, 그럼 그대로 받아갈겡~", "무역팀 타겟에 도착. 임무를 완수했습니다!", "｢힘｣이 부족하군.. ｢힘｣이 더 필요한가 본데? 크킄..", "무사히 자금 전달 완료!"]
costume_list.append(Siadel7457COSTUME)
박곰돌6127COSTUME = ["박곰돌", "6127", ["하이루~", "천만에~", "쟤 욕한대요~", "어서와, 이 동네는 처음이지?", "Dulce bellum inexpertis.", "돌려 돌려 돌림판~", "난 수학 모타는뎅...", "짜잔~", "펑!","반동이다! 전위대! 전위대!", "왜? 신도시라도 짓게?", "빠잉~", "얶께이~", "이 동네는 이제 쟤 겁니다!", "합체~!", "내 피조물님 들아 안녕?", "다 돌아가라~!", "이용해주셔서 고마워요~", "사딸라!", "돈 제대로 갚아! 알겠어?", "10원이 비는데요?", "한 상자가 비는데요?", "이체시 계좌 비밀번호 네자리를 입력하세용~", "솔직히 이런건 케바케지요 뭐."], ["하이루~", "ㅎㅇㅎㅇ", "안녕하살법!"], ["천만에~", "(뿌듯)", "(찡긋)"], ["감정 낭비 노노해!", "제정신으로 말한건 아니지?", "기분이 저기압일땐 고기 앞으로 가거라~"], ["Arislena에 어서와요! 여긴 처음이시죠~?\n방금 들어오신 당신을 위해 직접 안내해드릴게요!"], "형식이 안맞아용...", "범위가 안맞아용...", "권한이 부족해용...", "데이터가 없어용...", ["해당되는 명령어가 없어용..."], ["처리 끝!"], "이해주셔서 감사감사~", "이용해주셔서 감사감사~", "10원이 비는데요?", "이용해주셔서 감사감사~", "너 아직 빚쟁이잖아!", "전송 끝!", "전송 끝!", "스탯이 없잖아용...", "전송 끝!"]
costume_list.append(박곰돌6127COSTUME)
HRin6618COSTUME = ["HRin", "6618", ["아리가 인삿말에 화답합니다.", "아리가 쑥쓰러워 합니다.", "아리가 질색합니다.", "아리가 너 대신 안내합니다.", "아리가 곱게 샷건을 칩니다.", "아리가 주사위를 던졉니다.", "아리가 너는 모르는 근사나누기를 합니다.", "아리가 지역명을 나불댑니다. 잘났네, 잘났어.", "넌 이거 못합니다.", "넌 이거 못합니다.", "넌 이거 못합니다.", "넌 이거 못합니다.", "넌 이거 못합니다.", "넌 이거 못합니다", "넌 이거 못합니다.", "넌 이거 못합니다.", "스탯 사쉴?", "스탯 파쉴?", "돈 빌리쉴?", "아리가 징병관인 척 합니다."], ["반갑소, 화면 너머 내 친구.", "인사도 다하고 예의를 아는구만", "먼저 인사를 해? 요즘 젊은이들은 다르다더니 별로 그렇지 않네.", "어이구 흐린 양반 마침 잘 왔어."], ["으딜 감사질이야(///)","야. 야야. 감사하면 다냐?", "우잉? 내가 별 말을 다 듣네.", "너 감사가 헤픈 프렌즈구나?"], ["씨알 누군 욕 못 해서 못하는데 손가락 났다고 개소리 싸제껴도 되니?"], ["자 이대로만 하실 수 있으면 저랑 잘 지내실 수 있을 겁니다^^"],"야 그거 아니라고.", "야 범위 안에서 골라야지?", "내가 그랬잖아 너 그거 못한다고.", "몰라 멍청아!", ["그런 거 없다."], ["옛다."]]

command_list = ["인사", "고마워", "욕설", "환영", "아무말", "주사위", "근사나누기", "열람", "전쟁", "반란", "지역추가", "지역제거", "보호변경", "소유권이전", "병합", "원주민생성", "리프레시", "구매", "판매", "대출", "상환", "수출", "이체", "공격병비율"]
right_list = ["모두", "모두", "모두", "모두", "모두", "모두", "모두", "모두", "관리자", "관리자", "관리자", "관리자", "관리자", "관리자", "관리자", "관리자", "관리자", "왕", "왕", "왕", "왕", "왕", "왕", "왕"]

costume_form = '__NAME0000__COSTUME = ["__디코 이름__", "__식별번호__", ["__인사설명__", "__고마워설명__", "__욕설설명__", "__환영설명__", "__아무말설명__", "__주사위설명__", "__근사나누기설명__", "__열람설명__", "__전쟁설명__", "__반란설명__", "__지역추가설명__", "__지역제거설명__", "__보호변경설명__", "__소유권이전설명__", "__병합설명__", "__원주민생성설명__", "__리프레시설명__", "__구매설명__", "__판매설명__", "__대출설명__", "__상환설명__", "__수출설명__", "__이체설명__", "__공격병비율설명__"], ["__인사", "답변", "리스트__"], ["__고마워", "답변", "리스트__"], ["__욕설", "답변", "리스트__"], ["__환영", "답변", "리스트__"], "__형식에러메시지__", "__범위에러메시지__", "__권한제한메시지__", "__검색실패메시지__", ["__명령어이상", "메시지", "리스트__"], ["__임무완료", "메시지", "리스트__"], "__구매성공메시지__", "__판매성공메시지__", "__금액부족메시지__", "__대출메시지__", "__대출실패메시지__", "__상환메시지__", "__수출메시지__", "__스텟값부족메시지__", "__이체메시지__"]\ncostume_list.append(__NAME0000__COSTUME)'

categorist = ["지역", "오너", "나라", "식량", "자재", "기술", "비율", "자금", "보호"]

data = "ArislenaData.txt"
helper = "ArislenaHelper.txt"
receipt = "ArislenaReceipt.txt"
data_bck = "ArislenaData.bck.txt"
helper_bck = "ArislenaHelper.bck.txt"
receipt_bck = "ArislenaReceipt.bck.txt"
bck_date = "ArislenaBackupDate.txt"

@ari.event
async def on_ready():
    game = discord.Game("Arislena 관리")
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
    global is_play_stopped

    name = message.author.name
    disc = message.author.discriminator
    key = name + "#" + disc
    current_time = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    for c in costume_list:
        if c[0] == name and c[1] == disc:
            costume = c
            break
        costume = costume_list[0]
    cmd = parse(message.content)

    if cmd == None:
        return

    if is_play_stopped and not is_admin(message.author):
        print(current_time, key, message.content, "CANCELED!", sep="\t")
        await message.channel.send("플레이가 중지되었습니다. 관리자만 명령어를 사용할 수 있습니다.")
        return

    print(current_time, key, message.content, sep="\t")

    if cmd[0] == "강제종료":
        if not is_admin(message.author):
            await message.channel.send(costume[9])
        else:
            await message.channel.send("봇을 종료합니다.")
            exit(1)

    elif cmd[0] == "백업":
        if not is_admin(message.author):
            await message.channel.send(costume[9])
        elif len(cmd) == 2 and cmd[1] == "확인":
            copyfile(data, data_bck)
            copyfile(helper, helper_bck)
            copyfile(receipt, receipt_bck)
            with open(bck_date, "w") as f:
                f.write(current_time)
            await message.channel.send("데이터를 저장하였습니다.")
        else:
            try:
                last_date = open(bck_date, "r").read()
                await message.channel.send("`" + last_date + "` 에 백업한 데이터가 있습니다. 백업하시려면 `%백업 확인` 을 입력해주세요.")
            except:
                await message.channel.send("백업 데이터가 없습니다. 백업하시려면 `%백업 확인` 을 입력해주세요.")

    elif cmd[0] == "복구":
        if not is_admin(message.author):
            await message.channel.send(costume[9])
        elif len(cmd) == 2 and cmd[1] == "확인":
            try:
                last_date = open(bck_date, "r").read()
                copyfile(data_bck, data)
                copyfile(helper_bck, helper)
                copyfile(receipt_bck, receipt)
                await message.channel.send("`" + last_date + "` 에 백업한 데이터로 복구하였습니다.")
            except:
                await message.channel.send("복구 파일이 존재하지 않습니다.")
        else:
            try:
                last_date = open(bck_date, "r").read()
                await message.channel.send("`" + last_date + "` 에 백업한 데이터가 있습니다. 복구하시려면 `%복구 확인` 을 입력해주세요.")
            except:
                await message.channel.send("복구 파일이 존재하지 않습니다.")

    elif cmd[0] == "플레이중지":
        if not is_admin(message.author):
            await message.channel.send(costume[9])
        else:
            is_play_stopped = True
            await message.channel.send("플레이가 중지되었습니다. 관리자만 명령어를 사용할 수 있습니다.")
    
    elif cmd[0] == "플레이재개":
        if not is_admin(message.author):
            await message.channel.send(costume[9])
        else:
            is_play_stopped = False
            await message.channel.send("플레이가 재개되었습니다. 이제 명령어를 사용할 수 있습니다.")

    elif cmd[0] == "이름변경":
        if not is_admin(message.author):
            await message.channel.send(costume[9])
        else:
            subcommands = ["지역", "오너", "나라"]
            if len(cmd) != 4 or cmd[1] not in subcommands or cmd[2] == cmd[3]:
                await message.channel.send(costume[7])
                await message.channel.send("```%이름변경 변경값 (바꾸고 싶은 이름) (바꿀 이름)\n변경값 ∈ {지역, 오너, 나라}```\n(바꾸고 싶은 이름) ≠ (바꿀 이름)")
            else:
                data_cooked = decode(open(data, mode='rt', encoding='utf-8').read())
                def area_owner_nation(d):
                    return d[0] + "/" + d[1] + "/" + d[2]
                def same_area_owner_nation(d1, d2):
                    return d1[0] == d2[0]
                target = subcommands.index(cmd[1])
                changed = False
                result = discord.Embed(title = "변경 사항 목록")
                for d in data_cooked:
                    if d[target] == cmd[2]:
                        before = area_owner_nation(d)
                        d[target] = cmd[3]
                        after = area_owner_nation(d)
                        result.add_field(name=before, value=after)
                        changed = True
                if not changed:
                    await message.channel.send("주어진 조건에 맞는 지역을 찾을 수 없습니다.")
                else:
                    has_same = False
                    for i in range(len(data_cooked)):
                        for j in range(i + 1, len(data_cooked)):
                            if same_area_owner_nation(data_cooked[i], data_cooked[j]):
                                has_same = True
                                break
                    if has_same:
                        await message.channel.send("같은 이름을 가진 지역이 있습니다. 변경할 수 없습니다.")
                    else:
                        await message.channel.send(randomcatch(costume[12]))
                        await message.channel.send(embed=result)
                        r = open(data, mode='wt', encoding='utf-8')
                        r.write(encode(data_cooked))
                        r.close()

    elif cmd[0] == "값변경":
        if not is_admin(message.author):
            await message.channel.send(costume[9])
        else:
            subcommands = ["식량", "자재", "기술", "비율", "자금"]
            if len(cmd) != 4 or cmd[2] not in subcommands:
                await message.channel.send(costume[7])
                await message.channel.send("```%값변경 지역명 변경값 (변경할 값)\n변경값 ∈ {식량, 자재, 기술, 비율, 자금}\n(변경할 값) ∈ 정수```")
            else:
                data_cooked = decode(open(data, mode='rt', encoding='utf-8').read())
                target = None
                for d in data_cooked:
                    if d[0] == cmd[1]:
                        target = d
                        break
                if target == None:
                    await message.channel.send(costume[7])
                    await message.channel.send("```%값변경 지역명 변경값 (변경할 값)\n변경값 ∈ {식량, 자재, 기술, 비율, 자금}\n(변경할 값) ∈ 정수```")
                else:
                    result = discord.Embed(title = cmd[1] + " 값변경")
                    result.description = ("지역/오너/나라\n식량/자재/기술/비율/자금/보호")
                    target = subcommands.index(cmd[2]) + 3
                    try:
                        newval = int(cmd[3])
                        d[target] = "{0}".format(newval)
                        result.add_field(name="/".join(d[0:3]), value="/".join(d[3:]))
                        await message.channel.send(randomcatch(costume[12]))
                        await message.channel.send(embed=result)
                        r = open(data, mode='wt', encoding='utf-8')
                        r.write(encode(data_cooked))
                        r.close()
                    except:
                        await message.channel.send(costume[7])
                        await message.channel.send("```%값변경 지역명 변경값 (변경할 값)\n변경값 ∈ {식량, 자재, 기술, 비율, 자금}\n(변경할 값) ∈ 정수```")

    elif cmd[0] in ["도움", "설명", "안내"]:
        k = 0
        n = 1
        help = discord.Embed(title = "ArislenaSystem의 명령어 목록 1")
        explain = costume[2]
        for i in range(len(command_list)):
            help.add_field(name = command_list[i], value = explain[i] + "\n" + right_list[i])
            k += 1
            if k % 10 == 0:
                await message.channel.send(embed=help)
                k = 0
                n += 1
                help = discord.Embed(title = "ArislenaSystem의 명령어 목록 {0}".format(n))
        if k != 0:
            await message.channel.send(embed=help)
        
    elif cmd[0] == "인사":
        helloanswer = costume[3]
        answer = randomcatch(helloanswer)
        await message.channel.send(answer)
        
    elif cmd[0] == "고마워":
        thankanswer = costume[4]
        answer = randomcatch(thankanswer)
        await message.channel.send(answer)
        
    elif cmd[0] == "욕설":
        insultanswer = costume[5]
        answer = randomcatch(insultanswer)
        await message.channel.send(answer)
        
    elif cmd[0] == "환영":
        msglist = costume[6]
        msg = randomcatch(msglist) + "\n```1. 자기소개 채널에 자기소개\n2. 공리 확인 및 질문\n3. 나라 신청 여부 결정\n4. 정보글 작성 및 구인구직 (권장)```"
        await message.channel.send(msg)
        
    elif cmd[0] == "주사위":
        if len(cmd) != 3:
            await message.channel.send(costume[7])
            await message.channel.send("```%주사위 (최대 숫자) (횟수)\n1 ≤ 최대 숫자 ≤ 1000000\n1 ≤ 횟수 ≤ 100```")
        else:
            try:
                int(cmd[1])
                max_num = int(cmd[1])
                int(cmd[2])
                times = int(cmd[2])
                if min(max_num, times) == 0 or min(max_num, times) < 0 or max_num > 1000000 or times > 100:
                    await message.channel.send(costume[8])
                    await message.channel.send("```%주사위 (최대 숫자) (횟수)\n1 ≤ 최대 숫자 ≤ 1000000\n1 ≤ 횟수 ≤ 100```")
                else:
                    dices = []
                    total = 0
                    for t in range(times):
                        d = random.randint(1, max_num)
                        dices.append(d)
                        total += d
                    await message.channel.send(randomcatch(costume[12]))
                    await message.channel.send(dices)
                    await message.channel.send("도합 : {0}".format(total))
            except ValueError:
                await message.channel.send(costume[7])
                await message.channel.send("```%주사위 (최대 숫자) (횟수)\n1 ≤ 최대 숫자 ≤ 1000000\n1 ≤ 횟수 ≤ 100```")
                
    elif cmd[0] == "근사나누기":
        if len(cmd) != 3:
            await message.channel.send(costume[7])
            await message.channel.send("```%근사나누기 (정수 분자) (0 제외 정수 분모)\n|정수 분자| ≤ 1000000000000\n0 < |정수 분모| ≤ 1000000000000```")
        else:
            try:
                int(cmd[1])
                n = int(cmd[1])
                int(cmd[2])
                d = int(cmd[2])
                if abs(n) > 1000000000000 or abs(d) > 1000000000000 or d == 0:
                    await message.channel.send(costume[8])
                    await message.channel.send("```%근사나누기 (정수 분자) (0 제외 정수 분모)\n|정수 분자| ≤ 1000000000000\n0 < |정수 분모| ≤ 1000000000000```")
                else:
                    await message.channel.send(randomcatch(costume[12]))
                    appro = approxiDiv(n, d)
                    await message.channel.send(appro)
            except ValueError:
                await message.channel.send(costume[7])
                await message.channel.send("```%근사나누기 (정수 분자) (0 제외 정수 분모)\n|정수 분자| ≤ 1000000000000\n0 < |정수 분모| ≤ 1000000000000```")
                
    elif cmd[0] == "아무말":
        AMUMAL = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        mark = ['.', ',', '!', '?']
        msg = ""
        times = random.randint(1, 5)
        for t in range(times):
            length = random.randint(1, 14)
            for l in range(length):
                msg += randomcatch(AMUMAL)
            if t != times -1:
                msg += " "
            else:
                msg += randomcatch(mark)
        await message.channel.send(msg)
        
    elif cmd[0] == "전쟁":
        if not is_admin(message.author):
            await message.channel.send(costume[9])
        else:
            border = []
            name_check = set()
            for p in range(len(cmd)):
                if cmd[p] == "|":
                    border.append(p)
                name_check.add(cmd[p])
            if len(cmd) < 5 or len(border) != 1 or border[0] < 3 or border[0] == len(cmd) - 1:
                await message.channel.send(costume[7])
                await message.channel.send("```%전쟁 1 [(공격측) (나라들)...] | [(수비측) (나라들)...]\n%전쟁 2 [(공격측) (나라들)...] | (수비 지역)\n∀ 나라 or 지역 s.t. 비보호\n∀ 공격측 나라 s.t. 공격 가능\n나라 이름 중복 X```")
            elif len(name_check) != len(cmd):
                await message.channel.send(costume[8])
                await message.channel.send("```%전쟁 1 [(공격측) (나라들)...] | [(수비측) (나라들)...]\n%전쟁 2 [(공격측) (나라들)...] | (수비 지역)\n∀ 나라 or 지역 s.t. 비보호\n∀ 공격측 나라 s.t. 공격 가능\n나라 이름 중복 X```")
            else:
                try:
                    int(cmd[1])
                    battletype = int(cmd[1])
                    if battletype != 1 and battletype != 2:
                        await message.channel.send(costume[8])
                        await message.channel.send("```%전쟁 1 [(공격측) (나라들)...] | [(수비측) (나라들)...]\n%전쟁 2 [(공격측) (나라들)...] | (수비 지역)\n∀ 나라 or 지역 s.t. 비보호\n∀ 공격측 나라 s.t. 공격 가능\n나라 이름 중복 X```")
                    else:
                        a_team = []
                        b_team = []
                        teamcheck = True
                        for c in range(len(cmd)-2):
                            if cmd[c+2] == '|':
                                teamcheck = False
                            else:
                                if teamcheck:
                                    a_team.append(cmd[c+2])
                                else:
                                    b_team.append(cmd[c+2])
                        if battletype == 2 and len(b_team) != 1:
                            await message.channel.send(costume[7])
                            await message.channel.send("```%전쟁 1 [(공격측) (나라들)...] | [(수비측) (나라들)...]\n%전쟁 2 [(공격측) (나라들)...] | (수비 지역)\n∀ 나라 or 지역 s.t. 비보호\n∀ 공격측 나라 s.t. 공격 가능\n나라 이름 중복 X```")
                        else:
                            r = open(data, mode = 'rt', encoding='utf-8')
                            data_real = r.read()
                            r.close()
                            nationlist = get_category(data_real, 2)
                            a_data = []
                            b_data = []
                            a_linelist = []
                            b_linelist = []
                            arealist = get_category(data_real, 0)
                            error = False
                            forbidden = False
                            for a in a_team:
                                if a not in nationlist:
                                    error = True
                                else:
                                    for n in range(len(nationlist)):
                                        if nationlist[n] == a:
                                            line = get_line(data_real, n)
                                            if line[8] == "보호":
                                                forbidden = True
                                            else:
                                                a_data.append((int(line[3]), int(line[4]), int(line[5]), int(line[6])))
                                                a_linelist.append(n)
                            if battletype == 2:
                                if cmd[-1] not in arealist:
                                    error = True
                                else:
                                    for n in range(len(nationlist)):
                                        if arealist[n] == cmd[-1]:
                                            line = get_line(data_real, n)
                                            if line[2] in a_team or line[8] == "보호":
                                                forbidden = True
                                            else:
                                                b_data.append((int(line[3]), int(line[4]), int(line[5]), 1000))
                                                b_linelist.append(n)
                            else:
                                for b in b_team:
                                    if b not in nationlist:
                                        error = True
                                    else:
                                        for n in range(len(nationlist)):
                                            if nationlist[n] == b:
                                                line = get_line(data_real, n)
                                                if line[8] == "보호":
                                                    forbidden = True
                                                else:
                                                    b_data.append((int(line[3]), int(line[4]), int(line[5]), int(line[6])))
                                                    b_linelist.append(n)
                            if error:
                                await message.channel.send(costume[10])
                            elif forbidden:
                                await message.channel.send(costume[8])
                                await message.channel.send("```%전쟁 1 [(공격측) (나라들)...] | [(수비측) (나라들)...]\n%전쟁 2 [(공격측) (나라들)...] | (수비 지역)\n∀ 나라 or 지역 s.t. 비보호\n∀ 공격측 나라 s.t. 공격 가능\n나라 이름 중복 X```")
                            else:
                                await message.channel.send(randomcatch(costume[12]))
                                represename = [cmd[2], cmd[-1]]
                                result = battle(battletype, a_data, b_data, represename)
                                a_result = result[0]
                                b_result = result[1]
                                await message.channel.send(result[2])
                                a_fcoordi = []
                                b_fcoordi = []
                                a_mcoordi = []
                                b_mcoordi = []
                                a_rcoordi = []
                                b_rcoordi = []
                                for a in a_team:
                                    for n in range(len(nationlist)):
                                        if nationlist[n] == a:
                                            a_fcoordi.append((n, 3))
                                            a_mcoordi.append((n, 4))
                                            a_rcoordi.append((n, 6))
                                if battletype == 2:
                                    for n in range(len(arealist)):
                                        if arealist[n] == cmd[-1]:
                                            b_fcoordi.append((n, 3))
                                            b_mcoordi.append((n, 4))
                                            b_rcoordi.append((n, 6))
                                else:
                                    for b in b_team:
                                        for n in range(len(nationlist)):
                                            if nationlist[n] == b:
                                                b_fcoordi.append((n, 3))
                                                b_mcoordi.append((n, 4))
                                                b_rcoordi.append((n, 6))
                                d = decode(data_real)
                                for na in range(len(a_linelist)):
                                     d[a_fcoordi[na][0]][a_fcoordi[na][1]] = "{0}".format(a_result[na][0])
                                     d[a_mcoordi[na][0]][a_mcoordi[na][1]] = "{0}".format(a_result[na][1])
                                     d[a_rcoordi[na][0]][a_rcoordi[na][1]] = "{0}".format(a_result[na][3])
                                for nb in range(len(b_linelist)):
                                     d[b_fcoordi[nb][0]][b_fcoordi[nb][1]] = "{0}".format(b_result[nb][0])
                                     d[b_mcoordi[nb][0]][b_mcoordi[nb][1]] = "{0}".format(b_result[nb][1])
                                     d[b_rcoordi[nb][0]][b_rcoordi[nb][1]] = "{0}".format(b_result[nb][3])
                                linelist = []
                                for l in range(len(d)):
                                    linelist.append('/'.join(d[l]))
                                data_new = '\n'.join(linelist)
                                r = open(data, mode = 'wt', encoding='utf-8')
                                r.write(data_new)
                                r.close()
                except ValueError:
                    await message.channel.send(costume[7])
                    await message.channel.send("```%전쟁 1 [(공격측) (나라들)...] | [(수비측) (나라들)...]\n%전쟁 2 [(공격측) (나라들)...] | (수비 지역)\n∀ 나라 or 지역 s.t. 비보호\n∀ 공격측 나라 s.t. 공격 가능\n나라 이름 중복 X```")
                    
    elif cmd[0] == "열람":
        length = len(cmd)
        if length == 2:
            await message.channel.send(costume[7])
            await message.channel.send("```%열람\n%열람 범주 [(검색값) (리스트)...]\n범주 ∈ {지역, 오너, 나라, 식량, 자재, 기술, 비율, 자금, 보호}\n보호 검색값 ∈ {보호, 비보호}```")
        else:
            r = open(data, mode = 'rt', encoding='utf-8')
            data_real = r.read()
            r.close
            if length == 1:
                data_cooked = decode(data_real)
                await message.channel.send(randomcatch(costume[12]))
                result = discord.Embed(title = "지역 데이터 목록 1")
                result.description = ("지역/오너/나라\n식량/자재/기술/비율/자금/보호")
                for d in range(len(data_cooked)):
                    n = ""
                    v = ""
                    for l in range(len(data_cooked[d])):
                        if l < 3:
                            n += data_cooked[d][l]
                            if l != 2:
                                n += "/"
                        else:
                            v += data_cooked[d][l]
                            if l != len(data_cooked[d]) - 1:
                                v += "/"
                    result.add_field(name = n, value = v)
                    if d % 10 == 9:
                        await message.channel.send(embed=result)
                        result = discord.Embed(title = "지역 데이터 목록 {0}".format(d // 10 + 2))
                        result.description = ("지역/오너/나라\n식량/자재/기술/비율/자금/보호")
                if d % 10 != 9:
                    await message.channel.send(embed=result)
            else:
                searchset = set()
                for c in range(length - 2):
                    searchset.add(cmd[c+2])
                if cmd[1] not in categorist:
                    await message.channel.send(costume[8])
                    await message.channel.send("```%열람 범주 검색값\n범주 ∈ {지역, 오너, 나라, 식량, 자재, 기술, 비율, 자금, 보호}\n보호 검색값 ∈ {보호, 비보호}```")
                else:
                    error = False
                    for s in searchset:
                        if cmd[1] == "보호" and s not in ["보호", "비보호"]:
                            error = True
                    if error:
                        await message.channel.send(costume[8])
                        await message.channel.send("```%열람 범주 검색값\n범주 ∈ {지역, 오너, 나라, 식량, 자재, 기술, 비율, 자금, 보호}\n보호 검색값 ∈ {보호, 비보호}```")
                    else:
                        if length == 3:
                    	    subtitle = cmd[1] + " - " + cmd[2]
                        else:
                    	    subtitle = cmd[1] + " 복수 항목"
                        result = discord.Embed(title = subtitle + " 검색 결과 1")
                        result.description = ("지역/오너/나라\n식량/자재/기술/비율/자금/보호")
                        for i in range(len(categorist)):
                            if categorist[i] == cmd[1]:
                                break
                        cate = get_category(data_real, i)
                        data_not_found = False
                        for s in searchset:
                            if s not in cate:
                                data_not_found = True
                        if data_not_found:
                            await message.channel.send(costume[10])
                        else:
                            await message.channel.send(randomcatch(costume[12]))
                            k = -1
                            for c in range(len(cate)):
                                n = ""
                                v = ""
                                if cate[c] in searchset:
                                    k += 1
                                    line = get_line(data_real, c)
                                    for l in range(len(line)):
                                        if l < 3:
                                            n += line[l]
                                            if l != 2:
                                                n += "/"
                                        else:
                                            v += line[l]
                                            if l != len(line) - 1:
                                                v += "/"
                                    result.add_field(name = n, value = v)
                                    if k % 10 == 9:
                                        await message.channel.send(embed=result)
                                        result = discord.Embed(title = subtitle + " 검색 결과 {0}".format(k // 10 + 2))
                                        result.description = ("지역/오너/나라\n식량/자재/기술/비율/자금/보호")
                            if  k % 10 != 9:
                                await message.channel.send(embed=result)
            
    elif cmd[0] == "지역추가":
        if not is_admin(message.author):
            await message.channel.send(costume[9])
        else:
            if len(cmd) != 9:
                await message.channel.send(costume[7])
                await message.channel.send("```%지역추가 지역 오너 나라 식량 자재 기술 비율 자금```")
            else:
                try:
                    for u in range(5):
                        int(cmd[4+u])
                    r = open(data, mode = 'rt', encoding='utf-8')
                    data_real = r.read()
                    r.close()
                    data_real += "\n"
                    r = open(data, mode = 'wt', encoding='utf-8')
                    for u in range(8):
                        data_real += cmd[u+1]
                        data_real += "/"
                    data_real += "보호"
                    r.write(data_real)
                    r.close()
                    h = open(helper, mode = 'rt', encoding='utf-8')
                    helper_real = h.read()
                    h.close()
                    helper_real += "\n"
                    h = open(helper, mode = 'wt', encoding='utf-8')
                    helper_real += "{0}/{1}/{2}/{3}/{4}".format(cmd[1], cmd[2], cmd[3], cmd[4], cmd[5]) + "/FFFFFFF/0/0/0/7"
                    h.write(helper_real)
                    h.close()
                    await message.channel.send(randomcatch(costume[12]))
                except ValueError:
                    await message.channel.send(costume[7])
                    await message.channel.send("```%	지역추가 지역 오너 나라 식량 자재 기술 비율 자금```")
                    
    elif cmd[0] == "반란":
        if not is_admin(message.author):
            await message.channel.send(costume[9])
        else:
           if len(cmd) < 3:
               await message.channel.send(costume[7])
               await message.channel.send("```%반란 나라 [(해당) (지역들)...]\n지역들 ∈ 나라\n지역 ≠ 수도\n지역 ∉ 반란군```")
           else:
               r = open(data, mode = 'rt', encoding='utf-8')
               data_real = r.read()
               r.close()
               h = open(helper, mode = 'rt', encoding='utf-8')
               helper_real = h.read()
               h.close()
               arealist = get_category(data_real, 0)
               nationlist = get_category(data_real, 2)
               hnationlist = get_category(helper_real, 2)
               if cmd[1] not in nationlist:
                   await message.channel.send(costume[10])
               else:
                   data_not_found = False
                   error = False
                   coordi = []
                   for c in range(len(cmd)-2):
                       if cmd[c+2] not in arealist:
                           data_not_found = True
                       else:
                           for a in range(len(arealist)):
                               if arealist[a] == cmd[c+2]:
                                   line = get_line(data_real, a)
                                   if line[2] != cmd[1]:
                                       error = True
                   if data_not_found:
                       await message.channel.send(costume[10])
                   elif error:
                       await message.channel.send(costume[8])
                       await message.channel.send("```%반란 나라 [(해당) (지역들)...]\n지역들 ∈ 나라\n지역 ≠ 수도\n지역 ∉ 반란군```")
                   else:
                       searchset = set()
                       nationline = []
                       resistant = []
                       for hn in range(len(hnationlist)):
                           if hnationlist[hn] == cmd[1]:
                               hline = get_line(helper_real, hn)
                               if not hline[1].startswith("+"):
                                   capital = hline[0]
                       for n in range(len(nationlist)):
                           if nationlist[n] == cmd[1]:
                               nationline.append(n)
                       for n in nationline:
                           if hnationlist[n] != cmd[1]:
                               resistant.append(n)
                       d = decode(data_real)
                       hlp = decode(helper_real)
                       economy = total_economy(data_real, cmd[1])
                       for rst in resistant:
                           economy -= 7500
                           d[rst][7] = "7500"
                           d[rst][2] = "-" + cmd[1]
                           hlp[rst][2] = "-" + cmd[1]
                       for a in range(len(arealist)):
                           if arealist[a] == capital:
                               d[a][7] = "{0}".format(economy)
                       for u in range(len(d)):
                           if d[u][2] == cmd[1] or d[u][2] == "-" + cmd[1]:
                               searchset.add(d[u][0])
                       await message.channel.send(randomcatch(costume[12]))
                       linelist = []
                       for l in range(len(d)):
                           line = '/'.join(d[l])
                           linelist.append(line)
                       r = open(data, mode = 'wt', encoding='utf-8')
                       r.write('\n'.join(linelist))
                       r.close()
                       result = discord.Embed(title = cmd[1] + " 반란 결과 1")
                       result.description = ("지역/오너/나라\n식량/자재/기술/비율/자금/보호")
                       k = -1
                       for o in range(len(arealist)):
                           n = ""
                           v = ""
                           if arealist[o] in searchset:
                               k += 1
                               line = d[o]
                               for l in range(len(line)):
                                   if l < 3:
                                       n += line[l]
                                       if l != 2:
                                           n += "/"
                                   else:
                                       v += line[l]
                                       if l != len(line) - 1:
                                           v += "/"
                               result.add_field(name = n, value = v)
                               if k % 10 == 9:
                                   await message.channel.send(embed=result)
                                   result = discord.Embed(title = cmd[1] + " 반란 결과 {0}".format(k // 10 + 2))
                                   result.description = ("지역/오너/나라\n식량/자재/기술/비율/자금/보호")
                       if  k % 10 != 9:
                           await message.channel.send(embed=result)
                       
    elif cmd[0] == "보호변경":
        if not is_admin(message.author):
            await message.channel.send(costume[9])
        else:
            if len(cmd) != 2:
                await message.channel.send(costume[7])
                await message.channel.send("```%보호변경 오너명```")
            else:
                r = open(data, mode = 'rt', encoding='utf-8')
                data_real = r.read()
                r.close()
                owners = get_category(data_real, 1)
                if cmd[1] not in owners:
                    await message.channel.send(costume[10])
                else:
                    coordi = []
                    searchset = set()
                    d = decode(data_real)
                    for o in range(len(owners)):
                        if owners[o] == cmd[1]:
                            coordi.append((o, 8))
                    if d[coordi[0][0]][8] == "보호":
                        data_new = coord_change(data_real, coordi, "비보호")
                    else:
                        data_new = coord_change(data_real, coordi, "보호")
                    for u in range(len(data_new)):
                        if data_new[u][1] == cmd[1]:
                            searchset.add(data_new[u][1])
                    linelist = []
                    for l in range(len(data_new)):
                        line = '/'.join(data_new[l])
                        linelist.append(line)
                    r = open(data, mode = 'wt', encoding='utf-8')
                    r.write('\n'.join(linelist))
                    r.close()
                    await message.channel.send(randomcatch(costume[12]))
                    result = discord.Embed(title = cmd[1] + " 보호변경 결과 1")
                    result.description = ("지역/오너/나라\n식량/자재/기술/비율/자금/보호")
                    k = -1
                    for o in range(len(owners)):
                        n = ""
                        v = ""
                        if owners[o] in searchset:
                            k += 1
                            line = data_new[o]
                            for l in range(len(line)):
                                if l < 3:
                                    n += line[l]
                                    if l != 2:
                                        n += "/"
                                else:
                                    v += line[l]
                                    if l != len(line) - 1:
                                        v += "/"
                            result.add_field(name = n, value = v)
                            if k % 10 == 9:
                                await message.channel.send(embed=result)
                                result = discord.Embed(title = cmd[1] + " 보호변경 결과 {0}".format(k // 10 + 2))
                                result.description = ("지역/오너/나라\n식량/자재/기술/비율/자금/보호")
                    if  k % 10 != 9:
                        await message.channel.send(embed=result)
                    
    elif cmd[0] == "지역제거":
        if not is_admin(message.author):
            await message.channel.send(costume[9])
        else:
            if len(cmd) == 1:
                await message.channel.send(costume[7])
                await message.channel.send("```%지역제거 [(제거될) (지역명)...]```")
            else:
                r = open(data, mode = 'rt', encoding='utf-8')
                data_real = r.read()
                r.close()
                cate = get_category(data_real, 0)
                data_not_found = False
                for c in range(len(cmd)-1):
                    if cmd[c+1] not in cate:
                        data_not_found = True
                if data_not_found:
                    await message.channel.send(costume[10])
                else:
                    h = open(helper, mode = 'rt', encoding='utf-8')
                    helper_real = h.read()
                    h.close()
                    delete_reserve = set()
                    for c in range(len(cmd)-1):
                        for n in range(len(cate)):
                            if cmd[c+1] == cate[n]:
                                delete_reserve.add(n)
                    data_new = delete_line(data_real, delete_reserve)
                    helper_new = delete_line(helper_real, delete_reserve)
                    linelist = []
                    helplist = []
                    for l in range(len(data_new)):
                        line = '/'.join(data_new[l])
                        help = '/'.join(helper_new[l])
                        linelist.append(line)
                        helplist.append(help)
                    r = open(data, mode = 'wt', encoding='utf-8')
                    r.write('\n'.join(linelist))
                    r.close()
                    h = open(helper, mode = 'wt', encoding='utf-8')
                    h.write('\n'.join(helplist))
                    h.close()
                    await message.channel.send(randomcatch(costume[12]))
                    
    elif cmd[0] == "소유권이전":
        if not is_admin(message.author):
            await message.channel.send(costume[9])
        else:
            if len(cmd) < 3:
                await message.channel.send(costume[7])
                await message.channel.send("```%소유권이전 나라 [(지역) (이름들)...]\n∀지역 ∈ 나라```")
            else:
                r = open(data, mode = 'rt', encoding='utf-8')
                data_real = r.read()
                r.close()
                h = open(helper, mode = 'rt', encoding='utf-8')
                helper_real = h.read()
                h.close()
                arealist = get_category(data_real, 0)
                nationlist = get_category(data_real, 2)
                hnationlist = get_category(helper_real, 2)
                data_not_found = False
                areacheck = []
                if cmd[1] not in nationlist:
                    data_not_found = True
                for c in range(len(cmd)-2):
                    if cmd[c+2] not in arealist:
                        data_not_found = True
                    else:
                        areacheck.append(cmd[c+2])
                if data_not_found:
                    await message.channel.send(costume[10])
                else:
                    for hn in range(len(hnationlist)):
                        if hnationlist[hn] == cmd[1]:
                            hline = get_line(helper_real, hn)
                            if not hline[1].startswith("+"):
                                capital = hline[0]
                    coordi = []
                    searchset = set()
                    d = decode(data_real)
                    for a in range(len(arealist)):
                        if arealist[a] in areacheck:
                            coordi.append((a, 2))
                        elif arealist[a] == capital:
                            capitaline = a
                    economy = total_economy(data_real, cmd[1])
                    data_new = coord_change(data_real, coordi, cmd[1])
                    for x in coordi:
                        economy += int(d[x[0]][7])
                        data_new[x[0]][7] = "0"
                    data_new[capitaline][7] = "{0}".format(economy)
                    for u in range(len(data_new)):
                        if data_new[u][0] in areacheck:
                            searchset.add(data_new[u][0])
                    linelist = []
                    for l in range(len(data_new)):
                        line = '/'.join(data_new[l])
                        linelist.append(line)
                    r = open(data, mode = 'wt', encoding='utf-8')
                    r.write('\n'.join(linelist))
                    r.close()
                    await message.channel.send(randomcatch(costume[12]))
                    result = discord.Embed(title = cmd[1] + " 소유권이전 결과 1")
                    result.description = ("지역/오너/나라\n식량/자재/기술/비율/자금/보호")
                    k = -1
                    for a in range(len(arealist)):
                        n = ""
                        v = ""
                        if arealist[a] in searchset:
                            k += 1
                            line = data_new[a]
                            for l in range(len(line)):
                                if l < 3:
                                    n += line[l]
                                    if l != 2:
                                        n += "/"
                                else:
                                    v += line[l]
                                    if l != len(line) - 1:
                                        v += "/"
                            result.add_field(name = n, value = v)
                            if k % 10 == 9:
                                await message.channel.send(embed=result)
                                result = discord.Embed(title = cmd[1] + " 소유권이전 결과 {0}".format(k // 10 + 2))
                                result.description = ("지역/오너/나라\n식량/자재/기술/비율/자금/보호")
                    if  k % 10 != 9:
                        await message.channel.send(embed=result)

    elif cmd[0] == "원주민생성":
        if not is_admin(message.author):
            await message.channel.send(costume[9])
        else:
            r = open(data, mode = 'rt', encoding='utf-8')
            data_real = r.read()
            r.close()
            h = open(helper, mode = 'rt', encoding='utf-8')
            helper_real = h.read()
            h.close()
            playerlist = get_category(helper_real, 1)
            nativenumb = 0
            for o in range(len(playerlist)):
                if playerlist[o] == "???" or playerlist[o] == "+???":
                    nativenumb += 1
            if nativenumb < 10:
                nativecode = "00{0}".format(nativenumb)
            elif nativenumb < 100:
                nativecode = "0{0}".format(nativenumb)
            else:
                nativecode = "{0}".format(nativenumb)
            statcode = random.randint(0, 135)
            trinum = [1, 3, 6, 10, 15, 21, 28, 36, 45, 55, 66, 78, 91, 105, 120, 136]
            for t in range(len(trinum)):
                if statcode < trinum[t]:
                    tech = 15 - t
                    food = random.randint(0, t)
                    material = t - food
                    break
            techlist = nationtechlist(data_real)
            techeck = []
            for t in techlist:
                techeck.append(int(t[1]))
            hightech = max(techeck)
            if hightech > 16:
                food += 1
                material += 1
                tech += 1
            if hightech > 26:
                food += 2
                material += 2
                tech += 2
            if hightech > 41:
                food += 4
                material += 4
                tech += 4
            if hightech > 70:
                food += 8
                material += 8
                tech += 8
            food *= 100
            material *= 100
            rate = random.randint(0, 100)
            dline = nativecode + "/???/원주민" + nativecode + "/{0}/{1}/{2}/{3}/10000/비보호".format(food, material, tech, rate)
            hline = nativecode + "/???/원주민" + nativecode + "/{0}/{1}".format(food, material) + "/FFFFFFF/0/0/0/0"
            r = open(data, mode = 'wt', encoding='utf-8')
            data_real += "\n" + dline
            r.write(data_real)
            r.close()
            h = open(helper, mode = 'wt', encoding='utf-8')
            helper_real += "\n" + hline
            h.write(helper_real)
            h.close()
            await message.channel.send(randomcatch(costume[12]))
            
    elif cmd[0] == "병합":
        if not is_admin(message.author):
            await message.channel.send(costume[9])
        else:
            if len(cmd) != 3:
                await message.channel.send(costume[7])
                await message.channel.send("```%병합 나라 지역\n(지역 ∈ 나라) s.t. 병합 X\n나라 병합지역 수 < 병합횟수\nor\n나라 s.t. 반란중\n지역 ∈ 나라```")
            else:
                r = open(data, mode = 'rt', encoding='utf-8')
                data_real = r.read()
                r.close()
                arealist = get_category(data_real, 0)
                nationlist = get_category(data_real, 2)
                if cmd[1] not in nationlist or cmd[2] not in arealist:
                    await message.channel.send(costume[10])
                else:
                    h = open(helper, mode = 'rt', encoding='utf-8')
                    helper_real = h.read()
                    h.close()
                    for a in range(len(arealist)):
                        if arealist[a] == cmd[2]:
                            break
                    dline = get_line(data_real, a)
                    hline = get_line(helper_real, a)
                    if cmd[1].startswith('-'):
                        realnation = ""
                        for s in range(len(cmd[1])-1):
                            realnation += cmd[1][s+1]
                        if dline[2] != realnation:
                            await message.channel.send(costume[8])
                            await message.channel.send("```%병합 나라 지역\n(지역 ∈ 나라) s.t. 병합 X\n나라 병합지역 수 < 병합횟수\nor\n나라 s.t. 반란중\n지역 ∈ 나라```")
                        else:
                            d = decode(data_real)
                            hlp = decode(helper_real)
                            new_owner = "+" + dline[1]
                            d[a][1] = dline[1]
                            d[a][2] = cmd[1]
                            hlp[a][1] = new_owner
                            hlp[a][2] = cmd[1]
                            linelist = []
                            for l in range(len(d)):
                                line = '/'.join(d[l])
                                linelist.append(line)
                            r = open(data, mode = 'wt', encoding='utf-8')
                            r.write('\n'.join(linelist))
                            r.close()
                            linelist = []
                            for l in range(len(hlp)):
                                line = '/'.join(hlp[l])
                                linelist.append(line)
                            h = open(helper, mode = 'wt', encoding='utf-8')
                            h.write('\n'.join(linelist))
                            h.close()
                            result = discord.Embed(title = cmd[1] + " 병합 결과")
                            result.description = ("지역/오너/나라\n식량/자재/기술/비율/자금/보호")
                            result.add_field(name = d[a][0] + "/" + d[a][1] + "/" + d[a][2], value = d[a][3] + "/" + d[a][4] + "/" + d[a][5] + "/" + d[a][6] + "/" + d[a][7] + "/" + d[a][8])
                            await message.channel.send(embed = result)
                    else:
                        if dline[2] != cmd[1] or "+" in hline[2]:
                            await message.channel.send(costume[8])
                            await message.channel.send("```%병합 나라 지역\n(지역 ∈ 나라) s.t. 병합 X\n나라 병합지역 수 < 병합횟수\nor\n나라 s.t. 반란중\n지역 ∈ 나라```")
                        else:
                            ownerlist = get_category(data_real, 1)
                            hownerlist = get_category(helper_real, 1)
                            hnationlist = get_category(helper_real, 2)
                            techlist = nationtechlist(data_real)
                            techeck = []
                            for t in techlist:
                                if t[0] == cmd[1]:
                                    techeck.append(t[1])
                            if techeck[0] < 6:
                                max_merge = 0
                            elif techeck[0] < 14:
                                max_merge = 1
                            elif techeck[0] < 25:
                                max_merge = 2
                            elif techeck[0] < 71:
                                max_merge = 3
                            else:
                                max_merge = 4
                            nationarea = ""
                            mergedata = []
                            for a in range(len(arealist)):
                                dline = get_line(data_real, a)
                                hline = get_line(helper_real, a)
                                if dline[2] == cmd[1]:
                                    nationarea += dline[0]
                                    if "+" in hline[2]:
                                        mergedata.append(dline[0])
                            if len(mergedata) >= max_merge:
                                await message.channel.send(costume[8])
                                await message.channel.send("```%병합 나라 지역\n(지역 ∈ 나라) s.t. 병합 X\n나라 병합지역 수 < 병합횟수\nor\n나라 s.t. 반란중\n지역 ∈ 나라```")
                            else:
                                await message.channel.send(randomcatch(costume[12]))
                                for a in range(len(arealist)):
                                    if arealist[a] == cmd[2]:
                                        break
                                for n in range(len(nationlist)):
                                    if nationlist[n] == cmd[1]:
                                        howner = hownerlist[n]
                                        if hnationlist[n] == cmd[1] and "+" not in howner:
                                            cpt = n
                                            break
                                capitalowner = ownerlist[cpt]
                                d = decode(data_real)
                                hlp = decode(helper_real)
                                if d[a][1] == "???":
                                    new_owner = "+???"
                                else:
                                    new_owner = "+" + d[n][1]
                                d[a][1] = capitalowner
                                hlp[a][1] = new_owner
                                hlp[a][2] = cmd[1]
                                linelist = []
                                for l in range(len(d)):
                                    line = '/'.join(d[l])
                                    linelist.append(line)
                                r = open(data, mode = 'wt', encoding='utf-8')
                                r.write('\n'.join(linelist))
                                r.close()
                                linelist = []
                                for l in range(len(hlp)):
                                    line = '/'.join(hlp[l])
                                    linelist.append(line)
                                h = open(helper, mode = 'wt', encoding='utf-8')
                                h.write('\n'.join(linelist))
                                h.close()
                                result = discord.Embed(title = cmd[1] + " 병합 결과")
                                result.description = ("지역/오너/나라\n식량/자재/기술/비율/자금/보호")
                                result.add_field(name = d[a][0] + "/" + d[a][1] + "/" + d[a][2], value = d[a][3] + "/" + d[a][4] + "/" + d[a][5] + "/" + d[a][6] + "/" + d[a][7] + "/" + d[a][8])
                                await message.channel.send(embed = result)
                                
    elif cmd[0] == "공격병비율":
        r = open(data, mode = 'rt', encoding='utf-8')
        data_real = r.read()
        r.close()
        ownerlist = get_category(data_real, 1)
        disp = message.author.display_name
        if disp not in ownerlist:
            await message.channel.send(costume[9])
        else:
            if len(cmd) < 3 or len(cmd) % 2 != 1:
                await message.channel.send(costume[7])
                await message.channel.send("```%공격병비율 [(지역) (비율)]...\n지역 ∈ 본인 나라\n0 ≤ 비율 ≤ 1000```")
            else:
                arealist = get_category(data_real, 0)
                error = False
                data_not_found = False
                h = open(helper, mode = 'rt', encoding='utf-8')
                helper_real = h.read()
                h.close()
                helpowner = get_category(helper_real, 1)
                for n in range(len(helpowner)):
                    if helpowner[n] == disp:
                        helpline = get_line(helper_real, n)
                        ownation = helpline[2]
                try:
                    for n in range((len(cmd)-1)//2):
                        position = 2 * n + 2
                        int(cmd[position])
                        area = cmd[position - 1]
                        rate = int(cmd[position])
                        areacheck = []
                        if area not in arealist:
                            data_not_found = True
                        else:
                            areacheck.append(area)
                            for a in range(len(arealist)):
                                if arealist[a] == area:
                                    line = get_line(data_real, a)
                                    break
                            if rate < 0 or rate > 1000 or line[2] != ownation:
                                error = True
                    if error:
                        await message.channel.send(costume[8])
                        await message.channel.send("```%공격병비율 [(지역) (비율)]...\n지역 ∈ 본인 나라\n0 ≤ 비율 ≤ 1000```")
                    elif data_not_found:
                        await message.channel.send(costume[10])
                    else:
                        searchset = set()
                        data_new = decode(data_real)
                        for n in range((len(cmd)-1)//2):
                            position = 2 * n + 2
                            area = cmd[position - 1]
                            rate = int(cmd[position])
                            for a in range(len(arealist)):
                                if arealist[a] == area:
                                    data_new[a][6] = "{0}".format(rate)
                        for u in range(len(data_new)):
                            if data_new[u][0] in areacheck:
                                searchset.add(data_new[u][0])
                        linelist = []
                        for l in range(len(data_new)):
                            line = '/'.join(data_new[l])
                            linelist.append(line)
                        r = open(data, mode = 'wt', encoding='utf-8')
                        r.write('\n'.join(linelist))
                        r.close()
                        await message.channel.send(randomcatch(costume[12]))
                        result = discord.Embed(title = ownation + " 공격병비율 변경 결과 1")
                        result.description = ("지역/오너/나라\n식량/자재/기술/비율/자금/보호")
                        k = -1
                        for a in range(len(arealist)):
                            n = ""
                            v = ""
                            if arealist[a] in areacheck:
                                k += 1
                                line = data_new[a]
                                for l in range(len(line)):
                                    if l < 3:
                                        n += line[l]
                                        if l != 2:
                                            n += "/"
                                    else:
                                        v += line[l]
                                        if l != len(line) - 1:
                                            v += "/"
                                result.add_field(name = n, value = v)
                                if k % 10 == 9:
                                    await message.channel.send(embed=result)
                                    result = discord.Embed(title = ownation + " 공격병비율 변경 결과 {0}".format(k // 10 + 2))
                                    result.description = ("지역/오너/나라\n식량/자재/기술/비율/자금/보호")
                        if k % 10 != 9:
                            await message.channel.send(embed=result)
                except ValueError:
                    await message.channel.send(costume[7])
                    await message.channel.send("```%공격병비율 [(지역) (비율)]...\n지역 ∈ 본인 나라\n0 ≤ 비율 ≤ 1000```")
                   
    elif cmd[0] == "리프레시":
        if not is_admin(message.author):
            await message.channel.send(costume[9])
        else:
            r = open(data, mode = 'rt', encoding='utf-8')
            data_real = r.read()
            r.close()
            h = open(helper, mode = 'rt', encoding='utf-8')
            helper_real = h.read()
            h.close()
            c = open(receipt, mode = 'rt', encoding='utf-8')
            receipt_real = c.read()
            c.close()
            arealist = get_category(data_real, 0)
            ownerlist = get_category(data_real, 1)
            playerlist = get_category(helper_real, 1)
            dnationlist = get_category(data_real, 2)
            hnationlist = get_category(helper_real, 2)
            report = ""
            d = decode(data_real)
            hr = decode(helper_real)
            cp = decode(receipt_real)
            for a in range(len(arealist)):
                dline = d[a]
                hline = hr[a]
                capitalcheck = dnationlist[a] == hnationlist[a] or "+" in playerlist[a]
                nation = dnationlist[a]
                for n in range(len(hnationlist)):
                    if hnationlist[n] == nation and not playerlist[n].startswith("+"):
                        dcapitaline = get_line(data_real, n)
                        hcapitaline = get_line(helper_real, n)
                        break
                food_now = int(dline[3])
                food_default = int(hline[3])
                material_now = int(dline[4])
                material_default = int(hline[4])
                areatech = int(dline[5])
                if food_now >= 0:
                    if food_now < food_default:
                        food_add = 15 * food_default // 100
                        food_new = min(food_default, food_now + food_add)
                    else:
                        food_new = food_default
                else:
                    food_new = food_now
                if material_now >= 0:
                    if material_now < material_default:
                        material_add = 15 * material_default // 100
                        material_new = min(material_default, material_now + material_add)
                    else:
                        material_new = material_default
                else:
                    material_new = material_now
                capitaltech = int(dcapitaline[5])
                resistchance = random.randint(1, 100)
                rebel = max(10, areatech - capitaltech + 3)
                if dline[1] != hline[1] and "+" not in hline[1]:
                    if dline[1] == "원주민":
                        rebel += 10
                        if resistchance <= rebel:
                            await get_channel_by_position(0).send("원주민 " + dline[0] + " 반란")
                            nation_new = "-" + nation
                        else:
                            nation_new = nation
                    else:
                        rebel *= 5
                        rebel += 10
                        if resistchance <= rebel:
                            await get_channel_by_position(0).send(dline[0] + " 반란 기회")
                            nation_new = nation
                        else:
                            nation_new = nation
                else:
                    nation_new = nation
                log = hline[5]
                log_new = attacklog(log)
                economy = int(dline[6])
                dept = int(hline[7])
                inter = hline[8]
                if inter.startswith("+"):
                    interest = int(inter[1:len(inter)])
                else:
                    interest = (10 + int(inter)) * dept // 10
                dept_new = dept + interest
                alarm = int(hline[9])
                if alarm == 0:
                    alarm_new = alarm
                else:
                    alarm_new = alarm - 1
                    if alarm_new == 0:
                        await get_channel_by_position(0).send(dline[2] + " 보호 기간 만료")
                d[a][2] = nation_new
                d[a][3] = "{0}".format(food_new)
                d[a][4] = "{0}".format(material_new)
                hr[a][5] = "{0}".format(log_new)
                hr[a][7] = "{0}".format(dept_new)
                hr[a][9] = "{0}".format(alarm_new)
            food_prime = int(cp[2][0])
            oldestf = int(cp[0][2])
            olderf = int(cp[1][2])
            oldf = int(cp[2][2])
            material_prime = int(cp[2][1])
            oldestm = int(cp[0][3])
            olderm = int(cp[1][3])
            oldm = int(cp[2][3])
            food_latest = pricontrol(food_prime, oldestf, olderf, oldf)
            material_latest = pricontrol(material_prime, oldestm, olderm, oldm)
            receipt_new = delete_line(receipt_real, [0])
            linelist = []
            for l in range(len(d)):
                line = '/'.join(d[l])
                linelist.append(line)
            data_new = '\n'.join(linelist)
            r = open(data, mode = 'wt', encoding='utf-8')
            r.write(data_new)
            r.close()
            linelist = []
            for l in range(len(hr)):
                line = '/'.join(hr[l])
                linelist.append(line)
            h = open(helper, mode = 'wt', encoding='utf-8')
            h.write('\n'.join(linelist))
            h.close()
            linelist = []
            for l in range(len(receipt_new)):
                line = '/'.join(receipt_new[l])
                linelist.append(line)
            linelist.append("{0}/{1}/0/0".format(food_latest, material_latest))
            c = open(receipt, mode = 'wt', encoding='utf-8')
            c.write('\n'.join(linelist))
            c.close()
            nativenumb = 0
            for o in range(len(playerlist)):
                if playerlist[o] == "???" or playerlist[o] == "+???":
                    nativenumb += 1
                    for nt in nationtechlist(data_new):
                        for p in range(len(playerlist)):
                            if playerlist[p] != "???" and playerlist[p] != "+???" and nt[0] == dnationlist[p]:
                                break
                        nationtech = nt[1]
                        nativetech = int(d[n][5])
                        if native_assult(nationtech, nativetech):
                            await get_channel_by_position(0).send("원주민 " + d[n][0] + " 나라 " + nt[0] +"에 선전포고")
            nativembed = discord.Embed(title = "원주민 리프레시 결과 1")
            nativembed.description = ("지역/오너/나라\n식량/자재/기술/비율/자금/보호")
            k = -1
            for a in range(len(arealist)):
                n = ""
                v = ""
                if playerlist[a] == "???" or playerlist[a] == "+???":
                    k += 1
                    line = d[a]
                    for l in range(len(line)):
                        if l < 3:
                            n += line[l]
                            if l != 2:
                                n += "/"
                        else:
                            v += line[l]
                            if l != len(line) - 1:
                                v += "/"
                    nativembed.add_field(name = n, value = v)
                    if k % 10 == 9:
                        await get_channel_by_position(0).send(embed=nativembed)
                        nativembed = discord.Embed(title = "원주민 리프레시 결과 {0}".format(k // 10 + 2))
                        nativembed.description = ("지역/오너/나라\n식량/자재/기술/비율/자금/보호")
            if k % 10 != 9:
                await get_channel_by_position(0).send(embed=nativembed)
            await get_channel_by_position(1).send("식량1:{0}\n자재1:{1}\n기술1:1250+(거래 횟수)*125\n• 기술에 따라 거래/판매시에 일정량의 이득이 있을 수 있음".format(food_latest, material_latest))
            valid_area = []
            for a in range(len(arealist)):
                if hr[a][1] != "???" and hr[a][1] != "+???":
                    valid_area.append(d[a])
            position = 33 + nativenumb + 1
            for va in range(len(valid_area)):
                playerembed = discord.Embed(title = valid_area[va][0] + " 리프레시 결과")
                playerembed.description = ("지역/오너/나라\n식량/자재/기술/비율/자금/보호")
                playerembed.add_field(name = valid_area[va][0] + "/" + valid_area[va][1] + "/" + valid_area[va][2], value = valid_area[va][3] + "/" + valid_area[va][4] + "/" + valid_area[va][5] + "/" + valid_area[va][6] + "/" + valid_area[va][7] + "/" + valid_area[va][8])
                await get_channel_by_position(0).send(embed=playerembed)
            now = datetime.datetime.now()
            msg = "{0}년 {1}월 {2}일 이전 데이터 갱신 완료\n시스템 재시작".format(now.year, now.month, now.day)
            await get_channel_by_position(0).send(msg)
            
    elif cmd[0] == "구매":
        r = open(data, mode = 'rt', encoding='utf-8')
        data_real = r.read()
        r.close()
        ownerlist = get_category(data_real, 1)
        disp = message.author.display_name
        if disp not in ownerlist:
            await message.channel.send(costume[9])
        else:
            if len(cmd) != 5:
                await message.channel.send(costume[7])
                await message.channel.send("```%구매 지역 식량 자재 기술\n지역 ∈ 본인 나라\nmin(식량, 자재, 기술) ≥ 0```")
            else:
                try:
                    int(cmd[2])
                    food_request = int(cmd[2])
                    int(cmd[3])
                    material_request = int(cmd[3])
                    int(cmd[4])
                    tech_request = int(cmd[4])
                    if min(food_request, material_request, tech_request) < 0:
                        await message.channel.send(costume[8])
                        await message.channel.send("```%구매 지역 식량 자재 기술\n지역 ∈ 본인 나라\nmin(식량, 자재, 기술) ≥ 0```")
                    else:
                        arealist = get_category(data_real, 0)
                        if cmd[1] not in arealist:
                            await message.channel.send(costume[10])
                        else:
                            h = open(helper, mode = 'rt', encoding='utf-8')
                            helper_real = h.read()
                            h.close()
                            nationlist = get_category(data_real, 2)
                            hownerlist = get_category(helper_real, 1)
                            hnationlist = get_category(helper_real, 2)
                            for a in range(len(arealist)):
                                nation = nationlist[a]
                                if arealist[a] == cmd[1]:
                                    break
                            for n in range(len(nationlist)):
                                if nationlist[n] == nation:
                                    howner = hownerlist[n]
                                    if hnationlist[n] == nation and "+" not in howner:
                                        cpt = n
                                        break
                            capitalowner = ownerlist[cpt]
                            if disp != capitalowner:
                                await message.channel.send(costume[9])
                            else:
                                d = decode(data_real)
                                food = int(d[a][3])
                                material = int(d[a][4])
                                tech = int(d[a][5])
                                economy = int(d[cpt][7])
                                hlp = decode(helper_real)
                                for n in range(len(nationlist)):
                                   if nationlist[n] == nation and d[n][8] == "보호":
                                       d[n][8] = "비보호"
                                       hlp[n][9] = "0"
                                techcount = int(hlp[cpt][6])
                                c = open(receipt, mode = 'rt', encoding='utf-8')
                                receipt_real = c.read()
                                c.close()
                                rcp = decode(receipt_real)
                                f_exvolume = int(rcp[2][2])
                                m_exvolume = int(rcp[2][3])
                                price = get_price(receipt_real, food_request, material_request, tech_request, techcount)
                                if price > economy:
                                    await message.channel.send(costume[15])
                                else:
                                    new_economy = economy - price
                                    d[a][3] = "{0}".format(food + food_request * (100 + 7 * tech))
                                    d[a][4] = "{0}".format(material + material_request * (100 + 7 * tech))
                                    d[a][5] = "{0}".format(tech + tech_request)
                                    d[cpt][7] = "{0}".format(new_economy)
                                    hlp[cpt][6] = "{0}".format(techcount + 1)
                                    rcp[2][2] = "{0}".format(f_exvolume + food_request)
                                    rcp[2][3] = "{0}".format(m_exvolume + material_request)
                                    linelist = []
                                    for l in range(len(d)):
                                        line = '/'.join(d[l])
                                        linelist.append(line)
                                    r = open(data, mode = 'wt', encoding='utf-8')
                                    r.write('\n'.join(linelist))
                                    r.close()
                                    linelist = []
                                    for l in range(len(hlp)):
                                        line = '/'.join(hlp[l])
                                        linelist.append(line)
                                    h = open(helper, mode = 'wt', encoding='utf-8')
                                    h.write('\n'.join(linelist))
                                    h.close()
                                    linelist = []
                                    for l in range(len(rcp)):
                                        line = '/'.join(rcp[l])
                                        linelist.append(line)
                                    c = open(receipt, mode = 'wt', encoding='utf-8')
                                    c.write('\n'.join(linelist))
                                    c.close()
                                    if a == cpt:
                                        resultcheck = [a]
                                    else:
                                        resultcheck = [a, cpt]
                                    await message.channel.send(costume[13])
                                    nativenumb = 0
                                    for o in hownerlist:
                                        if o == "???" or "+???":
                                            nativenumb += 1
                                    result = discord.Embed(title = cmd[1] + " 스텟 구매 결과")
                                    result.description = ("지역/오너/나라\n식량/자재/기술/비율/자금/보호")
                                    k = -1
                                    for rsl in resultcheck:
                                        n = ""
                                        v = ""
                                        k += 1
                                        line = d[rsl]
                                        for l in range(len(line)):
                                            if l < 3:
                                                n += line[l]
                                                if l != 2:
                                                    n += "/"
                                            else:
                                                v += line[l]
                                                if l != len(line) - 1:
                                                    v += "/"
                                        result.add_field(name = n, value = v)
                                    await message.channel.send(embed=result)
                                    await get_channel_by_position(4).send(embed=result)
                except ValueError:
                    await message.channel.send(costume[7])
                    await message.channel.send("```%구매 지역 식량 자재 기술\n지역 ∈ 본인 나라\nmin(식량, 자재, 기술) ≥ 0```")
                    
    elif cmd[0] == "판매":
        r = open(data, mode = 'rt', encoding='utf-8')
        data_real = r.read()
        r.close()
        ownerlist = get_category(data_real, 1)
        disp = message.author.display_name
        if disp not in ownerlist:
            await message.channel.send(costume[9])
        else:
            if len(cmd) != 4:
                await message.channel.send(costume[7])
                await message.channel.send("```%판매 지역 식량 자재\n지역 ∈ 본인 나라\nmin(식량, 자재) ≥ 0\n판매량 ≤ 보유량```")
            else:
                try:
                    int(cmd[2])
                    food_request = int(cmd[2])
                    int(cmd[3])
                    material_request = int(cmd[3])
                    if min(food_request, material_request) < 0:
                        await message.channel.send(costume[8])
                        await message.channel.send("```%판매 지역 식량 자재\n지역 ∈ 본인 나라\nmin(식량, 자재) ≥ 0\n판매량 ≤ 보유량```")
                    else:
                        arealist = get_category(data_real, 0)
                        if cmd[1] not in arealist:
                            await message.channel.send(costume[10])
                        else:
                            h = open(helper, mode = 'rt', encoding='utf-8')
                            helper_real = h.read()
                            h.close()
                            nationlist = get_category(data_real, 2)
                            hownerlist = get_category(helper_real, 1)
                            hnationlist = get_category(helper_real, 2)
                            for a in range(len(arealist)):
                                nation = nationlist[a]
                                if arealist[a] == cmd[1]:
                                    break
                            for n in range(len(nationlist)):
                                if nationlist[n] == nation:
                                    howner = hownerlist[n]
                                    if hnationlist[n] == nation and "+" not in howner:
                                        cpt = n
                                        break
                            capitalowner = ownerlist[cpt]
                            if disp != capitalowner:
                                await message.channel.send(costume[9])
                            else:
                                d = decode(data_real)
                                food = int(d[a][3])
                                material = int(d[a][4])
                                tech = int(d[a][5])
                                if min(food - food_request * 100, material - material_request * 100) < 0:
                                    await message.channel.send(costume[8])
                                    await message.channel.send("```%판매 지역 식량 자재\n지역 ∈ 본인 나라\nmin(식량, 자재) ≥ 0\n판매량 ≤ 보유량```")
                                else:
                                    economy = int(d[cpt][7])
                                    hlp = decode(helper_real)
                                    techcount = int(hlp[cpt][6])
                                    c = open(receipt, mode = 'rt', encoding='utf-8')
                                    receipt_real = c.read()
                                    c.close()
                                    rcp = decode(receipt_real)
                                    f_exvolume = int(rcp[2][2])
                                    m_exvolume = int(rcp[2][3])
                                    price = get_price(receipt_real, food_request, material_request, 0, techcount)
                                    new_economy = economy + price * 80 // (100 + 7 * tech)
                                    d[a][3] = "{0}".format(food - food_request * 100)
                                    d[a][4] = "{0}".format(material - material_request * 100)
                                    d[cpt][7] = "{0}".format(new_economy)
                                    rcp[2][2] = "{0}".format(f_exvolume - food_request)
                                    rcp[2][3] = "{0}".format(m_exvolume - material_request)
                                    linelist = []
                                    for l in range(len(d)):
                                        line = '/'.join(d[l])
                                        linelist.append(line)
                                    r = open(data, mode = 'wt', encoding='utf-8')
                                    r.write('\n'.join(linelist))
                                    r.close()
                                    linelist = []
                                    for l in range(len(hlp)):
                                        line = '/'.join(hlp[l])
                                        linelist.append(line)
                                    h = open(helper, mode = 'wt', encoding='utf-8')
                                    h.write('\n'.join(linelist))
                                    h.close()
                                    linelist = []
                                    for l in range(len(rcp)):
                                        line = '/'.join(rcp[l])
                                        linelist.append(line)
                                    c = open(receipt, mode = 'wt', encoding='utf-8')
                                    c.write('\n'.join(linelist))
                                    c.close()
                                    if a == cpt:
                                        resultcheck = [a]
                                    else:
                                        resultcheck = [a, cpt]
                                    await message.channel.send(costume[14])
                                    nativenumb = 0
                                    for o in hownerlist:
                                        if o == "???" or "+???":
                                            nativenumb += 1
                                    result = discord.Embed(title = cmd[1] + " 스텟 판매 결과")
                                    result.description = ("지역/오너/나라\n식량/자재/기술/비율/자금/보호")
                                    k = -1
                                    for rsl in resultcheck:
                                        n = ""
                                        v = ""
                                        k += 1
                                        line = d[rsl]
                                        for l in range(len(line)):
                                            if l < 3:
                                                n += line[l]
                                                if l != 2:
                                                    n += "/"
                                            else:
                                                v += line[l]
                                                if l != len(line) - 1:
                                                    v += "/"
                                        result.add_field(name = n, value = v)
                                    await message.channel.send(embed=result)
                                    await get_channel_by_position(4).send(embed=result)
                except ValueError:
                    await message.channel.send(costume[7])
                    await message.channel.send("```%판매 지역 식량 자재\n지역 ∈ 본인 나라\nmin(식량, 자재) ≥ 0\n판매량 ≤ 보유량```")
                    
    elif cmd[0] == "대출":
        r = open(data, mode = 'rt', encoding='utf-8')
        data_real = r.read()
        r.close()
        ownerlist = get_category(data_real, 1)
        disp = message.author.display_name
        if disp not in ownerlist:
            await message.channel.send(costume[9])
        else:
            if len(cmd) != 3:
                await message.channel.send(costume[7])
                await message.channel.send("```%대출 형태 금액\n형태 ∈ {단리1, 단리2, 복리1, 복리2}\n100 ≤ 금액 ≤ 대출한도```")
            else:
                finantialist = ["단리1", "단리2", "복리1", "복리2"]
                if cmd[1] not in finantialist:
                    await message.channel.send(costume[8])
                    await message.channel.send("```%대출 형태 금액\n형태 ∈ {단리1, 단리2, 복리1, 복리2}\n100 ≤ 금액 ≤ 대출한도```")
                else:
                    try:
                        int(cmd[2])
                        dept = int(cmd[2])
                        if cmd[1] == "단리1":
                            borrowlimit = 5000
                            type = "단리 10% - "
                            interest = "+{0}".format(dept//10)
                        elif cmd[1] == "단리2":
                            borrowlimit = 10000
                            type = "단리 20% - "
                            interest = "+{0}".format(dept//5)
                        elif cmd[1] == "복리1":
                            borrowlimit = 20000
                            type = "복리 10% - "
                            interest = "1"
                        else:
                            borrowlimit = 50000
                            type = "복리 30% - "
                            interest = "3"
                        if 100 > dept or dept > borrowlimit:
                            await message.channel.send(costume[8])
                            await message.channel.send("```%대출 형태 금액\n형태 ∈ {단리1, 단리2, 복리1, 복리2}\n100 ≤ 금액 ≤ 대출한도```")
                        else:
                            h = open(helper, mode = 'rt', encoding='utf-8')
                            helper_real = h.read()
                            h.close()
                            nationlist = get_category(data_real, 2)
                            hownerlist = get_category(helper_real, 1)
                            hnationlist = get_category(helper_real, 2)
                            for o in range(len(ownerlist)):
                                nation = nationlist[o]
                                if ownerlist[o] == disp:
                                    break
                            for n in range(len(nationlist)):
                                if nationlist[n] == nation:
                                    howner = hownerlist[n]
                                    if hnationlist[n] == nation and "+" not in howner:
                                        cpt = n
                                        break
                            capitalowner = ownerlist[cpt]
                            if disp != capitalowner:
                                await message.channel.send(costume[9])
                            else:
                                hlp = decode(helper_real)
                                if int(hlp[o][7]) != 0:
                                    await message.channel.send(costume[17])
                                else:
                                    nativenumb = 0
                                    for o in hownerlist:
                                        if o == "???" or "+???":
                                            nativenumb += 1
                                    for ch in ari.get_all_channels():
                                        if ch.position == 3 and ch.type == discord.ChannelType.text:
                                            liabilitychannel = ch
                                            break
                                        # if ch.position == 31 + nativenumb + 1:
                                        #     liabilitychannel = ch
                                        #     break
                                    hlp[o][7] = cmd[2]
                                    hlp[o][8] = interest
                                    linelist = []
                                    for l in range(len(hlp)):
                                        line = '/'.join(hlp[l])
                                        linelist.append(line)
                                    h = open(helper, mode = 'wt', encoding='utf-8')
                                    h.write('\n'.join(linelist))
                                    h.close()
                                    await message.channel.send(costume[16])
                                    await liabilitychannel.send(nationlist[o] + ": " + type + cmd[2])
                    except ValueError:
                        await message.channel.send(costume[7])
                        await message.channel.send("```%대출 형태 금액\n형태 ∈ {단리1, 단리2, 복리1, 복리2}\n100 ≤ 금액 ≤ 대출한도```")
                        
    elif cmd[0] == "상환":
        r = open(data, mode = 'rt', encoding='utf-8')
        data_real = r.read()
        r.close()
        ownerlist = get_category(data_real, 1)
        disp = message.author.display_name
        if disp not in ownerlist:
            await message.channel.send(costume[9])
        else:
            if len(cmd) == 1:
                await message.channel.send(costume[7])
                await message.channel.send("```%상환 (분할 횟수)\n%상환 (분할 횟수) [지역들 목록...]\n0 < 분할 홧수\n∀지역 ∈ 본인 나라```")
            else:
                try:
                    int(cmd[1])
                    days = int(cmd[1])
                    if days < 1:
                        await message.channel.send(costume[8])
                        await message.channel.send("```%상환 (분할 횟수)\n%상환 (분할 횟수) [지역들 목록...]\n0 < 분할 홧수\n∀지역 ∈ 본인 나라```")
                    else:
                        h = open(helper, mode = 'rt', encoding='utf-8')
                        helper_real = h.read()
                        h.close()
                        nationlist = get_category(data_real, 2)
                        hownerlist = get_category(helper_real, 1)
                        hnationlist = get_category(helper_real, 2)
                        for o in range(len(ownerlist)):
                            nation = nationlist[o]
                            if ownerlist[o] == disp:
                                break
                        for n in range(len(nationlist)):
                            if nationlist[n] == nation:
                                howner = hownerlist[n]
                                if hnationlist[n] == nation and "+" not in howner:
                                    cpt = n
                                    break
                        capitalowner = ownerlist[cpt]
                        if disp != capitalowner:
                            await message.channel.send(costume[9])
                        else:
                            d = decode(data_real)
                            hlp = decode(helper_real)
                            economy = int(d[cpt][7])
                            repayment = 0
                            if len(cmd) == 2:
                                for o in range(len(ownerlist)):
                                    if nationlist[o] == disp:
                                        ownation = nationlist[o]
                                        break
                                for n in range(len(nationlist)):
                                    if nationlist[n] == ownation:
                                        interest = hlp[n][7]
                                        dept = int(hlp[n][8])
                                        if dept > 0:
                                            if interest.startswith('+'):
                                                repayment += simplerepay(dept, interest, days)
                                            else:
                                                repayment += compoundrepay(dept, interest, days)
                                if economy < repayment:
                                    await message.channel.send(costume[7])
                                else:
                                    nativenumb = 0
                                    for o in hownerlist:
                                        if o == "???" or "+???":
                                            nativenumb += 1
                                    for ch in ari.get_all_channels():
                                        if ch.position == 31 + nativenumb + 1:
                                            liabilitychannel = ch
                                            break
                                    areasave = []
                                    for n in range(len(nationlist)):
                                        if nationlist[n] == ownation:
                                            areasave.append(get_line(data_real, n))
                                            interest = hlp[n][7]
                                            dept = int(hlp[n][8])
                                            if dept > 0:
                                                if interest.startswith('+'):
                                                    economy -= simplerepay(dept, interest, days)
                                                    new_dept = dept - simplerepay(dept, interest, days)
                                                else:
                                                    economy -= compoundrepay(dept, interest, days)
                                                    new_dept = dept - compoundrepay(dept, interest, days)
                                    d[cpt][7] = "{0}".format(economy)
                                    hlp[n][8] = "{0}".format(new_dept)
                                    linelist = []
                                    for l in range(len(d)):
                                        line = '/'.join(d[l])
                                        linelist.append(line)
                                    r = open(data, mode = 'wt', encoding='utf-8')
                                    r.write('\n'.join(linelist))
                                    r.close()
                                    linelist = []
                                    for l in range(len(hlp)):
                                        line = '/'.join(hlp[l])
                                        linelist.append(line)
                                    h = open(helper, mode = 'wt', encoding='utf-8')
                                    h.write('\n'.join(linelist))
                                    h.close()
                                    await message.channel.send(costume[18])
                                    result = discord.Embed(title = cmd[1] + " 상환 결과 1")
                                    result.description = ("지역/오너/나라\n식량/자재/기술/비율/자금/보호")
                                    k = -1
                                    for o in range(len(owners)):
                                        n = ""
                                        v = ""
                                        if owners[o] in searchset:
                                            k += 1
                                            line = data_new[o]
                                            for l in range(len(line)):
                                                if l < 3:
                                                    n += line[l]
                                                    if l != 2:
                                                        n += "/"
                                                else:
                                                    v += line[l]
                                                    if l != len(line) - 1:
                                                        v += "/"
                                            result.add_field(name = n, value = v)
                                            if k % 10 == 9:
                                                await message.channel.send(embed=result)
                                                result = discord.Embed(title = cmd[1] + " 상환 결과 {0}".format(k // 10 + 2))
                                                result.description = ("지역/오너/나라\n식량/자재/기술/비율/자금/보호")
                                    if  k % 10 != 9:
                                        await message.channel.send(embed=result)
                            else:
                                await message.channel.send("여기는 공사중입니다......")
                except ValueError:
                    await message.channel.send(costume[7])
                    await message.channel.send("```%상환 (분할 횟수)\n%상환 (분할 횟수) [지역들 목록...]\n0 < 분할 홧수\n∀지역 ∈ 본인 나라```")
                    
    elif cmd[0] == "수출":
        r = open(data, mode = 'rt', encoding='utf-8')
        data_real = r.read()
        r.close()
        ownerlist = get_category(data_real, 1)
        disp = message.author.display_name
        if disp not in ownerlist:
            await message.channel.send(costume[9])
        else:
            if len(cmd) != 5:
                await message.channel.send(costume[7])
                await message.channel.send("```%수출 원산지 도착지 식량 자재\n원산지 ∈ 본인 나라\n원산지 ≠ 도착지\nmin(식량, 자재) ≥ 0\n판매량 ≤ 보유량```")
            else:
                try:
                    int(cmd[3])
                    food_export = int(cmd[3])
                    int(cmd[4])
                    material_export = int(cmd[4])
                    if min(food_export, material_export) < 0:
                        await message.channel.send(costume[8])
                        await message.channel.send("```%수출 원산지 도착지 식량 자재\n원산지 ∈ 본인 나라\n원산지 ≠ 도착지\nmin(식량, 자재) ≥ 0\n판매량 ≤ 보유량```")
                    elif cmd[1] == cmd[2]:
                        await message.channel.send(costume[8])
                        await message.channel.send("```%수출 원산지 도착지 식량 자재\n원산지 ∈ 본인 나라\n원산지 ≠ 도착지\nmin(식량, 자재) ≥ 0\n판매량 ≤ 보유량```")
                    else:
                        arealist = get_category(data_real, 0)
                        if cmd[1] not in arealist or cmd[2] not in arealist:
                            await message.channel.send(costume[10])
                        else:
                            for origin in range(len(arealist)):
                                if arealist[origin] == cmd[1]:
                                    break
                            for receive in range(len(arealist)):
                                if arealist[receive] == cmd[2]:
                                    break
                            h = open(helper, mode = 'rt', encoding='utf-8')
                            helper_real = h.read()
                            h.close()
                            nationlist = get_category(data_real, 2)
                            hownerlist = get_category(helper_real, 1)
                            hnationlist = get_category(helper_real, 2)
                            for a in range(len(arealist)):
                                nation = nationlist[a]
                                if arealist[a] == cmd[1]:
                                    break
                            for n in range(len(nationlist)):
                                if nationlist[n] == nation:
                                    howner = hownerlist[n]
                                    if hnationlist[n] == nation and "+" not in howner:
                                        cpt = n
                                        break
                            capitalowner = ownerlist[cpt]
                            if disp != capitalowner:
                                await message.channel.send(costume[9])
                            else:
                                d = decode(data_real)
                                food_origin = int(d[origin][3])
                                material_origin = int(d[origin][4])
                                if food_export > food_origin or material_export > material_origin:
                                    await message.channel.send(costume[20])
                                else:
                                    await message.channel.send(costume[19])
                                    food_receive = int(d[receive][3])
                                    material_receive = int(d[receive][4])
                                    tech_origin = int(d[origin][5])
                                    tech_receive = int(d[receive][5])
                                    food_origin -= food_export
                                    material_origin -= material_export
                                    food_receive += int(food_export * (100 + 7 * tech_receive) // (100 + 7 * tech_origin))
                                    material_receive += int(material_export * (100 + 7 * tech_receive) // (100 + 7 * tech_origin))
                                    d[origin][3] = "{0}".format(food_origin)
                                    d[origin][4] = "{0}".format(material_origin)
                                    d[receive][3] = "{0}".format(food_receive)
                                    d[receive][4] = "{0}".format(material_receive)
                                    linelist = []
                                    for l in range(len(d)):
                                        line = '/'.join(d[l])
                                        linelist.append(line)
                                    r = open(data, mode = 'wt', encoding='utf-8')
                                    r.write('\n'.join(linelist))
                                    r.close()
                                    result = discord.Embed(title = cmd[1] + " → " + cmd[2] + " 수출 결과")
                                    result.description = ("지역/오너/나라\n식량/자재/기술/비율/자금/보호")
                                    result.add_field(name = d[origin][0] + "/" + d[origin][1] + "/" + d[origin][2], value = d[origin][3] + "/" + d[origin][4] + "/" + d[origin][5] + "/" + d[origin][6] + "/" + d[origin][7] + "/" + d[origin][8])
                                    result.add_field(name = d[receive][0] + "/" + d[receive][1] + "/" + d[receive][2], value = d[receive][3] + "/" + d[receive][4] + "/" + d[receive][5] + "/" + d[receive][6] + "/" + d[receive][7] + "/" + d[receive][8])
                                    await get_channel_by_position(5).send(embed=result)
                                    await message.channel.send(embed=result)
                except ValueError:
                    await message.channel.send(costume[7])
                    await message.channel.send("```%수출 원산지 도착지 식량 자재\n원산지 ∈ 본인 나라\n원산지 ≠ 도착지\nmin(식량, 자재) ≥ 0\n판매량 ≤ 보유량```")
                        
    elif cmd[0] == "송금":
        r = open(data, mode = 'rt', encoding='utf-8')
        data_real = r.read()
        r.close()
        ownerlist = get_category(data_real, 1)
        disp = message.author.display_name
        if disp not in ownerlist:
            await message.channel.send(costume[9])
        else:
            if len(cmd) != 3:
                await message.channel.send(costume[7])
                await message.channel.send("```%송금 나라 금액\n나라 ≠ 본인 나라\n금액 ≥ 0\n금액 ≤ 보유량```")
            else:
                try:
                    int(cmd[2])
                    transfer = int(cmd[2])
                    if transfer < 0:
                        await message.channel.send(costume[8])
                        await message.channel.send("```%송금 나라 금액\n나라 ≠ 본인 나라\n금액 ≥ 0\n금액 ≤ 보유량```")
                    else:
                        nationlist = get_category(data_real, 2)
                        if cmd[1] not in nationlist:
                            await message.channel.send(costume[10])
                        else:
                            h = open(helper, mode = 'rt', encoding='utf-8')
                            helper_real = h.read()
                            h.close()
                            hownerlist = get_category(helper_real, 1)
                            hnationlist = get_category(helper_real, 2)
                            capitalownerlist = []
                            for o in range(len(ownerlist)):
                                if nationlist[o] == hnationlist[o] and ownerlist[o] == hownerlist[o] and ownerlist[o] != "???":
                                    capitalownerlist.append(ownerlist[o])
                            if disp not in capitalownerlist:
                                await message.channel.send(costume[9])
                            else:
                                for origin in range(len(ownerlist)):
                                    if hownerlist[origin] == disp:
                                        break
                                for receive in range(len(ownerlist)):
                                    if ownerlist[receive] in capitalownerlist and nationlist[receive] == cmd[1] and hnationlist[receive] == cmd[1]:
                                        break
                                d = decode(data_real)
                                economy_origin = int(d[origin][7])
                                if transfer > economy_origin:
                                    await message.channel.send(costume[15])
                                elif origin == receive:
                                    await message.channel.send(costume[8])
                                    await message.channel.send("```%송금 나라 금액\n나라 ≠ 본인 나라\n금액 ≥ 0\n금액 ≤ 보유량```")
                                else:
                                    await message.channel.send(costume[21])
                                    economy_receive = int(d[receive][7])
                                    economy_origin -= transfer
                                    economy_receive += transfer
                                    d[origin][7] = "{0}".format(economy_origin)
                                    d[receive][7] = "{0}".format(economy_receive)
                                    linelist = []
                                    for l in range(len(d)):
                                        line = '/'.join(d[l])
                                        linelist.append(line)
                                    r = open(data, mode = 'wt', encoding='utf-8')
                                    r.write('\n'.join(linelist))
                                    r.close()
                                    result = discord.Embed(title = d[origin][2] + " → " + cmd[1] + " 송금 결과")
                                    result.description = ("지역/오너/나라\n식량/자재/기술/비율/자금/보호")
                                    result.add_field(name = d[origin][0] + "/" + d[origin][1] + "/" + d[origin][2], value = d[origin][3] + "/" + d[origin][4] + "/" + d[origin][5] + "/" + d[origin][6] + "/" + d[origin][7] + "/" + d[origin][8])
                                    result.add_field(name = d[receive][0] + "/" + d[receive][1] + "/" + d[receive][2], value = d[receive][3] + "/" + d[receive][4] + "/" + d[receive][5] + "/" + d[receive][6] + "/" + d[receive][7] + "/" + d[receive][8])
                                    await get_channel_by_position(5).send(embed=result)
                                    await message.channel.send(embed=result)
                except ValueError:
                    await message.channel.send(costume[7])
                    await message.channel.send("```%송금 나라 금액\n나라 ≠ 본인 나라\n금액 ≥ 0\n금액 ≤ 보유량```")
                        
    elif cmd[0] == "원격조종":
        msg = ""
        for c in range(len(cmd)-1):
            msg += cmd[c+1]
            msg += " "
        for ch in ari.get_all_channels():
            if ch.position == 12 + 1:
                channel = ch
                break
        await channel.send(msg)
        
    elif cmd[0] == "위치조사":
        channel_list = [(ch.type, ch.position, ch.name) for ch in ari.get_all_channels()]
        channel_list.sort()
        print("\n".join([str(ch[0]) + "\t" + str(ch[1]) + "\t" + ch[2] for ch in channel_list]))
        
    elif cmd[0] == "테스트":
        for a in range(0):
            await message.channel.send(a)
            
    elif cmd[0] == "원주민화":
        pass

    else:
        await message.channel.send(randomcatch(costume[11]))

token = "NjU2MDY1NTk0MDA0NjAyOTEx.XfkEnA.JlQR2xcodwiRk7ElvRXhFM1qVNU"

ari.run(token)