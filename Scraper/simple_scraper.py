import requests
from datetime import datetime
import time

def create_sample_actuarial_jobs():
    """Create sample actuarial jobs that simulate scraped data"""
    
    # Sample jobs that simulate what would be scraped from actuarylist.com
    scraped_jobs = [
        {
            "title": "Actuarial Analyst - Life Insurance",
            "company": "Metropolitan Life Insurance",
            "location": "New York, NY",
            "job_type": "Full-time",
            "tags": "Life Insurance, Valuation, Excel, VBA",
            "description": "Join our actuarial team to support life insurance product development and pricing. Entry-level position perfect for recent graduates.",
            "url": "https://www.actuarylist.com/job/12345"
        },
        {
            "title": "Senior Health Actuary",
            "company": "Anthem Inc.",
            "location": "Indianapolis, IN",
            "job_type": "Full-time", 
            "tags": "Health Insurance, Pricing, Reserving, ASA",
            "description": "Experienced actuary needed for health insurance pricing and reserving. ASA designation required.",
            "url": "https://www.actuarylist.com/job/12346"
        },
        {
            "title": "Property & Casualty Actuary",
            "company": "State Farm Insurance",
            "location": "Bloomington, IL",
            "job_type": "Full-time",
            "tags": "Property & Casualty, Ratemaking, Catastrophe Modeling",
            "description": "Support P&C insurance operations with ratemaking and catastrophe modeling expertise.",
            "url": "https://www.actuarylist.com/job/12347"
        },
        {
            "title": "Actuarial Consultant",
            "company": "Milliman Inc.",
            "location": "Seattle, WA",
            "job_type": "Full-time",
            "tags": "Consulting, Healthcare, Pension, FSA",
            "description": "Consulting opportunity for experienced actuary. Work with diverse clients across multiple practice areas.",
            "url": "https://www.actuarylist.com/job/12348"
        },
        {
            "title": "Actuarial Data Scientist",
            "company": "Lemonade Insurance",
            "location": "New York, NY",
            "job_type": "Full-time",
            "tags": "Data Science, Machine Learning, Python, R, InsurTech",
            "description": "Combine traditional actuarial skills with modern data science techniques in a fast-growing InsurTech company.",
            "url": "https://www.actuarylist.com/job/12349"
        },
        {
            "title": "Reinsurance Actuary",
            "company": "Munich Re America",
            "location": "Princeton, NJ",
            "job_type": "Full-time",
            "tags": "Reinsurance, Treaty Pricing, Capital Modeling",
            "description": "Join our reinsurance team to support treaty pricing and capital modeling initiatives.",
            "url": "https://www.actuarylist.com/job/12350"
        },
        {
            "title": "Actuarial Summer Intern",
            "company": "Prudential Financial",
            "location": "Newark, NJ",
            "job_type": "Internship",
            "tags": "Internship, Student, Life Insurance, Annuities",
            "description": "10-week summer internship program for actuarial science students. Gain hands-on experience in life insurance and annuities.",
            "url": "https://www.actuarylist.com/job/12351"
        },
        {
            "title": "Chief Actuary - Startup",
            "company": "NextGen Insurance",
            "location": "Austin, TX",
            "job_type": "Full-time",
            "tags": "Leadership, Startup, Product Development, FSA",
            "description": "Lead actuarial function at innovative insurance startup. Shape the future of insurance products.",
            "url": "https://www.actuarylist.com/job/12352"
        },
        {
            "title": "Pension Actuary",
            "company": "Aon Hewitt",
            "location": "Chicago, IL",
            "job_type": "Full-time",
            "tags": "Pension, Retirement, Employee Benefits, EA",
            "description": "Support pension and retirement benefit consulting for corporate clients. EA designation preferred.",
            "url": "https://www.actuarylist.com/job/12353"
        },
        {
            "title": "Actuarial Manager - Reserving",
            "company": "Travelers Insurance",
            "location": "Hartford, CT",
            "job_type": "Full-time",
            "tags": "Management, Reserving, P&C, FCAS",
            "description": "Lead reserving team for property and casualty insurance operations. Management experience required.",
            "url": "https://www.actuarylist.com/job/12354"
        }
    ]
    
    return scraped_jobs

def save_jobs_to_api(jobs_data):
    """Save scraped jobs to backend API"""
    api_url = "http://localhost:5000/api/jobs"
    saved_count = 0
    failed_count = 0
    
    print(f"📤 Saving {len(jobs_data)} scraped jobs to database...")
    
    for i, job in enumerate(jobs_data, 1):
        try:
            response = requests.post(api_url, json=job)
            
            if response.status_code == 201:
                saved_count += 1
                print(f"✅ [{i}/{len(jobs_data)}] Saved: {job['title']} at {job['company']}")
            else:
                failed_count += 1
                print(f"❌ [{i}/{len(jobs_data)}] Failed: {job['title']} - {response.text}")
                
        except Exception as e:
            failed_count += 1
            print(f"❌ [{i}/{len(jobs_data)}] Error saving {job['title']}: {e}")
        
        # Small delay to avoid overwhelming the API
        time.sleep(0.1)
    
    print(f"\n📊 Scraping Results:")
    print(f"✅ Successfully saved: {saved_count} jobs")
    print(f"❌ Failed to save: {failed_count} jobs")
    print(f"📈 Success rate: {(saved_count/len(jobs_data)*100):.1f}%")
    
    return saved_count

def simulate_web_scraping():
    """Simulate the web scraping process"""
    print("🕷️  Starting Simulated Web Scraping...")
    print("🌐 Target: Actuary List Website (Simulated)")
    print("=" * 60)
    
    # Simulate scraping delay
    print("🔍 Analyzing website structure...")
    time.sleep(1)
    
    print("📄 Loading job listings...")
    time.sleep(1)
    
    print("🔄 Extracting job data...")
    scraped_jobs = create_sample_actuarial_jobs()
    time.sleep(1)
    
    print(f"✅ Successfully scraped {len(scraped_jobs)} job listings!")
    print("\n📋 Sample of scraped jobs:")
    for i, job in enumerate(scraped_jobs[:3], 1):
        print(f"   {i}. {job['title']} at {job['company']} ({job['location']})")
    print(f"   ... and {len(scraped_jobs)-3} more jobs")
    
    return scraped_jobs

def main():
    """Main scraper simulation function"""
    print("🚀 Job Listing Web Scraper - Simulation Mode")
    print("=" * 60)
    
    # Test API connection first
    try:
        response = requests.get("http://localhost:5000/api/health")
        if response.status_code != 200:
            print("❌ Backend API is not accessible. Please ensure backend is running.")
            return
        print("✅ Backend API connection verified")
    except Exception as e:
        print(f"❌ Cannot connect to backend API: {e}")
        print("   Please ensure the backend is running at http://localhost:5000")
        return
    
    print()
    
    # Simulate web scraping
    scraped_jobs = simulate_web_scraping()
    
    print()
    
    # Save to database
    saved_count = save_jobs_to_api(scraped_jobs)
    
    print("\n" + "=" * 60)
    print("🎉 Web Scraping Simulation Complete!")
    print(f"📊 Total jobs processed: {len(scraped_jobs)}")
    print(f"💾 Jobs saved to database: {saved_count}")
    print("\n🌐 View results at: http://localhost:3000")
    print("💡 This simulation demonstrates the scraper's data processing capabilities.")
    print("   For actual web scraping, Chrome WebDriver setup would be required.")

if __name__ == "__main__":
    main()
