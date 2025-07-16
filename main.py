import simpy
import random
import matplotlib as plt
numStudents = 61
students = {}

def trafficProcess(env):
    while True:
        print("light turned GRN @ t=" + str(env.now))
        yield env.timeout(30)
        print("light turned Yellow @ t=" + str(env.now))
        yield env.timeout(5)
        print("light turned RED @ t=" + str(env.now))
        yield env.timeout(20)

class Student:
    def __init__(self, id, env):
        self.id = id
        self.daysInfectious = 0
        self.isInfected = False
        self.env = env

    def InfectedStudent(self):
        self.isInfected = True
        self.daysInfectious = 3

for i in range(numStudents):
    students[i] = {i:Student(i, None)}
print(students[1][1].isInfected)

def infection(env, students, student, pValue):
    while student.daysInfectious > 0:
        for infecteeDict in students.values():
            if not infecteeDict.isInfected and infecteeDict.id != infecteeDict.id:
                infecteeDict.InfectedStudent()
                env.process(infection(env,students, infecteeDict))
        student.daysInfectious -= 1
        yield env.timeout(1)

env = simpy.Environment()
env.process(trafficProcess(env))
env.run(until=500)
print("sim complete")