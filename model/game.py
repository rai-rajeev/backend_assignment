import json
class Game:
    def __init__(self,id:str,player1_name:str,player2_name:str,result:str,winner:str,states:list,mine_x:int,mine_y:int):
        self.id=id
        self.player1_name=player1_name
        self.player2_name=player2_name
        self.result=result
        self.winner=winner
        self.states=states
        self.mine_x=mine_x
        self.mine_y=mine_y
    def to_json(self):
        return{
            "id":self.id,
            "player1_name":self.player1_name,
            "player2_name":self.player2_name,
            "result":self.result,
            "winner":self.winner,
            "states":self.states,
            "mine_x":self.mine_x,
            "mine_y":self.mine_y

        }