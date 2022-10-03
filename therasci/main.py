from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from bs4 import BeautifulSoup
import json




def data_scraping(value):
    # opts = Options()
    # opts.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
    # chrome_driver = os.getcwd() +"./chromedriver.exe"
    # driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)

    # driver = webdriver.Chrome()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)

    driver.get('https://www.asicminervalue.com/')

    price_element = driver.find_element("name", "electricitycost")
    price_element.clear()
    price_element.send_keys(f"{value}")
    price_element.submit()
    data_array = []
    try:
        soup = BeautifulSoup(driver.page_source,'lxml')
        datatable = soup.find('table', attrs={'id':'datatable_profitability'}).find('tbody').findAll('tr')
        for tr in datatable:
            td_counter = 1
            data_object = {}
            for td in tr:

                if td_counter == 1:
                    data_object['model'] = {
                        'name': td.get('data-search'),
                        'logo': td.find('img').get('src')
                    }
                elif td_counter == 2:
                    data_object['release'] = str(td.find('span').text).replace(u'\xa0', u' ')
                elif td_counter == 3:
                    hashrate_span_tags = td.findAll('span')
                    data_object['hashrate'] = str(hashrate_span_tags[0].text).strip()+str(hashrate_span_tags[1].text)
                elif td_counter == 4:
                    power_span_tags = td.findAll('span')
                    data_object['power'] = str(power_span_tags[0].text).strip()+str(power_span_tags[1].text)
                elif td_counter == 5:
                    noise_span_tags = td.findAll('span')
                    data_object['noise'] = str(noise_span_tags[0].text).strip()+str(noise_span_tags[1].text)
                elif td_counter == 6:
                    algo_data_string = str(td.get('data-sort'))
                    if ',' in algo_data_string:
                        algo_data_string = algo_data_string.split(',')
                    else:
                        algo_data_string = [algo_data_string]
                    data_object['algo'] = algo_data_string
                elif td_counter == 7:
                    try:
                        display_value_spans = td.findAll('span')
                        ivalue_b_tags = str(td.find('div').find('div').get('data-original-title')).replace(":","").replace("<b>", "").replace("</b>","").replace("Income","").replace("Electricity","").replace("<font color=green>","").replace("<font color=red>","").replace("</font>","").replace(" ","")
                        data_object['profitability'] = {
                            'display_value': str(display_value_spans[1].text).strip()+str(display_value_spans[2].text).strip(),
                            'income': ivalue_b_tags.split('<')[0],
                            'electricity': ivalue_b_tags.split('>')[-1]
                        }
                    except:
                        display_value_spans = td.find('span')
                        if display_value_spans:
                            data_object['profitability'] = {
                            'display_value': str(display_value_spans.text).strip(),
                            'income': None,
                            'electricity': None
                        }
                    print(data_object)
                    data_array.append(data_object)

                    with open("asicminervalue.json", "w", encoding='utf-8') as jsonfile:
                        convert_to_json = json.dumps(data_array, indent=4, ensure_ascii=False)
                        jsonfile.write(convert_to_json)
                
                else:
                    print('i am in else...............')
                    pass
                td_counter+=1
            # break
        return data_array
    except Exception as e:
        print('here is the exception: ', e)
