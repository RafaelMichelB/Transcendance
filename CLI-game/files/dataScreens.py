import json


class Screen :
    def __init__(self, jsonPath="./files/screens/screens.json") :
        with open(jsonPath) as jsonFile :
            self.info = json.load(jsonFile)
    
    def __str__(self) :
        return f"Informations : {self.info}"
    
    def getSpecificInfo(self, screen : str) :
        return self.info.get(screen, {})


def loadInfo(dictionnaryInfo : dict) : 
    with open(f'./files/screens/{dictionnaryInfo["fileID"]}') as file :
        toReturn = file.read()
    return toReturn

"""
+------------------------------------------------------------------------------------+
|                                                                                    |
|                                             _                                      |
|                                            /*\                                     |
|                                    +------+---+-----+                              |
|                                    |     Welcome    |                              |
|                                    |  Waiting for   |                              |
|                                    |    player2     |                              |
|                                    +----------------+                              |
|                                                                                    |
|                                                                                    |
|                                                                                    |
|                                                                                    |
|                                                                                    |
|                 *                                                 *                |
|                 |                                                 |                |
|            ____/ \_______________________________________________/ \____           |
|           /                                                             \          |
|          |              Room ID to give :                                |         |
|           \_____________________________________________________________/          |
|                                                                                    |
|                                                                                    |
|                                                                                    |
|                                                                                    |
+------------------------------------------------------------------------------------+
"""
