Further documentation and how to run the scenario can be found in the README document on the GitHub repository. 

# Scenario logic
This document details the assumptions made and the logic behind each of the individual components of the scenario.

This file has last been edited on the 7th of January, 2025. 

This code and explanation was written by Danielius Jonaitis.

The document is structured with assumptions and logic per scenario. The assumptions includes constants used in code, and various logical assumptions made.

Various suggestions and comments on the quality of the code are in italics. A more extensive list of improvements is typically available underneath the description of each file in the README.

## Scenarios 
1. UvA (``uva_scenario.py``)
2. Residents (``resident_scenario.py``)
3. Roetersstraat Primary School (``school_scenario.py``)

## UvA
This is the scenario of UvA students, based on the schedule.
### Assumptions
- ``unique_students`` - the amount of unique students that come every day. This number is counted from getting the maximum concurrent students and multiplying by a factor of 1.5.
- ``attendanceFactor`` - the percentage of people actually attending classes. (i.e. for a 100 person class you would expect ``100 * attendanceFactor``) people to show up. This number goes on top of ``unique_students``.
- ``fractionSimulation`` (DEPRECATED) - the percentage of the actual people to simulate. Because of computational efficiency concerns, a representative sample of the total amount of real agents can be simulated. Melnikov et al. (p. 2308), in their study of Amsterdam car traffic, use the fraction of their total agents compared and population size. In their study, there are 410 thousand cars, roughly 2.4 million people livig in Amsterdam (a fraction of around 0.1), hence they simulated 41 thousand agents (410 * 0.1). This is arbitrarily set in the code for now.
- ``fractionMode`` - this is a series of variables that denote the fraction of the UvA agents that use a certain mode of transport to get to UvA (e.g. ``fractionMetro = 0.3`` would mean 30% of students use the metro).
- ``weesperMetro`` - in this stage, any student using the metro will leave from the Weesperplein metro station exit nearest Valckenierstraat.
- ``fractionBreak`` - the percentage of students that will go to a third place for a break.
- ``breakCoordinates`` - a series of nearby businesses and places that students might go to during a break.
- The students arrive for a 9AM with a Gaussian distribution derived from combined observations from various buildings around REC. This distribution was pre-sampled 10 thousand times in the file ``10k_samples_9am.csv``, and a random time is selected from this file for any given student. *In the future this could be made abstracted to where the mean of the distribution is 0 (the start time of the class) and -0.5 and 0.5 would mean the student comes half an hour before or after the start time respectively.*
### Logic
1. The schedule is read and cleaned, filtered for only the relevant weekday defined in the variable ``weekday``.
2. The number of ``unique_students`` is counted, and ``attendanceFactor`` applied.
3. For every unique student: a ``home`` is sampled, and a random ``mode`` assigned based on the weights of ``fractionMode``. If the ``mode`` is ``Metro``, ``home`` is set to ``weesperMetro`` and the ``mode`` set to ``Walk``.
4. Each student gets assigned 1-4 classes from the schedule. When a class is assigned, the class ``size`` is reduced by 1, so that it will not pick classes that are full.
5. Two trips are generated based on the student's classes: home to class and class to home.
6. All breaks between classes are found, and if a break is greater than 2 hours, there is a ``fractionBreak`` chance a random place from ``breakCoordinates`` will be selected. Another trip will be added to that place, beginning at the end of the class, with another trip to the next class 10 minutes before it.
7. A person is generated, and the people array is populated.


## Residents

