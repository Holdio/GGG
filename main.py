from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from collections import defaultdict
from urllib.parse import urljoin
from curl_cffi import requests
from datetime import datetime
import pandas as pd
import traceback
import random
import json
import time
import uuid
import re

options = uc.ChromeOptions()
options.add_argument("--window-size=1280,800")
# options.add_argument("--incognito")
options.add_argument(
    f"--user-data-dir=/tmp/chrome-test-{uuid.uuid4()}"
)

driver = uc.Chrome(version_main=149, options=options)
shoes = []

locations = [
    {"Name": "Plano", "ID": "5478"},
    {"Name": "Dallas", "ID": "4455"},
    {"Name": "Oklahoma City", "ID": "4442"},
    {"Name": "Fayetteville", "ID": "5482"},
    {"Name": "Olathe", "ID": "4432"},
    {"Name": "Mesa", "ID": "4450"},
    {"Name": "Upland", "ID": "5498"},
    {"Name": "Naperville", "ID": "5430"},
    {"Name": "Orland Park", "ID": "4431"},
    {"Name": "Fairview Heights", "ID": "5494"},
    {"Name": "Avon", "ID": "4414"},
    {"Name": "Greenwood", "ID": "5451"},
]

urls = [
    {"link": "https://www.dickssportinggoods.com/p/hoka-womens-arahi-8-running-shoes-25fhqwrh8whtwhtxxftw/25fhqwrh8whtwhtxxftw?enteredSearchTerm=26801974",
    "color": "Pink/Pink"
     },
    {"link": "https://www.dickssportinggoods.com/p/hoka-mens-gaviota-5-running-shoes-23fhqmgvt5nmbscldmns/23fhqmgvt5nmbscldmns?sku=24484409",
    "color": "Black/White"
     },
    {
    "link": "https://www.dickssportinggoods.com/p/on-womens-the-roger-clubhouse-shoes-23mazwrgrclbhswhtftw/23mazwrgrclbhswhtftw?sku=26791228",
    "color": "White/Olive"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/new-balance-530-shoes-23nwbw530whtgrnxxftw/23nwbw530whtgrnxxftw?sku=27016877",
    "color": "Linen/Linen"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/hoka-mens-speedgoat-6-gtx-trail-running-shoes-24fhqmspdgt6gtxblmns/24fhqmspdgt6gtxblmns?sku=25758738",
    "color": "Orbit"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/nike-mens-killshot-2-shoes-24nikmkllshtwhtbrmns/24nikmkllshtwhtbrmns?sku=25485815",
    "color": "Sail/Midnight Navy/Gum"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/new-balance-womens-fresh-foam-x-more-v6-running-shoes-25newwrunnmrv6blkgedd/25newwrunnmrv6blkgedd?sku=26844070",
    "color": "Grey/Beige"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/asics-mens-gel-dedicate-8-pickleball-shoes-23asimglddct8pbwhsom/23asimglddct8pbwhsom?sku=25106780",
    "color": "Black/White"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/on-mens-cloudmonster-shoes-22mazmcldmnstrclxmns/22mazmcldmnstrclxmns?sku=26202147",
    "color": "White/Glacier"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/brooks-mens-glycerin-22-running-shoes-24bromglycrn22blkmns/24bromglycrn22blkmns?sku=26092811",
    "color": "Black/Black/Ebony"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/on-mens-the-roger-pro-2-tennis-shoes-24mazmthrgrpr2whtsom/24mazmthrgrpr2whtsom?sku=26215417",
    "color": "White"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/new-balance-womens-550-shoes-25nwbw550whtlghtpftw/25nwbw550whtlghtpftw?sku=27211605",
    "color": "White/Linen"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/hoka-womens-clifton-10-running-shoes-25fhqwclftn10blckftw/25fhqwclftn10blckftw?sku=26801078",
    "color": "Beige/Pink"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/on-mens-cloudsurfer-2-running-shoes-24mazmcldsrfr2blcmns/24mazmcldsrfr2blcmns?sku=26197742",
    "color": "Glacier"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/new-balance-womens-fresh-foam-x-more-v6-running-shoes-25newwrunnmrv6blkgedd/25newwrunnmrv6blkgedd?sku=26843992",
    "color": "Black/Gray"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/nike-mens-cortez-leather-shoes-24nikmcrtzblkwhtxmns/24nikmcrtzblkwhtxmns?sku=26592396",
    "color": "White/ Black"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/on-mens-cloudmonster-shoes-22mazmcldmnstrclxmns/22mazmcldmnstrclxmns?sku=23823551",
    "color": "Black"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/on-womens-cloudsurfer-max-running-shoes-25mazwcldsrfrmxblftw/25mazwcldsrfrmxblftw?sku=26786682",
    "color": "White/Light Blue"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/new-balance-womens-fresh-foam-x-more-v6-running-shoes-25newwrunnmrv6blkgedd/25newwrunnmrv6blkgedd?sku=26844054",
    "color": "White/Green"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/on-womens-cloudsurfer-max-running-shoes-25mazwcldsrfrmxblftw/25mazwcldsrfrmxblftw?sku=26786675",
    "color": "White/Pink"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/nike-womens-air-max-90-shoes-19nikwrmx90whtvltftw/19nikwrmx90whtvltftw?sku=22396320",
    "color": "Wht/Wht/Wht"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/on-mens-the-roger-advantage-shoes-22mazmrgrdvwhtlvxmns/22mazmrgrdvwhtlvxmns?sku=26786319",
    "color": "Wolf/Glacier"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/new-balance-womens-327-shoes-21nwbw327whtgryxxftw/21nwbw327whtgryxxftw?sku=22635454",
    "color": "Rust/Sand"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/nike-womens-pegasus-plus-running-shoes-24nikwpgsstrb4gryrnn/24nikwpgsstrb4gryrnn?sku=26818814",
    "color": "White/Mint"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/on-womens-cloud-6-shoes-24mazwcld6chmbrywftw/24mazwcld6chmbrywftw?sku=26791014",
    "color": "Bliss Orchid"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/nike-mens-shox-nz-running-shoes-25nikmcasushxnzblkbfb/25nikmcasushxnzblkbfb?sku=27211036",
    "color": "White/White"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/on-mens-cloudrock-mid-waterproof-hiking-boots-25mazmmcldrckwpmdfbo/25mazmmcldrckwpmdfbo?sku=26268554",
    "color": "Hunter/Black"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/on-mens-cloudtilt-shoes-23mazmcldtltwhtblmns/23mazmcldtltwhtblmns?sku=26785765",
    "color": "Glacier/Ice"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/nike-womens-pegasus-41-running-shoes-24nikwpgss41whtrdrnn/24nikwpgss41whtrdrnn?sku=26818867",
    "color": "Total Orange/Bordeaux"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/new-balance-kids-grade-school-574-v2-shoes-22nwby574v2grnblybsk/22nwby574v2grnblybsk?sku=27379587",
    "color": "Stone/Burgundy"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/nike-mens-killshot-2-shoes-24nikmkllshtwhtbrmns/24nikmkllshtwhtbrmns?sku=25485818",
    "color": "Sail/Midnight Navy/Gum"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/hoka-mens-mach-6-running-shoes-24fhqmmch6blckwhtmns/24fhqmmch6blckwhtmns?sku=24929504",
    "color": "Black/White"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/nike-womens-pegasus-41-running-shoes-24nikwpgss41whtrdrnn/24nikwpgss41whtrdrnn?sku=27159499",
    "color": "Guava Ice"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/nike-womens-pegasus-41-running-shoes-24nikwpgss41whtrdrnn/24nikwpgss41whtrdrnn?sku=26586280",
    "color": "Linen/White"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/new-balance-womens-fresh-foam-x-more-v6-running-shoes-25newwrunnmrv6blkgedd/25newwrunnmrv6blkgedd?sku=26891229",
    "color": "Peach Nectar"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/asics-mens-novablast-5-running-shoes-24asiwnvblst5blckftw/24asiwnvblst5blckftw?sku=26876962",
    "color": "White/Blue"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/new-balance-womens-327-shoes-21nwbw327whtgryxxftw/21nwbw327whtgryxxftw?sku=26373621",
    "color": "Terracotta Brown"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/new-balance-kids-preschool-530-bungee-shoes-25newycasu530pnkwhcem/25newycasu530pnkwhcem?sku=27751101",
    "color": "Linen"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/on-womens-cloudnova-form-shoes-24mazwcldnvfrm2whftw/24mazwcldnvfrm2whftw?sku=26788933",
    "color": "Truffle/Dew"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/new-balance-kids-grade-school-574-v2-shoes-22nwby574v2grnblybsk/22nwby574v2grnblybsk?sku=27057439",
    "color": "Navy/Pink"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/new-balance-womens-574-shoes-22nwbw574blktlmltftw/22nwbw574blktlmltftw?sku=26373730",
    "color": "Rose Pink"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/asics-superblast-2-running-shoes-24asiasprblst2lkgmns/24asiasprblst2lkgmns?sku=26890107",
    "color": "Blue/Purple"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/new-balance-womens-fresh-foam-x-880v15-running-shoes-24nwbw880v15rflctftw/24nwbw880v15rflctftw?sku=26843804",
    "color": "Grey/Red"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/new-balance-womens-574-shoes-22nwbw574blktlmltftw/22nwbw574blktlmltftw?sku=27016802",
    "color": "Rose Sugar"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/new-balance-480-shoes-23nwbw480whtwhtxxftw/23nwbw480whtwhtxxftw?sku=27215934",
    "color": "Black/White"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/brooks-womens-ghost-17-running-shoes-25browghst17blckbftw/25browghst17blckbftw?sku=26849786",
    "color": "Light Blue/Navy"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/reebok-womens-classic-az-shoes-25rbkwclssczchlkcftw/25rbkwclssczchlkcftw?sku=27161763",
    "color": "Green/Pink"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/reebook-womens-club-c-double-shoes-21rbkwclbcdblchlkftw/21rbkwclbcdblchlkftw?sku=27161735",
    "color": "Chalk/Black"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/asics-womens-gel-nimbus-27-running-shoes-24asiwglnmbs27blcftw/24asiwglnmbs27blcftw?sku=26409197",
    "color": "White/Light Purple"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/new-balance-740-shoes-25newacasu740bsqngbbe/25newacasu740bsqngbbe?sku=26950725",
    "color": "Castlerock"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/brooks-womens-adrenaline-24-running-shoes-24browdrnlngts24lftw/24browdrnlngts24lftw",
    "color": "Black/Black"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/asics-womens-gel-dedicate-8-tennis-shoes-23asiwglddct8whtlftw/23asiwglddct8whtlftw?color=Cream%2FBlue",
    "color": "Cream/Blue"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/hoka-womens-arahi-8-running-shoes-25fhqwrh8whtwhtxxftw/25fhqwrh8whtwhtxxftw?color=Alabaster%2FTangerine%20Glow",
    "color": "Alabaster/Lingonberry"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/nike-mens-pegasus-41-running-shoes-24nikmpgss41vltccrnn/24nikmpgss41vltccrnn?enteredSearchTerm=198486939584",
    "color": "White/Black/Blue"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/brooks-womens-ghost-17-running-shoes-25browghst17blckbftw/25browghst17blckbftw?color=Pink%2FFuschia",
    "color": "White/White/Grey"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/asics-mens-gel-nimbus-27-running-shoes-24asimglnmbs272blmns/24asimglnmbs272blmns?color=Black%2FGrey",
    "color": "Black/Grey"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/nike-mens-pegasus-41-running-shoes-24nikmpgss41vltccrnn/24nikmpgss41vltccrnn?enteredSearchTerm=197593779977",
    "color": "White/White/Pure Platinum"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/new-balance-mens-fuelcell-rebel-v5-running-shoes-25nwbmflcllrblv5wwlk/25nwbmflcllrblv5wwlk?color=Medusa%20Green%2FFaded%20Teal",
    "color": "Mint"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/nike-mens-free-metcon-6-training-shoes-24nikmfrmtcn6blkwprf/24nikmfrmtcn6blkwprf?color=Cannon%2FBlack%2FLight%20Silver",
    "color": "White/Black/Orange"
    },
    {
    "link": "https://www.dickssportinggoods.com/p/asics-mens-gel-dedicate-8-pickleball-shoes-23asimglddct8pbwhsom/23asimglddct8pbwhsom?color=Cream%2FTeal%20Tint",
    "color": "Cream/Teal Tint"
    }
]


