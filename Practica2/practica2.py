from multiprocessing import Process
from multiprocessing import Condition, Lock
from multiprocessing import Value
from multiprocessing import current_process
import time, random
from random import randint

NorthCars = randint(4,10) #final location North
SouthCars = randint(4,10) #final location South

print("There are",NorthCars,"cars who want to go North")
print("There are",SouthCars,"cars who want to go Soruth")

class Monitor(): 
    
    
    def __init__(self):
        self.nnorth = Value("i", 0) #coches que van al Norte
        self.nsouth = Value("i", 0) #coches que van al Sur
        self.nnorth_waiting = Value("i", 0) #coches que QUIEREN ir al Norte
        self.nsouth_waiting = Value("i", 0) #coches que QUIEREN ir al Sur
        self.turn = Value("i", 0)
        self.mutex = Lock() 
        self.no_north = Condition(self.mutex)
        self.no_south = Condition(self.mutex)
        
    def empty_south(self): #analiza si hay coches yendo y (esperando al Sur o si no es el turno del Sur)
        return self.nsouth.value == 0 and \
            (self.turn.value == 0 or self.nsouth_waiting.value == 0)
        
    def empty_north(self): #analiza si hay coches yendo y (esperando al Norte o si no es el turno del Norte)
        return self.nnorth.value == 0 and \
            (self.turn.value == 1 or self.nnorth_waiting.value == 0)
    
        
    def wants_go_south(self):
        self.mutex.acquire()
        self.nsouth_waiting.value += 1 
        self.no_north.wait_for(self.empty_north)
        self.nsouth_waiting.value -= 1 
        self.nsouth.value += 1
        self.mutex.release()
        
    def go_south(self):
        self.mutex.acquire()
        self.nsouth.value -= 1
        self.turn.value == 0
        if self.nsouth.value == 0:
            self.no_south.notify_all()
        self.mutex.release()
        
        
    def wants_go_north(self):
        self.mutex.acquire()
        self.nnorth_waiting.value += 1
        self.no_south.wait_for(self.empty_south)
        self.nnorth_waiting.value -= 1
        self.nnorth.value += 1
        self.mutex.release()
        
    def go_north(self):
        self.mutex.acquire()
        self.nnorth.value -= 1
        self.turn.value = 1
        if self.nnorth.value == 0:
            self.no_north.notify_all()
        self.mutex.release()
        
def delay(n=3):
        time.sleep(random.random()*n)
        
def south_car(monitor):
        delay()
        print(f"South car nº {current_process().name} wants to go South")
        monitor.wants_go_south()
        print(f"South car nº {current_process().name} enters the tunnel going South")
        delay()
        print(f"South car nº {current_process().name} leaves the tunnel from the South")
        monitor.go_south()
        
def north_car(monitor):
        delay()
        print(f"North car nº {current_process().name} wants to go North")
        monitor.wants_go_north()
        print(f"North car nº {current_process().name} enters the tunnel going North")
        delay()
        print(f"North car nº {current_process().name} leaves the tunnel from the North")
        monitor.go_north()
        
def main():
        monitor = Monitor()
        north_cars = [Process(target=north_car, name=f"{i}", args=(monitor,)) for i in range(NorthCars)]
        south_cars = [Process(target=south_car, name=f"{i}", args=(monitor,)) for i in range(SouthCars)] 
        for x in north_cars+south_cars:
            x.start()
        for x in north_cars+south_cars:
            x.join()
            
if __name__ == "__main__":
        main()
