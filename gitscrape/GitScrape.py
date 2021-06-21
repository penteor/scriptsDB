import os, time, random

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup as bs

PageNo = 0
def writefile(sourcecode):
    f = open("sources.txt", "a")
    f.write(str(sourcecode))
    f.close()


options = Options()
options.headless = False
driver = webdriver.Firefox(options=options, executable_path=os.getcwd() + '/gecko/geckodriver')
print('[*] Browse to Github')
driver.get("https://github.com/clicknull")

# Sleep
print('[*] Click on Repositories button')
Delay = random.randint(3, 10)
print('[*] Sleep for ' + str(Delay) + ' seconds.')
time.sleep(Delay)
href = "/clicknull?tab=repositories"
driver.find_element_by_xpath('//a[@href="' + href + '"]').click()
PageNo += 1

print('[*] Parse Repositories')
Delay = random.randint(3, 10)
print('[*] Sleep for ' + str(Delay) + ' seconds.')
time.sleep(Delay)
writefile(driver.page_source)

#soup = bs(html_source, "html.parser")


#AllLinks = [a for a in soup.find_all("a", href=True)]

isNext = True

while isNext:
    # Click on Next button
    try:
        Delay = random.randint(5, 20)
        print('[*] Sleep for ' + str(Delay) + ' seconds.')
        time.sleep(Delay)
        driver.find_element_by_xpath('//a[@rel="nofollow"][text()="Next"]').click() #  and [contains(text()="Next")]]'
        #driver.find_element_by_partial_link_text('Next').click()
        writefile(driver.page_source)
        PageNo += 1
        print('[*] Page: ' + str(PageNo))

        #Links = [a for a in soup.find_all("a", href=True)]
        #AllLinks += Links

        isNext = True
    except Exception as err:
        isNext = False
        print(str(err))
