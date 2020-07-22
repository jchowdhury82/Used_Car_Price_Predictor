from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import re
import time
import sys

pd.set_option('display.max_colwidth',None)

def cleanstr(s):
    return re.sub(r'[\r\n]','',s).strip()


driver = webdriver.Chrome("/usr/local/bin/chromedriver")

attrlist = []

for i in range(30):
    print("***** Start scrape for " + str(i))
    url = f'https://www.truecar.com/used-cars-for-sale/listings/price-below-75000/?page={i+1}&sort[]=best_match'
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    #soup = BeautifulSoup(open("cars.xml"), 'lxml')
    all_matches = soup.find_all('div', {'data-qa': 'Listings'})
    for car in all_matches:
        try:
            vin = ''
            year= ''
            make = ''
            model = ''
            trim = ''
            pricecat = ''
            pricevar = ''
            pricevalue = ''
            mileage = ''
            city = ''
            state = ''
            colext = ''
            colint = ''
            acchist = ''
            owner = ''
            usage = ''


            link=car.find('a')
            vin = link.attrs['data-test-item-vin'] if link.has_attr('data-test-item-vin') else ''

            if link.attrs['data-qa'] == 'VehicleCard':

                yearmakemodel = car.find('div', {'data-test':'vehicleCardYearMakeModel'})
                year = yearmakemodel.find('span', {'class':'vehicle-card-year'})
                year = cleanstr(year.text)

                makemodel = yearmakemodel.find('span', {'class':'vehicle-header-make-model'})
                makemodel = cleanstr(makemodel.text) if makemodel is not None else ''
                make,model = makemodel.split(' ',1)


                trim = car.find('div', {'data-test': 'vehicleCardTrim'})
                trim = cleanstr(trim.text) if trim is not None else ''

                marketcontext = car.find('div', {'data-qa':'VehicleCardMarketContextBlock'})
                pricecat = marketcontext.find('span', {'class': 'graph-icon-title'})
                pricecat = cleanstr(pricecat.text) if pricecat is not None else ''
                pricevar = marketcontext.find('div', {'class': 'font-size-1 text-truncate'})
                pricevar = cleanstr(pricevar.text) if pricevar is not None else ''
                pricevar = pricevar.replace(',','')


                price = car.find('h4', {'data-test': 'vehicleCardPricingBlockPrice'})
                pricevalue = cleanstr(price.text) if price is not None else ''
                pricevalue = pricevalue.replace(',','').replace('$','') if price is not None else '0'

                mileagedisc = car.find('div', {'data-qa':'MileageAndDiscount'})
                mileage = mileagedisc.find('div', {'data-test': 'vehicleMileage'})
                mileage = re.sub(r'<svg>*</svg>','',mileage.text) if mileage is not None else ''
                mileage = mileage.replace(' miles','').replace(',','') if mileage is not None else ''
                mileage = cleanstr(mileage)

                location = car.find('div', {'data-qa':'Location'})
                loc = re.sub(r'<svg>*</svg>','',location.text) if location is not None else ''
                loc = cleanstr(loc)
                city,state = [x.strip() for x in loc.split(',')]

                extintcol = car.find('div', {'data-qa':'ExteriorInteriorColor'})
                color = re.sub(r'<svg>*</svg>','',extintcol.text) if extintcol is not None else ''
                color = cleanstr(color)
                colext,colint = [x.strip() for x in color.split(',')]
                colext = colext.replace(' exterior','')
                colint = colint.replace(' interior','')

                conditionhist = car.find('div', {'data-qa':'ConditionHistory'})
                cond = re.sub(r'<svg>*</svg>','',conditionhist.text) if conditionhist is not None else ''
                cond = cleanstr(cond)
                condparts = cond.split(',')
                for part in condparts:
                    if 'accident' in part.lower():
                        acchist = part.lower().replace(' accidents','').replace(' accident','')
                    if 'owner' in part.lower():
                        owner = part.lower().replace(' owners', '').replace(' owner', '')
                    if 'use' in part.lower():
                        usage = part.lower().replace(' use', '')


                attr = {
                        'vin' : vin,
                        'year' : year,
                        'make' : make,
                        'model' : model,
                        'trim' : trim,
                        'pricecategory' : pricecat,
                        'pricevariance' : pricevar,
                        'price' : pricevalue,
                        'mileage' : mileage,
                        'city' : city,
                        'state' : state,
                        'colorexterior' : colext,
                        'colorinterior' : colint,
                        'accidenthist' : acchist,
                        'owner' : owner,
                        'usage' : usage
                        }

                attrlist.append(attr)
        except:
            print("Error in vin {}, {}".format(vin,sys.exc_info()[0]))
    print("***** Completed for pass " + str(i))
    time.sleep(30)

df = pd.DataFrame.from_dict(attrlist)
df.to_csv("cars1.csv",sep='|', index=False, header=True )
