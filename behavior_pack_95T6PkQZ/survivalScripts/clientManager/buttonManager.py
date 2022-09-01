from mod.client.ui.screenNode import ScreenNode

import mod.client.extraClientApi as clientApi


class ButtonManager(ScreenNode):
    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
        self.uiNode = None
        self.buttonUIControl = None
        self.buttonUIControl2 = None
        self.playerId = clientApi.GetLocalPlayerId()

    def Create(self):
        self.uiNode = clientApi.GetUI("DoomsdaySurvivalMod", "Button")
        self.buttonUIControl = self.uiNode.GetBaseUIControl("/panel0/button0").asButton()
        self.buttonUIControl.AddTouchEventParams({"isSwallow": True})
        self.buttonUIControl.SetButtonTouchUpCallback(self.onButtonTouchUpCallback)

        self.buttonUIControl2 = self.uiNode.GetBaseUIControl("/panel0/button1").asButton()
        self.buttonUIControl2.AddTouchEventParams({"isSwallow": True})
        self.buttonUIControl2.SetButtonTouchUpCallback(self.onButtonTouchUpCallback)

    def onButtonTouchUpCallback(self, args):
        if args["ButtonPath"] == "/panel0/button0":
            screenNode = clientApi.GetUI("DoomsdaySurvivalMod", "Panel")
            screenUIControl = screenNode.GetBaseUIControl("/panel0")
            screenUIControl.SetVisible(True)
            self.buttonUIControl.SetVisible(False)

        if args["ButtonPath"] == "/panel0/button1":
            stats = clientApi.CreateComponent(self.playerId, "DoomsdaySurvivalMod", "statsComponent")
            comp = clientApi.GetEngineCompFactory().CreateGame(self.playerId)
            comp.SetPopupNotice(clientApi.GenerateColor("RED") + "成功", "你已成功释放恶意! 请在此期间尽可能获得更多生存点数和降低感染 ")
            stats.SetSurvivalLevel(99)
            stats.SetEyi(True)
            self.buttonUIControl2.SetVisible(False)
