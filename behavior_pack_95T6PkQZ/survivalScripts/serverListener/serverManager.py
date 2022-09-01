# coding=utf-8
import mod.server.extraServerApi as serverApi

ServerSystem = serverApi.GetServerSystemCls()
import mod.server.extraServerApi as serverApi
import mod.common.minecraftEnum as enum
import random


class ServerManager(ServerSystem):
    def __init__(self, namespace, systemName):
        ServerSystem.__init__(self, namespace, systemName)
        self.ListenEvent()
        self.tick = 0

    def ListenEvent(self):
        self.ListenForEvent("DoomsdaySurvivalMod", "ModUiRegister", "BroadCastClientEvent", self, self.OnBroadCast)
        self.ListenForEvent("DoomsdaySurvivalMod", "ModUiRegister", "RemoveHealthEvent", self, self.OnRemoveHealth)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "DamageEvent", self,
                            self.OnDamageEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "MobDieEvent", self,
                            self.OnMobDieEvent)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "DestroyBlockEvent", self,
                            self.OnDestoryBlock)
        self.ListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "PlayerDieEvent", self,
                            self.OnPlayerDieEvent)

    def Destory(self):
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "DestroyBlockEvent", self,
                            self.OnDestoryBlock)
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "MobDieEvent", self,
                            self.OnMobDieEvent)
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "DamageEvent", self,
                            self.OnDamageEvent)
        self.UnListenForEvent(serverApi.GetEngineNamespace(), serverApi.GetEngineSystemName(), "PlayerDieEvent", self,
                            self.OnPlayerDieEvent)
        self.UnListenForEvent("DoomsdaySurvivalMod", "ModUiRegister", "BroadCastClientEvent", self, self.OnBroadCast)
        self.UnListenForEvent("DoomsdaySurvivalMod", "ModUiRegister", "RemoveHealthEvent", self, self.OnBroadCast)

    def OnBroadCast(self, args):
        comp = serverApi.GetEngineCompFactory().CreateTime(serverApi.GetLevelId())
        passedTime = comp.GetTime()
        day = passedTime / 24000

        dayInfo = self.CreateEventData()
        dayInfo["day"] = day
        self.BroadcastToAllClient("BroadCastServerEvent", dayInfo)

    def OnRemoveHealth(self, args):
        playerId = args['playerId']
        comp = serverApi.GetEngineCompFactory().CreateAttr(playerId)
        comp2 = serverApi.GetEngineCompFactory().CreateEffect(playerId)
        comp2.AddEffectToEntity("hunger", 5, 10, True)
        health = comp.GetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH)
        amount = health - 2
        comp.SetAttrValue(serverApi.GetMinecraftEnum().AttrType.HEALTH, amount)

    # 挖掘事件
    def OnDestoryBlock(self, args):
        playerId = args['playerId']
        data = self.CreateEventData()
        data['playerId'] = playerId
        self.NotifyToClient(playerId, "DestoryChangeEvent", data)

    def OnPlayerDieEvent(self, args):
        self.tick = self.tick + 1
        comp = serverApi.GetEngineCompFactory().CreateTime(serverApi.GetLevelId())
        comp.SetTime(0)
        playerId = args['id']
        data = self.CreateEventData()
        data['playerId'] = playerId
        self.NotifyToClient(playerId, "PlayerDieChangeEvent", data)

    # 伤害事件
    def OnDamageEvent(self, args):
        victim = args["entityId"]
        cause = args["cause"]

        if cause == enum.ActorDamageCause.EntityAttack:
            data = self.CreateEventData()
            data["PlayerId"] = victim
            self.NotifyToClient(victim, "DamageChangeEvent", data)

    # 死亡事件
    def OnMobDieEvent(self, args):
        attacker = args["attacker"]
        data = self.CreateEventData()
        data["PlayerId"] = attacker
        self.NotifyToClient(attacker, "MobDieChangeEvent", data)

    def Update(self):
        self.tick = self.tick + 1
        comp = serverApi.GetEngineCompFactory().CreateDimension(serverApi.GetLevelId())
        passedTime = comp.GetLocalTime(0)
        day = passedTime / 24000
        day2 = day * 4
        delay = 500 - day2
        if delay < 60:
            delay = 60
        if self.tick > delay:
            self.tick = 0
            night3 = 24000 * day
            night2 = 23000 + night3
            night = 14000 + night3
            if night2 > passedTime > night:
                for playerId in serverApi.GetPlayerList():
                    comp = serverApi.GetEngineCompFactory().CreatePos(playerId)
                    entityFootPos = comp.GetPos()
                    playerX = entityFootPos[0]
                    playerY = entityFootPos[1]
                    playerZ = entityFootPos[2]
                    randomX = random.randint(-5, 10)
                    randomZ = random.randint(-5, 10)

                    spawnLocX = playerX + randomX
                    spawnLocZ = playerZ + randomZ
                    comp = serverApi.GetEngineCompFactory().CreateBlockInfo(serverApi.GetLevelId())
                    blockData = comp.GetBlockNew((int(spawnLocX), int(playerY - 1), int(spawnLocZ)), 0)
                    blockData2 = comp.GetBlockNew((int(spawnLocX), int(playerY + 1), int(spawnLocZ)), 0)
                    while blockData2['name'] != "minecraft:air":
                        playerY = playerY + 1
                        blockData2 = comp.GetBlockNew((int(spawnLocX), int(playerY + 1), int(spawnLocZ)), 0)
                    while blockData['name'] == "minecraft:air":
                        playerY = playerY - 1
                        blockData = comp.GetBlockNew((int(spawnLocX), int(playerY - 1), int(spawnLocZ)), 0)

                    randomSpawn = random.randint(1, 3)
                    if randomSpawn == 1:
                        self.CreateEngineEntityByTypeStr('minecraft:zombie', (spawnLocX, playerY, spawnLocZ),
                                                                (0, 0), 0)
                    elif randomSpawn == 2:
                        self.CreateEngineEntityByTypeStr('minecraft:spider', (spawnLocX, playerY, spawnLocZ),
                                                                (0, 0), 0)
                    elif randomSpawn == 3:
                        self.CreateEngineEntityByTypeStr('minecraft:husk', (spawnLocX, playerY, spawnLocZ),
                                                                (0, 0), 0)
