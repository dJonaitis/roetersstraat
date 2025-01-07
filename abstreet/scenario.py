from uva_scenario import generateUvA
from resident_scenario import generate9to5
from school_scenario import generateSchool
from scenario_tools import write_scenario

uvaParams = {
    'weekday': 'Monday',
}

residentParams = {
    'residents': 7200,
}

schoolParams = {
    'students': 300,
}

def scenario_combiner(name, uvaParams, residentParams, schoolParams):
    uvaPeople = generateUvA(uvaParams['weekday'])
    residentPeople = generate9to5(residentParams['residents'])
    schoolPeople = generateSchool(schoolParams['students'])
    people = uvaPeople + residentPeople + schoolPeople
    # people = uvaPeople
    print(f'STATISTICS FOR COMBINED SCENARIO')
    print(f'Number of people in UvA scenario: {len(uvaPeople)}')
    print(f'Number of people in Resident scenario: {len(residentPeople)}')
    print(f'Number of people in School scenario: {len(schoolPeople)}')
    print(f'Total number of people in scenario: {len(people)}')

    write_scenario(name, people)
    return 'Scenario succesfully written to file.'

scenario_combiner('main', uvaParams, residentParams, schoolParams)

