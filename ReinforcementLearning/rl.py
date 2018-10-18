# Adapted from Malmo Python tutorial_6.py, copyright 2016 Microsoft Corporation
import MalmoPython
from typing import Optional, Tuple, List, Dict
import json
import logging
import random
import sys
import time

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.handlers = []
logger.addHandler(logging.StreamHandler(sys.stdout))

actions = ["movenorth 1", "movesouth 1", "movewest 1", "moveeast 1"]

max_retries = 3
num_repeats = 150

State = Tuple[int, int]


def run_trials(agent_host):
    # Load the mission

    # -- set up the mission -- #
    mission_xml = """
    <?xml version="1.0" encoding="UTF-8" standalone="no" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

      <About>
        <Summary>Cliff walking mission based on Sutton and Barto.</Summary>
      </About>

      <ServerSection>
        <ServerInitialConditions>
            <Time><StartTime>1</StartTime></Time>
        </ServerInitialConditions>
        <ServerHandlers>
          <FlatWorldGenerator generatorString="15;10,220*1,5*3,2;3;,biome_1"/>
          <DrawingDecorator>
            <!-- coordinates for cuboid are inclusive -->
            <DrawCuboid x1="-2" y1="46" z1="-2" x2="13" y2="50" z2="10" type="air" />            <!-- limits of our arena -->
            <DrawCuboid x1="-2" y1="45" z1="-2" x2="13" y2="45" z2="10" type="lava" />           <!-- lava floor -->
            <DrawCuboid x1="1"  y1="45" z1="1"  x2="11" y2="45" z2="3" type="sandstone" />      <!-- floor of the arena -->
            <DrawCuboid x1="4"  y1="45" z1="1"  x2="7" y2="45" z2="8" type="sandstone" />      <!-- floor of the arena -->
            <DrawCuboid x1="10"  y1="45" z1="1"  x2="12" y2="45" z2="8" type="sandstone" />      <!-- floor of the arena -->
            <DrawBlock x="1"  y="45" z="1" type="cobblestone" />    <!-- the starting marker -->
            <DrawBlock x="11"  y="45" z="7" type="lapis_block" />     <!-- the destination marker -->
          </DrawingDecorator>
          <ServerQuitFromTimeUp timeLimitMs="20000"/>
          <ServerQuitWhenAnyAgentFinishes/>
        </ServerHandlers>
      </ServerSection>

      <AgentSection mode="Survival">
        <Name>Cristina</Name>
        <AgentStart>
          <Placement x="1.5" y="46.0" z="1.5" pitch="30" yaw="0"/>
        </AgentStart>
        <AgentHandlers>
          <DiscreteMovementCommands/>
          <ObservationFromFullStats/>
          <RewardForTouchingBlockType>
            <Block reward="-100.0" type="lava" behaviour="onceOnly"/>
            <Block reward="100.0" type="lapis_block" behaviour="onceOnly"/>
          </RewardForTouchingBlockType>
          <RewardForSendingCommand reward="-1" />
          <AgentQuitFromTouchingBlockType>
              <Block type="lava" />
              <Block type="lapis_block" />
          </AgentQuitFromTouchingBlockType>
        </AgentHandlers>
      </AgentSection>

    </Mission>
    """

    # For Malmo, each episode is a new re-start of the Mission.
    # We want to measure the agent's performance by tracking how much reward it accumulates total over each episode.
    cumulative_rewards: List[float] = []
    q: Dict[Tuple[State, str], float] = {}  # The q-function we're learning
    for i in range(num_repeats):
        print()
        print('Repeat %d of %d' % (i + 1, num_repeats))
        # A mission record tracks the outcome of a given mission
        my_mission_record = MalmoPython.MissionRecordSpec()
        # Retries here have to do with successfully contacting the Malmo server
        for retry in range(max_retries):
            my_mission = MalmoPython.MissionSpec(mission_xml, True)
            # add 10% holes for interest
            for x in range(1, 4):
                for z in range(1, 13):
                    if random.random() < 0.1:
                        my_mission.drawBlock(x, 45, z, "lava")

            try:
                # Here's where the mission starts from the XML
                agent_host.startMission(my_mission, my_mission_record)
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    print("Error starting mission:", e)
                    exit(1)
                else:
                    time.sleep(2.5)

        print("Waiting for the mission to start", end=' ')
        init_state = agent_host.getWorldState()
        # Wait for the mission to start
        while not init_state.has_mission_begun:
            print(".", end="")
            time.sleep(0.1)
            init_state = agent_host.getWorldState()
            for error in init_state.errors:
                print("Error:", error.text)
        print()
        print("Mission start!")
        # OK, now we can finally run the agent
        # -- run the agent in the world -- #
        cumulative_reward = qlearn_episode(q, agent_host)
        print('Cumulative reward: %d' % cumulative_reward)
        cumulative_rewards += [cumulative_reward]

        # -- clean up -- #
        time.sleep(0.5)  # (let the Mod reset)
    print("Total net reward:", sum(cumulative_rewards))
    print("Mean reward:", sum(cumulative_rewards) / float(len(cumulative_rewards)))


