import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import json
import re
import time
import random 

# baseurl = 'https://us.peugeot-saveurs.com/en_us/'

headers = {
    'User-Agent': 'Mozilla/5.0'
}

# =========================================
# 🔹 DISABLED: Scraping all product links
# =========================================

# all_links = []
# page = 1

# while True:
#     print(f"Scraping page {page}...")

#     url = f'https://us.peugeot-saveurs.com/en_us/shop-all-mills?p={page}'
#     r = requests.get(url, headers=headers)
#     soup = BeautifulSoup(r.content, 'lxml')

#     products = soup.select('ol.products.list.items.product-items.flex li.item.product.product-item')

#     # Stop if no products found
#     if not products:
#         print("No more products found. Stopping...")
#         break

#     for item in products:
#         a_tag = item.find('a', href=True)
#         if a_tag:
#             full_link = urljoin(baseurl, a_tag['href'])
#             all_links.append(full_link)

#     page += 1

# # Remove duplicates
# all_links = list(set(all_links))

# df = pd.DataFrame(all_links, columns=['product_link'])
# df.to_csv('product_links.csv', index=False)

# print(f"Total links scraped: {len(all_links)}")


# =========================================
# 🔹 ACTIVE: Test SKU Scraper
# =========================================
"""
test_url = "https://us.peugeot-saveurs.com/en_us/line-electric-pepper-mill-electrical-metal-carbon-6in-u-select.html"

def scrape_peugeot_product(url):
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "lxml")

        # 1. SKU (Standard)
        sku_tag = soup.select_one('[itemprop="sku"]')
        sku = sku_tag.get_text(strip=True) if sku_tag else "N/A"

        # 2. Short Description
        desc_tag = soup.select_one('.product-short_description .value.text')
        description = desc_tag.get_text(strip=True) if desc_tag else "N/A"

        # 3. OVERVIEW (The "Hidden Data" Strategy)
        overview = "N/A"
        # We look for a script tag that contains the actual product data in JSON format
        # This is where the text actually lives before the JavaScript moves it to the <p> tags
        script_data = soup.find_all('script', type='text/x-magento-init')
        for script in script_data:
            if 'product_details' in script.text or 'description' in script.text:
                # Use regex to find anything that looks like a description in the background code
                found_text = re.search(r'"content":"(.*?)"', script.text)
                if found_text:
                    raw_html = found_text.group(1).encode().decode('unicode_escape')
                    overview = BeautifulSoup(raw_html, "lxml").get_text().split('.')[0] + "."
                    break
        
        # Fallback for Overview: If JSON fails, grab the first non-empty <p> in the focus section
        if overview == "N/A":
            focus_paragraphs = soup.select('.focus__inner .text p')
            for p in focus_paragraphs:
                text = p.get_text(strip=True)
                if text: # If the paragraph isn't empty
                    overview = text.split('\n')[0]
                    break

        # 4. IMAGE (Matches your screenshot)
        # We target exactly what you showed in image_b5e0c3.png
        image_link = "N/A"
        img_tag = soup.select_one('div.fotorama__stage__frame img.fotorama__img')
        if img_tag:
            image_link = img_tag.get('src')
        else:
            # Pro Fallback: The Social Media tag
            image_meta = soup.find("meta", property="og:image")
            image_link = image_meta["content"] if image_meta else "N/A"

        return {
            "SKU": sku,
            "Brand": "PEUGEOT",
            "Description": description,
            "Overview": overview,
            "Image_URL": image_link
        }

    except Exception as e:
        return {"Error": str(e)}

# --- EXECUTION ---
test_url = "https://us.peugeot-saveurs.com/en_us/line-electric-pepper-mill-electrical-metal-carbon-6in-u-select.html"
data = scrape_peugeot_product(test_url)

print("\nRESULTS:")
for k, v in data.items():
    print(f"{k}: {v}")
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd
import json
import re

# baseurl = 'https://us.peugeot-saveurs.com/en_us/'

headers = {
    'User-Agent': 'Mozilla/5.0'
}

# =========================================
# 🔹 DISABLED: Scraping all product links
# =========================================

# all_links = []
# page = 1

# while True:
#     print(f"Scraping page {page}...")

#     url = f'https://us.peugeot-saveurs.com/en_us/shop-all-mills?p={page}'
#     r = requests.get(url, headers=headers)
#     soup = BeautifulSoup(r.content, 'lxml')

#     products = soup.select('ol.products.list.items.product-items.flex li.item.product.product-item')

#     # Stop if no products found
#     if not products:
#         print("No more products found. Stopping...")
#         break

#     for item in products:
#         a_tag = item.find('a', href=True)
#         if a_tag:
#             full_link = urljoin(baseurl, a_tag['href'])
#             all_links.append(full_link)

#     page += 1

# # Remove duplicates
# all_links = list(set(all_links))

# df = pd.DataFrame(all_links, columns=['product_link'])
# df.to_csv('product_links.csv', index=False)

# print(f"Total links scraped: {len(all_links)}")


# =========================================
# 🔹 ACTIVE: Test SKU Scraper
# =========================================
"""
test_url = "https://us.peugeot-saveurs.com/en_us/line-electric-pepper-mill-electrical-metal-carbon-6in-u-select.html"

