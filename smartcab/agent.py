import random
from environment import Agent, Environment
from planner import RoutePlanner
from simulator import Simulator

class LearningAgent(Agent):
    """An agent that learns to drive in the smartcab world."""

    def __init__(self, env):
        super(LearningAgent, self).__init__(env)  # sets self.env = env, state = None, next_waypoint = None, and a default color
        self.color = 'red'  # override color
        self.planner = RoutePlanner(self.env, self)  # simple route planner to get next_waypoint
        self.q = {}
        self.last_waypoint = None
        # amount of exploration to do
        self.epsilon = 0.05
        # learning discount
        self.alpha = 0.2
        # discount for future awards
        self.gamma = 0.9
        # TODO: Initialize any additional variables here
        #self.destination = self.env.agent_states(self)

    def unpackState(self, state):
        return (
            state.get('light', None), 
            state.get('oncoming', None), 
            state.get('right', None), 
            state.get('left', None)
        )

    def getScore(self, state, action, next_waypoint):
        # returns 0 as default
        return self.q.get((self.unpackState(state), action, next_waypoint), 0.0)

    def getMaxScore(self, state, next_waypoint):
        return max([self.getScore(state, a, next_waypoint) for a in Environment.valid_actions[1:]])

    def learn(self, state1, action, reward, state2, next_waypoint):
        expected_reward = self.getMaxScore(state2, next_waypoint)
        expected_reward = expected_reward * self.gamma

        old_q = self.q.get((self.unpackState(state1), action, next_waypoint), None)
        if old_q is None:
            # add the current reward
            self.q[(self.unpackState(state1), action, next_waypoint)] = reward
        else:
            # blend them using the learning discount
            self.q[(self.unpackState(state1), action, next_waypoint)] = old_q + self.alpha * (reward - expected_reward)

    def think(self, state, next_waypoint):
        #Think! Let us see whether to we should randomly explore or go with our table
        if random.random() < self.epsilon:
            # walk randomly
            action = random.choice(Environment.valid_actions[1:])
        else:
            # do the smart thing
            scores = [self.getScore(state, a, next_waypoint) for a in Environment.valid_actions[1:]]
            max_score = max(scores)

            # sometimes we get ties, like all 0's
            if scores.count(max_score) > 1:
                # randomly pick from the best
                idx = random.choice([a for a in range(0, len(Environment.valid_actions[1:])) if scores[a] == max_score])
            else:
                idx = scores.index(max_score)

            action = Environment.valid_actions[1:][idx]
        return action


    def reset(self, destination=None):
        self.planner.route_to(destination)
        # TODO: Prepare for a new trip; reset any variables here, if required

    def update(self, t):
        # Gather inputs
        self.next_waypoint = self.planner.next_waypoint()  # from route planner, also displayed by simulator
        inputs = self.env.sense(self)
        deadline = self.env.get_deadline(self)

        action = self.think(inputs, self.next_waypoint)

        # Execute action and get reward
        reward = self.env.act(self, action)

        # TODO: Learn policy based on state, action, reward
        self.learn(inputs, action, reward, self.env.sense(self), self.next_waypoint)

        print "LearningAgent.update(): deadline = {}, inputs = {}, action = {}, reward = {}".format(deadline, inputs, action, reward)  # [debug]


def run():
    """Run the agent for a finite number of trials."""

    # Set up environment and agent
    e = Environment()  # create environment (also adds some dummy traffic)
    a = e.create_agent(LearningAgent)  # create agent
    e.set_primary_agent(a, enforce_deadline=False)  # set agent to track

    # Now simulate it
    sim = Simulator(e, update_delay=0.1)  # reduce update_delay to speed up simulation
    sim.run(n_trials=10)  # press Esc or close pygame window to quit


if __name__ == '__main__':
    run()
