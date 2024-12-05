import json
import random

# Takes as input string in format HH:MM in 24 hour time
# Returns time in seconds after midnight
# Sample input: '00:20'
# Sample output: 1200 (i.e. 1200 seconds after midnight followed by four zeros)
def convert_time(inStr):
    outStr = ''
    hours, minutes = inStr.split(':')
    # base case: midnight is treated as 1 second after midnight
    if inStr == '00:00':
        outStr = '1'
    # count the number of seconds after midnight
    else:
        outStr = str(int(hours) * 3600 + int(minutes) * 60)
    return int(outStr + '0000')

# Takes as input a float in the format HH.MM
# Returns the time in string format HH:MM
# Sample input: 17.3
# Sample output: '17:18'
def convert_time_frac_string(inFrac):
    hours, minutes = divmod(inFrac * 60, 60)
    return '{0:02.0f}:{1:02.0f}'.format(hours, minutes)


def generate_departure_time(mean, std, n):
    sample = [random.gauss(mean, std) for _ in range(n)]
    sample = [convert_time_frac_string(x) for x in sample]
    return [convert_time(x) for x in sample]

print(generate_departure_time(9, 0.25, 1))

def write_scenario(name, people):
    scenario = {
        'scenario_name': name,
        'people': people
    }
    with open(f'{name}.json', "w") as f:
        f.write(json.dumps(scenario, indent=2))
    return "Scenario saved"

def generate_trip(timeDeparture, origin, destination, mode):
    return {
        'departure': timeDeparture,
        'origin': {
            'Position': {
                'latitude': origin[0],
                'longitude': origin[1]
            }
        },
        'destination': {
            'Position': {
                'latitude': destination[0],
                'longitude': destination[1]
            }
        },
        'mode': mode,
        'purpose': 'Work'
    }
def generate_person(trips):
    return {'trips': trips} 



