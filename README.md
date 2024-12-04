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

The scenario matches the nearest building, within 100 meters.

Further documentation on the scenarios in A/BStreet can be found [here](https://a-b-street.github.io/docs/tech/dev/formats/scenarios.html).

### uva_scenario.py (v1.0)
This contains the functions necessary to convert a distribution of students arrival times and rooster schedule data and combine that into a scenario ready to load into A/BStreet.

**Room for improvement**:
1. Discuss what the implications are of using a csv of 10 thousands samples of the distribution of arrival times.
2. Normalise that distribution where class start time = 0, anyone arriving before has a negative number and anyone after a positive number (in seconds). Then, given any time, you could conver it to seconds after midnight and add the value sampled from the distribution. E.g. ``arrivalTime = convert_time(classStart) + sampledTime`` or ``arrivalTime = convert_time('11:00') + -180`` meaning that the student arrived 180 seconds (3 minutes) before 11:00, or at 10:57.
3. Implementing a different mechanism for departure time. Right now the arrivalTime is calculated and 5-15 minutes is subtracted. Perhaps it makes more sense to subtract a set time so as to retain information in regards to the arrivalTime. Maybe this could be calculated as a function of the distance between the ``origin`` and ``destination``. E.g. the distance is 2km, hence subtract ``15 * 2`` minutes for people who walk, ``7 * 2`` for those who bike and so on.
4. Implementing a different mechanism for departure location. Right now, all those who arrive with a metro get out at the metro station near Valckenierstraat and everyone else gets a randomly assigned coordinate from the entire coordinate list. We need to implement a system where that is done more realistically and off-map locations are considered.

### scenario_tools.py
This file contains the functions to create a scenario given certain parameters. There are a number of functions that can be imported into a working file to make creating scenarios easier. 

### scenario.py
This file combines all the functions that return separate arrays of people into one JSON file for the scenario. This is where the parameters for each individual scenario should be adjusted.

**Modules**:
1. ``write_scenario(name, people)`` - takes a string for ``name`` and array of ``people``, saves JSON file and returns message.
2. ``convert_time(inStr)`` - takes a string for ``inStr`` in the format of '00:20' or '19:35' and returns it as an integer in terms of seconds after midnight. DO NOT FORGET TO ADD FOUR ZEROES AT THE END OF THE OUTPUT. This is not done in the function so that operations can still be done on the time afterwards. Example usage: ``departureTime = int(str(convert_time(inStr)) + '0000')``.
3. ``generate_person(timeDeparture, origin, destination, mode)`` - takes ``timeDeparture`` as integer of seconds after midnight (with trailing zeroes), ``origin`` and ``destination`` as array of coordinates of length 2 (e.g. ``[52.356346, 67.75475]``) and ``mode`` as string of values ``Walk``, ``Bike``, ``Drive`` or ``Transit``. ``Transit`` is unused for this application and ``Walk`` should be used from metro station.

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
