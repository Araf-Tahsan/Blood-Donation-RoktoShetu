from django.core.management.base import BaseCommand
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from blood_availability.models import BloodStock
import time
import logging
import requests
import json

class Command(BaseCommand):
    help = "Scrape blood data from the website"
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--method',
            default='api',
            help='Method to use: "selenium" or "api" (default: api)',
        )
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting the scraping process..."))
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        method = options['method']
        
        if method == 'api':
            self._scrape_using_api(logger)
        else:
            self._scrape_using_selenium(logger)
    
    def _scrape_using_api(self, logger):
        """Scrape blood data directly using the API endpoint"""
        try:
            # Headers to simulate a browser request
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36',
                'Referer': 'https://bbms.dghs.gov.bd/',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest'
            }
            
            # Parameters required by DataTables
            data = {
                'draw': '1',
                'start': '0',
                'length': '100',  # Get up to 100 records
            }
            
            # Make the POST request
            response = requests.post(
                'https://bbms.dghs.gov.bd/data_sync/national_bag/',
                headers=headers,
                data=data
            )
            
            if response.status_code == 200:
                try:
                    json_data = response.json()
                    if 'data' in json_data:
                        rows = json_data['data']
                        logger.info(f"Retrieved {len(rows)} records from API")
                        
                        success_count = 0
                        for row in rows:
                            try:
                                # The API returns a list for each row
                                if len(row) >= 4:
                                    facility_name = row[0].strip()
                                    blood_group = row[1].strip()
                                    bag_number = row[2].strip()
                                    component = row[3].strip()
                                    
                                    # Only create/update if we have valid data
                                    if facility_name and blood_group and bag_number and component:
                                        BloodStock.objects.update_or_create(
                                            facility_name=facility_name,
                                            blood_group=blood_group,
                                            bag_number=bag_number,
                                            defaults={
                                                'component': component,
                                            }
                                        )
                                        success_count += 1
                            except Exception as e:
                                logger.error(f"Error processing row: {e}")
                        
                        self.stdout.write(self.style.SUCCESS(f"API scraping finished. Processed {success_count} records successfully."))
                    else:
                        logger.error("No 'data' field in API response")
                        self.stdout.write(self.style.ERROR("No data found in API response"))
                except json.JSONDecodeError:
                    logger.error("Failed to parse JSON response")
                    self.stdout.write(self.style.ERROR("Failed to parse response as JSON"))
            else:
                logger.error(f"API request failed with status code: {response.status_code}")
                self.stdout.write(self.style.ERROR(f"API request failed with status code: {response.status_code}"))
        
        except Exception as e:
            logger.error(f"An error occurred during API scraping: {e}")
            self.stdout.write(self.style.ERROR(f"An error occurred during API scraping: {e}"))
    
    def _scrape_using_selenium(self, logger):
        """Scrape blood data using Selenium browser automation"""
        # Setup Chrome driver with improved options
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
        
        driver = webdriver.Chrome(service=service, options=options)
        
        try:
            # Navigate directly to main page which contains the table
            driver.get("https://bbms.dghs.gov.bd/")
            logger.info("Main page loaded")
            
            # Take screenshot for debugging
            driver.save_screenshot("page_loaded.png")
            logger.info("Screenshot saved")
            
            # Wait for table to load - using a longer timeout and looking specifically for table rows
            try:
                # First wait for table to be present
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.ID, "example"))
                )
                logger.info("Table with ID 'example' found")
                
                # Then wait for at least one row to appear
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#example tbody tr"))
                )
                logger.info("Table rows loaded")
                
                # Add extra delay to ensure AJAX data is fully loaded
                time.sleep(5)
                
            except Exception as e:
                logger.error(f"Failed to find table or rows: {e}")
                
                # Save page source for debugging
                page_source = driver.page_source
                with open("page_source.html", "w", encoding="utf-8") as f:
                    f.write(page_source)
                logger.info("Page source saved to page_source.html")
                
                self.stdout.write(self.style.ERROR("Failed to find the data table"))
                return
            
            # Get rows from the table
            table = driver.find_element(By.ID, "example")
            rows = table.find_elements(By.CSS_SELECTOR, "tbody tr")
            
            logger.info(f"Found {len(rows)} rows in the table")
            self.stdout.write(self.style.SUCCESS(f"Found {len(rows)} rows in the table"))
            
            # Create a counter for successful records
            success_count = 0
            
            for index, row in enumerate(rows):
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) >= 4:
                        facility_name = cells[0].text.strip()
                        blood_group = cells[1].text.strip()
                        bag_number = cells[2].text.strip()
                        component = cells[3].text.strip()
                        
                        logger.info(f"Row {index}: {facility_name} | {blood_group} | {bag_number} | {component}")
                        
                        # Only create/update if we have valid data
                        if facility_name and blood_group and bag_number and component:
                            BloodStock.objects.update_or_create(
                                facility_name=facility_name,
                                blood_group=blood_group,
                                bag_number=bag_number,
                                defaults={
                                    'component': component,
                                }
                            )
                            success_count += 1
                except Exception as e:
                    logger.error(f"Error processing row {index}: {e}")
            
            self.stdout.write(self.style.SUCCESS(f"Selenium scraping finished. Processed {success_count} records successfully."))
            
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            self.stdout.write(self.style.ERROR(f"An error occurred: {e}"))
        finally:
            driver.quit()
            logger.info("Browser closed")