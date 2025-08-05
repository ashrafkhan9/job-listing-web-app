# Job Listing Web Application

A full-stack job listing web application built with Flask (Python), React (JavaScript), and Selenium for web scraping. This application allows users to view, add, edit, delete, and filter job listings, with data scraped from actuarial job websites.

## 🚀 **Quick Start** (Application is Ready!)

The application is fully built and configured. To run:

1. **Backend**: `cd backend && python app.py` (MySQL database with 17+ jobs)
2. **Frontend**: `cd frontend && npm start` (React app at http://localhost:3000)
3. **Demo Data**: Run `python Scraper/simple_scraper.py` for more sample jobs

**Current Status**: ✅ Fully functional with MySQL database and populated job listings!

## 🚀 Features

### Backend (Flask API)
- **RESTful API** with full CRUD operations
- **Database integration** with SQLAlchemy (PostgreSQL/MySQL support)
- **Advanced filtering and sorting** by job type, location, tags, and search terms
- **Input validation and error handling**
- **CORS enabled** for frontend integration

### Frontend (React)
- **Responsive design** that works on desktop and mobile
- **Job listing display** with clean, professional cards
- **Add/Edit job forms** with validation
- **Delete functionality** with confirmation
- **Real-time filtering and sorting**
- **Search functionality** across titles, companies, and descriptions

### Web Scraper (Selenium)
- **Automated job scraping** from Actuary List website
- **Data extraction** for title, company, location, posting date, job type, and tags
- **Database integration** to populate job listings
- **Error handling** and graceful failures

## 📁 Project Structure

```
Job Listing Web App/
├── backend/
│   ├── app.py                    # Main Flask application
│   ├── config.py                 # Database configuration (MySQL)
│   ├── db.py                     # Database initialization
│   ├── .env                      # Environment variables
│   ├── .env.example              # Environment template
│   ├── models/
│   │   └── job.py                # SQLAlchemy Job model
│   ├── routes/
│   │   └── job_routes.py         # Job API endpoints
│   └── requirements.txt          # Python dependencies
├── Scraper/
│   ├── scrape.py                 # Selenium scraping logic
│   ├── simple_scraper.py         # Simulation scraper (working)
│   ├── test_scraper.py           # API integration tests
│   └── requirements.txt          # Scraper dependencies
├── frontend/
│   ├── public/
│   │   └── index.html            # HTML template
│   ├── src/
│   │   ├── Components,Pages/
│   │   │   ├── AddEditJob.js     # Add and edit jobs
│   │   │   ├── DeleteJob.js      # Delete jobs
│   │   │   ├── FilterSortJob.js  # Filter and sort jobs
│   │   │   └── JobCard.js        # Job display component
│   │   ├── App.js, App.jsx       # Main logic
│   │   ├── App.css               # Styling
│   │   ├── api.js, api.jsx       # Connection with backend
│   │   ├── index.js, index.jsx   # Entry point
│   │   └── .env.example          # Frontend environment template
│   └── package.json              # Node.js dependencies
└── README.md                     # This file
```

## 🛠️ Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 14+
- MySQL database (configured and tested)
- Chrome browser (for actual web scraping - optional)

### 1. Database Setup

#### MySQL (Currently Configured)
```bash
# Create database (no password required for root)
mysql -u root -e "CREATE DATABASE IF NOT EXISTS job_listing_db;"

# Verify database creation
mysql -u root -e "SHOW DATABASES;"
```

#### Alternative: PostgreSQL
```bash
# Install PostgreSQL and create database
createdb job_listing_db

# Create user (optional)
psql -c "CREATE USER your_username WITH PASSWORD 'your_password';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE job_listing_db TO your_username;"
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables (create .env file)
echo "DATABASE_URL=mysql+pymysql://root@localhost:3306/job_listing_db" > .env
echo "FLASK_ENV=development" >> .env
echo "SECRET_KEY=dev-secret-key-change-in-production" >> .env

# Run the application
python app.py
```

The backend will be available at `http://localhost:5000`

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

The frontend will be available at `http://localhost:3000`

### 4. Web Scraper Setup

```bash
# Install scraper dependencies (globally or in virtual environment)
pip install -r Scraper/requirements.txt

# Option 1: Run simulation scraper (recommended for demo)
python Scraper/simple_scraper.py

# Option 2: Test API integration
python Scraper/test_scraper.py

# Option 3: Run actual Selenium scraper (requires Chrome WebDriver)
python Scraper/scrape.py
```

## 📊 API Endpoints

### Jobs
- `GET /api/jobs` - Get all jobs with optional filtering
- `GET /api/jobs/<id>` - Get single job by ID
- `POST /api/jobs` - Create new job
- `PUT /api/jobs/<id>` - Update existing job
- `DELETE /api/jobs/<id>` - Delete job
- `GET /api/jobs/stats` - Get job statistics

### Query Parameters for Filtering
- `job_type` - Filter by job type (Full-time, Part-time, etc.)
- `location` - Filter by location (partial match)
- `tag` - Filter by tag (partial match)
- `search` - Search in title, company, and description
- `sort` - Sort results (posting_date_desc, posting_date_asc, title_asc, etc.)

### Example API Calls
```bash
# Get all full-time jobs
curl "http://localhost:5000/api/jobs?job_type=Full-time"

# Search for Python jobs
curl "http://localhost:5000/api/jobs?search=Python"

# Get jobs sorted by title
curl "http://localhost:5000/api/jobs?sort=title_asc"
```

## 🎯 Usage

### Adding Jobs
1. Click "Add New Job" button
2. Fill in the required fields (Title, Company, Location)
3. Optionally add job type, tags, description, and URL
4. Click "Add Job" to save

### Editing Jobs
1. Click "Edit" button on any job card
2. Modify the fields as needed
3. Click "Update Job" to save changes

### Deleting Jobs
1. Click "Delete" button on any job card
2. Confirm deletion in the popup dialog

### Filtering and Sorting
1. Use the filter controls to narrow down results
2. Search across job titles, companies, and descriptions
3. Sort by date, title, or company name
4. Reset filters to show all jobs

### Web Scraping
1. Ensure the backend is running at `http://localhost:5000`
2. **For demo purposes:** Run `python Scraper/simple_scraper.py` (creates realistic sample data)
3. **For actual scraping:** Run `python Scraper/scrape.py` (requires Chrome WebDriver setup)
4. The scraper will automatically populate the MySQL database with job listings

## 🔧 Configuration

### Environment Variables
Create a `.env` file in the backend directory:

```env
# Current MySQL Configuration
DATABASE_URL=mysql+pymysql://root@localhost:3306/job_listing_db
FLASK_ENV=development
SECRET_KEY=dev-secret-key-change-in-production

# Alternative PostgreSQL Configuration
# DATABASE_URL=postgresql://username:password@localhost/job_listing_db
```

### Database Configuration
The application is currently configured for MySQL:
- **Database:** MySQL 9.2.0
- **Connection:** No password required for root user
- **Database Name:** job_listing_db
- **Driver:** PyMySQL

To switch to PostgreSQL, update the `DATABASE_URL` in `.env` and install `psycopg2-binary`.

## 🚨 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Verify database is running
   - Check connection string in `.env` file
   - Ensure database exists and user has permissions

2. **CORS Errors**
   - Backend includes CORS headers
   - Ensure frontend is running on port 3000
   - Check proxy setting in `frontend/package.json`

3. **Scraper Issues**
   - For demo: Use `python Scraper/simple_scraper.py` (always works)
   - For actual scraping: Ensure Chrome browser is installed and updated
   - Check if website structure has changed
   - Verify backend is running before scraping

4. **Frontend Build Errors**
   - Delete `node_modules` and run `npm install` again
   - Check Node.js version compatibility
   - Ensure all dependencies are installed

5. **MySQL Connection Issues**
   - Verify MySQL service is running
   - Check if database `job_listing_db` exists
   - Ensure no password is set for root user (or update connection string)

6. **"View Original" Button Shows 404**
   - This is expected behavior for demo/sample jobs
   - Sample jobs use placeholder URLs that don't exist
   - For real scraped jobs, URLs would point to actual job postings

## 📝 Notes and Assumptions

- **Database**: Currently configured with MySQL 9.2.0 (17+ jobs populated)
- **Job Types**: Defaults to "Full-time" if not specified during scraping
- **Tags**: Stored as comma-separated strings for simplicity
- **Scraping**: Simulation scraper provides realistic demo data
- **File Structure**: Matches project requirements with `Components,Pages/` folder
- **URLs**: Sample jobs have placeholder URLs (404 expected for "View Original" button)
- **Authentication**: Not implemented as per requirements
- **Testing**: Unit tests not included as per requirements

## ✅ **Implementation Status**

### **Completed Features:**
- ✅ **Backend API**: Complete Flask REST API with CRUD operations
- ✅ **Database**: MySQL 9.2.0 with 17+ populated job listings
- ✅ **Frontend**: Responsive React app with professional UI
- ✅ **Web Scraping**: Simulation scraper + API integration working
- ✅ **File Structure**: Matches project requirements exactly
- ✅ **Filtering & Sorting**: Advanced search and filter capabilities
- ✅ **Error Handling**: Comprehensive validation and error management

### **Technical Stack:**
- **Backend**: Flask 2.3.2, SQLAlchemy 1.4.48, PyMySQL 1.1.0
- **Frontend**: React 18.2.0, Axios for API calls
- **Database**: MySQL 9.2.0 with job_listing_db
- **Scraping**: Selenium 4.15.0, BeautifulSoup4, WebDriver Manager

### **Live Demo:**
- **Frontend**: http://localhost:3000 (React development server)
- **Backend API**: http://localhost:5000 (Flask development server)
- **Database**: MySQL with 17+ actuarial job listings ready for testing

## 🤝 Contributing

This is a take-home project for demonstration purposes. The code is organized for clarity and maintainability, with proper error handling and user feedback throughout the application.

### **Security Notes:**
- ✅ `.env` files are ignored (contains database credentials)
- ✅ `node_modules/` is ignored (large dependency folder)
- ✅ Database files are ignored (local data)
- ✅ Virtual environments are ignored (Python venv)
- ✅ IDE and OS files are ignored

### **After Cloning:**
Anyone cloning your repository will need to:
1. Copy `.env.example` to `.env` and configure database
2. Install dependencies (`pip install -r requirements.txt`, `npm install`)
3. Set up MySQL database
4. Run the application

## 📄 License

This project is created for educational and demonstration purposes.
