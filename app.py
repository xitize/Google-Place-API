import requests
import time
import csv


class Scraper:
    def __init__(self):
        self.types = []
        with open("./scrap_type.txt") as file:
           for line in file:
               print(line)
               self.types.append(line.replace("\n", "").replace("_", " "))
        print(self.types)

    def scrap_all_types(self):
        with open("./output_d.csv","w",newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name","type","location","address"])
            for x  in self.types:
                print(x)
                data  = self.scrap_type(x)
                writer.writerows(data)
    

    def scrap_type(self,type_select="accounting"):  #scraps the type passed
        GOOGLE_API_KEY = 'GOOGLE_API_KEY_HERE'
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-35.348301,149.243302&radius=3000&keyword={type_select}&key={GOOGLE_API_KEY}"
        print(url)
        res  = requests.get(url)
        print(res.json())
        try:
            next_page_token = res.json()["next_page_token"]
            print("at scrape type : "+next_page_token)
        except:
            next_page_token = None

        results = res.json()["results"]
        first = []
        for r in results:
            geometry = r["geometry"]["location"]
            name  = r["name"]
            address = r["vicinity"]
            data  = [name,type_select,geometry,address]
            print(data)
            first.append(data)

        print("first : ",first)
        next_data = first
        #scrap new_page places
        while(next_page_token!=None):
            data  = self.scrap_type_next_page(type_select,next_page_token)
            print(data)
            next_page_token = data["next_page_token"]
            next_data.extend(data["items"])
    
        print("---------")
        print(len(next_data))
        print(next_data)
    
        return next_data



    def scrap_type_next_page(self,type_select,next_page_token="Aap_uEDczRDOtdgz1X7Fd9pOKm9aVw0hOSsESZiAnWk8XLIDgfHLvXaNC42gTxhK1tHkP50pHcq4WB9vyocZ9rMFjyak83e0FC2XvAXxzQSYA_v_IopSXrwHqOx0mJnb8jUeeF0dTd-kJbq2fgmQTb5oXpp1fw24jW3WUHFvGvbz6EjsaJ8hyW2vJXMuImGRl75ALJpL1AYMeRMOM25OhptB9UfqxeYCxYXfKT67OD7PztEuseIXuKDVJAybbfyEPTcPKWl_y-fpQbPqWWT2GyYgJZzBUGhyKgt7Qmc4k0mAFujJ0paEePfUTGX3Y7EiOOypdplj_IfHiiikootGC2btkf-TsqqCqFKMPReiqyu4t11NslabBkQR9cBzGVZFRWeIDWQuY57ONCrImCecgnRjhl6SMXExPTUR8WsRWmq8TAa6KwsAAmNs1YXeVTbh0UgIyxxWvXKPtU4oR8fQXA5uIsAImD0DTx66NodPJbtpPO8tF9bedsqqwSDu8slHa5rFbRXEKTqEJLH5UVQTUPvfNfeae8bmEm3sJvBuugHgd7HNlLTxouyKLJvEcgEq6-a5Bi1G1fW9e9KFiA4NtNb5V1dd8rQSqgAIirMv4zu6JLEWT-ck9jI1NxFFiViB4jYs_IabVjpLaWCbhxAdhg"):
        time.sleep(5)
        print(next_page_token)
        url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?pagetoken={next_page_token}&key=AIzaSyDC5UvrE0Sq-G8hrscjc1dUrfYIlVdSdAs"
        print(url)
        res  = requests.get(url)
        print(res.json())

        try:
            print(res.json()["next_page_token"])
            next_page_token = res.json()["next_page_token"]
        except:
            next_page_token = None
        
        results = res.json()["results"]
        items = []
        for r in results:
            geometry = r["geometry"]["location"]
            name  = r["name"]
            address = r["vicinity"]
            item  = [name,type_select,geometry,address]
            print(item)
            items.append(item)
        print("next page : ", len(items))
        return {"next_page_token":next_page_token,"items":items}

       
scrapper = Scraper()
scrapper.scrap_all_types()