import mod.client.extraClientApi as clientApi

ComponentCls = clientApi.GetComponentCls()


class StatsComponent(ComponentCls):
    def __init__(self, entityId):
        ComponentCls.__init__(self, entityId)
        self.infectionPoints = 0.0
        self.survivalPoints = 0
        self.survivalLevel = 0
        self.isEyi = False

    def is_Eyi(self):
        return self.isEyi

    def SetEyi(self, val):
        self.isEyi = bool(val)

    def GetInfectionPoints(self):
        return self.infectionPoints

    def SetInfectionPoints(self, val):
        self.infectionPoints = float(val)

    def GetSurvivalPoints(self):
        return self.survivalPoints

    def SetSurvivalPoints(self, val):
        self.survivalPoints = int(val)

    def GetSurvivalLevel(self):
        return self.survivalLevel

    def SetSurvivalLevel(self, val):
        self.survivalLevel = int(val)
