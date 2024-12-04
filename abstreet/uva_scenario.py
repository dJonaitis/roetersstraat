import pandas as pd
from cleaner import cleanRooster
from scenario_tools import write_scenario, generate_person, convert_time
import random
import json

random.seed(42)

# This file generates the people array for UvA students using Rooster data

# read csv to an array
samples_9am = pd.read_csv('rooster/data/10k_samples_9am.csv').values
samples_9am = samples_9am.flatten().tolist()

attendanceFactor = 1 # percentage of people attending classes 0-1
fractionSimulation = 0.1 # how much of the real data to simulate 0-1

fractionMetro = 0.3 # fraction of people using metro 0-1
fractionBike = 0.3 # fraction of people using bike 0-1
fractionCar = 0.1 # fraction of people using car 0-1
fractionWalk = 0.3 # fraction of people walking 0-1


recCoordinates = {
    'REC_M': [52.3651602,4.9116465],
    'REC_ABC': [52.3629328,4.9119699],
    'REC_V': [52.3626311,4.9130096],
    'REC_G': [52.3636084,4.912418],
    'REC_E': [52.3638465,4.9112789],
    'REC_J/K': [52.3630387,4.914365],
    'REC_LAB': [52.3636084,4.9124119] 
}

weesperMetro = [4.9081389973987655,52.361556080685006]


# get random coordinates for each building
allCoordinates = pd.read_csv('coordinates/scraped_addresses.csv')
allCoordinates = allCoordinates[['Latitude', 'Longitude']]

# FUNCTIONS
weekday = 'Monday' # day of the week for the scenario

def generate9AMArrival(weekday):
    ## variables
    # import and clean schedule
    schedule = pd.read_csv('rooster/data/calendar_week_nov_4_8_2024.csv')
    schedule = cleanRooster(schedule)
    schedule_grouped = schedule.groupby(['day', 'start_time', 'location'])['size'].sum().reset_index(name='total_size')

    ## logic
    schedule_grouped = schedule_grouped[schedule_grouped['day'] == weekday]
    schedule_grouped = schedule_grouped[schedule_grouped['start_time'] == '09:00']
    schedule_grouped['total_size'] = schedule_grouped['total_size'] * attendanceFactor

    people = []

    for building, coordinates in recCoordinates.items():
        print(f'Iterating through {building}')
        size = schedule_grouped[schedule_grouped['location'] == building]['total_size']
        print(f'Total people in {building}today: {size}')
        sizes = {
            'Metro': int(size * fractionMetro),
            'Bike': int(size * fractionBike),
            'Drive': int(size * fractionCar),
            'Walk': int(size * fractionWalk)
        }

        for mode, count in sizes.items():
            for _ in range(count):
                arrivalTime = random.choice(samples_9am) # choose randomly from sample of 9am arrivals (format: 9.50)
                arrivalTime = str(int(arrivalTime)) + ':' + str(int((arrivalTime % 1) * 60))
                departureTime = convert_time(arrivalTime) - random.randint(5, 15) * 60 # 5-15 minutes before arrival
                departureTime = int(str(departureTime) + '0000')
                if mode == 'Metro':
                    origin = weesperMetro
                    destination = coordinates
                    mode = 'Walk'
                else:
                    origin = allCoordinates.sample().values # THIS IS A PLACEHOLDER
                    origin = origin[0]
                    destination = coordinates

                people.append(generate_person(departureTime, origin, destination, mode))


    print(f'STATISTICS FOR THIS UVA SCENARIO')
    print(f'Number of people: {len(people)}')
    print(f'Number of people using Bike: {len([p for p in people if p["trips"][0]["mode"] == "Bike"])}')
    print(f'Number of people using Drive: {len([p for p in people if p["trips"][0]["mode"] == "Drive"])}')
    print(f'Number of people using Walk: {len([p for p in people if p["trips"][0]["mode"] == "Walk"])}')

    people = random.sample(people, int(len(people) * fractionSimulation))
    return people



                    
