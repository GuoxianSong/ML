from  numpy import *
import urllib
import json

def LoadData(filename):
    dataMat = []
    fr = open(filename)
    for line in fr.readlines():
        curLine = line.strip().split("\t")
        fltLine = map(float,curLine)
        dataMat.append(fltLine)
    return mat(dataMat)

def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA-vecB,2)))

def randCent(dataSet,k): #return k random center
    n = shape(dataSet)[1]
    centroids = mat(zeros((k,n)))
    for i in range(n):
        MinI = min(dataSet[:,i])
        MaxI = max(dataSet[:,i])
        RangeI= MaxI-MinI
        centroids[:,i] = MinI + float(RangeI)*random.rand(k,1)
    return centroids



def kMeans(dataSet,k,disrMeans=distEclud,createCent =randCent):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m,2)))
    centroids = createCent(dataSet,k)
    ifChanged = True
    while ifChanged :
        ifChanged =False
        for i in range(m):
            minIndex = 0
            minDist = distEclud(dataSet[i,:],centroids[0,:])
            for j in range(k):
                tmpIndex =j
                if distEclud(dataSet[i,:],centroids[j,:])< minDist:
                    minIndex = j;
                    minDist = distEclud(dataSet[i,:],centroids[minIndex,:])
            if clusterAssment[i,0]!= minIndex : ifChanged = True
            clusterAssment[i,:] = minIndex,minDist
        for cent in range(k):
            ptsInClust = dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]
            centroids[cent,:] = mean(ptsInClust,axis = 0)
    return centroids,clusterAssment

def biKmeans(dataSet,k, distMeas = distEclud):
    m = shape(dataSet)[0]
    clusterAssment = mat(zeros((m,2)))
    centrod0 = mat(mean(dataSet,axis=0 ))
    centList = [centrod0]
    for i in range(m):
        clusterAssment[i,1]=distMeas(mat(centrod0),dataSet[i,:])**2
    while( len(centList)< k):
        lowestSSE = inf
        for i in range(len(centList)):
            tmpDataSet = dataSet[nonzero(clusterAssment[:,0].A==i)[0]]
            tmpCentrods,tmpClusterAss =kMeans(tmpDataSet,2)
            NoSpitSSE = sum(clusterAssment[nonzero(clusterAssment[:,0].A!=i)[0],1])
            SpitSSE = sum(tmpClusterAss[:,1])
            if SpitSSE+NoSpitSSE<lowestSSE:
                lowestSSE = SpitSSE+NoSpitSSE
                BestIndex = i
                BestNewCents = tmpCentrods
                BestNewClustAss=tmpClusterAss
        BestNewClustAss[nonzero(BestNewClustAss[:,0].A==1)[0],0]= len(centList)
        BestNewClustAss[nonzero(BestNewClustAss[:, 0].A != 1)[0], 0] = BestIndex
        centList[BestIndex]=BestNewCents[0,:].tolist()[0]
        centList.append(BestNewCents[1,:].tolist()[0])
        clusterAssment[nonzero(clusterAssment[:,0].A==BestIndex)[0],:]=BestNewClustAss
    print centList
    return mat(centList),clusterAssment



#dataMat = LoadData("testSet2.txt")
#biKmeans(dataMat,3)

def geoGrab(stAddress, city):
    apiStem = 'http://where.yahooapis.com/geocode?'  #create a dict and constants for the goecoder
    params = {}
    params['flags'] = 'J'#JSON return type
    params['appid'] = 'aaa0VN6k'
    params['location'] = '%s %s' % (stAddress, city)
    url_params = urllib.urlencode(params)
    yahooApi = apiStem + url_params      #print url_params
    print yahooApi
    c=urllib.urlopen(yahooApi)
    return json.loads(c.read())

from time import sleep
def massPlaceFind(fileName):
    fw = open('places.txt', 'w')
    for line in open(fileName).readlines():
        line = line.strip()
        lineArr = line.split('\t')
        retDict = geoGrab(lineArr[1], lineArr[2])
        if retDict['ResultSet']['Error'] == 0:
            lat = float(retDict['ResultSet']['Results'][0]['latitude'])
            lng = float(retDict['ResultSet']['Results'][0]['longitude'])
            print "%s\t%f\t%f" % (lineArr[0], lat, lng)
            fw.write('%s\t%f\t%f\n' % (line, lat, lng))
        else: print "error fetching"
        sleep(1)
    fw.close()
geoGrab('1 VA Center','Augusta, ME')
