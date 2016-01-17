### What is the agent's behavior?

Initially, the agent made random moves...as was to be expected by just implementing random.choice() on the action set. Surprisingly, the agent eventually made it to the destination several times.

### Why are these states important?

I decided to use the following inputs:

* Light
* Oncoming
* Right
* Left
* Deadline

I think that the light status, the oncoming status, what's to the left, and what's to the right are important for the agent to learn about the traffic rules of the road. The deadline I initially left out because I thought it might add to much complexity to the lookup table, but I ended up adding it. I added deadline because it would be important for the agent to learn a "sense of urgency" as the deadline approaches. Maybe it's worth running a red light here or there if the deadline is nearing.

### How does Q-learning affect the agent?

Q-learning appears to help add some order to the agent's behavior - more willing to go towards the target and obey traffic rules.

### Changes to basic Q-learning

I have added some inputs to the learning function:

* epsilon
* alpha
* gamma

These parameters affect the tradeoff between exploration and explotation, the learning decay rate, and the future discount on rewards, respectively. Let's dig into Epsilon. This paramater essentially sets the number of times the agent will make a random move, regardless of what it has learned. This is important because there may be unexplored states and the agent could get stuck in a local maxima. In think, if a random number comes back less than epsilon, than the agent is not greeding but decides to explore. Otherwise, he looks for the max score. 

When learning about the world, the agent gathers information every move. Early on, he goes from knowing nothing (0) to knowing something - the reward. However, as the agent continues to revisit a state, the additional information adds less to his knowledge and is discounted by alpha as a result. In this way, we start zeroing in on the expected value instead of constantly jumping from reward to reward - approaching a stable estimate earlier on in the process.

Finally, when learning about the world, we're going to discount future rewards (ie what happens in state2) but the paramater gamma. This feature is important because we can't think only about the future when considering actions today, but we still need to be cognizant of what may be coming down the road. 


### How well does the agent perform?

The agent arrives at the destination every trial in the runs I've performed.

### Does the agent find the optimal policy?

The agent appears to arrive at the destination after fewer steps in each trial - indicating some level of learning. Of course, there is a random element in the starting parameters, but the agent seems to be performing better each trial. More trials would probably help reach the optimal policy in addition to tweaking the alpha, epsilon, and gamma parameters. It would be interesting to save off the q-table between runs and load them to other agents so that they don't have to start from zero.


