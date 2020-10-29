

import random
from enum import Enum


#random.seed(42)

MAX_ARR = 100_000
MAX_SALES_CYCLE = 6
AVG_REP_WORK_TIME = [3,5,4]
NUM_STAGES = 4

class Pipestage(Enum):
    lost = -1
    new = 0
    sdr = 1
    demo = 2
    ae = 3
    won = NUM_STAGES

class Company():
    def __init__(self, env, name):
        self.env = env
        self.name = name
        self.max_potential_arr = MAX_ARR * random.random()
        self.relevance = round(random.random() * 3, 2)
        self.stage = Pipestage.new
        


class SalesRep():
    def __init__(self, env, name, stage):
        self.env = env
        self.name = name
        self.stage = stage
        self.process = env.process(self.working())
        self.time_factor = random.uniform(0.5,1.5)
        self.sell_score = random.uniform(0.5,1)
        self.process = env.process(self.working())

    def working(self):
        while True:
            start_time = self.env.now
            while True:
                c = get_company(env, self.stage)
                if c is None:
                    yield self.env.timeout(1)
                else:
                    print('Stage', self.stage, self.name, 'waited', self.env.now - start_time)
                    break
            print('Rep', self.name, self.stage, 'starting on', c.name, 'time', self.env.now)
            yield self.env.timeout(AVG_REP_WORK_TIME[self.stage.value] * (1 + self.time_factor + random.random()))
            passed = random.random() < c.relevance * self.sell_score
            print('Stage', self.stage, self.name, 'passed' if passed else 'lost', c.name, 'time', self.env.now) 
            c.stage = Pipestage(self.stage.value + 1) if passed else Pipestage.lost

def get_company(env, stage):
    if stage == Pipestage.new:
        tapped_market.append(Company(env, len(tapped_market)))
        return tapped_market[-1]
    else:
        relevant_companies = [c for c in tapped_market if c.stage == stage]
        return relevant_companies[0] if relevant_companies else None

env = simpy.Environment()
team = sum([[SalesRep(env, i, Pipestage(j)) for i in range(4)] for j in range(NUM_STAGES)], [])
tapped_market = []
env.run(until=50)

