import sys
import random
import numpy as np


class queue:
    def __init__(self, num_of_prob):
        self.totalServiceTime = 0.0
        self.totalWaitingTime = 0.0
        self.numInQueue = 0
        self.NumOfTested = 0
        self.numberOfArrival = 0
        self.clk = 0.0
        self.Ti = [0.0 for i in range(num_of_prob)] 
        self.clk_arr =[]
        self.Sclk_arr =[]
        
    def update_time(self, w_time, clock, systemTotal):
        self.clk += 0.0
    def dequeue(self, clock):        
        (self.clk_arr).pop(0)
        (self.Sclk_arr).pop(0)
        #self.Ti[self.numInQueue] += (clock - self.clk)
        #self.totalWaitingTime +=clock-(self.Sclk_arr).pop(0)
        self.numInQueue -= 1
        self.NumOfTested += 1
        self.clk = clock
        
    def inqueue(self,clock, servingTime):
        if self.numInQueue == 0:
            (self.clk_arr).append(clock)
            (self.Sclk_arr).append(servingTime+clock)
        else:
            (self.clk_arr).append(clock)
            (self.Sclk_arr).append(servingTime+(self.Sclk_arr)[self.numInQueue-1]) 
   
        self.totalWaitingTime +=((self.Sclk_arr)[self.numInQueue]) - (self.clk_arr)[self.numInQueue]
        self.Ti[self.numInQueue] += (clock - self.clk)
        self.numberOfArrival += 1
        self.numInQueue += 1
        self.clk = clock
    def handle_depart(self, clock, flag):
        #print("handling departure")
        pop = 0
        for i in range(len(self.Sclk_arr)):
            #print(str(i) +" "+ str(self.Sclk_arr[i]) + " clock" + str(clock))
            if flag == False:
                if clock > self.Sclk_arr[i]:
                    self.Ti[self.numInQueue-pop] += (self.Sclk_arr[i] - self.clk)
                    self.clk=self.Sclk_arr[i]
                    pop +=1
                    
            else:
                pop +=1
                #self.Ti[self.numInQueue-pop] += (self.Sclk_arr[i] - self.clk)
                #self.clk=self.Sclk_arr[i]
                
        for i in range(pop):
            (self.clk_arr).pop(0)
            (self.Sclk_arr).pop(0)
            self.NumOfTested += 1
            self.numInQueue -= 1
        
    def update_service_time(self, time):
        self.totalServiceTime += time
    def get_num_in_queue(self):
        return self.numInQueue
    def get_prob_i(self, i):
        return (self.Ti)[i]
    def get_num_tested(self):
        return self.NumOfTested
    def get_waiting_time(self):
        return self.totalWaitingTime
    def get_service_time(self):
        return self.totalServiceTime
    def get_num_arrivals(self):
        return self.numberOfArrival
    def get_clk(self):
        return self.clk
    def get_last_depart(self):
        if self.numInQueue==0:
            return 0.0
        return self.clk_arr[self.numInQueue-1]

        
