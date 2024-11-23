import json

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
    return int(outStr + '0000')

print(convert_time('00:20'))
    

def write_scenario(name, people):
    scenario = {
        'scenario_name': name,
        'people': people
    }
    with open(f'{name}.json', "w") as f:
        f.write(json.dumps(scenario, indent=2))
    return "Scenario saved"
    
# example run
people = [
    {
        'trips': [
            {
                'departure': 10000,
                'origin': { # rec abc
                    'Position': {
                        'longitude': 4.911440253356261,
                        'latitude': 52.3629002425848
                    }
                },
                'destination':{ # metro station
                    'Position': {
                        'longitude': 4.9081389973987655,
                        'latitude': 52.361556080685006
                    }
                },
                'mode': 'Walk', # Walk, Bike, Transit
                'purpose': 'Work' 
            }
        ]
    }
]

write_scenario('test', people)