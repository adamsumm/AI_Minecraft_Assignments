from __future__ import print_function
from __future__ import division
# ------------------------------------------------------------------------------------------------
# Copyright (c) 2016 Microsoft Corporation
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
# associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute,
# sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT
# NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
# ------------------------------------------------------------------------------------------------

from builtins import range
from past.utils import old_div
import MalmoPython
import json
import math
import os
import random
import sys
import time
import malmoutils

from noise import pnoise3, snoise3


import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as st
malmoutils.fix_print()

agent_host = MalmoPython.AgentHost()
malmoutils.parse_command_line(agent_host)
recordingsDirectory = malmoutils.get_recordings_directory(agent_host)
video_requirements = '<VideoProducer><Width>860</Width><Height>480</Height></VideoProducer>' if agent_host.receivedArgument("record_video") else ''

#-------------------------------------------------------------------------------------------------------------------------------------
#Very simple script to test drawing code - starts a mission in order to draw, but quits after a second.
#-------------------------------------------------------------------------------------------------------------------------------------


def GenTree(x,y,z,trunk_width,trunk_height,leaf_width):
    return '\n'.join([    
                ' '.join(['<DrawCuboid x1="', str(x-trunk_width-1) , 
                           '" y1="' , str(y) , 
                           '" z1="' , str(z-trunk_width-1) , 
                           '" x2="' , str(x+trunk_width) , 
                           '" y2="' , str(y+trunk_height) , 
                           '" z2="' , str(z+trunk_width) , 
                           '" type="log"/>']),
                ' '.join([    '<DrawSphere x="' , str(x) , 
                            '" y="' , str(y+trunk_height+leaf_width) , 
                            '" z="' , str(z) , 
                            '" radius="' , str(leaf_width) ,
                            '" type="leaves"/>']),


        ])

def GenMountain(xx,yy,zz,freq=256,octaves=3,height=80000,width=32):

    data = [[abs(pnoise3(x / freq, y / freq,random.randint(0,10000), octaves)) for x in range(width)] for y in range(width)]
    data = np.array(data)




    def gkern(kernlen=32, nsig=3):
        """Returns a 2D Gaussian kernel array."""

        interval = (2*nsig+1.)/(kernlen)
        x = np.linspace(-nsig-interval/2., nsig+interval/2., kernlen+1)
        kern1d = np.diff(st.norm.cdf(x))
        kernel_raw = np.sqrt(np.outer(kern1d, kern1d))
        kernel = kernel_raw/kernel_raw.sum()
        return kernel

    data = data*height*gkern(width)

    genstring = []
    for y in range(width):
        for x in range(width):
            genstring.append(GenCuboid(int(xx+x-width/2),int(yy),int(zz+y-width/2),int(xx+x-width/2+1),int(yy+data[y][x]),int(zz+y-width/2+1),'bedrock'))
    return '\n'.join(genstring)

def GenCuboid(x1, y1, z1, x2, y2, z2, blocktype):
    return '<DrawCuboid x1="' + str(x1) + '" y1="' + str(y1) + '" z1="' + str(z1) + '" x2="' + str(x2) + '" y2="' + str(y2) + '" z2="' + str(z2) + '" type="' + blocktype + '"/>'

def GenItem(x, y, z, itemtype):
    return '<DrawItem x="' + str(x) + '" y="' + str(y) + '" z="' + str(z) + '" type="' + itemtype + '"/>'
def GenEntity(x,y,z,type):
    return '<DrawEntity x="' + str(x) + '" y="' + str(y) + '" z="' + str(z) + '" type="' + type + '"/>'
#----------------------------------------------------------------------------------------------------------------------------------
#snowy mountain? 3;1*minecraft:bedrock,7*minecraft:dirt,1*minecraft:grass;13;village
#grass field? "3;1*minecraft:bedrock,7*minecraft:dirt,1*minecraft:grass;4;village" />
#3 is desert
#tallgrass is grass