class Simulation:
    def __init__(self, run_time, queues, arrival_rate, service_rate, prob_vec):
        self.runTime = run_time
        self.numOfQueues = queues
        self.clock = 0.0
        self.SystemTotal = 0
        self.NumOfTested = 0
        self.numOfQuits = 0
       
        self.stop = 0
        self.arrivalRate = ((arrival_rate))
        self.serviceRate = ((service_rate))
       
        self.Prob_vec = prob_vec
        self.numInQueues = []
        
        self.Qlist = [i for i in range(queues)] 
        
        self.lastD = 0.0 
        self.arrivals = random.expovariate(self.arrivalRate)
        self.leaves = []
        (self.leaves).append((float('inf'),float('inf'))) 
        
        self.Queues = []
        for i in range(queues):
            (self.Queues).append(queue(len(prob_vec)))
        self.isOne = False  #new
        self.VaccineId = -1   #new
        self.numBeinTreated = 0 #new

    def arrival(self, queueNum):
        #print("qNum " + str(queueNum) + " num in queue " + str((self.Queues[queueNum]).get_num_in_queue()))
        #print("arrival function " + str((self.Queues[queueNum]).get_num_in_queue()))
        if self.numBeinTreated == 0:  #new
            self.VaccineId=queueNum #new
            self.numBeinTreated += 1 #new
            
        (self.Queues[self.VaccineId]).handle_depart(self.clock, False)
        #print("qNum " + str(queueNum) + " num in queue " + str((self.Queues[queueNum]).get_num_in_queue()))
        prob = (self.Prob_vec)[(self.Queues[self.VaccineId]).get_num_in_queue()]  
        r = random.randint(1,10)
        r /= 10
        #print("r " + str(r) + " p " + str(prob))
        if (prob <=random.random() ):
            #(self.leaves).insert(0,self.lastD)
            self.numOfQuits += 1
        else:
           
            self.SystemTotal += 1
            #print("here")
            next = random.expovariate(self.serviceRate)
            (self.Queues[self.VaccineId]).inqueue(self.clock, next)
            leaving_timestamp =(self.Queues[self.VaccineId]).get_last_depart()
            if leaving_timestamp == 0:
                leaving_timestamp = self.clock
            #if self.lastD[0] < float('inf'):
              #  (self.leaves).insert(0,self.lastD)
            #(self.leaves).append((leaving_timestamp+ next,queueNum))
            #(self.leaves).sort(key=lambda x:x[0],reverse=False)
            (self.Queues[self.VaccineId]).update_service_time(next)
            
        self.arrivals = self.clock + random.expovariate(self.arrivalRate)
   
   
    
    def departure(self):
        '''
        (self.Queues[queueNum]).dequeue(self.clock)
        self.NumOfTested += 1
        self.SystemTotal -= 1 
        if len(self.leaves) == 0:
            (self.leaves).append((float('inf'),float('inf'))) 
        '''
        maxClk=0.0
        for i in range(self.numOfQueues):
            #print("maxClk " + str(maxClk) + " (self.Queues[i]).get_last_depart() " + str((self.Queues[i]).get_last_depart()))
            maxClk = max((self.Queues[i]).get_last_depart(),maxClk)
        self.clock = maxClk
        for i in range(self.numOfQueues):
            (self.Queues[i]).handle_depart(self.clock, True)
        self.numBeinTreated = (self.Queues[self.VaccineId]).get_num_in_queue() #new
     
   
    def simulate(self):
        while True:
            minArrival = self.arrivals
            #minDeparts = (self.leaves).pop(0)
            #self.lastD = minDeparts
            #print("minarrival" + " " + str(minArrival))
            #print("minDeparts" + " " + str(minDeparts))
            self.clock = minArrival
            if minArrival > self.runTime:
                if self.SystemTotal == 0:
                    self.printResults()
                    return
                #minArrival = float('inf')
                self.stop = 1
            #testingTime = min(minArrival, minDeparts[0])
            if self.stop == 1:
                self.departure()
                for i in range(self.numOfQueues):
                    self.NumOfTested+=(self.Queues[i]).get_num_tested()
                self.printResults()
                return
            
            #if minDeparts[0] > minArrival:
            queueNum = random.choice(self.Qlist)
            r = random.randint(0,self.numOfQueues-1)
            self.arrival(queueNum)
                
           # else:
               # self.departure(minDeparts[1])



        
    def printResults(self):
        #should remove T0 and Z0
        avgWaitTime = 0.0
        avgService = 0.0
        avgArrivals = 0.0
        if self.NumOfTested != 0:
            for i in range(self.numOfQueues):
                if (((self.Queues)[i]).get_num_tested()) != 0:
                    avgWaitTime += ((((self.Queues)[i]).get_waiting_time() - (((self.Queues)[i]).get_service_time())) /  ((self.Queues)[i]).get_num_tested())
                    avgService += (((self.Queues)[i]).get_service_time()) / (((self.Queues)[i]).get_num_tested())
                if (((self.Queues)[i]).get_clk()) != 0.0:
                    avgArrivals += (((self.Queues)[i]).get_num_arrivals()) / (((self.Queues)[i]).get_clk())
        pWaitTime = avgWaitTime  # do not divide with the number of queues because only one queue is running
        pServiceTime = avgService 
        pArrivals = avgArrivals 
        
        pString = str(self.NumOfTested) + " "   #OK

        pString  += str(self.numOfQuits) + " "   #OK

        pString  += str(self.clock) + " "        #OK
        Ti = [0.0 for i in range(len(self.Prob_vec))] 
        for i in range(len(self.Prob_vec)):
            for j in range(self.numOfQueues):
                Ti[i] += (((self.Queues)[j]).get_prob_i(i))
            if i !=0:
                Ti[i] /=  (self.numOfQueues)
        #pString += str(Ti[0]) + " " #T0
        for time in Ti:    #Ati
            pString  += str(time) + " "
        
        #pString += str((Ti[0])/(self.clock)) + " " #Z0        
        for time in Ti:    #Zi
            pString  += str(time/self.clock) + " "

        pString  += str(pWaitTime) + " " + str(pServiceTime) + " " + str(pArrivals) + " "

        print(pString )

   
   
if __name__ == "__main__":
    runTime = int(sys.argv[1])
    queues = int(sys.argv[2])
    arrival_rate = float(sys.argv[3])
    service_rate = float(sys.argv[4])
    prob_vec = []
    length=len(sys.argv)
    for i in range(5, length):
        prob_vec.append(float(sys.argv[i]))
    s1 = Simulation(runTime, queues, arrival_rate, service_rate, prob_vec)
    s1.simulate()