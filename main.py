import simpy
import random
import matplotlib.pyplot as plt
numStudents = 61
pValue = 0.01
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

def infection(env, students, student, pValue):
    while student.daysInfectious > 0:
        for infecteeDict in students.values():
            if not infecteeDict.isInfected and infecteeDict.id != infecteeDict.id:
                infecteeDict.InfectedStudent()
                env.process(infection(env,students, infecteeDict)) #run recursively until loops back to tommy
        student.daysInfectious -= 1
        yield env.timeout(1)

def runProgram():
    for i in range(numStudents):
        students[i] = Student(i, None)

    env = simpy.Environment()
    tommy = students[0]
    tommy.InfectedStudent()

    env.process(infection(env, students=students, student=tommy, pValue=pValue))

    infected_counts = []

    def dailyTracker(env, students):
        while True:
            count = sum(1 for stud in students.values() if stud.isInfected)
            infected_counts.append(count)
            yield env.timeout(1)

    env.process(dailyTracker(env, students))
    env.run(until=60)

    return infected_counts

infected_counts = runProgram()

plt.plot(infected_counts)
plt.xlabel('Day')
plt.ylabel('Cumulative Infected Students')
plt.title('Flu Spread in a Classroom')
plt.grid()
plt.show()

print("sim complete")