def generate_world_and_description():
    description_string = []
    missionXML = '''<?xml version="1.0" encoding="UTF-8" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <About>
            <Summary></Summary>
        </About>

        <ServerSection>
            <ServerHandlers>
    '''
    in_words = ["I'm in ","I'm standing in "]
    description_string.append(random.choice(in_words))


    locales = [ 
                ("a grassy field ", '<FlatWorldGenerator generatorString="3;1*minecraft:bedrock,7*minecraft:dirt,1*minecraft:grass;4;village" />'),
                ("a snowy field ", '<FlatWorldGenerator generatorString="3;1*minecraft:bedrock,7*minecraft:dirt,1*minecraft:snow;13;village" />'),
                ("the desert ", '<FlatWorldGenerator generatorString="3;1*minecraft:bedrock,7*minecraft:dirt,1*minecraft:sand;2;village" />'),
                ]
    locale = random.choice(locales)

    description_string.append(locale[0])



    things = [('mountains',),
              ('tree','trees','forest',),
              ('river','lake',),
              ('pig',),
              ('cow',),
              ('zombie',),
              ('creeper',)]
    number_of_things = random.randint(1,3)
    missionXML += locale[1] 
    chosen = [random.choice(random.choice(things)) for _ in range(number_of_things)]
    thing_string = []
    to_add = ''
    for c in chosen:
        if c == 'mountains':
            thing_string.append(random.choice(['some mountains',
                                                 'mountains in the distance',
                                                 'mountains',
                                   ]))
            for r in range(random.randint(3,7)):
                to_add += GenMountain(random.randint(-100,100),9,random.randint(50,100),width=random.randint(32,64)) 
    if c == 'tree':
        thing_string.append(random.choice(['a tree','a lonely tree','a tree, all alone']))
        to_add += GenTree(random.randint(-10,10),9,random.randint(0,10),0, random.randint(2,4), random.randint(2,4))
    if c == 'trees':
        thing_string.append(random.choice(['some trees','a few trees']))
        for ii in range(random.randint(2,4)):
            to_add += GenTree(random.randint(-10,10),9,random.randint(0,10), 0,random.randint(2,4), random.randint(2,4))
    if c == 'forest':
        thing_string.append(random.choice(['a forest', 'a dense forest']))
        for ii in range(random.randint(15,30)):
            to_add += GenTree(random.randint(-30,30),9,random.randint(0,30),0, random.randint(2,4), random.randint(2,4))
    if c == 'river':
        pass
    if c == 'lake':
        pass
    if c == 'pig':
        thing_string.append('a pig')
        to_add += GenEntity(random.randint(-10,10),9,random.randint(-5,0),'Pig')
    if c == 'cow':
        thing_string.append('a cow')
        to_add += GenEntity(random.randint(-10,10),9,random.randint(-5,0),'Cow')
    if c == 'sheep':
        thing_string.append('a sheep')
        to_add += GenEntity(random.randint(-10,10),9,random.randint(-5,0),'Sheep`')
    if c == 'zombie':
        thing_string.append('a zombie')
        to_add += GenEntity(random.randint(-10,10),9,random.randint(-5,0),'Zombie')
    if c == 'creeper':
        thing_string.append('a creeper')
        to_add += GenEntity(random.randint(-10,10),9,random.randint(-5,0),'Creeper')

    if len(thing_string) >= 1:
        missionXML +=  '\n<DrawingDecorator>\n' + to_add + '</DrawingDecorator>'
    if len(thing_string) > 2:
        description_string.append('and see')
        description_string.append(', '.join(thing_string[:-1]))

        description_string.append('and ' + thing_string[-1])

    elif len(thing_string) > 1:
        description_string.append('and see')
        description_string.append(thing_string[0] + ' and ' + thing_string[1])
    elif len(thing_string) == 1:
        description_string.append('and see')
        description_string.append(thing_string[0])
    missionXML += '''
                <ServerQuitFromTimeUp timeLimitMs="1000" description="out_of_time"/>
                <ServerQuitWhenAnyAgentFinishes />
            </ServerHandlers>
        </ServerSection>

        <AgentSection mode="Survival">
            <Name>The Explorer</Name>
            <AgentStart>
                <Placement x="0.5" y="9.0" z="-10"/>
            </AgentStart>
            <AgentHandlers>
                <ObservationFromFullStats/>
                <ObservationFromGrid>
                    <Grid name="nearby">
                        <min x="-1" y="-1" z="-1"/>
                        <max x="1" y="-1" z="1"/>
                    </Grid>
                    <Grid name="far" absoluteCoords="true">
                        <min x="12" y="79" z="417"/>
                        <max x="14" y="79" z="419"/>
                    </Grid>
                    <Grid name="very_far" absoluteCoords="true">
                        <min x="-10711" y="55" z="347"/>
                        <max x="-10709" y="55" z="349"/>
                    </Grid>
                </ObservationFromGrid>''' + video_requirements + '''
            </AgentHandlers>
        </AgentSection>

    </Mission>'''
    return ' '.join(description_string).replace('  ',' '), missionXML


