import random
import sys
import matplotlib

from memory import Memory
from v1 import DQN
from copy import deepcopy
from helpers import *
import torch

import gym

ENV = gym.make("CartPole-v1", render_mode="human")

is_ipython = 'inline' in matplotlib.get_backend()
if is_ipython:
    from IPython import display


class Agent:
    # Number of episodes
    MAX_EP = 1_000_000

    # Q Value vals
    DISCOUNT = 0.9
    LEARNING_RATE = 0.01

    # Soft update
    TAU = 0.1

    # Epsilon GREEDY vals
    EPS = 0.9999
    EPS_DECAY = 0.999
    EPS_MIN = 0.5
    EPS_MAX = 1.0

    # Memory vals
    MEM_SIZE = 500_000
    MIN_MEM_SIZE = 1_000
    MEM_BATCH = 250
    TARGET_UPDATE_FREQ = 25

    def __init__(self, maxEp:int=10_000, env=gym.make("CartPole-v1")):

        # Bootstrapping to maintain stability of prediction
        self.memory = Memory(maxCapacity=self.MEM_SIZE)
        self.model = DQN(n_obsv=4, n_actions=2, n_layer=2, n_layerSize=128,learningRate=self.LEARNING_RATE)  # updates every iteration
        self.targetModel = deepcopy(self.model)  # updates only once threshold has been reached

        # Setting individual stats for the environment to run
        self.maxEpisode = maxEp
        self.env = env
        self.episodeCounter = 0
        self.totalReward = 0

    def __printStats(self):
        print(f"EPS: {self.EPS:.3f} | MEM: {len(self.memory)} | EP: {self.episodeCounter} | AVG: {self.totalReward/self.episodeCounter:.5f}")

    def __printPerEp(self, score:float):
        print(f"EPS: {self.EPS:.3f} | MEM: {len(self.memory)} | EP: {self.episodeCounter} | SCORE: {score} | AVG: {self.totalReward/self.episodeCounter:.5f}")

    def predict(self, environment:ParseEnvironment) -> int:
        if self.EPS < self.EPS_MIN:
            res = self.targetModel.forward(environment.toTensor())
            return torch.argmax(res).detach().numpy()
        else:
            # print("USING RANDOM")
            self.EPS = self.EPS * self.EPS_DECAY
            return random.randint(0,1)


    def getMaxQ(self, environment:ParseEnvironment) -> torch.tensor:
        res = self.model.forward(environment.toTensor())
        # print(res)
        return res.clone().detach().numpy()


    def train(self):
        if len(self.memory) < self.MEM_BATCH:
            return

        batch = self.memory.sample(size=self.MEM_BATCH)

        oldValsToFit = []
        valsToFit = []

        for index, env in enumerate(batch):
            maxFutureQ = np.max(self.getMaxQ(env.nextState))
            curQ = np.max(self.getMaxQ(env.state))

            if not env.state.isDone:
                newQ = curQ + self.LEARNING_RATE * (env.reward + (self.DISCOUNT * maxFutureQ))
            else:
                newQ = curQ + env.reward

            oldFit = self.getMaxQ(env.state)
            toFit = deepcopy(oldFit)
            toFit[env.action] = newQ


            oldValsToFit.append(oldFit)
            valsToFit.append(toFit)

        loss = self.model.crit(torch.tensor(np.array(oldValsToFit), requires_grad=True), torch.tensor(np.array(valsToFit), requires_grad=False))
        self.model.optim.zero_grad()
        loss.backward()
        self.model.optim.step()

        if self.episodeCounter % self.TARGET_UPDATE_FREQ == 0:
            # OLD METHOD TO FORCE UPDATE
            self.targetModel.load_state_dict(self.model.state_dict())

            # # NEW METHOD using soft update
            # modelNet = self.model.state_dict()
            # targetModelNet = self.targetModel.state_dict()
            #
            # for key in targetModelNet:
            #     modelNet[key] = (1-self.TAU)*modelNet[key] + self.TAU*targetModelNet[key]
            #
            # self.targetModel.load_state_dict(modelNet)


    def run(self):
        while self.episodeCounter < self.maxEpisode:
            self.episodeCounter += 1
            cReward = 0.0
            curEnv = ParseEnvironment(self.env.reset()[0], reward=1.0, isDone=False, isTruncated=False)

            while curEnv.isDone is not True:

                # interact with env
                action = self.predict(curEnv)
                prevEnv = curEnv
                curEnv = ParseEnvironment(*self.env.step(action))

                # save record of what just happened
                thisRecord = ParseRecord(prevEnv, action, curEnv, curEnv.reward)
                self.memory.push(thisRecord)

                # # train model
                self.train()

                # # update local variables
                cReward += curEnv.reward
                self.totalReward += curEnv.reward
                # self.__printStats()
            self.__printPerEp(cReward)


if __name__ == '__main__':
    agent = Agent(maxEp=1_000_000)
    agent.run()
