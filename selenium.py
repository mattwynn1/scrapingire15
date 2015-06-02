from bs4 import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from datetime import date, timedelta

today = date.today()

def num_padder(x):
    if len(str(x)) == 1:
        return "0" + str(x)
    else:
        return str(x)
        
datestring = num_padder(today.month) + "/" + num_padder(today.day) + "/" + str(today.year)

driver = webdriver.Chrome()
driver.get("http://www.sarpy.com/claims")

assert "Sarpy County" in driver.title

print "Connected!"

elem = driver.find_elements_by_class_name("igte_EditInContainer")

driver.execute_script('var elm = document.getElementsByClassName("igte_EditInContainer"); elm[0].removeAttribute("readonly"); elm[1].removeAttribute("readonly");')

begin = elem[0]
end = elem[1]

begin.click()
begin.send_keys(datestring)

end.click()
end.send_keys(datestring)

driver.find_element_by_id("MainContent_btnFinish__3").click()

page = driver.page_source
soup = BeautifulSoup(page)

driver.close()

f = open('sarpy_claims.txt', 'wb')

table = soup.findAll('table')[10]

counter = 1

amount = []

for row in table.findAll('tr'):
    col = row.findAll('td')
    date = col[0].string.strip().split("/")
    newdate = date[2] + '-' + num_padder(date[0]) + "-" + num_padder(date[1])
    dept = col[1].string.strip()
    payee = col[2].string.strip()
    print payee
    amt = col[3].string.strip().replace('$','').replace(',', '')
    amount.append(float(amt))
    descrip = col[4].string.strip()
    rec = ('',newdate, 'Sarpy County', dept, payee, descrip, amt, '','','')
    f.write("|".join(rec) + "\n")
    counter += 1

total = sum(amount)
print str(counter - 1) + ' new Sarpy claims worth $' + str("{:,}".format(total))
    
f.flush()
f.close()