missionXML = '''<?xml version="1.0" encoding="UTF-8" ?>
    <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
        <About>
            <Summary>It's Fun To Build Things!</Summary>
        </About>

        <ServerSection>
            <ServerHandlers>
                <FlatWorldGenerator generatorString="3;1*minecraft:bedrock,7*minecraft:dirt,1*minecraft:snow;1;village" />
                <DrawingDecorator>'''+ GenMountain(0,9,50,width=32) + GenMountain(-50,9,50,width=32) + GenMountain(30,9,40,width=32) +'\n' +GenTree(0,9,0, 0, 4, 4)  +'''
                </DrawingDecorator>
                <ServerQuitFromTimeUp timeLimitMs="1000" description="out_of_time"/>
                <ServerQuitWhenAnyAgentFinishes />
            </ServerHandlers>
        </ServerSection>

        <AgentSection mode="Survival">
            <Name>The Explorer</Name>
            <AgentStart>
                <Placement x="0.5" y="9.0" z="-10"/>
            </AgentStart>
            <AgentHandlers>
                <ObservationFromFullStats/>
                <ObservationFromGrid>
                    <Grid name="nearby">
                        <min x="-1" y="-1" z="-1"/>
                        <max x="1" y="-1" z="1"/>
                    </Grid>
                    <Grid name="far" absoluteCoords="true">
                        <min x="12" y="79" z="417"/>
                        <max x="14" y="79" z="419"/>
                    </Grid>
                    <Grid name="very_far" absoluteCoords="true">
                        <min x="-10711" y="55" z="347"/>
                        <max x="-10709" y="55" z="349"/>
                    </Grid>
                </ObservationFromGrid>''' + video_requirements + '''
            </AgentHandlers>
        </AgentSection>

    </Mission>'''

description_string, missionXML = generate_world_and_description()
print(description_string)
my_mission = MalmoPython.MissionSpec(missionXML,True)
my_mission_record = MalmoPython.MissionRecordSpec()
if recordingsDirectory:
    my_mission_record.recordRewards()
    my_mission_record.recordObservations()
    my_mission_record.recordCommands()
    my_mission_record.setDestination(recordingsDirectory + "//" + "Mission_1.tgz")
    if agent_host.receivedArgument("record_video"):
        my_mission_record.recordMP4(24,2000000)

max_retries = 3
for retry in range(max_retries):
    try:
        agent_host.startMission( my_mission, my_mission_record )
        break
    except RuntimeError as e:
        if retry == max_retries - 1:
            print("Error starting mission",e)
            print("Is the game running?")
            exit(1)
        else:
            time.sleep(2)

world_state = agent_host.peekWorldState()
while not world_state.has_mission_begun:
    time.sleep(0.1)
    world_state = agent_host.peekWorldState()
    
while world_state.is_mission_running:
    world_state = agent_host.peekWorldState()

# We also use this sample as a test. In this section we verify that
# the expected things were received.
if agent_host.receivedArgument("test"):
    # check the height of the player in the last observation    
    assert len(world_state.observations) > 0, 'No observations received'
    obs = json.loads( world_state.observations[-1].text )
    player_y = obs[u'YPos']
    print('Player at y =',player_y)
    assert math.fabs( player_y - 83.0 ) < 0.01, 'Player not at expected height'
    
    # check the grid observations
    for obs in world_state.observations:
        assert '"nearby":["air","quartz_block","quartz_block","air","wool","wool","air","wool","air"]' in obs.text, 'Nearby observation incorrect:'+obs.text
        assert '"far":["ice","ice","air","ice","ice","air","quartz_block","quartz_block","quartz_block"]' in obs.text, 'Far observation incorrect:'+obs.text
        assert '"very_far":["stained_glass","stained_glass","stained_glass","stained_glass","stained_glass","stained_glass","stained_glass","stained_glass","stained_glass"]' in obs.text, 'Vey far observation incorrect:'+obs.text

# mission has ended.
print("Mission over - feel free to explore the world.")
