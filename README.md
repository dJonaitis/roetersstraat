# Roetersstraat
This is the project repository for the second year bachelor's programme Computational Social Science at the Universiteit van Amsterdam.

# Directories
## /abstreet
The agent-based model of the Roetersstraat is constructed using A/BStreet. This repository does not contain A/BStreet itself, which can be found [here](https://github.com/a-b-street/abstreet).

This directory contains the code for creating the scenarios and the map files necessary to be able to replicate the model.

An example scenario in A/BStreet can be found below. 

```json
{
  "scenario_name": "minimal",
  "people": [
    {
      "trips": [
        {
          "departure": 10000,
          "origin": {
            "Position": {
              "longitude": -122.303723,
              "latitude": 47.6372834
            }
          },
          "destination": {
            "Position": {
             "longitude": -122.3190500,
              "latitude": 47.6378600
        }
          },
          "mode": "Bike",
          "purpose": "Meal"
        },
        {
          "departure": 12000000,
          "origin": {
            "Position": {
             "longitude": -122.3190500,
              "latitude": 47.6378600
        }
          },
          "destination": {
            "Position": {
              "longitude": -122.3075948,
              "latitude": 47.6394773
        }
          },
          "mode": "Walk",
          "purpose": "Recreation"
        }
      ]
    }
  ]
}
```

In this scenario, named "minimal", there is one person, making two trips. The first begins at one second past midnight (``10000``) from coordinates ``-122.30``, ``47.637`` to coordinates ``-122.32``, ``47.638``. The person uses a bike to travel. Their next trip begins at 00:20, ``1200`` seconds after midnight. The purpose field is not necessary.

For complex scenarios where you need trips where it is unclear what the next departure time (e.g. a parent dropping their kid off at school, then going to work, won't know when exactly they get to the school, and thus won't know when to leave) you need to ensure that the trip with the unknown departure time has a time greater than the previous known departure time, and less than the next known departure time.

The scenario matches the nearest building, within 100 meters.

Further documentation on the scenarios in A/BStreet can be found [here](https://a-b-street.github.io/docs/tech/dev/formats/scenarios.html).

**To be done**:
1. Parking needs to be implemented, as OpenStreetMap cannot accurately map parking to its streets. In order to do so, consult [this](https://a-b-street.github.io/docs/software/parking_mapper.html) part of the documentation.
### scenarios.md
This file contains the logic and assumptions for every individual scenario. It can be found [here](abstreet/scenarios.md).
### uva_scenario.py (v1.0)
This contains the functions necessary to convert a distribution of students arrival times and rooster schedule data and combine that into a scenario ready to load into A/BStreet.

**Room for improvement**:
1. Discuss what the implications are of using a csv of 10 thousands samples of the distribution of arrival times.
2. Normalise that distribution where class start time = 0, anyone arriving before has a negative number and anyone after a positive number (in seconds). Then, given any time, you could conver it to seconds after midnight and add the value sampled from the distribution. E.g. ``arrivalTime = convert_time(classStart) + sampledTime`` or ``arrivalTime = convert_time('11:00') + -180`` meaning that the student arrived 180 seconds (3 minutes) before 11:00, or at 10:57.
3. Implementing a different mechanism for departure time. Right now the arrivalTime is calculated and 5-15 minutes is subtracted. Perhaps it makes more sense to subtract a set time so as to retain information in regards to the arrivalTime. Maybe this could be calculated as a function of the distance between the ``origin`` and ``destination``. E.g. the distance is 2km, hence subtract ``15 * 2`` minutes for people who walk, ``7 * 2`` for those who bike and so on.
4. Implementing a different mechanism for departure location. Right now, all those who arrive with a metro get out at the metro station near Valckenierstraat and everyone else gets a randomly assigned coordinate from the entire coordinate list. We need to implement a system where that is done more realistically and off-map locations are considered.

### resident_scenario.py
**Room for improvement**:
1. Not all residents that live in the area actually work inside the same area. Many people are likely to be working outside the area defined by the geojson-file. However, this could possibly be accounted by estimating or doing desk research to find out how many workers actually work in their immediate surroundings, in this case the geojson-file.
2. A lot of working residents also work out of home for a significant amount of time, following official CBS Statistics. This needs to be taken into account to make the model as accurate as possible. For this, statistics from the CBS haven been taken, in which it says 52% of the working population work out of home and out of this 52%, of which the specific statistics estimations predict these people work around 37.5% of their total work time at home.
3. Another consideration point has to do with the workforce that has workdays in the weekend. Taking this into account can also be important, but would make the model too complex probably. This is something we need to weigh out before deciding if we take this into account.
4. In Amsterdam, a higher than average amount of students are living, which means it is likely we will overestimate the amount of working residents. By knowing 7% of residents in Amsterdam are students, we could take this into account by calculating the difference towards the country-wide percentage of students in the Netherlands. 
5. Sampling more workers to the bigger employers (like UvA) would change the traffic flow in the street as well by making it more accurate.


### school_scenario.py

### scenario.py
This file combines all the functions that return separate arrays of people into one JSON file for the scenario. This is where the parameters for each individual scenario should be adjusted.

### scenario_tools.py
This file contains the functions to create a scenario given certain parameters. There are a number of functions that can be imported into a working file to make creating scenarios easier. 

**Modules**:
1. ``write_scenario(name, people)`` - takes a string for ``name`` and array of ``people``, saves JSON file and returns message. ``people`` array is made up of dictionaries generated by ``generate_person()``.
2. ``convert_time(inStr)`` - takes a string for ``inStr`` in the format of '00:20' or '19:35' and returns it as an integer in terms of seconds after midnight. DO NOT FORGET TO ADD FOUR ZEROES AT THE END OF THE OUTPUT. This is not done in the function so that operations can still be done on the time afterwards. Example usage: ``departureTime = int(str(convert_time(inStr)) + '0000')``.
3. ``generate_person(trips)`` - takes an array of trips (returned from ``generate_trip()``) and returns a formatted person dictionary.
4. ``generate_trip(timeDeparture, origin, destination, mode)`` - takes ``timeDeparture`` as integer of seconds after midnight (with trailing zeroes), ``origin`` and ``destination`` as array of coordinates of length 2 (e.g. ``[52.356346, 67.75475]``) and ``mode`` as string of values ``Walk``, ``Bike``, ``Drive`` or ``Transit``. ``Transit`` is unused for this application and ``Walk`` should be used from metro station. Returns a dictionary of one trip.
5. ``generate_departure(mean, std, n)`` - takes ``mean`` as float of time (e.g. ``9.5`` for 9:30), ``std`` as float of time in same format (e.g. ``0.25`` for 15 minutes) and ``n`` as integer. Returns an array of length ``n`` of samples of a normal distribution with ``mean`` and ``std``. 
6. ``convert_time_frac_string(inFrac)`` - takes ``inFrac`` as a float of time and returns a string in the format ``HH:MM``. Example input and output: ``9.5`` becomes ``9:30``.

### geojson.json
This is the GeoJSON file used for the model. In order to replicate the agent-based model, this is the file to import into A/BStreet to create the map of the Roetersstraat and its immediate surroundings.
## /accidents
This folder contains the datasets for accident data in Amsterdam.
## /coordinates
This folder contains the code for scraping a list of coordinates that match to every building within the limits of the model designated in the [GeoJSON file](/abstreet/geojson.json).
### scraping_addresses.ipynb
This Jupyter Notebook file contains the code used to obtain all relevant coordinates in the area highlighted by the geojson file and that will thereby be included in the Agent-Based Model. 
In this Notebook, the following process has been followed:
1. Getting the relevant boundary coordinates from the geojson file
2. Manually converting these geojson coordinates into x- and y-values that can be used on the [Kadasterregister website](https://bagviewer.kadaster.nl/lvbag/bag-viewer/?zoomlevel=1)
3. Manually selecting all relevant building block URLs inside the boundaries of our Agent-Based Model on the website of the Kadasterregister and putting them into a CSV-file
4. Using these URLs to get all addresses in the relevant buidling blocks
5. Obtain the coordinates, function and name of these addresses by using the geopy-library
6. Save the values in a list and exporting this list to a CSV-file

## /rooster
This directory contains scraped data, and data processing for [Rooster](rooster.uva.nl).
### scraper.ipynb
The basic procedure for the scraper is as follows:
1. Open the schedule with Selenium.
2. Click the “Add Timetable” button and read all the timetable names, saving them as an array.
3. Iterate through, opening each timetable, 25 at a time. 
4. Once timetables are open, read the relevant information (Location, size, time, course number, date)
5. Repeat steps 3-4 until all timetables are read. 
6. Save to csv file.

### data_work.ipynb
Data pre-processing.

# Tools & Packages
## Python
- [Selenium](https://selenium-python.readthedocs.io/)
- [Pandas](https://pandas.pydata.org/)
- [Matplotlib](https://matplotlib.org/)
## Agent-based modelling
- [A/B Street](https://github.com/a-b-street/abstreet)
