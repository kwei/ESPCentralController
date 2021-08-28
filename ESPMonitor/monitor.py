import json, os
from ESPMonitor.fileHandler import FileHandler

HaveMonitors = {}
OnlineMonitors = {}
fileHandler = FileHandler()
class MonitorService:
    def __init__(self):
        with open('espConfig.json', newline='') as espConfig:
            configData = json.load(espConfig)
            _ipTable = configData['espTable']
            MAXCache = configData['MAXCache']
            self.monitorIds = _ipTable.keys()

        for espi in self.monitorIds:
            for espj in self.monitorIds:
                if espi == espj:
                    self.setExist(espi,espj,True)
                    continue
                if fileHandler.Len(espi,espj) >= MAXCache:
                    self.setExist(espi,espj,True)
                else:
                    self.setExist(espi,espj,False)
                

    def setOnline(self,Id):
        global OnlineMonitors
        OnlineMonitors[Id] = True

    def getOnline(self):
        ret = {}
        for monitorId in self.monitorIds:
            if monitorId in OnlineMonitors:
                ret[monitorId] = True
            else:
                ret[monitorId] = False
        return ret


    def setExist(self,Id, targetId,result):
        global HaveMonitors
        if Id in HaveMonitors:
            HaveMonitors[Id][targetId] = result
        else:
            HaveMonitors[Id] ={}
            HaveMonitors[Id][targetId] = result

    def getExist(self):
        global HaveMonitors
        ret = {}
        for monitorId in self.monitorIds:
            ret[monitorId] = {}
            for cacheKey in self.monitorIds:
                if monitorId == cacheKey:
                    continue
                if monitorId in HaveMonitors:
                    if cacheKey in HaveMonitors[monitorId]:
                        ret[monitorId][cacheKey] = HaveMonitors[monitorId][cacheKey]
                    else:
                         ret[monitorId][cacheKey] = False
                else:
                    ret[monitorId][cacheKey] = False
        return ret




