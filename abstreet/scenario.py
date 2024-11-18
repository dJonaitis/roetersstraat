import json
def write_scenario(name, people):
    scenario = {
        'scenario_name': name,
        'people': people
    }
    with open(name, "w") as f:
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
                'purpose': 'placeholder' # can be anything
            }
        ]
    }
]

write_scenario('test', people)