from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json
import time

def extract_and_save_json(image_range, output_file):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ensures Chrome runs in headless mode
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")
    chrome_options.add_argument("--blink-settings=imagesEnabled=false")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--log-level=3")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--enable-strict-powerful-feature-restrictions")
    chrome_options.add_argument("--enable-features=NetworkService,NetworkServiceInProcess")

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    data_batch = []  # List to store batch of records

    try:
        for image_id in image_range:
            url = f"https://civitai.com/images/{image_id}"
            driver.get(url)
            # Check for 404 by looking for common 404 page elements
            page_not_found_elements = driver.find_elements(By.XPATH, "//title[contains(text(), 'Share your models')]")
            if page_not_found_elements:
                print(f"Page not found for image ID {image_id}, skipping...")
                continue

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "__NEXT_DATA__"))
                )
                time.sleep(1)  # Extra time for loading
                json_data = json.loads(driver.find_element(By.ID, "__NEXT_DATA__").get_attribute('innerHTML'))
                image_info = json_data['props']['pageProps']['trpcState']['json']['queries'][0]['state']['data']
                data_batch.append(image_info)

                # Write to file every 100 records
                if len(data_batch) >= 100:
                    with open(output_file, 'a', encoding='utf-8') as f:
                        for data in data_batch:
                            json.dump(data, f)
                            f.write('\n')
                    print(f"Saved batch ending with image ID {image_id}")
                    data_batch = []  # Reset the batch list

            except Exception as e:
                print(f"Error processing image ID {image_id}: {str(e)}")

        # Write any remaining data in the batch list
        if data_batch:
            with open(output_file, 'a', encoding='utf-8') as f:
                for data in data_batch:
                    json.dump(data, f)
                    f.write('\n')
            print("Saved final batch.")

    finally:
        driver.quit()

# Specify the range of images and the file to save JSON data
image_range = range(1, 10001)  # Adjust this range as needed
output_file = "YOUR_FILE_OUTPUT"

extract_and_save_json(image_range, output_file)
