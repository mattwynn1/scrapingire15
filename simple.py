#We need some basic libraries to get started.
import requests # "An elegant and simple HTTP library for Python." Gets us around the web.
from bs4 import * # "A library for pulling data out of HTML and XML files." 
import csv # "implements classes to read and write tabular data in CSV format"

# First, we identify the page we want to scrape. This is just a string.
url = "http://en.wikipedia.org/wiki/List_of_cities_in_Pennsylvania"

# Then we open it using the requests library. 
response = requests.get(url)
html = response.content

# And turn it into a Beautiful Soup object. This turns it from a string into parseable HTML.
soup = BeautifulSoup(html)

# Luckily, there's one table that has all our data. We can quickly find it.
table = soup.find('table')

# Let's create an empty list to contain our data. We'll append to this later.
list_of_rows = []

# We can go through this table row by row, extracting each cell.
for row in table.findAll('tr')[1:]:
    list_of_cells = []
    for cell in row.findAll('td'):
        text = cell.text.replace('&nbsp;', '')
        list_of_cells.append(text)
    list_of_rows.append(list_of_cells)
    
# Once that's over, list_of_rows will be full of data that look startlingly like a csv. Let's write it!
outfile = open('cities.txt', 'wb')
writer = csv.writer(outfile)
writer.writerows(list_of_rows)
