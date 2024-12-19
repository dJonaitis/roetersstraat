from uva_scenario import generateUvA
from resident_scenario import generate9to5
from school_scenario import generateSchool
from scenario_tools import write_scenario

uvaParams = {
    'weekday': 'Monday',
    'attendanceFactor' : 1, # how much of the real data to simulate 0-1
    'fractionBreak' : 0.7, # percentage of people that go to a cafe/other break places during breaks 0-1

}

residentParams = {
    'residents': 1000,
}

schoolParams = {
    'students': 300,
}

def scenario_combiner(name, uvaParams, residentParams, schoolParams):
    uvaPeople = generateUvA(uvaParams['weekday'], uvaParams['attendanceFactor'], uvaParams['fractionBreak'])
    residentPeople = generate9to5(residentParams['residents'])
    schoolPeople = generateSchool(schoolParams['students'])
    people = uvaPeople + residentPeople + schoolPeople
    print(f'STATISTICS FOR COMBINED SCENARIO')
    print(f'Number of people in UvA scenario: {len(uvaPeople)}')
    print(f'Number of people in Resident scenario: {len(residentPeople)}')
    print(f'Number of people in School scenario: {len(schoolPeople)}')
    print(f'Total number of people in scenario: {len(people)}')

    write_scenario(name, people)
    return 'Scenario succesfully written to file.'

scenario_combiner('uva_long_test', uvaParams, residentParams, schoolParams)

