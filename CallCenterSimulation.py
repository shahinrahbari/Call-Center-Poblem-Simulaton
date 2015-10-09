# simulation : call center problem

InterArrivalTime  = []
TimeArrival = []
WhenAbleAvai = []
WhenBakerAvai = []
ServerChosen = []
ServiceTime = []
TimeBeginService = []

AbleServiceCompTime = []
BakerServiceCompTime = []
CallerDelay = []
SystemTime = []

#############################################################
####### define initial values for probability tables  #######
#############################################################

T = [1,2,3,4]
P = [0.25 ,0.40 , 0.20 , 0.15]


# baker
t1 = [3,4,5,6]
p1 = [0.35 , 0.25 , 0.20 , 0.20]

#able
t2 = [2,3,4,5]
p2 = [0.30 , 0.28 , 0.25 , 0.17]

n = 400

#############################################################
#############################################################
#############################################################



from random import *


def ResetValues():
    del InterArrivalTime [:]
    del TimeArrival[:]
    del WhenAbleAvai[:]
    del WhenBakerAvai[:]
    del ServerChosen[:]
    del ServiceTime[:]
    del TimeBeginService[:]

    del AbleServiceCompTime[:]
    del BakerServiceCompTime[:]
    del CallerDelay[:]
    del SystemTime[:]
    del BakerServiceTime[:]
    del AbleServiceTime[:]


def GetProbability(probs):
    res = []
    b = [0,probs[0]*100]
    res.append(b)
    for i in range(len(probs)-1):
        temp = res[i][1]
        b = [temp + 1  , temp + probs[i+1]*100]
        res.append(b)
    return res

def GetRandomWithRange(Times , Probs):
    rrr =  randint(1,100)
    probs = GetProbability(Probs)
    for i in range(0,len(Probs)):
        if( rrr <= probs[i][1] and rrr >= probs[i][0]):
            return Times[i]
        



def SetInterArrivalTime():
    InterArrivalTime.append(0)
    for i in range(1,n):
        InterArrivalTime.append(GetRandomWithRange(T , P))
        
def SetArrivalTime():
    TimeArrival.append(0)
    for i in range(1 , n):
        TimeArrival.append(TimeArrival[i-1] + InterArrivalTime[i])

BakerServiceTime = []
AbleServiceTime = []
def SetBakerServiceTime():

    for i in range(n):
        BakerServiceTime.append(GetRandomWithRange(t1 , p1))



def SetAbleServiceTime():

    for i in range(n):
        AbleServiceTime.append(GetRandomWithRange(t2 , p2))


def Main():
    SetInterArrivalTime()
    SetArrivalTime()
    SetBakerServiceTime()
    SetAbleServiceTime()
    Preload()
    FillTable()
    ##DrawDiagram()
    print "ArrivalTime : "
    print TimeArrival
    print "TimeBeginService : "
    print TimeBeginService
    print"ServerChosen : "
    print ServerChosen
    print "AbleServiceCompTime : "
    print AbleServiceCompTime
    print "BakerServiceCompTime : "
    print BakerServiceCompTime
    print "Caller Delay Frequency"
    print GetFrequencyOfCallerDelay()
    ResetValues()

def Preload():
    ServerChosen.append("Able")
    TimeBeginService.append(0)
    ServiceTime.append(AbleServiceTime[0])
    AbleServiceCompTime.append(ServiceTime[0])
    BakerServiceCompTime.append(0)
    CallerDelay.append(0)
    SystemTime.append(ServiceTime[0])
    
    
##InterArrivalTime  = []
##TimeArrival = []
##WhenAbleAvai = []
##WhenBakerAvai = []
##ServerChosen = []
##ServiceTime = []
##TimeBeginService = []
##
##AbleServiceCompTime = []
##BakerServiceCompTime = []
##CallerDelay = []
##SystemTime = []
##
def FillTable():
    for i  in range(1,n):
        if(TimeArrival[i] >= AbleServiceCompTime[i-1]):
            ServerChosen.append("Able")
            TimeBeginService.append(TimeArrival[i])
            ServiceTime.append(AbleServiceTime[i])
            AbleServiceCompTime.append(TimeBeginService[i] + ServiceTime[i])
            BakerServiceCompTime.append(BakerServiceCompTime[i-1])
            CallerDelay.append(0)
            SystemTime.append(ServiceTime[i])

        elif(TimeArrival[i] >= BakerServiceCompTime[i-1]):
            ServerChosen.append("Baker")
            TimeBeginService.append(TimeArrival[i])
            ServiceTime.append(BakerServiceTime[i])
            BakerServiceCompTime.append(TimeBeginService[i] + ServiceTime[i])
            AbleServiceCompTime.append(AbleServiceCompTime[i-1])
            CallerDelay.append(0)
            SystemTime.append(ServiceTime[i])
        else :
            if(AbleServiceCompTime[i-1] <= BakerServiceCompTime[i-1] ):
                delay = AbleServiceCompTime[i-1] - TimeArrival[i]
               
                ServerChosen.append("Able")
                TimeBeginService.append(TimeArrival[i] + delay)
                ServiceTime.append(AbleServiceTime[i])
                AbleServiceCompTime.append(TimeBeginService[i] + ServiceTime[i])
                BakerServiceCompTime.append(BakerServiceCompTime[i-1])
                CallerDelay.append(delay)
                SystemTime.append(ServiceTime[i] + delay)
            elif(AbleServiceCompTime[i-1] > BakerServiceCompTime[i-1] ):
               
                delay = AbleServiceCompTime[i-1] - TimeArrival[i]
                ServerChosen.append("Baker")
                TimeBeginService.append(TimeArrival[i] + delay)
                ServiceTime.append(BakerServiceTime[i])
                BakerServiceCompTime.append(TimeBeginService[i] + ServiceTime[i])
                AbleServiceCompTime.append(AbleServiceCompTime[i-1])
                CallerDelay.append(delay)
                SystemTime.append(ServiceTime[i] + delay)
        





def GetFrequencyOfCallerDelay():
    result = []
    for i in range(50):
        delayCount = 0
        for j in range(n):
            if(CallerDelay[j] == i):
                delayCount += 1
        result.append(delayCount)

    return result



def DrawDiagram():
    import plotly.plotly as py
    from plotly.graph_objs import *
    Callers = []
    for i in range (0,50):
        Callers.append(i)
        
    data = Data([
        Bar(
            x=Callers,
            y=GetFrequencyOfCallerDelay()
        )
    ])
    plot_url = py.plot(data, filename='basic-bar')




Main()




















    
