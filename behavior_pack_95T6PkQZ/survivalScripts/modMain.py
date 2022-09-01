# coding=utf-8
from mod.common.mod import Mod
import mod.client.extraClientApi as clientApi
import mod.server.extraServerApi as serverApi


@Mod.Binding(name="DoomsdaySurvivalMod", version="0.0.1")
class DoomsdaySurvivalMod(object):

    def __init__(self):
        pass

    # 服务端脚本初始化的入口函数
    @Mod.InitServer()
    def DoomsdaySurvivalServerInit(self):
        serverApi.RegisterSystem("DoomsdaySurvivalMod", "ServerManager",
                                 "survivalScripts.serverListener.serverManager.ServerManager")

    # 服务端脚本在退出时执行的析构函数
    @Mod.DestroyServer()
    def DoomsdaySurvivalServerDestroy(self):
        pass

    # 客户端脚本初始化的入口函数
    @Mod.InitClient()
    def DoomsdaySurvivalClientInit(self):
        clientApi.RegisterSystem("DoomsdaySurvivalMod", "ModUiRegister",
                                 "survivalScripts.clientListener.modUiRegister.ModUiRegister")

        clientApi.RegisterComponent("DoomsdaySurvivalMod", "statsComponent", "survivalScripts.compManager"
                                                                             ".statsComponent.StatsComponent")

        comp = clientApi.GetEngineCompFactory().CreateConfigClient(clientApi.GetLevelId())
        stats = comp.GetConfigData("addon_Stats", False)
        ferp = clientApi.CreateComponent(clientApi.GetLocalPlayerId(), "DoomsdaySurvivalMod", "statsComponent")
        if stats.has_key('infectionPoints'):
            ferp.SetInfectionPoints(stats['infectionPoints'])
        if stats.has_key('survivalPoints'):
            ferp.SetSurvivalPoints(stats['survivalPoints'])
        if stats.has_key('survivalLevel'):
            ferp.SetSurvivalLevel(stats['survivalLevel'])
        if stats.has_key('is_Eyi'):
            ferp.SetEyi(stats['is_Eyi'])
    # 客户端脚本在退出时执行的析构函数+
    @Mod.DestroyClient()
    def DoomsdaySurvivalClientDestroy(self):
        comp = clientApi.GetEngineCompFactory().CreateConfigClient(clientApi.GetLevelId())
        stats = clientApi.CreateComponent(clientApi.GetLocalPlayerId(), "DoomsdaySurvivalMod", "statsComponent")
        data = {"infectionPoints": stats.GetInfectionPoints(), "is_Eyi": stats.is_Eyi(),
                "survivalPoints": stats.GetSurvivalPoints(), "survivalLevel": stats.GetSurvivalLevel()}
        comp.SetConfigData("addon_Stats", data, False)
        print data
