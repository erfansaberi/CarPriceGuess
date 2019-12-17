#this script collect information from bama.ir and help you guess your car price
#developed by erfan saberi
#Special Thanks to Jadi :)
x , y , data , kar = [], [], [], []

lang = input('Select Language  Fa/En  : ')
if lang == 'Fa' or lang =='FA' or lang == 'fa':
    title = 'تخمین قیمت خودرو'
    selectcar = 'از ليست موجود يک ماشين را انتخاب کنيد : '
    selectmodel = 'لطفا از بين مدل هاي موجود انتخاب کنيد : '
    unknowncar = 'ماشين شناخته نشده'
    selectmodelunknown = 'لطفا مدل ماشين مورد نظرتان را وارد کنيد : '
    howmany = 'چند صفحه اطلاعات جمع کنم ؟ تعداد صفحات بيشتر باعث افزايش دقت نرم افزار ميشود : '
    inprogress = '        در حال جمع آوري اطلاعات'
    carpr = 'قیمت ماشین شما حدودا  %i تومان است'
    insertkarkard = 'کارکرد ماشین را به کیلومتر وارد کنید'
    insertyear = 'سال توليد ماشين را وارد کنيد'
    donetext = 'برای استفاده مجدد اینتر بزنید ، در غیر اینصورت با تایپ هر چیزی میتوانید از برنامه خارج شوید'
if lang == 'En' or lang == 'EN' or lang == 'en':
    title = 'Car Price Guess'
    selectcar = 'Please select a car brand from list : '
    selectmodel = 'Please enter your car model from list : '
    unknowncar = 'Unknown car'
    selectmodelunknown = 'Please insert your car model : '
    howmany = 'How much of web pages i have to crawl? (give me a number): '
    inprogress = 'Crawling web pages ...'
    carpr = 'Your car price is around %i'
    insertkarkard = 'how many kilometers this car traveled? : '
    insertyear = 'Please insert your car product year : '
    donetext = 'Press enter for another guess or type something to exit'
print(title)

#ask user for car brand and model
print('peugeot , kia , pride , bmw , renault')
cartype = input(selectcar)
if cartype == 'peugeot':
    print('206-ir , pars , 207 , 405 , 206sd , 2008 , 207sd')
    carmodel = input(selectmodel)
elif cartype == 'kia':
    print('cerato-ir , optima , sportage , cerato , sorento')
    carmodel = input(selectmodel)
elif cartype =='bmw':
    print('5-series-sedan , x4 , x3 , 3-series-sedan , 7-series')
    carmodel = input(selectmodel)
elif cartype == 'pride':
    print('131 , 111 , sedan , 132')
    carmodel = input(selectmodel)
elif cartype == 'renault':
    print('tondar90 , sandero-stepway , sandero , talisman , koleos , megan-ir , pars-tondar')
    carmodel = input(selectmodel)
else:
    print(unknowncar)
    carmodel = input(selectmodelunknown)

a = int(input(howmany))

print('=======================')
print(inprogress)
print('=======================')

import requests
import re
from sklearn import tree
from bs4 import BeautifulSoup

#Exctracting data from web
for i in range(1,a+1):
    session = requests.get('https://bama.ir/car/%s/%s/all-trims?hasprice=true&page=%i' % (cartype, carmodel, i))
    soup = BeautifulSoup(session.text, 'html.parser')
    res = soup.find_all('div', attrs={'class':'listdata'})
    
    for car in res:
        name = car.find('h2', attrs={'itemprop':'name'})
        name = re.sub(r'\s+', ' ', name.text).strip()
        try:
            brand = car.find('span', attrs={'class':'hidden-xs mod-date-car-page product-company-name'})
            brand = (re.sub(r'\s+', ' ', brand.text).strip())
        except:
            brand = 'unknown'
        year = car.find('span', attrs={'itemprop':'releaseDate'})
        work = car.find('p', attrs={'class':'price hidden-xs'})
        year,work = re.sub(r'\s+', ' ', year.text), re.sub(r'\s+', ' ', work.text)
        kar.append(work)
        if work == ' کارکرد صفر ' or work == 'کارتکس':
            work = 0
        elif not work == '-':
            try:
                work = re.sub(r'\کارکرد', '', work).strip()
                work = re.sub(r',', '', work).strip()
                work = int(work)
            except:
                pass
        else:
            work = 0
        year = re.sub(r'، ', '', year)
        city = car.find('p', attrs={'class':'provice hidden-xs'})
        city = re.sub(r'\s+', ' ', city.text).strip()
        cost = car.find('p', attrs={'class':'cost'})
        cost = re.sub(r'\s+', ' ', cost.text).strip()
        cost = re.sub(r' تومان', '', cost)
        cost = re.sub(r',', '', cost)
        if not cost == 'در توضیحات' and not cost == 'حواله' and not cost == 'توافقی':
            cost = int(cost)
        if type(cost)==int:
            data.append(year)
            data.append(work)
            y.append(cost)
            x.append(data)
            data = []
    print('page ', i, 'done')
print('=======================')

#Fit extracted data on a Decision Tree Classifier
clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)

def carprice(karkard, sal):
    price = clf.predict([[sal, karkard]])
    print(carpr%(price))

def checkcarprice():
    print(title, cartype, carmodel)
    karkard = input(insertkarkard)
    sal = input(insertyear)
    carprice(karkard, sal)

check = ''
while check == '':
    checkcarprice()
    check = input(donetext)