def scrape_peugeot_product(url):
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "lxml")

        # 1. SKU (Standard)
        sku_tag = soup.select_one('[itemprop="sku"]')
        sku = sku_tag.get_text(strip=True) if sku_tag else "N/A"

        # 2. Short Description
        desc_tag = soup.select_one('.product-short_description .value.text')
        description = desc_tag.get_text(strip=True) if desc_tag else "N/A"

        # 3. OVERVIEW (The "Hidden Data" Strategy)
        overview = "N/A"
        # We look for a script tag that contains the actual product data in JSON format
        # This is where the text actually lives before the JavaScript moves it to the <p> tags
        script_data = soup.find_all('script', type='text/x-magento-init')
        for script in script_data:
            if 'product_details' in script.text or 'description' in script.text:
                # Use regex to find anything that looks like a description in the background code
                found_text = re.search(r'"content":"(.*?)"', script.text)
                if found_text:
                    raw_html = found_text.group(1).encode().decode('unicode_escape')
                    overview = BeautifulSoup(raw_html, "lxml").get_text().split('.')[0] + "."
                    break
        
        # Fallback for Overview: If JSON fails, grab the first non-empty <p> in the focus section
        if overview == "N/A":
            focus_paragraphs = soup.select('.focus__inner .text p')
            for p in focus_paragraphs:
                text = p.get_text(strip=True)
                if text: # If the paragraph isn't empty
                    overview = text.split('\n')[0]
                    break

        # 4. IMAGE (Matches your screenshot)
        # We target exactly what you showed in image_b5e0c3.png
        image_link = "N/A"
        img_tag = soup.select_one('div.fotorama__stage__frame img.fotorama__img')
        if img_tag:
            image_link = img_tag.get('src')
        else:
            # Pro Fallback: The Social Media tag
            image_meta = soup.find("meta", property="og:image")
            image_link = image_meta["content"] if image_meta else "N/A"

        return {
            "SKU": sku,
            "Brand": "PEUGEOT",
            "Description": description,
            "Overview": overview,
            "Image_URL": image_link
        }

    except Exception as e:
        return {"Error": str(e)}

# --- EXECUTION ---
test_url = "https://us.peugeot-saveurs.com/en_us/line-electric-pepper-mill-electrical-metal-carbon-6in-u-select.html"
data = scrape_peugeot_product(test_url)

print("\nRESULTS:")
for k, v in data.items():
    print(f"{k}: {v}")
