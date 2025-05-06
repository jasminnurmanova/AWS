# AWS Full-Stack Web Application Deployment

## Project Overview
This project implements a complete web application deployment using AWS cloud services: EC2 for compute, RDS with PostgreSQL for database backend, and S3 for static content hosting. The application allows users to view, add, and delete data from a dataset sourced from Kaggle.

## Architecture
- **Frontend**: Static HTML/CSS/JS files hosted on Amazon S3
- **Backend**: Application server running on Amazon EC2 (Ubuntu) using Python/Flask
- **Database**: PostgreSQL running on Amazon RDS

## Features
- Display data from PostgreSQL database
- Add new data entries to the database
- Delete existing data entries from the database
- Real-time database interaction

## How to Run the Application

### Access the Application
- **Web Interface**: [http://your-s3-bucket-url.s3-website.region.amazonaws.com/index_yourname.html](http://your-s3-bucket-url.s3-website.region.amazonaws.com/index_yourname.html)
- **Backend API**: [http://your-ec2-public-ip:port](http://your-ec2-public-ip:port)

### Local Development Setup
1. Clone this repository:
   ```
   git clone https://github.com/yourusername/webapp_yourname.git
   cd webapp_yourname
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure database connection:
   - Update the database connection string in `app.py` with your RDS endpoint

4. Run the application:
   ```
   python app.py
   ```

## AWS Resources
- **S3 Bucket**: `your-s3-bucket-name` (Static Website Hosting)
- **EC2 Instance**: `your-ec2-instance-id` (Ubuntu with Python/Flask)
- **RDS Database**: `db_yourname` (PostgreSQL)
- **Database Table**: `tbl_yourname_dataset`

## Project Structure
```
webapp_yourname/
├── app.py                 # Backend Flask application
├── requirements.txt       # Python dependencies
├── static/                # Static assets (deployed to S3)
│   ├── css/
│   ├── js/
│   └── index_yourname.html
├── templates/             # Flask templates
└── data/                  # Dataset and import scripts
```

## Technologies Used
- AWS (EC2, RDS, S3)
- Python/Flask
- PostgreSQL
- HTML/CSS/JavaScript