def wait_for_observation(agent_host) -> Tuple[MalmoPython.WorldState, float]:
    current_r = 0
    while True:
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            logger.error("Error: %s", error.text)
        for reward in world_state.rewards:
            current_r += reward.getValue()
        if world_state.is_mission_running and len(world_state.observations) > 0 and not world_state.observations[-1].text == "{}":
            break
        if not world_state.is_mission_running:
            break
    return world_state, current_r


def wait_for_nonzero_reward(agent_host) -> Tuple[MalmoPython.WorldState, float]:
    # wait for non-zero reward
    current_r = 0
    world_state = agent_host.getWorldState()
    while world_state.is_mission_running and current_r == 0:
        time.sleep(0.1)
        world_state = agent_host.getWorldState()
        for error in world_state.errors:
            logger.error("Error: %s", error.text)
        for reward in world_state.rewards:
            current_r += reward.getValue()
    return world_state, current_r


def pick_action(state: State, q: Dict[Tuple[State, str], float]) -> str:
    epsilon = 0.01
    # A. Implement your action selection policy here
    return random.choice(actions)


def state_from_malmo(world_state) -> Optional[State]:
    if not world_state.is_mission_running or len(world_state.observations) == 0:
        return None
    obs_text = world_state.observations[-1].text
    obs = json.loads(obs_text)  # most recent observation
    logger.debug(obs)
    if u'XPos' not in obs or u'ZPos' not in obs:
        logger.error("Incomplete observation received: %s", obs_text)
        return None
    return (int(obs[u'XPos']), int(obs[u'ZPos']))


def qlearn_episode(q, agent_host):
    alpha = 0.01
    gamma = 0.001
    # Malmo has some tricky stuff since rewards aren't immediate and the world might not be totally ready yet
    time.sleep(2)
    world_state, _ = wait_for_observation(agent_host)
    net_reward = 0
    reward = 0
    while world_state.is_mission_running:
        # Perform an action, then wait for the reward
        reward = 0
        state = state_from_malmo(world_state)
        if not state:
            continue
        action = pick_action(state, q)
        agent_host.sendCommand(action)
        _, first_reward = wait_for_nonzero_reward(agent_host)
        reward += first_reward
        # Then also wait until our next regular observation because rewards may come in succession
        new_world_state, next_rewards = wait_for_observation(agent_host)
        reward += next_rewards
        print("reward:", reward)
        # Now things have settled down so we can compute new q values
        new_state = state_from_malmo(new_world_state)
        # Now that we have the new state, the reward, and the old state and action choice, we can update q-values
        old_q = q.get((state, action), 0)
        if new_state is None:
            # New state might be None if the mission has ended already
            # B. Do your q-update here
            #q[(state, action)] = ...
            pass
        else:
            pass
            # C. And here.  What's different about this and the case above?
            #q[(state, action)] = ...

        # Now we can finally act again
        world_state = new_world_state
        net_reward += reward
    # Finally, return the net reward.
    return net_reward


if __name__ == "__main__":
    # Malmo boilerplate
    host = MalmoPython.AgentHost()
    try:
        host.parse(sys.argv)
    except RuntimeError as e:
        print('ERROR:', e)
        print(host.getUsage())
        exit(1)
    if host.receivedArgument("help"):
        print(host.getUsage())
        exit(0)

    if host.receivedArgument("test"):
        num_repeats = 1

    run_trials(host)
