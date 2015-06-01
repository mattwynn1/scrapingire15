#We need some basic libraries to get started.
import requests
from bs4 import *

# Our end goal is a pipe-delimited text file. Let's open that file up now so we have somewhere to put our data.
f = open('inspections.txt', 'wb')

# As of right now, there are 33 pages of results in ZIP code 19107. We can use that to set a range and loop through them.
for i in range(32):
    # If it's our second time through, we'll want to roll the counter forward.
    try:
        counter += 20
    # Otherwise we can just start at record one.
    except:
        counter = 1

    # The url has one piece that needs to change; a digit that represents the first record. We can accomodate this by splitting it into three pieces...
    prefix = "http://philadelphia.pa.gegov.com/philadelphia/search.cfm?start="
    suffix = "&searchType=zip&zc=19107"
    # And then tying them together
    url = prefix + str(counter) + suffix
    
    # This part won't change! We want to open the page and convert it to nice, clean, beautiful soup.
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html)

    # Business names are in bold, but outside of the div containing business information.
    # There are also some extraneous bold links. We need to eliminate those by specifying a range.
    names = soup.find_all('b')[1:21]


    # Our information is inside a div with a specific style. We can use that style to identify the "containers" we're after.
    divs = soup.find_all('div', style='margin-bottom:10px;')

    # And now for the super kludgy payoff pitch. Since we have two lists, we need to stitch the name with the right information. We'll do this by using 'enumerate,' which gives us a loop number in addition to our data.
    for idx, item in enumerate(divs):
        name = names[idx].string
        # Stripping some fugly text
        address = item.contents[0].string.strip('\r\n\t\t\t\t\t')
        # Using bs4 to access the content of the date -- again, it's wrapped in some awfulness
        inspected = item.contents[3].contents[1].string
        # Creating the record. '\n' is a linebreak character in Windows
        record = (name, address, inspected, '\n')
        # Writing to a file
        f.write("|".join(record))
        # print is a great way to keep us apprised of the script's progress. Then if it breaks, we know where.
        print "wrote %s" % name
    
f.close()


