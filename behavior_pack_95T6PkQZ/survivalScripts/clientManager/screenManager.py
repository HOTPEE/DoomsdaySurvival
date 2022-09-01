# coding=utf-8
from mod.client.ui.screenNode import ScreenNode

import mod.client.extraClientApi as clientApi


class screenManager(ScreenNode):
    def __init__(self, namespace, name, param):
        ScreenNode.__init__(self, namespace, name, param)
        self.UIControl = None
        self.PlayerId = clientApi.GetLocalPlayerId()

    def Create(self):
        uiNode = clientApi.GetUI("DoomsdaySurvivalMod", "Panel")

        buttonUIControl = uiNode.GetBaseUIControl("/panel0/button0").asButton()
        buttonUIControl.AddTouchEventParams({"isSwallow": True})
        buttonUIControl.SetButtonTouchUpCallback(self.onButtonTouchUpCallback)

        buttonUIControl2 = uiNode.GetBaseUIControl("/panel0/button1").asButton()
        buttonUIControl2.AddTouchEventParams({"isSwallow": True})
        buttonUIControl2.SetButtonTouchUpCallback(self.onButtonTouchUpCallback)

        self.UIControl = uiNode.GetBaseUIControl("/panel0")

    def onButtonTouchUpCallback(self, args):
        if args["ButtonPath"] == "/panel0/button0":
            screenNode = clientApi.GetUI("DoomsdaySurvivalMod", "Button")
            screenUIControl = screenNode.GetBaseUIControl("/panel0/button0").asButton()
            screenUIControl.SetVisible(True)
            self.UIControl.SetVisible(False)
        if args["ButtonPath"] == "/panel0/button1":
            storeNode = clientApi.GetUI("DoomsdaySurvivalMod", "Store")
            storeUIControl = storeNode.GetBaseUIControl("/panel0")
            storeUIControl.SetVisible(True)
            self.UIControl.SetVisible(False)
