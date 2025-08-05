import time
import sys
import os
import re
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import requests
import json

# Add backend to path for database access
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

class ActuaryListScraper:
    def __init__(self, headless=True, max_jobs=50):
        """Initialize the scraper"""
        self.max_jobs = max_jobs
        self.base_url = "https://www.actuarylist.com"
        self.jobs_url = f"{self.base_url}/jobs"
        self.scraped_jobs = []
        
        # Setup Chrome options
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

        # Initialize driver with better error handling
        try:
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
            self.wait = WebDriverWait(self.driver, 10)
            print("Chrome WebDriver initialized successfully!")
        except Exception as e:
            print(f"Error initializing Chrome WebDriver: {e}")
            print("Please make sure Chrome browser is installed and try again.")
            raise
        
    def parse_posting_date(self, date_text):
        """Parse posting date from various formats"""
        if not date_text:
            return datetime.now()
        
        date_text = date_text.lower().strip()
        
        # Handle "X days ago", "X weeks ago", etc.
        if "day" in date_text:
            days_match = re.search(r'(\d+)\s*day', date_text)
            if days_match:
                days = int(days_match.group(1))
                return datetime.now() - timedelta(days=days)
        
        if "week" in date_text:
            weeks_match = re.search(r'(\d+)\s*week', date_text)
            if weeks_match:
                weeks = int(weeks_match.group(1))
                return datetime.now() - timedelta(weeks=weeks)
        
        if "month" in date_text:
            months_match = re.search(r'(\d+)\s*month', date_text)
            if months_match:
                months = int(months_match.group(1))
                return datetime.now() - timedelta(days=months*30)
        
        # Handle "today", "yesterday"
        if "today" in date_text:
            return datetime.now()
        if "yesterday" in date_text:
            return datetime.now() - timedelta(days=1)
        
        # Default to current date if parsing fails
        return datetime.now()
    
    def extract_job_type(self, job_text):
        """Extract job type from job text"""
        job_text_lower = job_text.lower()
        
        if any(word in job_text_lower for word in ['intern', 'internship']):
            return 'Internship'
        elif any(word in job_text_lower for word in ['part-time', 'part time']):
            return 'Part-time'
        elif any(word in job_text_lower for word in ['contract', 'contractor', 'consulting']):
            return 'Contract'
        elif any(word in job_text_lower for word in ['temporary', 'temp']):
            return 'Temporary'
        else:
            return 'Full-time'
    
    def scrape_jobs(self):
        """Main scraping method"""
        try:
            print(f"Starting to scrape jobs from {self.jobs_url}")
            self.driver.get(self.jobs_url)
            
            # Wait for page to load
            time.sleep(3)
            
            # Accept cookies if present
            try:
                cookie_button = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Accept') or contains(text(), 'OK')]"))
                )
                cookie_button.click()
                time.sleep(1)
            except TimeoutException:
                print("No cookie banner found or already accepted")
            
            # Find job listings
            job_count = 0
            page = 1
            
            while job_count < self.max_jobs:
                print(f"Scraping page {page}...")
                
                # Find job cards/listings
                job_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                    ".job-listing, .job-card, .job-item, [class*='job'], .listing-item")
                
                if not job_elements:
                    # Try alternative selectors
                    job_elements = self.driver.find_elements(By.CSS_SELECTOR, 
                        "article, .card, [data-job], .position")
                
                if not job_elements:
                    print("No job elements found. Checking page structure...")
                    # Print page source for debugging (first 1000 chars)
                    print(self.driver.page_source[:1000])
                    break
                
                print(f"Found {len(job_elements)} job elements on page {page}")
                
                for job_element in job_elements:
                    if job_count >= self.max_jobs:
                        break
                    
                    try:
                        job_data = self.extract_job_data(job_element)
                        if job_data:
                            self.scraped_jobs.append(job_data)
                            job_count += 1
                            print(f"Scraped job {job_count}: {job_data['title']} at {job_data['company']}")
                    
                    except Exception as e:
                        print(f"Error extracting job data: {e}")
                        continue
                
                # Try to go to next page
                if job_count < self.max_jobs:
                    if not self.go_to_next_page():
                        break
                    page += 1
                    time.sleep(2)
                else:
                    break
            
            print(f"Scraping completed. Total jobs scraped: {len(self.scraped_jobs)}")
            return self.scraped_jobs

        except Exception as e:
            print(f"Error during scraping: {e}")
            return self.scraped_jobs

        finally:
            self.driver.quit()

    def extract_job_data(self, job_element):
        """Extract job data from a job element"""
        try:
            job_data = {}

            # Extract title
            title_selectors = [
                ".job-title", ".title", "h2", "h3", "h4",
                "[class*='title']", ".position-title", ".job-name"
            ]
            title = self.find_text_by_selectors(job_element, title_selectors)
            if not title:
                return None
            job_data['title'] = title.strip()

            # Extract company
            company_selectors = [
                ".company", ".company-name", ".employer",
                "[class*='company']", ".organization", ".firm"
            ]
            company = self.find_text_by_selectors(job_element, company_selectors)
            if not company:
                company = "Unknown Company"
            job_data['company'] = company.strip()

            # Extract location
            location_selectors = [
                ".location", ".job-location", ".city",
                "[class*='location']", ".address", ".place"
            ]
            location = self.find_text_by_selectors(job_element, location_selectors)
            if not location:
                location = "Remote/Not Specified"
            job_data['location'] = location.strip()

            # Extract posting date
            date_selectors = [
                ".date", ".posted", ".job-date",
                "[class*='date']", ".time", ".posted-date"
            ]
            date_text = self.find_text_by_selectors(job_element, date_selectors)
            job_data['posting_date'] = self.parse_posting_date(date_text)

            # Extract job type
            full_text = job_element.text
            job_data['job_type'] = self.extract_job_type(full_text)

            # Extract tags
            tags_selectors = [
                ".tags", ".skills", ".categories",
                "[class*='tag']", ".keywords", ".labels"
            ]
            tags_text = self.find_text_by_selectors(job_element, tags_selectors)
            if tags_text:
                # Split by common delimiters and clean
                tags = [tag.strip() for tag in re.split(r'[,|•·]', tags_text) if tag.strip()]
                job_data['tags'] = ','.join(tags[:5])  # Limit to 5 tags
            else:
                job_data['tags'] = ''

            # Extract description (if available)
            desc_selectors = [
                ".description", ".job-description", ".summary",
                "[class*='description']", ".details"
            ]
            description = self.find_text_by_selectors(job_element, desc_selectors)
            job_data['description'] = description[:500] if description else ''  # Limit length

            # Extract URL (if available)
            try:
                link_element = job_element.find_element(By.CSS_SELECTOR, "a")
                href = link_element.get_attribute('href')
                if href and href.startswith('http'):
                    job_data['url'] = href
                elif href:
                    job_data['url'] = self.base_url + href
                else:
                    job_data['url'] = ''
            except:
                job_data['url'] = ''

            return job_data

        except Exception as e:
            print(f"Error extracting job data: {e}")
            return None

    def find_text_by_selectors(self, element, selectors):
        """Try multiple CSS selectors to find text"""
        for selector in selectors:
            try:
                found_element = element.find_element(By.CSS_SELECTOR, selector)
                text = found_element.text.strip()
                if text:
                    return text
            except:
                continue
        return None

    def go_to_next_page(self):
        """Navigate to next page"""
        try:
            # Try different next page selectors
            next_selectors = [
                "a[aria-label='Next']",
                ".next", ".pagination-next",
                "a:contains('Next')", "a:contains('>')",
                ".page-next", "[class*='next']"
            ]

            for selector in next_selectors:
                try:
                    next_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if next_button.is_enabled():
                        next_button.click()
                        time.sleep(2)
                        return True
                except:
                    continue

            return False

        except Exception as e:
            print(f"Error navigating to next page: {e}")
            return False

    def save_to_api(self, jobs_data):
        """Save scraped jobs to backend API"""
        api_url = "http://localhost:5000/api/jobs"
        saved_count = 0

        for job in jobs_data:
            try:
                # Convert datetime to string for JSON serialization
                if isinstance(job.get('posting_date'), datetime):
                    job['posting_date'] = job['posting_date'].isoformat()

                response = requests.post(api_url, json=job)

                if response.status_code == 201:
                    saved_count += 1
                    print(f"Saved job: {job['title']} at {job['company']}")
                else:
                    print(f"Failed to save job: {job['title']} - {response.text}")

            except Exception as e:
                print(f"Error saving job {job.get('title', 'Unknown')}: {e}")

        print(f"Successfully saved {saved_count} out of {len(jobs_data)} jobs to database")
        return saved_count

def main():
    """Main function to run the scraper"""
    print("Starting Actuary List Job Scraper...")

    # Initialize scraper
    scraper = ActuaryListScraper(headless=False, max_jobs=50)  # Set headless=True for production

    try:
        # Scrape jobs
        jobs = scraper.scrape_jobs()

        if jobs:
            print(f"\nSuccessfully scraped {len(jobs)} jobs")

            # Save to JSON file as backup
            with open('scraped_jobs.json', 'w') as f:
                # Convert datetime objects to strings for JSON serialization
                jobs_for_json = []
                for job in jobs:
                    job_copy = job.copy()
                    if isinstance(job_copy.get('posting_date'), datetime):
                        job_copy['posting_date'] = job_copy['posting_date'].isoformat()
                    jobs_for_json.append(job_copy)

                json.dump(jobs_for_json, f, indent=2)
            print("Jobs saved to scraped_jobs.json")

            # Save to API
            print("\nSaving jobs to database via API...")
            scraper.save_to_api(jobs)

        else:
            print("No jobs were scraped")

    except Exception as e:
        print(f"Error in main: {e}")

if __name__ == "__main__":
    main()
