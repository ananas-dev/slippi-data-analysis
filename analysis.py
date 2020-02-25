# File --analysis.py--

import numpy as np
import pandas as pd

## CHARACTER ##

#def characters(game, port):
#    characters = [x.character for x in game.start.players if x != None]
#    return(characters[port])

## DATA FRAME ##
class Data:
    def __init__(self, game, port, port2):
        self.game = game
        self.port = port
        self.port2 = port2

    def Stage(self):
        stage = self.game.start.stage
        return(stage)

    def ProcessData(self):
       
        df = pd.DataFrame()
       
        # State of the main player 
        df['state'] = [x.ports[self.port].leader.post.state
                for x in self.game.frames]
        df = df.loc[df['state'].shift(-1) != df['state']]
        df = df.loc[df['state'].isin([199, 200, 201])]
    
        # Character's id of the main player
        df['character'] = [[x.ports[self.port].leader.post.character
                for x in self.game.frames][index] for index in df.index]
        
        # Position of main player on the x axis
        df['position_x'] = [[x.ports[self.port].leader.post.position.x
                for x in self.game.frames][index] for index in df.index]

        # Position of the main player on the y axis
        df['position_y'] = [[x.ports[self.port].leader.post.position.y
                for x in self.game.frames][index] for index in df.index]
        
        # Damage of the main player
        damage_unfiltered = [[x.ports[self.port].leader.post.damage
                for x in self.game.frames][index] for index in df.index]
        damage = []
        for x in damage_unfiltered:
                if 0 <= x <= 20:
                        damage.append(1) # Low
                elif 20 < x <= 70:
                        damage.append(2) # Middle
                elif 70 < x <= 110:
                        damage.append(3) # High
                elif 110 < x <= 999:
                        damage.append(4) # Very high
        df['damage'] = damage
        
        # Stock count of the main player
        df['stocks'] = [[x.ports[self.port].leader.post.stocks
                for x in self.game.frames][index] for index in df.index]

        # Character's id of the opponent
        df['character_op'] = [[x.ports[self.port2].leader.post.character
                for x in self.game.frames][index] for index in df.index]

        # Position of the opponent on the x axis
        position_x_op = [[x.ports[self.port2].leader.post.position.x
                for x in self.game.frames][index] for index in df.index]

        # Position of the opponent on the y axis
        position_y_op = [[x.ports[self.port2].leader.post.position.y
                for x in self.game.frames][index] for index in df.index]

        # Distance between the 2 players
        diff_x_squared = np.array(np.square(np.subtract(df['position_x'], position_x_op)))
        diff_y_squared = np.array(np.square(np.subtract(df['position_y'], position_y_op)))
        diffs = np.array(np.add(diff_x_squared, diff_y_squared))
        df['dist'] = np.array(np.sqrt(diffs))

        # Angle between the 2 players
        diff_x = np.array(np.subtract(df['position_x'], position_x_op))
        diff_y = np.array(np.subtract(df['position_y'], position_y_op))
        df['angle'] = np.array(np.arctan2(diff_y, diff_x)* 180 / np.pi)

        # Last attack landed by the opponent    
        last_attack_landed_op_unfiltered = [[0 if x.ports[self.port2].leader.post.last_attack_landed == None 
                else x.ports[self.port2].leader.post.last_attack_landed.value for x in self.game.frames][index]
                for index in df.index]
        
        last_attack_landed_op = []
        for x in last_attack_landed_op_unfiltered:
                if x == 1:
                        last_attack_landed_op.append(4) # Other
                elif 1 < x <= 12:
                        last_attack_landed_op.append(2) # 
                elif 12 < x <= 17:
                        last_attack_landed_op.append(3)
                elif 17 < x <= 21:
                        last_attack_landed_op.append(3)
                elif 49 < x <= 52:
                        last_attack_landed_op.append(2)
                elif 52 < x <= 56:
                        last_attack_landed_op.append(1)
                elif 60 < x <= 62:
                        last_attack_landed_op.append(4) #Other
        df['last_attack_landed_op'] = last_attack_landed_op




        return(df)
