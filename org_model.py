

import random
from enum import Enum

class Pipestage(Enum):
    lost = -1
    new = 0
    sdr = 1
    demo = 2
    ae = 3
    won = NUM_STAGES

#random.seed(42)

MAX_ARR = 100_000
MAX_SALES_CYCLE = 6
AVG_REP_WORK_TIME = [3,5,4]
NUM_STAGES = 4

class Company():
    def __init__(self, env, name):
        self.env = env
        self.name = name
        self.max_potential_arr = MAX_ARR * random.random()
        self.relevance = round(random.random() * 3, 2)
        self.stage = Pipestage.new
        self.process = env.process(self.engaging())

    def engaging(self):
        while self.stage != Pipestage.won and self.stage != Pipestage.lost:
            if random.random() < self.relevance:
                yield self.env.timeout(random.randint(0, MAX_SALES_CYCLE))
                self.stage = 
            else:
                self.stage = Pipestage.lost
            print('Company ', self.name, self.relevance, self.stage, self.env.now)



class SalesRep():
    def __init__(self, env, name, stage):
        self.env = env
        self.name = name
        self.stage = stage
        self.process = env.process(self.working())
        self.time_factor = random.uniform(0.5,1.5)
        self.sell_score = random.uniform(0.5,1)

    def working(self):
        while True:
            start_time = self.env.now
            while True:
                c = get_company(env, stage)
                if c is None:
                    yield self.env.timeout(1)
                else:
                    print('Stage', self.stage, self.name, 'waited', self.env.now - start_time)
                    break
            print('Rep', self.name, self.stage, 'starting on', c.name, self.env.now)
            yield self.env.timeout(AVG_REP_WORK_TIME[self.stage] * self.time_factor * (1 + random.random()))
            passed = random.random() < c.relevance * self.sell_score:
            print('Stage', self.stage, self.name, if passed 'passed' else 'lost', c.name, self.env.now) 
            c.stage = Pipestage(self.stage.value + 1) if passed else Pipestage.lost

def get_company(env, stage):
    if stage == Pipestage.new:
        tapped_market.append(Company(env, len(tapped_market)))
        return tapped_market[-1]
    else:
        relevant_companies = [c for c in tapped_market if c.stage == stage]
        return relevant_companies[0] if relevant_companies else None

env = simpy.Environment()
team = sum([[SalesRep(env, i, j) for i in range(4)] for j in range(NUM_STAGES)], [])
env.run(until=50)




    
    
#class SDR(object, env):
#    def __init__(self, env):
        
        

# class Sales:
#     pass

# @dataclass
# class AE:
#     name: str
#     salary = float
#     vertical = , close_time_stat, cash_win_rate_stat)
#         self.name = name, salary, vertical, close_time_stat, cash_win_rate_stat)
#         self.
#         self.
#         self.
#         self.
#         self.
#         self.
#         self.

# sales = Sales()

# sales.ae_list = []

# sales.ae_list.append()


# Sales = { 'input': }