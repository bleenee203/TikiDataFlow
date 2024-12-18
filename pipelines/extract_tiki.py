import os
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException, TimeoutException, WebDriverException,InvalidSessionIdException
from time import sleep
import threading
from queue import Queue
import re
import ast
import pickle
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
print_lock = threading.Lock()


class func:
    def __init__(self):
        pass

    @staticmethod
    def get_elem(driver, elem, full_info_elem = None, elem_type = ''):
        print("Da vao get_elem")
        if elem_type == 'prod_link':
            pl = driver.find_elements(By.CSS_SELECTOR, elem)
            output = [i.get_attribute('href') for i in pl]
        elif elem_type == 'cate':
            cate = driver.find_elements(By.CSS_SELECTOR, elem)
            output = [i.text for i in cate]
        elif elem_type == 'img':
            img_elem = driver.find_element(By.CSS_SELECTOR, elem)
            output = img_elem.find_element(By.TAG_NAME, 'img').get_attribute('srcset').split(' ')[0]
        elif elem_type == 'discount' or elem_type == 'price' or elem_type == 'sale_q' or elem_type == 'rating':
            output = driver.find_element(By.CSS_SELECTOR, elem).text
        elif elem_type == 'info_elems':
            info_elems = driver.find_elements(By.CSS_SELECTOR, elem)
            title_elem, detail_info_elem, describe_elem = full_info_elem[0], full_info_elem[1], full_info_elem[2]
            info, describe, seller, seller_star, seller_reviews_quantity = np.nan, np.nan, np.nan, np.nan, np.nan
            for i in info_elems:
                try:
                    title = i.find_element(By.CSS_SELECTOR, title_elem)
                    title = title.text
                except:
                    title = np.nan
                if title == 'Thông tin chi tiết':
                    try:
                        info_row = i.find_elements(By.CSS_SELECTOR, detail_info_elem)
                        info = [i.text.split('\n') for i in info_row]
                    except Exception as e:
                        print(f'info except: {threading.current_thread().name} - {type(e).__name__}')
                        info = np.nan
                        print('detail_info nan')
                elif title == 'Mô tả sản phẩm':
                    try:
                        describe = i.find_element(By.CSS_SELECTOR, describe_elem).text
                    except Exception as e:
                        print(f'describe except: {threading.current_thread().name} - {type(e).__name__}')
                        describe = np.nan
                        print('describe nan')
                try:
                    seller_header = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".SellerHeader__SellerHeaderStyled-sc-la7c6v-0.bfJGpi"))
                )
                    seller = seller_header.find_element(By.CSS_SELECTOR, ".seller-name a span").text
                    print(f'seller name {seller}')
                except Exception as e:
                    print(f'seller except: {threading.current_thread().name} - {type(e).__name__}')
                    seller = np.nan
                    print('seller nan')
                try:
                    seller_evaluation_elems = seller_header.find_element(By.CSS_SELECTOR, '.item.review')
                    print(f'seller evaluation_elems {seller_evaluation_elems}')
                except Exception as e:
                    print(f'seller eval except: {threading.current_thread().name} - {type(e).__name__}')
                    seller_evaluation_elems = np.nan
                    print('seller_evaluation nan')
                try:
                    seller_star = seller_evaluation_elems.find_element(By.CSS_SELECTOR, '.title').text
                    print(f'seller star {seller_star}')
                except Exception as e:
                    print(f'seller star except: {threading.current_thread().name} - {type(e).__name__}')
                    seller_star = np.nan
                    print('seller_star nan')
                try:
                    seller_reviews_quantity = seller_evaluation_elems.find_element(By.CSS_SELECTOR, '.sub-title').text
                    print(f'seller reviews_quantity {seller_reviews_quantity}')
                except Exception as e:
                    print(f'seller review except: {threading.current_thread().name} - {type(e).__name__}')
                    seller_reviews_quantity = np.nan
                    print('seller_reviews_quantity nan') 
            output = (info, describe, seller, seller_star, seller_reviews_quantity)
        else:
            print('no output')
        return output
    
    @staticmethod
    def wait(driver, time, elem):
        print("Da vao wait")
        wait = WebDriverWait(driver, time)
        elem_to_wait = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, elem)))
        return elem_to_wait
    
    @staticmethod
    def scroll(driver, scroll_iters = 10, scroll_amount = 300, scroll_interval = 0.2):
        try:
            for _ in range(scroll_iters):
                driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_amount)
                sleep(scroll_interval)
        except Exception as e:
            print(f'scroll except: {threading.current_thread().name} - {type(e).__name__}')
            func.scroll(driver, scroll_iters = 10, scroll_amount = 300, scroll_interval = 0.2)
            print(f'Try to re-scroll sucessfully')

    @staticmethod
    def get(driver, link):
        with print_lock:
            print('Đang vào get link')
        try:
            ready_state = driver.execute_script("return document.readyState")
            print(f"Page ready state before loading: {ready_state}")
            driver.set_page_load_timeout(60)
            driver.get(link)
            print(f"Đã vào trang: {link}")
        except:
            driver.refresh()
            ready_state = driver.execute_script("return document.readyState")
            print(f"Page ready state before loading: {ready_state}")
            driver.set_page_load_timeout(60)
            driver.get(link)
            print(f"Đã thu lai vào trang: {link}")

    @staticmethod
    def load_multi_page(driver, n, link = str):
        print('da vao multi page')
        driver.maximize_window()
        link = f'{link}?page={n}'
        print(f"Calling get with link: {link}")
        func.get(driver, link)
        # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        sleep(0.5)

    @staticmethod
    def get_data(driver, que,
                prod_link_elem, category_bar_elem, image_elem, 
                price_elem, discount_elem,
                sales_quantity_elem, rating_elem, 
                info_elem, detail_info_elem, 
                describe_elem,
                extend_page_elem,
                title_elem,
                preventive_prod_link_elem):   
        print("Da vao get_data")
        func.scroll(driver, 150)
        sleep(2)
        try:
            func.wait(driver, 100, prod_link_elem)
            print('pass wait')
            pl = func.get_elem(driver, prod_link_elem, elem_type = 'prod_link')
            print(f'{threading.current_thread().name} - Take Product links succesfully')
        except Exception as e:
            print(f'{threading.current_thread().name} - First Product link not exist')
            print(f'Error when get product {str(e)}')
            try:
                func.wait(driver, 100, preventive_prod_link_elem)
                pl = func.get_elem(driver, preventive_prod_link_elem, elem_type = 'prod_link')
                print(f'{threading.current_thread().name} - Take prevent Product link succesfully')
            except Exception as e:
                print(f'{threading.current_thread().name} - Prevent Product link not exist also')
                print(f'Error when get prevent product{str(e)}')
                pl = []
        page_features = []
        for i, prod_link in enumerate(pl):
            try:
                func.get(driver, pl[i])
            except:
                print('Prod_link die. Get next prod_link')
                func.get(driver, pl[i + 1])

            driver.maximize_window()

            #expandpage
            func.scroll(driver, 15, 300, 0.2)
            try:
                elem_to_wait = func.wait(driver, 2, extend_page_elem)
                elem_to_wait.click()
            except ElementClickInterceptedException:
                print(f'click except: {threading.current_thread().name}')
                try:
                    func.scroll(driver, 2)
                    elem_to_wait.click()
                except Exception as e:
                    print(f'Cant not click: {threading.current_thread().name} - {type(e).__name__}')
            except TimeoutException:
                print(f'Expand page not exist')
            #cate
            try:
                func.wait(driver, 1, category_bar_elem)
                cate = func.get_elem(driver, category_bar_elem, elem_type = 'cate')
            except Exception as e:
                print(f'cate except: {threading.current_thread().name} - {type(e).__name__}')
                cate = np.nan
                print('cate nan')
            #img
            try:
                func.wait(driver, 10, image_elem)
                img = func.get_elem(driver, image_elem, elem_type = 'img')
            except Exception as e:
                print(f'img except: {threading.current_thread().name} - {type(e).__name__}')
                img = np.nan
                print('img nan')
            #price
            try:
                func.wait(driver, 1, price_elem)
                price = func.get_elem(driver, price_elem, elem_type = 'price')
            except Exception as e:
                print(f'price except: {threading.current_thread().name} - {type(e).__name__}')
                price = np.nan
                print('price nan')
            #discount
            try:
                func.wait(driver, 1, discount_elem)
                discount = func.get_elem(driver, discount_elem, elem_type = 'discount')
            except Exception as e:
                print(f'discount except: {threading.current_thread().name} - {type(e).__name__}')
                discount = np.nan
                print('discount nan')
            #rating
            try:
                func.wait(driver, 1, rating_elem)
                rating = func.get_elem(driver, rating_elem, elem_type = 'rating')
            except Exception as e:
                print(f'rating except: {threading.current_thread().name} - {type(e).__name__}')
                rating = np.nan
                print('rating nan')
            #sales quant
            try:
                func.wait(driver, 1, sales_quantity_elem)
                sale_q = func.get_elem(driver, sales_quantity_elem, elem_type = 'sale_q')
            except Exception as e:
                print(f'sale_q except: {threading.current_thread().name} - {type(e).__name__}')
                sale_q = np.nan
                print('sale_q nan')
            #full_info
                
            info, describe, seller, seller_star, seller_reviews_quantity = func.get_elem(driver, 
                                                                                                        info_elem, 
                                                                                                        (title_elem, detail_info_elem, describe_elem), 
                                                                                                        elem_type = 'info_elems')
            features = [prod_link, cate, img, price, discount, sale_q, rating, info, describe, seller, seller_star, seller_reviews_quantity]
            page_features.append(features)
        que.put(page_features)


    @staticmethod
    def wrangling(col, delimiter = None):
        if col.name == 'product_link'\
                or col.name == 'image'\
                    or col.name == 'describe'\
                        or col.name == 'seller'\
                            or col.name == 'seller_star':
            result = col

        elif col.name == 'category':
            x = []
            for i in col:
                if isinstance(i, str):
                    i = ast.literal_eval(i).split(delimiter)
                elif isinstance(i, list):
                    i = i[0].split(delimiter)
                else:
                    i = [np.nan, np.nan, np.nan]
                x.append(i)
            name = []
            detail_cate = []
            large_cate = []
            for i in x:
                name.append(i[-1])
                detail_cate.append(i[-2])
                large_cate.append(i[-3])

            result = pd.DataFrame({'name': name, 'detail_cate': detail_cate, 'large_cate': large_cate})

        elif col.name == 'price':
            prices = []
            for i in col:
                try:
                    p = int(re.sub(r'[^0-9]', '', i))
                except:
                    p = np.nan
                prices.append(p)
            result = pd.Series(prices, name = col.name)

        elif col.name == 'discount':
            discounts = []
            for i in col:
                try:
                    d = float(i.replace('%', ''))/ 100
                except:
                    d = np.nan
                discounts.append(d)
            result = pd.Series(discounts, name = col.name)

        elif col.name == 'sale_quantity':
            c = []
            for i in col:
                try:
                    x = float(''.join(re.findall(r'\d', i)))
                except:
                    x = np.nan
                c.append(x)
            result = pd.Series(c, name = col.name)

        elif col.name == 'rating':
            rating_star = []
            rating_quantity = []
            for i in col:
                try:
                    rs, rq = i.split(delimiter)
                    rs = float(re.sub(r'[^0-9]', '', rs)) / 10
                    rq = int(re.sub(r'[^0-9]', '', rq))
                except:
                    rs, rq = np.nan, np.nan
                rating_star.append(rs)
                rating_quantity.append(rq)
            result = pd.DataFrame({'rating_star': rating_star, 'rating_quantity': rating_quantity})

        elif col.name == 'info':
            col = [ast.literal_eval(i) if isinstance(i, str) else i for i in col]
            col_name = []
            for i in col:
                if not isinstance(i, float):
                    for v in i:
                        if v[0] not in col_name:
                            col_name.append(v[0])
            di = {i: [] for i in col_name}
            processed = []
            for i in col:
                try:
                    info_i = []
                    for v in i:
                        info_i.append(v[0])
                    lack = [i for i in di.keys() if i not in info_i]
                    for l in lack:
                        i.append([l, np.nan])
                except:
                    i = [[k, np.nan] for k in di.keys()]
                processed.append(i)
            for i in processed:
                for v in i:
                    di[v[0]].append(v[1])

            result = pd.DataFrame(di)

        elif col.name == 'seller_reviews_quantity':
            result = []
            for i in col:
                try:
                    cleaned_str = re.sub(r'[^\d.ktr]', '', i)
                    cleaned_str = cleaned_str.replace('k', '000').replace('tr', '000000')
                    i = float(cleaned_str)
                except:
                    i = np.nan
                result.append(i)
            result = pd.Series(result, name = col.name)
        else:
            col = col

        return result.reset_index(drop = True)