session = requests.Session()

all_items = []

# ---------- GROUP COLORS BY PRODUCT PAGE ----------
grouped_products = defaultdict(list)

for item in urls:

    base_url = item["link"].split("?")[0]

    grouped_products[base_url].append({
        "color": item["color"],
        "original_url": item["link"]
    })

# ---------- SCRAPE EACH PRODUCT PAGE ONCE ----------
for base_url, targets in grouped_products.items():

    try:

        print(f"Loading {base_url}")

        driver.get(base_url)

        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located(
                (By.ID, "dcsg-ngx-pdp-server-state")
            )
        )

        time.sleep(random.uniform(8, 10))

        script = driver.find_element(
            By.ID,
            "dcsg-ngx-pdp-server-state"
        )

        raw_json = script.get_attribute("textContent")
        data = json.loads(raw_json)

        product_key = next(
            k for k in data
            if k.startswith("product-url-")
        )

        skus = data[product_key]["productsData"][0]["skus"]

        # Build lookup of desired colors
        target_colors = {
            t["color"].strip().lower(): t
            for t in targets
        }

        # Find images for requested colors
        imgs = driver.find_elements(By.CSS_SELECTOR, "img")

        image_lookup = {}

        for img in imgs:

            alt = img.get_attribute("alt")

            if not alt:
                continue

            alt = alt.strip().lower()

            if alt in target_colors:

                image_lookup[alt] = img.get_attribute("src")

        # Extract matching SKUs
        for sku in skus:

            try:

                attrs = {
                    a["name"]: a["value"]
                    for a in sku["definingAttributes"]
                }

                color = attrs.get(
                    "Color",
                    ""
                ).strip().lower()

                if color not in target_colors:
                    continue

                url = target_colors[color]["original_url"]

                new_sku = sku["partNumber"]

                parsed = urlparse(url)
                query = parse_qs(parsed.query)

                query["sku"] = [new_sku]

                new_url = urlunparse(
                    parsed._replace(query=urlencode(query, doseq=True))
                )

                all_items.append({
                    "Image": f'=IMAGE("{image_lookup.get(color, "")}")',
                    "SKU": new_sku,
                    "Name": sku["name"],
                    "Color": attrs.get("Color"),
                    "Size": attrs.get("Shoe Size"),
                    "URL": new_url
                })

            except Exception as e:
                print(f"SKU parse error: {e}")

    except Exception as e:
        print(f"Exception type: {type(e).__name__}")
        print(f"Exception repr: {repr(e)}")
        traceback.print_exc()

