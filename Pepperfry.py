import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re


# Function to scrape data for a given page
def scrape_page(page_number, csv_writer):
    url = f"https://www.pepperfry.com/category/dining-sets.html?cat_id=" \
          f"27&requestPlatform=web&sort_field=sorting_score&sort_by=desc&type=hamburger-clp&page={page_number}"
    values = []
    mydriver.get(url)
    time.sleep(5)
    images = mydriver.find_elements(By.XPATH,
                                    '//*[@class="pf-col xs-6 sm-3 clip-product-card-wrapper '
                                    'marginBottom-12 ng-star-inserted"]//*[@class="product-card-top marginBottom-8"]')

    for img in images:
        try:
            # Scroll to the element
            mydriver.execute_script("arguments[0].scrollIntoView();", img)

            # Click on the image
            img.click()
            time.sleep(4)

            # Switch to the new window or tab
            new_window = mydriver.window_handles[-1]
            mydriver.switch_to.window(new_window)

            # Wait for the price element on the new page
            price_element = WebDriverWait(mydriver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@class="text-xxl font-bold ng-tns-c165-1"]'))
            ).text

            sales = WebDriverWait(mydriver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@class="vip-product-rating-count color-tertiary ng-star-inserted"]'))
            ).text

            sales_numeric = int(re.search(r'\d+', sales).group())
            price_numeric = int(re.sub(r'[^\d.]', '', price_element))

            label_elements = mydriver.find_elements(By.XPATH, '//*[@class="vip-product-details-label font-bold"]')
            value_elements = mydriver.find_elements(By.XPATH, '//*[@class="vip-product-details-value font-medium"]')

            # Initialize variables to store product details
            product_details = {"Brand": None,
                               "Color": None,
                               "Collections": None,
                               "Assembly":None,
                               # "Dimensions(in cm)":None,
                               # "Dimensions(in inches)":None,
                               "Warranty":None,
                               "Primary material":None,
                               "Top material":None,
                               "Seating height":None,
                               "Weight":None,
                               "Sku":None,
                               "Room type": None,
                               "Price": None,
                               "Sales": None,
                               "H" : None,
                               "W" : None,
                               "D" : None}

            # Iterate through label and value elements to collect product details
            for label_element, value_element in zip(label_elements, value_elements):
                label = label_element.text.strip()
                value = value_element.text.strip()
                # print(label)
                # print(value)
                # Check if the label is "Brand" and append the corresponding value; otherwise, append None
                if label.lower() == "brand":
                    product_details["Brand"] = value
                elif label.lower() == "colour":
                    product_details["Color"] = value
                # elif label.lower() == "collections":
                #     product_details["Collections"] = value
                # elif label.lower() == "assembly":
                #     product_details["Assembly"] = value
                # elif label.lower() == "dimensions (in centimeters)":
                #     product_details["Dimensions(in cm)"] = value
                elif label.lower() == "dimensions (in inches)":
                    product_details["Dimensions(in inches)"] = value
                elif label.lower() == "primary material":
                    product_details["Primary material"] = value

                elif label.lower() == "product rating":
                    product_details["Product rating"] = value
                # elif label.lower() == "room type":
                #     product_details["Room type"] = value
                elif label.lower() == "top material":
                    product_details["Top material"] = value
                elif label.lower() == "warranty":
                    warranty_element = value
                    warranty_numeric = int(re.search(r'\d+', warranty_element).group())
                    product_details["Warranty"] = warranty_numeric

                elif label.lower() == "seating height":
                    product_details["Seating height"] = value

                elif label.lower() == "dimensions (in centimeters)":
                    # Extract and format dimensions data
                    dimensions_data = value.split(';')
                    # print(dimensions_data)
                    tab_dim = dimensions_data[0]
                    tab = tab_dim.strip().split(' ')
                    # print(tab)
                    for ele in range(len(tab)):
                        if tab[ele] == "H":
                            product_details["H"] = tab[ele+1]
                        elif tab[ele] == "W":
                            product_details["W"] = tab[ele+1]
                        elif tab[ele] == "D":
                            product_details["D"] = tab[ele+1]

            product_details["Price"] = price_numeric
            product_details["Sales"] = sales_numeric
            row = [
                product_details["Brand"],
                # product_details["Assembly"],
                # product_details["Collections"],
                product_details["Color"],
                # product_details["Dimensions(in cm)"],
                # product_details["Dimensions(in inches)"],
                product_details["Primary material"],
                product_details["Product rating"],
                # product_details["Room type"],
                product_details["Seating height"],
                product_details["Top material"],
                product_details["Warranty"],
                # product_details["Weight"],
                # product_details["Sku"],
                product_details["Price"],
                product_details["Sales"],
                product_details["H"],
                product_details["W"],
                product_details["D"],
            ]

            csv_writer.writerow(row)
            print(row)
        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Close the new window or tab
            if len(mydriver.window_handles) > 1:
                mydriver.close()

            # Switch back to the main window if there are still open handles
            if mydriver.window_handles:
                mydriver.switch_to.window(mydriver.window_handles[0])

    # Write data to CSV file
    csv_writer.writerows(values)


# Initialize WebDriver
mydriver = webdriver.Chrome()


# Open CSV file for writing
csv_filename = "final1.csv"
with open(csv_filename, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    # header = ["Brand", "Color", "Dimensions", "Price", "Sales"]
    header = ["Brand", "Color",
              "Primary material", "Rating", "Seating height", "Top material",
              "Warranty", "Price", "Sales", "Height", "Weight", "Depth"]
    csv_writer.writerow(header)

    # Iterate through pages from 1 to 15
    for page_number in range(3, 16):
        scrape_page(page_number, csv_writer)

# Close the browser
mydriver.quit()