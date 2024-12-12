import pandas as pd
from cleaner import cleanRooster
from scenario_tools import write_scenario, generate_person, convert_time, convert_time_frac_string, generate_trip
import random
import json


pd.options.mode.chained_assignment = None  # default='warn'
# random.seed(42)

# This file generates the people array for UvA students using Rooster data

# read csv to an array
samples_9am = pd.read_csv('rooster/data/10k_samples_9am.csv').values
samples_9am = samples_9am.flatten().tolist()
samples_normalised = pd.read_csv('rooster/data/10k_uva_samples.csv').values
samples_normalised = samples_normalised.flatten().tolist()

samples = pd.read_csv('rooster/data/10k_uva_samples.csv').values
samples =  samples.flatten().tolist()

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

weesperMetro = [52.361556080685006, 4.9081389973987655]


# get random coordinates for each building
allCoordinates = pd.read_csv('coordinates/scraped_addresses.csv')
homes = allCoordinates[allCoordinates['Category'].isin(['house', 'apartments'])].copy()
homes = homes[['Latitude', 'Longitude']]

# FUNCTIONS
weekday = 'Monday' # day of the week for the scenario

def estimate_unique_students(weekday):
    # Load and clean data
    schedule = cleanRooster(pd.read_csv('rooster/data/calendar_week_nov_4_8_2024.csv'))
    
    # Group by start time to find concurrent classes
    schedule_grouped = schedule[schedule['day'] == weekday].copy()
    
    # Convert times to float hours for easier comparison
    schedule_grouped['start_time'] = schedule_grouped['start_time'].apply(
        lambda x: int(x.split(':')[0]) + int(x.split(':')[1])/60
    )
    schedule_grouped['end_time'] = schedule_grouped['end_time'].apply(
        lambda x: int(x.split(':')[0]) + int(x.split(':')[1])/60
    )

    # Find peak concurrent attendance
    max_concurrent = 0
    for hour in range(8, 21):  # 8am to 9pm
        for minute in range(0, 60, 15):  # Check every 15 minutes
            time_point = hour + minute/60
            concurrent_students = schedule_grouped[
                (schedule_grouped['start_time'] <= time_point) & 
                (schedule_grouped['end_time'] > time_point)
            ]['size'].sum()
            max_concurrent = max(max_concurrent, concurrent_students)

    # Apply correction factor based on assumptions:
    # - Average student takes 3 classes per day
    # - Classes are spread throughout the day
    estimated_unique_students = int(max_concurrent * 1.5)  # Correction factor
    
    return {
        'max_concurrent': max_concurrent,
        'estimated_unique': estimated_unique_students
    }

def has_overlap(class1, class2):
    return ((class1['start_time'] <= class2['end_time']) and 
            (class1['end_time'] >= class2['start_time']))

def get_classes(schedule, num_classes):
    selected_classes = []
    available_classes = schedule.copy()
    available_classes[available_classes['size'] > 0]
    
    while len(selected_classes) < num_classes and not available_classes.empty:
        # Randomly select one class
        new_class = available_classes.sample(n=1).iloc[0]
        selected_classes.append(new_class)
        
        # Remove all classes that overlap with the selected class
        available_classes = available_classes[
            ~available_classes.apply(lambda x: has_overlap(x, new_class), axis=1)
        ]
    
    return pd.DataFrame(selected_classes)

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
                arrivalTime = convert_time_frac_string(arrivalTime)
                departureTime = convert_time(arrivalTime) - (15 * 60) # 15 minutes before arrival
                departureTime = int(str(departureTime))
                if mode == 'Metro':
                    origin = weesperMetro
                    destination = coordinates
                    mode = 'Walk'
                else:
                    origin = allCoordinates.sample().values # THIS IS A PLACEHOLDER
                    origin = origin[0]
                    destination = coordinates
                trips = [generate_trip(departureTime, origin, destination, mode)]
                people.append(generate_person(trips))

    people = random.sample(people, int(len(people) * fractionSimulation))
    print(f'STATISTICS FOR THIS UVA SCENARIO')
    print(f'Number of people: {len(people)}')
    print(f'Number of people using Bike: {len([p for p in people if p["trips"][0]["mode"] == "Bike"])}')
    print(f'Number of people using Drive: {len([p for p in people if p["trips"][0]["mode"] == "Drive"])}')
    print(f'Number of people using Walk: {len([p for p in people if p["trips"][0]["mode"] == "Walk"])}')

    
    return people

