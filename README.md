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
## /accidents
## /rooster
This directory contains scraped data, and data processing for [Rooster](rooster.uva.nl)
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
