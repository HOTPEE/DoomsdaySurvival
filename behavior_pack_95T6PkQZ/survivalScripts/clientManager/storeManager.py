# coding=utf-8
from mod.client.ui.screenNode import ScreenNode

import mod.client.extraClientApi as clientApi


class StoreManager(ScreenNode):
    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
        self.playerId = clientApi.GetLocalPlayerId()

    def Create(self):
        storeNode = clientApi.GetUI("DoomsdaySurvivalMod", "Store")
        jinghuaPurchaseButton = storeNode.GetBaseUIControl("/panel0/shangpin1/image2/button0").asButton()
        jinghuaPurchaseButton.AddTouchEventParams({"isSwallow": True})
        jinghuaPurchaseButton.SetButtonTouchUpCallback(self.PurchaseCallback)

        eyiPurchaseButton = storeNode.GetBaseUIControl("/panel0/shangpin2/image3/button2").asButton()
        eyiPurchaseButton.AddTouchEventParams({"isSwallow": True})
        eyiPurchaseButton.SetButtonTouchUpCallback(self.PurchaseCallback)

        closeButton = storeNode.GetBaseUIControl("/panel0/button1").asButton()
        closeButton.AddTouchEventParams({"isSwallow": True})
        closeButton.SetButtonTouchUpCallback(self.PurchaseCallback)

    def PurchaseCallback(self, args):
        storeNode = clientApi.GetUI("DoomsdaySurvivalMod", "Store")
        if args["ButtonPath"] == "/panel0/shangpin1/image2/button0":
            stats = clientApi.CreateComponent(self.playerId, "DoomsdaySurvivalMod", "statsComponent")
            storePanel = storeNode.GetBaseUIControl("/panel0")
            comp = clientApi.GetEngineCompFactory().CreateGame(self.playerId)
            if stats.GetSurvivalPoints() < 50:
                comp.SetPopupNotice(clientApi.GenerateColor("RED") + "警告",
                                    clientApi.GenerateColor("WHITE") + "购买失败! 你的生存点数不足")
                storePanel.SetVisible(False)
                buttonNode = clientApi.GetUI("DoomsdaySurvivalMod", "Button")
                buttonUIControl = buttonNode.GetBaseUIControl("/panel0/button0").asButton()
                buttonUIControl.SetVisible(True)
            else:
                amount = stats.GetSurvivalPoints() - 50
                infectionAmounts = stats.GetInfectionPoints() - 50.0
                stats.SetSurvivalPoints(amount)
                stats.SetInfectionPoints(infectionAmounts)
                comp.SetPopupNotice(clientApi.GenerateColor("BLUE") + "成功",
                                    clientApi.GenerateColor("WHITE") + "你购买了净化药水 你的感染值降低了 50%")
                storePanel.SetVisible(False)
                buttonNode = clientApi.GetUI("DoomsdaySurvivalMod", "Button")
                buttonUIControl = buttonNode.GetBaseUIControl("/panel0/button0").asButton()
                buttonUIControl.SetVisible(True)

        if args["ButtonPath"] == "/panel0/shangpin2/image3/button2":
            stats = clientApi.CreateComponent(self.playerId, "DoomsdaySurvivalMod", "statsComponent")
            storePanel = storeNode.GetBaseUIControl("/panel0")
            comp = clientApi.GetEngineCompFactory().CreateGame(self.playerId)
            if stats.GetSurvivalPoints() < 100:
                comp.SetPopupNotice(clientApi.GenerateColor("RED") + "警告",
                                    clientApi.GenerateColor("WHITE") + "购买失败! 你的生存点数不足")
                storePanel.SetVisible(False)
                buttonNode = clientApi.GetUI("DoomsdaySurvivalMod", "Button")
                buttonUIControl = buttonNode.GetBaseUIControl("/panel0/button0").asButton()
                buttonUIControl.SetVisible(True)
            else:
                amount = stats.GetSurvivalPoints() - 100
                infectionAmounts = stats.GetSurvivalLevel() + 50
                stats.SetSurvivalPoints(amount)
                stats.SetSurvivalLevel(infectionAmounts)
                comp.SetPopupNotice(clientApi.GenerateColor("BLUE") + "成功",
                                    clientApi.GenerateColor("WHITE") + "你购买了净化药水 你的恶意值增加了 50%")
                storePanel.SetVisible(False)
                buttonNode = clientApi.GetUI("DoomsdaySurvivalMod", "Button")
                buttonUIControl = buttonNode.GetBaseUIControl("/panel0/button0").asButton()
                buttonUIControl.SetVisible(True)

        if args["ButtonPath"] == "/panel0/button1":
            storeNode = clientApi.GetUI("DoomsdaySurvivalMod", "Store")
            buttonNode = clientApi.GetUI("DoomsdaySurvivalMod", "Button")
            buttonUIControl = buttonNode.GetBaseUIControl("/panel0/button0").asButton()
            buttonUIControl.SetVisible(True)
            storeNode.GetBaseUIControl("/panel0").SetVisible(False)