# ---------- DEDUPE SKUS ----------
unique_skus = list({item["SKU"] for item in all_items})


# ---------- HELPER: CHUNK ----------
def chunk(lst, size):
    for i in range(0, len(lst), size):
        yield lst[i:i + size]


# ---------- HEADERS ----------
headers = {
    "accept": "application/json",
    "origin": "https://www.dickssportinggoods.com",
    "referer": "https://www.dickssportinggoods.com/",
    "user-agent": driver.execute_script("return navigator.userAgent"),
    "x-api-key": "pdp-90c1c1ae-1580-11ec-a613-4f5255dd8e74",
    "x-dsg-platform": "v2",
}


# ---------- PHASE 2: INVENTORY LOOKUP ----------
inventory = {}

for location in locations:

    session.cookies.clear()

    for cookie in driver.get_cookies():
        session.cookies.set(cookie["name"], cookie["value"])

    location_name = location["Name"]
    location_id = location["ID"]

    print(f"Checking inventory for {location_name} ({location_id})")

    for sku_chunk in chunk(unique_skus, 40):

        apiUrl = (
            "https://availability.dickssportinggoods.com/v2/inventoryapis/searchinventory"
            f"?location={location_id}&sku={','.join(sku_chunk)}"
        )

        try:
            response = session.get(
                apiUrl,
                headers=headers,
                timeout=30
            )

            if response.status_code != 200:
                print(
                    f"Inventory error for {location_name}: "
                    f"{response.status_code}"
                )
                continue

            data = response.json()

            for item in data.get("data", {}).get("skus", []):

                sku = item["sku"]
                qty = item.get("isaqty", 0)

                if sku not in inventory:
                    inventory[sku] = {}

                inventory[sku][location_name] = qty

            time.sleep(random.uniform(3.5, 5.5))

        except Exception as e:
            print(
                f"Inventory batch error "
                f"({location_name}): {e}"
            )

# ---------- PHASE 3: MERGE RESULTS ----------
for item in all_items:

    sku = item["SKU"]

    for location in locations:

        location_name = location["Name"]

        item[location_name] = (
            inventory
            .get(sku, {})
            .get(location_name, 0)
        )

# ---------- OUTPUT ----------
final_shoe = pd.DataFrame(all_items)

location_columns = [loc["Name"] for loc in locations]

final_shoe = final_shoe[
    ["Image", "SKU", "Name", "Color", "Size", "URL"]
    + location_columns
]

final_shoe = final_shoe.replace("", 0).fillna(0)

datetime_string = datetime.now().strftime("%m-%d-%Y %H:%M")

final_shoe = final_shoe.sort_values(
    by=["Name", "Color", "Size"],
    ascending=[True, True, True]
)

final_shoe.to_csv(
    f"{datetime_string} practice.csv",
    index=False
)

driver.quit()
