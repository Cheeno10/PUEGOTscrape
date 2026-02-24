import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
import json
import os  # Add this at the very top of your script with the other imports

def get_spec_value(soup, spec_name):
    h3_tag = soup.find('h3', string=lambda text: text and spec_name in text)
    if h3_tag:
        span_tag = h3_tag.find_next('span')
        if span_tag:
            return span_tag.get_text(strip=True)
    return f"{spec_name} not found"

def scrape_walmart_undetected(url):
    options = uc.ChromeOptions()
    driver = uc.Chrome(options=options)
    
    scraped_data = None
    
    try:
        print("Bypassing bot protection...")
        driver.get(url)
        
        # Add a human-like pause to let the page settle
        time.sleep(3) 

        try:
            print("Looking for 'More details' button...")
            more_details_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[aria-label="More details"]'))
            )
            # Use JavaScript click to ensure it triggers correctly
            driver.execute_script("arguments[0].click();", more_details_btn)
            print("Clicked! Waiting for specs to load...")
            time.sleep(2) 
        except Exception as e:
            print("No 'More details' button found or it was already open.")

        # Grab the updated HTML after clicking
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        
        image_tag = soup.find('img', {'data-testid': 'hero-image'})
        image_link = image_tag.get('src') if image_tag else "Image link not found"
        
        overview_text = "Overview not found"
        all_dangerous_divs = soup.find_all('div', class_='dangerous-html mb3')
        for div in all_dangerous_divs:
            text = div.get_text(strip=True)
            if "Peugeot Tidore" in text or "nutmeg" in text.lower():
                overview_text = text
                break
                
        # JSON-LD Fallback for Overview
        if overview_text == "Overview not found":
            seo_script = soup.find('script', {'data-seo-id': 'schema-org-product'})
            if seo_script:
                try:
                    seo_data = json.loads(seo_script.string)
                    overview_text = seo_data.get('description', 'Overview not found in JSON')
                except json.JSONDecodeError:
                    pass

        size = get_spec_value(soup, "Size")
        material = get_spec_value(soup, "Material")
        weight = get_spec_value(soup, "Weight")

        scraped_data = {
            "Product URL": url,
            "Image Link": image_link,
            "Overview": overview_text,
            "Size": size,
            "Material": material,
            "Weight": weight
        }

    except Exception as e:
        print(f"An error occurred during scraping: {e}")

    finally:
        # This safely swallows the annoying Windows Handle error on exit
        try:
            driver.quit()
        except OSError:
            pass # Ignore the WinError 6
            
    return scraped_data

if __name__ == "__main__":
    test_link = "https://www.walmart.com/ip/Peugeot-Tidore-Nutmeg-Gringer-and-Mill-Clear/190537224?classType=REGULAR"
    data = scrape_walmart_undetected(test_link)
    
    if data:
        print("\n--- Scraped Data ---")
        print(json.dumps(data, indent=4))
        
    # Force a clean, immediate exit without triggering the buggy Windows garbage collector
    os._exit(0)