import sys
import json
sys.path.append("/Games/th-umb")
def saveWorld(logic):
    world_key = f"world_{logic.worldCoords[0]}_{logic.worldCoords[1]}_{logic.floor}"
    
    data = {
        "world": list(logic.world),
        "worldType": logic.worldType,
        "waterLine": logic.waterLine,
        "entities": logic.el.entities if logic.el else [],
        "floor": logic.floor
    }
    try:
        try:
            with open('/Games/th-umb/worlds.json', "r") as save_file:
                all_worlds = json.load(save_file)
        except (OSError, Exception):
            all_worlds = {}
        
        all_worlds[world_key] = data
        
        with open('/Games/th-umb/worlds.json', "w") as save_file:
            json.dump(all_worlds, save_file)
        
        print("World saved successfully.")
    except OSError as e:
        print("Error saving world:", e)
    
def loadWorld(logic, Logic, sprites):
    
    world_key = f"world_{logic.worldCoords[0]}_{logic.worldCoords[1]}_{logic.floor}"
    
    try:
        with open('/Games/th-umb/worlds.json', "r") as save_file:
            try:
                all_worlds = json.load(save_file)
            except Exception:
                print("Error: Save file is empty or contains invalid JSON.")
                return False
        
            if world_key in all_worlds:
                data = all_worlds[world_key]
                logic.world = bytearray(data.get("world", [0] * len(logic.world)))
                logic.worldType = data.get("worldType", 0)
                logic.waterLine = list(data.get("waterLine", [0, 0, 0]))
                logic.floor = data.get("floor", 0)
                allEntities = list(data.get("entities", []))
                
                if logic.firstLoad:
                    logic.el = Logic(logic, allEntities, sprites)
                    logic.firstLoad = False
                else:
                    logic.el.entities = allEntities
                
                print("World loaded successfully")
                print("World Pos:", logic.worldCoords[0], logic.worldCoords[1])
                return True
            else:
                print("No data found for world at", logic.worldCoords[0], logic.worldCoords[1])
                return False
    except OSError as e:
        if e.args[0] == 2:
            print("Save file not found. Generating a new world.")
            return False
        else:
            print("Error loading world:", e)
            return False

def loadSpecificWorld(logic, Logic, sprites, worldID):
    try:
        with open('/Games/th-umb/pSave.json', "r") as save_file:
            try:
                all_worlds = json.load(save_file)
            except Exception:
                print("Error: Save file is empty or contains invalid JSON.")
                return False
        
            if worldID < len(all_worlds):
                data = all_worlds[worldID]
                logic.world = bytearray(data.get("world", [0] * len(logic.world)))
                logic.worldType = data["worldType"]
                logic.waterLine = [0,0,0]
                allEntities = data.get("entities", [])
                
                if logic.firstLoad:
                    logic.el = Logic(logic, allEntities, sprites)
                    logic.firstLoad = False
                else:
                    logic.el.entities = allEntities
                    
                print("World loaded successfully:", logic.world, logic.worldType, logic.waterLine)
                print("World Pos:", logic.worldCoords[0], logic.worldCoords[1])
                return True
            else:
                print("No data found for world at", logic.worldCoords[0], logic.worldCoords[1])
                return False
    except OSError as e:
        if e.args[0] == 2:
            print("Save file not found. Generating a new world.")
            return False
        else:
            print("Error loading world:", e)
            return 

def playerSave(logic):
    data = {
        "pos": list(logic.pInt),
        "inv": list(logic.inv),
        "worldLoc": list(logic.worldCoords),
        "beds": list(logic.beds)
    }
    
    try:
        with open('/Games/th-umb/charSave.json', "w") as save_file:
            save_file.write('')
            json.dump(data, save_file)
    except OSError as e:
        print("Error saving player:", e)
        pass

def playerLoad(logic):
    try:
        with open('/Games/th-umb/charSave.json', "r") as save_file:
            try:
                playerData = json.load(save_file)
            except json.JSONDecodeError:
                print("Error: Save file is empty or contains invalid JSON.")
                return False
            
            logic.pInt = playerData.get("pos", [0, 0])
            logic.inv = playerData.get("inv", [0] * 8)
            logic.worldCoords = playerData.get("worldLoc", [0, 0])
            logic.beds = playerData.get("beds", [0, 0])
                
            print("Player loaded successfully:", logic.pInt, logic.inv)
            print("World Pos:", logic.worldCoords[0], logic.worldCoords[1])
            print("Beds: ", logic.beds)
            return True
    except OSError as e:
        if e.errno == 2:
            print("Save file not found.")
        else:
            print("Error loading player:", e)
        return False
