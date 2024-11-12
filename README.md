# Roetersstraat
This is the project repository for the second year bachelor's programme Computational Social Science at the Universiteit van Amsterdam.

# Directories
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
