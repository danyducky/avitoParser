"""
Avito Parse Application
"""
from time import sleep
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.proxy import Proxy, ProxyType
from excelBuilder import excelBuilder

excel = excelBuilder()


avitoShops = 'https://www.avito.ru/shops/ekaterinburg'

options = Options()
#options.add_argument('--headless')



profile = webdriver.FirefoxProfile()
profile.set_preference("browser.cache.disk.enable", False)
profile.set_preference("browser.cache.memory.enable", False)
profile.set_preference("browser.cache.offline.enable", False)
profile.set_preference("network.http.use-cache", False)


browser = Firefox(profile, options=options, executable_path=r'C:\Program Files\geckodriver\geckodriver.exe')
browser.get('https://www.avito.ru/shops/ekaterinburg')


linkWithPageNumber = browser.find_elements_by_class_name('pagination-page')[-1].get_attribute('href')
pageNum = [int(letter) for letter in linkWithPageNumber if letter.isdigit()]
pageNum = int(''.join(str(i) for i in pageNum))

data = dict()

# проход по всем страницам на этом домене
for page in range(1, pageNum+1):
    try:
        browser.get(f'{avitoShops}?p={page}')
        # t_s_i
        elements = browser.find_elements_by_class_name('t_s_i')
        # t_s_photo_link
        sub_elements = [elem.find_element_by_class_name('t_s_photo_link') for elem in elements]
        # href links from t_s_photo_link
        links = [elem.get_attribute('href') for elem in sub_elements]

        for link in links:
            try:
                browser.get(link)
                sleep(1)
                name = browser.find_element_by_class_name('shop-header-shop-header-title-1VQXz')
                phone = browser.find_element_by_class_name('shop-header-shop-header-phone-3Ivio')
                browser.delete_all_cookies()
                excel.addRow(name.text, phone.text)
                data[name.text] = phone.text
                print(f'Company name: {name.text} \nPhone: {phone.text}\n')
            except Exception as e:
                print(f"EXCEPTION! -----------------------\n{e}")
                continue


    except Exception as e:
        print(f"EXCEPTION FROM SWITCHING PAGES! \n{e}")


excel.save()

browser.quit()

