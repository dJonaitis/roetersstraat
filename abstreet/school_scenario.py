import random
import pandas as pd
from scenario_tools import generate_person, convert_time, convert_time_frac_string, generate_departure_time, generate_trip


random.seed(4)
# PROCEDURE
# Each kid goes to school before the school start time, and leaves after the class ends
# Each kid has a chance to have a parent
# If the kid has a parent, the kid goes to school from home with their parent and then their parent picks them up




school = [52.3635266,4.909961]
weesperMetro = [52.361556080685006, 4.9081389973987655]

schoolHours = [8, 16] # school hours


fractionMetro = 0.3 # fraction of people using metro 0-1
fractionBike = 0.4 # fraction of people using bike 0-1
fractionWalk = 0.3 # fraction of people walking 0-1

fractionParentMetro = 0.2
fractionParentBike = 0.4
fractionParentWalk = 0.3
fractionParentCar = 0.1 # faction of parents using a car 0-1

parentChance = 0.5 # fraction of kids with parents 0-1
 
# DATASETS
coordsDf = pd.read_csv('coordinates/scraped_addresses.csv')
# homes where category column is 'house', 'apartments'
homes = coordsDf[coordsDf['Category'].isin(['house', 'apartments'])].copy()
workplaces = coordsDf[~coordsDf['Category'].isin(['house', 'apartments'])].copy()


class Child:
    def __init__(self, home, mode, departHome, parent):
        self.home = home
        self.mode = mode
        self.departHome = departHome
        self.parent = parent
    
    def getDepartureTime(self):
        if self.parent:
            return self.parent.departHome + 6000000
        else:
            return generate_departure_time(schoolHours[1] - 0.25, 0.25, 1)[0]

class Parent:
    def __init__(self, home, work, mode, departHome, departWork):
        self.home = home
        self.work = work
        self.mode = mode
        self.departHome = departHome
        self.departWork = departWork

def generateSchool(students):
    people = []

    for _ in range(students):
        parent = None
        home = homes.sample()[['Latitude', 'Longitude']].values[0]
        mode = random.choices(['Bike', 'Walk', 'Metro'], weights=[fractionBike, fractionWalk, fractionMetro])[0]
        parentDriving = False
        if random.choices([0, 1], weights=[1-parentChance, parentChance])[0]: # add a parent if child has parent
            work = workplaces.sample()[['Latitude', 'Longitude']].values[0]
            parentMode = random.choices(['Bike', 'Walk', 'Metro', 'Drive'], weights=[fractionParentBike, fractionParentWalk, fractionParentMetro, fractionParentCar])[0]
            if parentMode == 'Drive': # do not spawn a child agent
                # set bool to true, to not generate kid 
                parentDriving = True
            parent = Parent(home, work, parentMode, generate_departure_time(schoolHours[0] - 0.5, 0.25, 1)[0], generate_departure_time(schoolHours[1], 0.5, 1)[0])
            if parent.mode == 'Metro':
                parent.mode = 'Walk'
                home = weesperMetro
            homeSchool = generate_trip(parent.departHome, parent.home, school, parent.mode)
            # the idea behind adding 10 minutes is that if the parent lives closer to the school (i.e. comes in <10 minutes)
            # they are more likely to be part of the roetersstraat and surrounding community
            # they are more likely to wait and chat with other parents, also members of that community
            schoolWork = generate_trip(parent.departHome + 6000000, school, work, parent.mode) # add ten minutes after arrival at school
            workSchool = generate_trip(parent.departWork, work, school, parent.mode)
            schoolHome = generate_trip(parent.departWork + 6000000, school, parent.home, parent.mode)
            trips = [homeSchool, schoolWork, workSchool, schoolHome]
            people.append(generate_person(trips))
        if not parentDriving:
            # code to generate kid
            if parent: 
                child = Child(home, parent.mode, parent.departHome, parent)
            else:
                child = Child(home, mode, generate_departure_time(schoolHours[0] - 0.5, 0.25, 1)[0], None)
            if child.mode == 'Metro':
                child.home = weesperMetro
                child.mode = 'Walk'
            homeSchool = generate_trip(child.departHome, child.home, school, child.mode)
            schoolHome = generate_trip(child.getDepartureTime(), school, child.home, child.mode)
            trips = [homeSchool, schoolHome]
            people.append(generate_person(trips))
    return people