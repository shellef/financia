import simpy
import random, sys
from enum import Enum
import logging

MAX_ARR = 100_000
MAX_SALES_CYCLE = 6
AVG_REP_WORK_TIME = [3,5,4]
NUM_STAGES = 4
WEEKS_IN_YEAR = 52

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
        self.arr = 0


class SalesRep():
    def __init__(self, env, name, stage):
        self.env = env
        self.name = name
        self.stage = stage
        self.time_factor = random.uniform(0.5,1.5)
        self.sell_score = random.uniform(0.5,1)
        self.ramp_up_time = 12
        self.total_wait_time = 0

        self.rep_str = f'Rep {self.stage.name}_{self.name}'

        self.process = env.process(self.working())

    def working(self):
        while True:
            start_time = self.env.now
            while True:
                c = self.env.sim.get_company(self.stage)
                if c is None:
                    yield self.env.timeout(1)
                else:
                    wait_time = self.env.now - start_time
                    if wait_time:
                        logging.info(f'{self.rep_str} waited {wait_time}')
                        self.total_wait_time += wait_time
                    break
            logging.info(f'{self.rep_str} starting on company_{c.name} at time {self.env.now:0.2f}')
            work_time = round(AVG_REP_WORK_TIME[self.stage.value-1] * (1 + self.time_factor + random.random()), 2)
            yield self.env.timeout(work_time)
            passed = random.random() < c.relevance * self.sell_score
            logging.info(f'{self.rep_str} {"passed" if passed else "lost"} company_{c.name} at time {self.env.now:0.2f}') 
            c.stage = Pipestage(self.stage.value + 1) if passed else Pipestage.lost
            if c.stage == Pipestage.won: #closing stage determines deal size
                c.arr = round(random.random() * c.max_potential_arr)

class Simulation():
    def __init__(self, seed):
        random.seed(seed)
        self.env = simpy.Environment()
        self.env.sim = self
        self.team = sum([[SalesRep(self.env, i, Pipestage(j+1)) for i in range(2)] for j in range(NUM_STAGES-1)], [])
        self.tapped_market = []
        self.env.run(until=WEEKS_IN_YEAR)
        self.total_bookings = sum(c.arr for c in self.tapped_market)

    def get_company(self, stage):
        if stage == Pipestage.sdr:
            self.tapped_market.append(Company(self.env, len(self.tapped_market)))
            return self.tapped_market[-1]
        else:
            relevant_companies = [c for c in self.tapped_market if c.stage == stage]
            return relevant_companies[0] if relevant_companies else None


for i in range(10):
    seed = random.randrange(sys.maxsize)
    sim = Simulation(seed)
    print(f'total bookings {sim.total_bookings}, num_won {sum(c.stage == Pipestage.won for c in sim.tapped_market)} for seed {seed}')
    

