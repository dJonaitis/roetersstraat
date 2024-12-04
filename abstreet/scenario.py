from uva_scenario import generate9AMArrival
from resident_scenario import generate9to5
from scenario_tools import write_scenario

uvaParams = {
    'weekday': 'Monday',
}

residentParams = {
    'residents': 100,
}


def scenario_combiner(name, uvaParams, residentParams):
    uvaPeople = generate9AMArrival(uvaParams['weekday'])
    residentPeople = generate9to5(residentParams['residents'])
    people = uvaPeople + residentPeople
    print(f'STATISTICS FOR COMBINED SCENARIO')
    print(f'Number of people in UvA scenario: {len(uvaPeople)}')
    print(f'Number of people in Resident scenario: {len(residentPeople)}')
    print(f'Total number of people in scenario: {len(people)}')

    write_scenario(name, people)
    return 'Scenario succesfully written to file.'

scenario_combiner('combined_scenario', uvaParams, residentParams)