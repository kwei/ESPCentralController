import numpy as np
import os
        
class FileHandler:
    def __init__(self):
        pass

    def CreateIfNotExist(self,devieId,TargetId):
        isExist = os.path.isfile('./cache/RSS_{}_to_{}.csv'.format(devieId, TargetId))                
        if not isExist:
            f = open("./cache/RSS_{}_to_{}.csv".format(devieId, TargetId), "w")
            f.close()

    def Append(self,devieId,TargetId,rssList):
        rssListNp = np.asarray([rssList]).T
        with open("./cache/RSS_{}_to_{}.csv".format(devieId, TargetId),"a") as f:
            np.savetxt(f, rssListNp, fmt='%s', delimiter=",")
    
    def Clear(self,devieId,TargetId):
        f = open("./cache/RSS_{}_to_{}.csv".format(devieId, TargetId), "w")
        f.close()
    
    def Len(self,devieId,TargetId):
        rssListLen = sum(1 for row in open("./cache/RSS_{}_to_{}.csv".format(devieId, TargetId)))
        return rssListLen
        
    def Clone(self,devieId,TargetId,start,end):
        cacheCSV = np.genfromtxt("./cache/RSS_{}_to_{}.csv".format(devieId, TargetId),delimiter=',',dtype=int)
        maxLen = len(cacheCSV)
        if start > maxLen:
            start = maxLen
        if end > maxLen:
            end = maxLen
        # print(cacheCSV)
        saveCSV = np.asarray([cacheCSV[start:end]],dtype=int).T
        # print(saveCSV)
        np.savetxt("./save/RSS_{}_to_{}.csv".format(devieId, TargetId), saveCSV , fmt='%s', delimiter=",")