class TikiCrawler(func):
    def __init__(self, root_link, n_browers, 
                 prod_link_elem, category_bar_elem, image_elem, 
                 price_elem, discount_elem,
                 sales_quantity_elem, rating_elem, 
                 info_elem, detail_info_elem, 
                 describe_elem,
                 extend_page_elem,
                 title_elem,
                 preventive_prod_link_elem,
                 all_data = None,
                 wrangled_data = None,
                 be_wrangled = None):
        self.root_link = root_link
        self.n_browers = n_browers
        self.idx_page = [i for i in range(1, n_browers + 1)]
        self.que = Queue()
        self.prod_link_elem = prod_link_elem
        self.preventive_prod_link_elem = preventive_prod_link_elem
        self.category_bar_elem = category_bar_elem
        self.image_elem = image_elem
        self.price_elem = price_elem
        self.discount_elem = discount_elem
        self.sales_quantity_elem = sales_quantity_elem
        self.rating_elem = rating_elem
        self.info_elem = info_elem
        self.detail_info_elem = detail_info_elem
        self.describe_elem = describe_elem
        self.extend_page_elem = extend_page_elem
        self.title_elem = title_elem
        self.all_data = all_data
        self.wrangled_data = wrangled_data
        self.be_wrangled = be_wrangled
    
    def open_drivers(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("user-agent=Mozilla/5.0")
        chrome_options.add_argument('--disable-software-rasterizer')
        chrome_options.add_argument('--disable-extensions')
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['timeouts'] = {
            "implicit": 120,
            "pageLoad": 240,
            "script": 240
        }
        chrome_options.set_capability('timeouts', capabilities['timeouts'])
        self.drivers = [
            
            webdriver.Remote(
                command_executor='http://chrome:4444/wd/hub',
                options=chrome_options

            ) for _ in range(self.n_browers)
        ]
        print('success open driver')


    def load_multi_browers(self):
        print('da vao load multi broswer')
        for driver, page in zip(self.drivers, self.idx_page):
            t = threading.Thread(target = func.load_multi_page, args = (driver, page, self.root_link))
            t.start()

    def run(self):
        threads = []
        for driver in self.drivers:
            print('--Running--')
            t = threading.Thread(target = func.get_data, 
                                 args = (driver, self.que, self.prod_link_elem, 
                                         self.category_bar_elem, self.image_elem, 
                                         self.price_elem, self.discount_elem,
                                         self.sales_quantity_elem, self.rating_elem, 
                                         self.info_elem, self.detail_info_elem, 
                                         self.describe_elem, self.extend_page_elem,
                                         self.title_elem, self.preventive_prod_link_elem))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        results = []
        while not self.que.empty():
            results.extend(self.que.get())
        return results
    
    def crawl_multipage(self, page_crawl = 3):
        self.all_data = pd.DataFrame()
        i = 1
        while self.idx_page[0] < page_crawl:
            print(f'--------------------------------------PHARSE {i}--------------------------------------')
            self.open_drivers()
            self.load_multi_browers()
            sleep(0.5)
        
            all_features = self.run()
            page_df = pd.DataFrame(
                all_features,
                columns = ['product_link', 'category', 'image', 'price', 
                           'discount', 'sale_quantity', 'rating', 
                           'info', 
                           'describe', 'seller', 'seller_star', 
                           'seller_reviews_quantity']
            )
            self.all_data = pd.concat([self.all_data, page_df], axis = 0)
            self.idx_page = [i + self.n_browers for i in self.idx_page]
            self.close()
            i += 1

        
    def wrangling_data(self, delimiter = None):
        data = []
        if self.all_data.empty:
            print("No data collected.")
            self.wrangled_data = None
        else:
            for col in self.all_data.columns:
                part = func.wrangling(self.all_data[col], delimiter)
                data.append(part)
            concat_data = pd.concat(data, axis = 1)
            self.wrangled_data = concat_data.drop_duplicates(subset = ['name']).reset_index(drop = True)
            self.be_wrangled = True
    
    def close(self):
        for driver in self.drivers:
            driver.quit()


    def save(self, pickle_file_path):
        save_dict = {k: v  for k, v in self.__dict__.items() if k not in ['que', 'drivers', 'idx_page']}
        with open(pickle_file_path, 'wb') as file:
            pickle.dump(save_dict, file)

    @classmethod
    def load(cls, pickle_file_path):
        with open(pickle_file_path, 'rb') as file:
            data_dict = pickle.load(file)
        return cls(**data_dict)


# class SubCrawler:
#     crawlers = []
#     def __init__(self, name, core):
#         self.name = name
#         self.core = core
#         self.done = False
#         self.error = False

#     @classmethod
#     def get_crawlers(cls, TikiCrawlerObj, sub_link_elem, preventive_sub_link_elem):
#         temp_drive = webdriver.Chrome()
#         temp_drive.get(TikiCrawlerObj.root_link)
#         try:
#             func.wait(temp_drive, 100, sub_link_elem)
#             sub_link_elem = temp_drive.find_elements(By.CSS_SELECTOR, sub_link_elem)
#         except:
#             func.wait(temp_drive, 100, preventive_sub_link_elem)
#             sub_link_elem = temp_drive.find_elements(By.CSS_SELECTOR, preventive_sub_link_elem)
#         info = [(i.text, i.get_attribute('href')) for i in sub_link_elem]
#         for name, link in info:
#             core = TikiCrawler(
#                 link,
#                 TikiCrawlerObj.n_browers,
#                 TikiCrawlerObj.prod_link_elem, 
#                 TikiCrawlerObj.category_bar_elem, TikiCrawlerObj.image_elem, 
#                 TikiCrawlerObj.price_elem, TikiCrawlerObj.discount_elem,
#                 TikiCrawlerObj.sales_quantity_elem, TikiCrawlerObj.rating_elem, 
#                 TikiCrawlerObj.info_elem, TikiCrawlerObj.detail_info_elem, 
#                 TikiCrawlerObj.describe_elem, TikiCrawlerObj.extend_page_elem,
#                 TikiCrawlerObj.title_elem, TikiCrawlerObj.preventive_prod_link_elem
#             )
#             subcrawler = SubCrawler(name, core)
#             cls.crawlers.append(subcrawler)
#         temp_drive.close()

#     @classmethod
#     def super_crawling(cls, n_page):
#         for i in cls.crawlers:
#             try:
#                 i.core.crawl_multipage(n_page)
#                 i.done = True
#             except:
#                 i.error = True

def extract_tiki_data():
    crawler = TikiCrawler(
        root_link="https://tiki.vn/sach-truyen-tieng-viet/c316",
        n_browers=2,
        prod_link_elem = '.style__ProductLink-sc-1axza32-2.ezgRFw.product-item',
        category_bar_elem=".breadcrumb",
        image_elem=".image-frame",
        price_elem=".product-price__current-price",
        discount_elem=".product-price__discount-rate",
        sales_quantity_elem = '.styles__StyledQuantitySold-sc-1onuk2l-3.eWJdKv',
        rating_elem = '.styles__StyledReview-sc-1onuk2l-1.dRFsZg',
        info_elem = '.WidgetTitle__WidgetContainerStyled-sc-12sadap-0.bufoOo',
        detail_info_elem = '.WidgetTitle__WidgetContentStyled-sc-12sadap-2.hNNYbU',
        describe_elem = '.style__Wrapper-sc-6as7kb-0.eba-dki.content',
        extend_page_elem = '.btn-more',
        title_elem = '.WidgetTitle__WidgetTitleStyled-sc-12sadap-1.bPRVIq',
#sub_link_elem will be used for crawl detail category in root_link you put
        # sub_link_elem = '.styles__TreeItemStyled-sc-1uq9a9i-2.ThXqv a',
        preventive_prod_link_elem = '.style__ProductLink-sc-139nb47-2.cKoUly.product-item'
        # preventive_sub_link_elem = '.item.item--category'
    )
    # Chạy crawler để lấy dữ liệu từ nhiều trang
    crawler.crawl_multipage(page_crawl=5) 

    # Xử lý dữ liệu thu thập được
    crawler.wrangling_data(delimiter = '\n')
    # Lưu dữ liệu ra file pickle
    # crawler.save('./data/tiki_data.pkl')
    if crawler.wrangled_data is not None:
        crawler.wrangled_data.to_csv('./data/tiki_data.csv', index=False)
    else:
        print("crawler.wrangled_data is None, cannot save to CSV.")
