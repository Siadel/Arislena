import random
import openpyxl


def str_to_list(string):
    
    return string.split(',')


class Data:
    
    
    
    
    def set(self, *args):
        # Player(str, Permission, Group, list)
        # Task()
        # 
        
        for ar, d in zip(args, self.__dict__.keys()):
            
            self.__dict__[d] = ar



class Permission(Data):
    
    pass
    
    

class Freeman(Permission):
    
    level = 0
    
    

class Owner(Permission):
    
    level = 1



class Player(Data):
    
    players = []
    
    def __init__(self):
        
        self.author = ''
        self.permission = Permission
        self.group = Group
        self.areas = []
        self.tasks = []
    
    
    def elevate(self):
        
        try:
            
            level = self.permission.level
            
        except:
            
            self.permission = Freeman
            
        else:
            
            if level == 0:
                
                self.permission = Owner


class Task(Data):
    
    def __init__(self, player_id, command_name, req, **cost):
        
        self.name = f'task_{player_id}_{command_name}'
        self.req = req # turn(s) required
        self.cost = cost # dict of costs
        # Task.cost -> {Resource/Power : int}
        
        self.__complete = False


    @classmethod
    def isname(cls, name):
        
        if name == cls.__name__:
            
            return True
    
    
    def do(self):
        
        # zawon somo?
        
        if self.req > 0:
            self.req -= 1
        
        if self.req == 0:
            self.__complete = True
            


class Resource(Data):
    
    def __init__(self):
        
        self.current = 0
        self.store_limit = 0
        
        
    def add(self, amount):
        
        too_big = False if max(self.current+amount, self.store_limit) == self.store_limit else True
        
        if not too_big:
            self.current += amount
        else:
            pass # raise custom error
    
    
    def produce(self, amount):
        
        self.add(amount)
    
    
    def subtract(self, amount):
        
        too_small = False if min(self.current-amount, 0) == 0 else True
        
        if not too_small:
            self.current -= amount
        else:
            pass # raise custom error



class Food(Resource):
    
    pass



class Material(Resource):
    
    
    def __init__(self):
        super().__init__()
        
        self.produced = 0
        self.produce_limit = 0
        
    
    def isdepleted(self):
        
        if self.produced >= self.produce_limit:
            return True
        else:
            return False
    
    
    def produce(self, amount):
        # overrnameed
        
        too_many = False if max(self.produced+amount, self.produce_limit) == self.produce_limit else True
        
        if not too_many:
            
            self.produced += amount
            self.add(amount)



class Population(Resource):
    
    def __init__(self):
        super().__init__() # current, store_limit
        
        self.growth = 0
        
        self.food_usage = 0
        self.material_usage = 0
        
        self.labor = 0
        self.force = 0
        
    

class Power(Data):
    
    def __init__(self):
        
        self.current = 0
        self.use_limit = 0
        self.tasks = []
        
    
    
    
    
    def use(self, amount):
        
        too_much = False if max(self.current+amount, self.use_limit) == self.use_limit else True
            
        if not too_much:
            
            self.current += amount

    
    def disuse(self, name):
        
        pass



class Labor(Power):
    pass



class Force(Power):
    pass



class Adm(Power):
    pass



class Area(Data):
    
    grade = '1111222222233333333333344444444444444444555555555555555555556666666666666666677777777777788888889999'
    
    
    
    def __init__(self):
        
        self.id = ''
        self.name = ''
        
        gch = self.gchoicer
        
        self.fert = gch()
        self.resr = gch()
        self.hei = gch()
        self.flat = gch()
        
        self.food = Food()
        self.material = Material()
        self.population = Population()

    
    @classmethod
    def gchoicer(cls):
        
        return random.choice(cls.grade)
    

        
        






        





class Group(Data):
    
    
    def __init__(self):
        
        self.id = ''
        self.name = ''
        self.high_list = []
        self.low_list = []
        self.adm = Adm()
        self.labor = Labor()
        self.force = Force()
        self.fund = 0
        




a = Area()
g = Group()

f = a.food
m = a.material
p = a.population


f.set(0, 400)
m.set(0, 400, 0, 10000)
f.produce(300)
m.produce(350)

print(f.__dict__, m.__dict__, sep= '\n')

