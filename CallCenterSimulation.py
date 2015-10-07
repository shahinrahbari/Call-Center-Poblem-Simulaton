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



from random import *


def GetProbability(p0,p1,p2,p3):
    b1  = [0,p0*100]
    b2 = [(100*p0)+1 , (p0*100)+(p1*100)]
    b3 = [(b2[1]) + 1  , (b2[1]) + (p2*100)]
    b4 = [(b3[1]) + 1  , (b3[1]) + (p3*100)]
    return[b1,b2,b3,b4]

def GetRandomWithRange(Times , Probs):
    rrr =  randint(1,100)
    probs = GetProbability(Probs[0],Probs[1],Probs[2],Probs[3])
    for i in range(0,4):
        if( rrr <= probs[i][1] and rrr >= probs[i][0]):
            return Times[i]
        


T = [1,2,3,4]
P = [0.25 ,0.40 , 0.20 , 0.15]

def SetInterArrivalTime():
    InterArrivalTime.append(0)
    for i in range(1,100):
        InterArrivalTime.append(GetRandomWithRange(T , P))
        
def SetArrivalTime():
    TimeArrival.append(0)
    for i in range(1 , 100):
        TimeArrival.append(TimeArrival[i-1] + InterArrivalTime[i])

# baker
t1 = [3,4,5,6]
p1 = [0.35 , 0.25 , 0.20 , 0.20]

#able
t2 = [2,3,4,5]
p2 = [0.30 , 0.28 , 0.25 , 0.17]
BakerServiceTime = []
AbleServiceTime = []
def SetBakerServiceTime():

    for i in range(100):
        BakerServiceTime.append(GetRandomWithRange(t1 , p1))



def SetAbleServiceTime():

    for i in range(100):
        AbleServiceTime.append(GetRandomWithRange(t2 , p2))


def Main():
    SetInterArrivalTime()
    SetArrivalTime()
    SetBakerServiceTime()
    SetAbleServiceTime()
    Preload()
    FillTable()
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

def Preload():
    ServerChosen.append("Able")
    TimeBeginService.append(0)
    ServiceTime.append(AbleServiceTime[0])
    AbleServiceCompTime.append(ServiceTime[0])
    BakerServiceCompTime.append(0)
    CallerDelay.append(0)
    SystemTime.append(ServiceTime[0])
    
    

def FillTable():
    for i  in range(1,100):
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
        

Main()




















    
