# coding=utf-8
from mod.client.system.clientSystem import ClientSystem
import mod.client.extraClientApi as clientApi
import random


class ModUiRegister(ClientSystem):
    def __init__(self, namespace, systemName):
        ClientSystem.__init__(self, namespace, systemName)
        self.Listen()
        self.stats = None
        self.PlayerId = clientApi.GetLocalPlayerId()
        self.tick = 0

    # 监听
    def Listen(self):
        self.ListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "UiInitFinished", self,
                            self.OnUIInitFinished)
        self.ListenForEvent("DoomsdaySurvivalMod", "ServerManager", "BroadCastServerEvent", self, self.OnUpdate)
        self.ListenForEvent("DoomsdaySurvivalMod", "ServerManager", "DamageChangeEvent", self, self.OnDamageChangeEvent)
        self.ListenForEvent("DoomsdaySurvivalMod", "ServerManager", "MobDieChangeEvent", self, self.OnMobDieChangeEvent)
        self.ListenForEvent("DoomsdaySurvivalMod", "ServerManager", "DestoryChangeEvent", self,
                            self.OnDestoryChangeEvent)
        self.ListenForEvent("DoomsdaySurvivalMod", "ServerManager", "PlayerDieChangeEvent", self,
                            self.OnPlayerDieChangeEvent)

    # 销毁
    def Destory(self):
        self.UnListenForEvent(clientApi.GetEngineNamespace(), clientApi.GetEngineSystemName(), "UiInitFinished", self,
                              self.OnUIInitFinished)
        self.UnListenForEvent("DoomsdaySurvivalMod", "ServerManager", "BroadCastServerEvent", self, self.OnUpdate)
        self.UnListenForEvent("DoomsdaySurvivalMod", "ServerManager", "DamageChangeEvent", self,
                              self.OnDamageChangeEvent)
        self.UnListenForEvent("DoomsdaySurvivalMod", "ServerManager", "MobDieChangeEvent", self,
                              self.OnMobDieChangeEvent)
        self.UnListenForEvent("DoomsdaySurvivalMod", "ServerManager", "DestoryChangeEvent", self,
                              self.OnDestoryChangeEvent)
        self.UnListenForEvent("DoomsdaySurvivalMod", "ServerManager", "PlayerDieChangeEvent", self,
                              self.OnPlayerDieChangeEvent)

    # 初始化
    def OnUIInitFinished(self, args):
        clientApi.RegisterUI("DoomsdaySurvivalMod", "Panel", "survivalScripts.clientManager.screenManager"
                                                             ".screenManager", "panel.main")
        clientApi.RegisterUI("DoomsdaySurvivalMod", "Store", "survivalScripts.clientManager.storeManager"
                                                             ".StoreManager", "store.main")
        clientApi.RegisterUI("DoomsdaySurvivalMod", "Button", "survivalScripts.clientManager.buttonManager"
                                                              ".ButtonManager", "button.main")

        mButtonNode = clientApi.CreateUI("DoomsdaySurvivalMod", "Button", {"isHud": 1})
        mStatsUINode = clientApi.CreateUI("DoomsdaySurvivalMod", "Panel", {"isHud": 1})
        mStoreUINode = clientApi.CreateUI("DoomsdaySurvivalMod", "Store", {"isHud": 1})

        mButtonPanel = mButtonNode.GetBaseUIControl("/panel0/button0")
        mButtonPanel2 = mButtonNode.GetBaseUIControl("/panel0/button1")
        mStatsPanel = mStatsUINode.GetBaseUIControl("/panel0")

        mStatsPanel.SetVisible(False)
        mButtonPanel2.SetVisible(False)
        mStoreUINode.GetBaseUIControl("/panel0").SetVisible(False)
        mButtonPanel.SetVisible(True)

    def OnPlayerDieChangeEvent(self, data):
        playerId2 = data["playerId"]
        stats = clientApi.CreateComponent(playerId2, "DoomsdaySurvivalMod", "statsComponent")

        stats.SetEyi(False)
        stats.SetInfectionPoints(0)
        stats.SetSurvivalPoints(0)
        stats.SetSurvivalLevel(0)

    def OnDestoryChangeEvent(self, data):
        playerId2 = data["playerId"]
        stats = clientApi.CreateComponent(playerId2, "DoomsdaySurvivalMod", "statsComponent")

        if stats.GetInfectionPoints() > 50:
            comp = clientApi.GetEngineCompFactory().CreateGame(playerId2)
            comp.SetPopupNotice(clientApi.GenerateColor("RED") + "警告", "你的感染值已达到 一半 以上 请注意把控! ")
        amount = stats.GetInfectionPoints() + 0.05
        stats.SetInfectionPoints(amount)

    def OnDamageChangeEvent(self, data):
        playerId2 = data["PlayerId"]
        stats = clientApi.CreateComponent(playerId2, "DoomsdaySurvivalMod", "statsComponent")
        if stats.is_Eyi():
            return
        if stats.GetInfectionPoints() > 50:
            comp = clientApi.GetEngineCompFactory().CreateGame(playerId2)
            comp.SetPopupNotice(clientApi.GenerateColor("RED") + "警告", "你的感染值已达到 一半 以上 请注意把控! ")
        amount = stats.GetInfectionPoints() + 6.0
        stats.SetInfectionPoints(amount)

    def OnMobDieChangeEvent(self, data):
        playerId2 = data["PlayerId"]
        stats = clientApi.CreateComponent(playerId2, "DoomsdaySurvivalMod", "statsComponent")
        chance = random.uniform(1.0, 100.0)
        if stats.is_Eyi():
            amount = stats.GetInfenctionPoints() - 0.8
            stats.SetInfenctionPoints(amount)
            if 75.0 > chance:
                if stats.GetSurvivalPoints() < 300:
                    comp = clientApi.GetEngineCompFactory().CreateGame(playerId2)
                    comp.SetPopupNotice(clientApi.GenerateColor("BLUE") + "恭喜",
                                        clientApi.GenerateColor("WHITE") + "你获得了 1 点生存点数")
                    amount = stats.GetSurvivalPoints() + 1
                    stats.SetSurvivalPoints(amount)
                else:
                    comp = clientApi.GetEngineCompFactory().CreateGame(playerId2)
                    comp.SetPopupNotice(clientApi.GenerateColor("RED") + "警告", "你的生存点数已到达饱和 ")
            return
        if 12.0 > chance:
            if stats.GetSurvivalPoints() < 300:
                comp = clientApi.GetEngineCompFactory().CreateGame(playerId2)
                comp.SetPopupNotice(clientApi.GenerateColor("BLUE") + "恭喜",
                                    clientApi.GenerateColor("WHITE") + "你获得了 1 点生存点数")
                amount = stats.GetSurvivalPoints() + 1
                stats.SetSurvivalPoints(amount)
            else:
                comp = clientApi.GetEngineCompFactory().CreateGame(playerId2)
                comp.SetPopupNotice(clientApi.GenerateColor("RED") + "警告", "你的生存点数已到达饱和 ")

    def OnUpdate(self, dayInfo):
        day = dayInfo.get("day", "1")
        uiNode = clientApi.GetUI("DoomsdaySurvivalMod", "Panel")
        stats = clientApi.CreateComponent(self.PlayerId, "DoomsdaySurvivalMod", "statsComponent")

        if stats.GetInfectionPoints() < 0:
            stats.SetInfectionPoints(0)

        if stats.GetSurvivalPoints() < 0:
            stats.SetSurvivalPoints(0)

        survivalPoints = uiNode.GetBaseUIControl("/panel0/panel2/label2").asLabel()
        survivalPoints.SetText(str(stats.GetSurvivalPoints()) + " / 300")

        Progress = uiNode.GetBaseUIControl("/panel0/panel2/progress_bar1").asProgressBar()
        infection = stats.GetInfectionPoints() / 100.0
        Progress.SetValue(infection)

        Progress2 = uiNode.GetBaseUIControl("/panel0/panel2/progress_bar0").asProgressBar()
        survivalLevel = stats.GetSurvivalLevel() / 100
        Progress2.SetValue(survivalLevel)

        survivalDays = uiNode.GetBaseUIControl("/panel0/panel2/label1").asLabel()
        survivalDays.SetText(str(day) + " 天")

    def Update(self):
        self.tick = self.tick + 1
        Data = self.CreateEventData()
        Data["id"] = clientApi.GetLocalPlayerId()
        self.NotifyToServer("BroadCastClientEvent", Data)
        stats = clientApi.CreateComponent(self.PlayerId, "DoomsdaySurvivalMod", "statsComponent")
        if stats.GetSurvivalLevel() < 0:
            stats.SetSurvivalLevel(0)
            stats.SetEyi(False)
        if stats.GetSurvivalLevel() >= 100:
            uiNode = clientApi.GetUI("DoomsdaySurvivalMod", "Button")
            buttonUIControl2 = uiNode.GetBaseUIControl("/panel0/button1").asButton()
            buttonUIControl2.SetVisible(True)
        if self.tick > 150:
            self.tick = 0
            if stats.is_Eyi():
                eyi = stats.GetSurvivalLevel() - 3
                stats.SetSurvivalLevel(eyi)

            if stats.GetInfectionPoints() >= 100:
                Data = self.CreateEventData()
                Data["playerId"] = clientApi.GetLocalPlayerId()
                self.NotifyToServer("RemoveHealthEvent", Data)
                comp = clientApi.GetEngineCompFactory().CreateGame(self.PlayerId)
                comp.SetPopupNotice(clientApi.GenerateColor("RED") + "警告",
                                    clientApi.GenerateColor("WHITE") + "你的感染值已满.. 你将会持续减血...")