"""

baseurl = 'https://peugeotmillsaustralia.com.au'
start_url = 'https://peugeotmillsaustralia.com.au/collections/pepper-mills?page=1'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

baseurl = 'https://peugeotmillsaustralia.com.au'
# Start with a template for the collection URL
collection_url_template = 'https://peugeotmillsaustralia.com.au/collections/pepper-mills?page={}'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

"""def get_all_product_links():
    all_links = []
    page = 1
    
    while True:
        # Construct the URL for the current page
        url = collection_url_template.format(page)
        
        try:
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.content, 'lxml')

            # Identify product headings based on the provided HTML
            product_headings = soup.select('h3.card__heading.h5')
            
            # If no products are found on this page, we've reached the end
            if not product_headings:
                break
            
            page_links_count = 0
            for heading in product_headings:
                a_tag = heading.find('a', href=True)
                if a_tag:
                    full_link = urljoin(baseurl, a_tag['href'])
                    # Avoid duplicates if the site shows same products across pages
                    if full_link not in all_links:
                        all_links.append(full_link)
                        print(full_link)
                        page_links_count += 1
            
            # If a page was loaded but no new links were extracted, stop to prevent infinite loops
            if page_links_count == 0:
                break
                
            page += 1
            
        except Exception as e:
            print(f"Error on page {page}: {e}")
            break

    # Print the final count at the very end
    print(f"\nTotal Links: {len(all_links)}")

