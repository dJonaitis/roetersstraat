import pandas as pd
from scenario_tools import generate_person_2trip, generate_departure_time
import random

random.seed(42)
# PROCEDURE
# Each person has two trips: one to work and one back home
# These trips are roughly on a 9-5 schedule. 
# The first trip is sampled from a normal distribution with a mean of 9am and a standard deviation of 15 minutes
# The second trip is sampled from the same distribution

fractionBike = 0.4 # fraction of people using bike 0-1
fractionCar = 0.15 # fraction of people using car 0-1
fractionWalk = 0.55 # fraction of people walking 0-1

# DATASETS
coordsDf = pd.read_csv('coordinates/scraped_addresses.csv')
# homes where category column is 'house', 'apartments'
homes = coordsDf[coordsDf['Category'].isin(['house', 'apartments'])].copy()
workplaces = coordsDf[~coordsDf['Category'].isin(['house', 'apartments'])].copy()


class Person:
    def __init__(self, home, work, mode, departHome, departWork):
        self.home = home
        self.work = work
        self.mode = mode
        self.departHome = departHome
        self.departWork = departWork

# params: residents (int) - number of residents
def generate9to5(residents):
    people = []
    for i in range(residents):
        home = homes.sample()[['Latitude', 'Longitude']].values[0]
        home = [home[1], home[0]]
        work = workplaces.sample()[['Latitude', 'Longitude']].values[0]
        work = [work[1], work[0]]
        # mode is randomly chosen through an uneven coin-toss with values noted above
        mode = random.choices(['Bike', 'Drive', 'Walk'], weights=[fractionBike, fractionCar, fractionWalk])[0]
        # the line below should be changed to adjust how people leave for work and home, and with what deviation
        person = Person(home, work, mode, generate_departure_time(9, 0.25, 1)[0], generate_departure_time(17, 0.25, 1)[0])
        people.append(generate_person_2trip(person.departHome, person.home, person.work, person.mode, person.departWork, person.work, person.home, person.mode))
    print(f'STATISTICS FOR THIS 9 TO 5 SCENARIO')
    print(f'Number of people: {len(people)}')
    print(f'Number of people using Bike: {len([p for p in people if p["trips"][0]["mode"] == "Bike"])}')
    print(f'Number of people using Drive: {len([p for p in people if p["trips"][0]["mode"] == "Drive"])}')
    print(f'Number of people using Walk: {len([p for p in people if p["trips"][0]["mode"] == "Walk"])}')
    return people

