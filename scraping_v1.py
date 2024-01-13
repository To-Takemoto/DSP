import requests, re, time
from bs4 import BeautifulSoup

class ScrapigHandler:
    def __init__(self) -> None:
        pass

    def format_date(self, num) -> str:
        num = str(f"{num:02}")
        return num
        
    def delete_space(self, passed :str) -> str:
        passed = passed.replace(" ","")
        passed = re.sub(r"\n","",passed)
        passed = re.sub(r"\r","",passed)
        passed = re.sub(r"\xa0","",passed)
        return passed
        
    def req_soup(self, date :dict) -> BeautifulSoup:
        year = date["year"]
        month = self.format_date(date["month"])
        date = self.format_date(date["day"])
        try:
            res = requests.get(f"https://tenki.jp/past/{year}/{month}/{date}/weather/3/16/")
            if res.status_code == 200:
                soup = BeautifulSoup(res.text, 'html.parser')
                return soup
            else:
                print("対象ページがエラーっぽい…日付間違えてないか再度確認を")
                return
        except:
            print("対象ページにアクセスできないっぽい…")
            return
    
    def get_info(self, soup) -> dict:
        date = soup.select_one("#main-column > section > section:nth-child(7) > h3 > span")
        date = self.delete_space(date.text)

        tennki = soup.select_one("#past-live-area-pref-list-entries > tr:nth-child(2) > td.weather-telop-entry")
        tennki = self.delete_space(tennki.text)

        saikoukionn = soup.select_one("#past-live-area-pref-list-entries > tr:nth-child(2) > td.max-temp-entry")
        saikoukionn = self.delete_space(saikoukionn.text)

        saiteikionn = soup.select_one("#past-live-area-pref-list-entries > tr:nth-child(2) > td.min-temp-entry")
        saiteikionn = self.delete_space(saiteikionn.text)

        kousuiryou = soup.select_one("#past-live-area-pref-list-entries > tr:nth-child(2) > td.precip-entry")
        kousuiryou = self.delete_space(kousuiryou.text)
        
        data = {"date":date, "tennki":tennki, "saikoukionn":saikoukionn, "saiteikionn":saiteikionn, "kousuiryou":kousuiryou}
        return data


    def run(self, date_dic :dict) -> dict:
        time.sleep(0.5)
        soup = self.req_soup(date_dic)
        if soup:
            data = self.get_info(soup)
            return data