# --- EXECUTION ---
get_all_product_links()
"""

'''
# =========================================
# 🔹 CONFIGURATION
# =========================================
baseurl = 'https://peugeotmillsaustralia.com.au'
collection_url_template = 'https://peugeotmillsaustralia.com.au/collections/pepper-mills?page={}'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# =========================================
# 🔹 STEP 1: SCRAPE ALL PRODUCT LINKS
# =========================================
def get_all_product_links():
    all_links = []
    page = 1
    print("--- PHASE 1: FINDING ALL PRODUCT LINKS ---")
    while True:
        url = collection_url_template.format(page)
        try:
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
            soup = BeautifulSoup(r.content, 'lxml')
            
            # Identify products on the page
            product_headings = soup.select('h3.card__heading.h5')
            if not product_headings:
                break
            
            page_links_count = 0
            for heading in product_headings:
                a_tag = heading.find('a', href=True)
                if a_tag:
                    full_link = urljoin(baseurl, a_tag['href'])
                    if full_link not in all_links:
                        all_links.append(full_link)
                        page_links_count += 1
            
            if page_links_count == 0: break
            print(f"Page {page} processed... Found {len(all_links)} links so far.")
            page += 1
            time.sleep(1) 
        except Exception as e:
            print(f"Error on page {page}: {e}")
            break
    return all_links

# =========================================
# 🔹 STEP 2: SCRAPE DETAILS FROM EACH LINK
# =========================================
def scrape_au_product_details(url):
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "lxml")

        product_data = {
            "Product Name": "n/a",
            "SKU": "n/a",
            "Image URL": "n/a",
            "Item Description": "n/a",
            "Color": "n/a",
            "Size": "n/a",
            "Material": "n/a",
            "URL": url
        }

        # 1. Product Name
        title_div = soup.select_one('.product__title')
        if title_div:
            product_data["Product Name"] = title_div.get_text(strip=True)

        # 2. Image URL
        img_tag = soup.select_one('button.global-media-settings img') or \
                  soup.select_one('.product__media img')
        if img_tag:
            img_src = img_tag.get('src') or img_tag.get('data-src')
            if img_src:
                product_data["Image URL"] = urljoin("https:", img_src)

        # 3. Item Description (General Container)
        desc_container = soup.select_one('.product__description.rte.quick-add-hidden')
        if desc_container:
            for script in desc_container(["script", "style"]):
                script.decompose()
            product_data["Item Description"] = desc_container.get_text(strip=True, separator=' ')

        # 4. Specs (SKU, Color, Size, Material)
        specs_container = soup.select_one('ul.metafield-single_line_text_field-array') or \
                          soup.select_one('ul.list-unstyled')

        if specs_container:
            items = specs_container.find_all('li')
            for item in items:
                text = item.get_text(strip=True)
                lower_text = text.lower()
                if "sku:" in lower_text:
                    product_data["SKU"] = text.split(":", 1)[1].strip()
                elif "color:" in lower_text or "colour:" in lower_text:
                    product_data["Color"] = text.split(":", 1)[1].strip()
                elif "size:" in lower_text:
                    product_data["Size"] = text.split(":", 1)[1].strip()
                elif "material:" in lower_text:
                    product_data["Material"] = text.split(":", 1)[1].strip()

        return product_data
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# =========================================
# 🔹 EXECUTION (FULL RUN - NO LIMIT)
# =========================================
# Step 1: Get every product link from the site
all_links = get_all_product_links()

print(f"\nPhase 1 Complete. Total links to process: {len(all_links)}\n")

# Step 2: Iterate through every single link
final_data = []
for i, link in enumerate(all_links):
    print(f"[{i+1}/{len(all_links)}] Scraping: {link}")
    details = scrape_au_product_details(link)
    if details:
        final_data.append(details)
    
    # Random sleep to keep the connection safe (prevents bot detection)
    time.sleep(random.uniform(1.2, 2.5))

# Step 3: Save the final database to CSV
df = pd.DataFrame(final_data)
df.to_csv('peugeot_au_full_inventory.csv', index=False)

print("\nMISSION COMPLETE! Full inventory saved to 'peugeot_au_full_inventory.csv'")
'''
from seleniumbase import Driver
import time
import random
import pandas as pd
from bs4 import BeautifulSoup

def scrape_walmart_links():
    # UC=True helps bypass the initial "Verify you are human" blocks
    driver = Driver(uc=True, headless=False)
    
    all_links = set()
    base_url = "https://www.walmart.com"
    # The template for the Peugeot brand browse pages
    url_template = "https://www.walmart.com/browse/0?facet=brand%3APP+PEUGEOT&seo=0&page={}&affinityOverride=default"
    
    current_page = 1

    try:
        while True:
            print(f"\n--- SCRAPING PAGE {current_page} ---")
            driver.get(url_template.format(current_page))

            # Initial wait for the first page to handle any Captcha manually
            if current_page == 1:
                print("Solve the Captcha if it appears (Waiting 15s)...")
                time.sleep(15)
            else:
                # Random delay between pages to look more like a human
                time.sleep(random.uniform(5, 8))

            # Scroll loop to trigger lazy-loading of all 40+ items on the page
            print(f"Scrolling page {current_page} to load all products...")
            for i in range(8): 
                driver.execute_script(f"window.scrollTo(0, {i * 1000});")
                time.sleep(1)

            # Parse the current page content
            soup = BeautifulSoup(driver.page_source, "html.parser")
            
            # Walmart uses 'link-identifier' for its product grid links
            links = soup.find_all('a', attrs={'link-identifier': True})
            
            new_links_found = 0
            for a in links:
                href = a.get('href')
                # Filter for actual product 'IP' links and clean them of tracking parameters
                if href and '/ip/' in href:
                    full_link = base_url + href.split('?')[0]
                    if full_link not in all_links:
                        all_links.add(full_link)
                        new_links_found += 1
            
            print(f"Captured {new_links_found} new links from Page {current_page}.")

            # STOP CONDITION: If no new links were found, we've hit the end of the results
            if new_links_found == 0:
                print("No more new products found. Finished!")
                break
            
            # Move to next page
            current_page += 1
            
            # Safety break to prevent infinite loops (Walmart results usually cap around page 10-15)
            if current_page > 20:
                break

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        print(f"\nTotal Unique Links Captured: {len(all_links)}")
        # Save results to CSV
        df = pd.DataFrame(list(all_links), columns=["URL"])
        df.to_csv("walmart_peugeot_links.csv", index=False)
        print("Links saved to 'walmart_peugeot_links.csv'")
        driver.quit()

if __name__ == "__main__":
    scrape_walmart_links()