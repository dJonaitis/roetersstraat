import json
import random

# Takes as input string in format HH:MM in 24 hour time
# Returns time in seconds after midnight
# Sample input: '00:20'
# Sample output: 12000000 (i.e. 1200 seconds after midnight followed by four zeros)
def convert_time(inStr):
    outStr = ''
    hours, minutes = inStr.split(':')
    # base case: midnight is treated as 1 second after midnight
    if inStr == '00:00':
        outStr = '1'
    # count the number of seconds after midnight
    else:
        outStr = str(int(hours) * 3600 + int(minutes) * 60)
    return int(outStr)

def generate_departure_time(mean, std, n):
    sample = [random.gauss(mean, std) for _ in range(n)]
    return [str(int(i)) + ':' + str(int((i % 1) * 60)) for i in sample]  

def write_scenario(name, people):
    scenario = {
        'scenario_name': name,
        'people': people
    }
    with open(f'{name}.json', "w") as f:
        f.write(json.dumps(scenario, indent=2))
    return "Scenario saved"

def generate_person_2trip(timeDeparture1, origin1, destination1, mode1, timeDeparture2, origin2, destination2, mode2):
    return {
        'trips': [
            {
                'departure': timeDeparture1,
                'origin': {
                    'Position': {
                        'longitude': origin1[0],
                        'latitude': origin1[1]
                    }
                },
                'destination': {
                    'Position': {
                        'longitude': destination1[0],
                        'latitude': destination1[1]
                    }
                },
                'mode': mode1,
                'purpose': 'Work'
            },
            {
                'departure': timeDeparture2,
                'origin': {
                    'Position': {
                        'longitude': origin2[0],
                        'latitude': origin2[1]
                    }
                },
                'destination': {
                    'Position': {
                        'longitude': destination2[0],
                        'latitude': destination2[1]
                    }
                },
                'mode': mode2,
                'purpose': 'Work'
            }
        ]
    }

# 1 trip version
def generate_person(timeDeparture, origin, destination, mode):
    return {'trips': [
            {
                'departure': timeDeparture,
                'origin': {
                    'Position': {
                        'longitude': origin[0],
                        'latitude': origin[1]
                    }
                },
                'destination': {
                    'Position': {
                        'longitude': destination[0],
                        'latitude': destination[1]
                    }
                },
                'mode': mode,
                'purpose': 'Work'
            },
    ]}