# ASSUMTPIONS
# Students take 1-5 classes per day randomly
# Students go home after their last class of the day
# If there's a gap >2 hours between classes, students visit a cafe -> undone
# Students start from home before their first class
# Each student gets assigned one random home location
# Class schedule gaps determine break behavior

# PROCEDURE
# Filter schedule for specific weekday
# Generate student population:
# Create students based on maximum possible attendance
# Assign random homes
# Assign random number of classes (1-4)
# Create trips for each student:
# Morning trip from home to first class
# Trips between classes (including cafe visits)
# Evening trip from last class to home

def generateUvA(weekday):  
    people = []   
    schedule = cleanRooster(pd.read_csv('rooster/data/calendar_week_nov_4_8_2024.csv'))
    schedule= schedule[schedule['day'] == weekday]
    schedule['start_time'] = schedule['start_time'].apply(lambda x: int(x.split(':')[0]) + int(x.split(':')[1]) / 60)
    schedule['end_time'] = schedule['end_time'].apply(lambda x: int(x.split(':')[0]) + int(x.split(':')[1])/60)
    # schedule_grouped = schedule.groupby(['day', 'start_time', 'end_time','location'])['size'].sum().reset_index(name='total_size')
    
    print(schedule.head())

    # GENERATE THE STUDENT POPULATION

    # Estimate amount of unique students
    results = estimate_unique_students(weekday)
    print(f"Max concurrent students: {results['max_concurrent']}")
    print(f"Estimated unique students: {results['estimated_unique']}")
    unique_students = results['estimated_unique']

    print(f'Average size of classes: {schedule["size"].mean()}')

    for student in range(unique_students):
        # get random home
        home = homes.sample().values[0]
        # get random mode
        mode = random.choices(['Bike', 'Drive', 'Walk', 'Metro'], weights=[fractionBike, fractionCar, fractionWalk, fractionMetro])[0]
        if mode == 'Metro':
            home = weesperMetro
            mode = 'Walk'
        # assign a random number of classes (1-4) (MAYBE LOOK INTO GETTING A DISTRIBUTION OF CLASSES?)
        num_classes = random.randint(1, 4)
        classes = get_classes(schedule, num_classes)
        # subtract one from the size of the classes assigned to classes
        for _, class_row in classes.iterrows():
            schedule.loc[(schedule['code'] == class_row['code']) & 
                        (schedule['start_time'] == class_row['start_time']) & 
                        (schedule['room'] == class_row['room']), 'size'] -= 1

        # sort schedule by start_time
        classes = classes.sort_values(by='start_time')
        # generate two trips - first and last class
        # LATER: ADD TRIPS BETWEEN CLASSES AND CAFE VISITS
        trips = []
        # first trip - home -> class
        firstClass = classes.iloc[0]
        arrivalTime = firstClass['start_time'] + random.choice(samples_normalised) # sample from the distribution for arrival times

        # ASSUMPTION: students leave 30 minutes before they arrive
        arrivalTime = convert_time_frac_string(arrivalTime - 0.5)
        arrivalTime = convert_time(arrivalTime)
        trips.append(generate_trip(arrivalTime, home, recCoordinates[firstClass['location']], mode))
        # intermediate trips (LATER) - class -> cafe -> class
        # last trip - class -> home
        lastClass = classes.iloc[-1]
        departureTime = lastClass['end_time'] + random.choice(samples_normalised)
        departureTime = convert_time_frac_string(departureTime)
        departureTime = convert_time(departureTime)
        trips.append(generate_trip(departureTime, recCoordinates[lastClass['location']], home, mode))

        people.append(generate_person(trips))
        
        if student % 500 == 0:
            print(f'Generated {student/unique_students*100}% of students')

    print(f'Average size of classes after assignment: {schedule["size"].mean()}')
    return people



generateUvA('Monday')
