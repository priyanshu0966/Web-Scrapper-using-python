# Task 3: Web Scraper for News Headlines

## 📌 Objective
Create a Python-based web scraper that automatically fetches the top headlines from a public news website and saves them to a `.txt` file.

## 🛠️ Tools & Libraries Used
- **Python 3.x**
- **requests** – for sending HTTP requests
- **BeautifulSoup** (from `bs4`) – for parsing and extracting data from HTML

## 🧠 Project Overview
This script scrapes top news headlines by:
1. Fetching the HTML content of a news website using `requests`.
2. Parsing the HTML with `BeautifulSoup` to extract `<h2>` tags or other relevant title elements.
3. Writing the extracted headlines into a `.txt` file for offline access.

## 🚀 How to Run the Script
1. **Install Dependencies** (if not already installed):
   ```bash
   pip install requests beautifulsoup4