This part is simulated in a similar manner to the default 9-to-5 preset in A/BStreet, information about that can be found in [this](https://a-b-street.github.io/docs/tech/trafficsim/index.html) part of the documentation.

### Assumptions
- ``residents`` - the number of residents within our map. *This could be generated from population density maps and records, similar to Melnikov et al., as well as through the use of data about a fraction of the population that works from home, etc.*
- ``fractionMode`` - this is a series of variables that denote the fraction of the resident agents that use a certain mode of transport to get to work (e.g. ``fractionMetro = 0.3`` would mean 30% of agents use the metro). 
- ``home`` and ``work`` - these are sampled from the dataset of scraped coordinates we have. Each coordinate with category label of ``house`` or ``apartments`` is a valid home, and every coordinate that isn't those two labels can be a workplace (e.g. ``office``, ``school``, ``college`` are all valid workplaces). *The issues here are twofold. Firstly, this potentially neglects mixed use buildings. Places like Kriterion might have both housing and a workplace inside them. Secondly, this neglects the fact that certain workplaces might have different amounts of workers, giving equal weight to every workplace. A large office building might have hundreds of workers, while Bagels & Beans might have 5. Another minor point is that this neglects all non-9-to-5 schedules.*
### Logic
1. For every resident, sample ``home`` and ``workplace`` from the list previously defined.
2. Randomly select a mode with a weighted choice, with weights of ``fractionMode``.
3. Generate a departure time from home to work and from work to home. This is done by sampling two normal distributions with a mean of ``9`` and ``17`` and standard deviation of ``0.25`` (15 minutes).
4. Generate the two trips and generate a person from it, populating the array. Repeat for the total amount of residents.
## Roetersstraat Primary School

This scenario simulates the pupils at the primary school and their parents going to and from school, and if applicable work.

### Assumptions
- ``students`` - this is the amount of students that goes to the school daily.
- ``schoolHours`` - this is when the school starts and ends. The assumption is that it starts and ends at the same time for everyone. This can be made more realistic by inquiring what the actual hours are.
- ``fractionMode`` - this is a series of variables that denote the fraction of the children agents that use a certain mode of transport to get to school (e.g. ``fractionMetro = 0.3`` would mean 30% of agents use the metro). A similar set exists for parents, also including them driving (as kids wouldn't drive to primary school).
- ``parentChance`` - this is the chance that a parent accompanies the kid to school (e.g. if ``students = 100`` and ``parentChance = 0.5``, you would expect around 50 parents to accompany their kids).
- ``home`` and ``work`` are identical to the ``Residents`` scenario.
- ``weesperMetro`` - in this stage, any agent using the metro will leave from the Weesperplein metro station exit nearest Valckenierstraat.

### Logic
1. For each child, their ``home`` is randomly sampled from the list of homes prepared and their ``mode`` of transportation is randomly chosen with weights ``fractionMode``.
2. A biased coin toss happens to figure out whether a child is accompanied by their parent with weight ``parentChance``. 
3. If a parent accompanies the child, their ``work`` is randomly sampled from the list. They get the same ``home`` as the child.
4. Their ``mode`` of transportation is randomly selected from the available modes, with weights ``fractionParentMode``. **If the parent is driving,** the kid is not generated, and only the parent is. This means that there are not two cars, and only one, representing the parent dropping their kid off and leaving.
5. 4 trips are generated for the parent: home-school (1), school-work (2), work-school (3), school-home (4). The departure time from home is sampled from a normal distribution with a mean of half an hour before class starts and standard deviation of 15 minutes. The departure time from work to school has a mean of when the class ends with standard deviation of 15 minutes. *These values thus far are arbitrary*.
6. The other two trips; school-work, school-home are defined in relation to the departure times of trips 1 and 3. 10 minutes after the parent departs from home, they will depart from the school towards work for trip 2, similarly for trip 4. If the parent takes more than 10 minutes making trips 1 and 3, the software will delay the trips that follow, immediately executing them when they reach the school. Otherwise, they will wait for the difference of the time and then leave. This is done for two reasons. The first is that A/BStreet scenarios are not aware of the arrival times, as you cannot infer from the scenario file whether there will be a traffic jam or any other obstacle. The second is that this represents the effect of parents living closer (within 10 minutes of the school) being part of the Roetersstraat and its' surroundings community, being more likely to stay around for a few minutes chatting with other parents that are members of that community. *The value of 10 minutes is arbitrary, further research about network theory as it relates to communities and physical distance might be necessary to refine this estimate.*
7. These trips for the parents are then turned into one person dictionary that is populated into the array of people.
8. If the parent is not driving, the child can be generated. If the child does not have a parent, they get assigned a random home, mode of transportation, as outlined in step 1. They also get assigned a departure time by sampling from a normal distribution with a mean of half an hour before class and standard deviation of 15 minutes.
9. They also get assigned a departure time from school. If they have a parent, they get their parent's departure time from work + 10 minutes. *This could lead to the child leaving alone if the parent takes more than 10 minutes to get to the school.* If they don't, their departure time is sampled from normal distribution with mean of 15 minutes before class ends, with a standard deviation of 15 minutes.
10. If the child (and/or their parent) takes the metro, the child's home is assigned to be the ``weesperMetro``.
11. The trips of the child are combined to create a person, and the person is populated into the people array.

# Bibliography
Melnikov, V. R., Krzhizhanovskaya, V. V., Lees, M. H., & Boukhanovsky, A. V. (2016). Data-driven Travel Demand Modelling and Agent-based Traffic Simulation in Amsterdam Urban Area. Procedia Computer Science, 80, 2030–2041. https://doi.org/10.1016/j.procs.2016.05.523
