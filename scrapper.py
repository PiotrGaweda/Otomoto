import requests
from bs4 import BeautifulSoup
import pandas as pd

brand = "opel"
model = "astra"

data = []

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}
for page in range(1,159):
    url = f"https://www.otomoto.pl/osobowe/{brand}/{model}?page={page}"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")

    offers = soup.find_all("article")


    for offer in offers:
        name_tag = offer.find("h2")
        price_tag = offer.find("h3")
        link_tag = offer.find("a", href=True)
        mileage_tag = offer.find("dd", attrs={"data-parameter": "mileage"})
        fuel_tag = offer.find("dd", attrs={"data-parameter": "fuel_type"})
        gearbox_tag = offer.find("dd", attrs={"data-parameter": "gearbox"})
        year_tag = offer.find("dd", attrs={"data-parameter": "year"})


        if name_tag and price_tag and link_tag and mileage_tag:
            name = name_tag.get_text(strip=True)
            price = price_tag.get_text(strip=True)
            link = link_tag["href"]
            mileage = mileage_tag.get_text(strip=True)
            fuel = fuel_tag.get_text(strip=True)
            gearbox = gearbox_tag.get_text(strip=True)
            year = year_tag.get_text(strip=True)
            print(f"{name} , {price} zł , {mileage} , {fuel} , {gearbox} , {year}")
        
            data.append({
                "Nazwa": name,
                "Cena": price,
                "Przebieg": mileage,
                "Paliwo": fuel,
                "Skrzynia biegów": gearbox,
                "Rok": year,
            })

df = pd.DataFrame(data)
df.to_excel("otomoto_oferty.xlsx", index=False)
print("Dane pomyślnie zapisane")
