#!/usr/bin/env python3
"""
News Headlines Web Scraper
Scrapes top headlines from news websites and saves them to a text file.
"""

import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import os

class NewsHeadlineScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_bbc_news(self):
        """Scrape headlines from BBC News"""
        url = "https://www.bbc.com/news"
        headlines = []
        
        try:
            print(f"Fetching headlines from BBC News...")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # BBC uses various selectors for headlines
            selectors = [
                'h2[data-testid="card-headline"]',
                'h3[data-testid="card-headline"]',
                'h2.sc-4fedabc7-3',
                'h3.sc-4fedabc7-3',
                '.gs-c-promo-heading__title',
                '[data-testid="card-headline"]'
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                for element in elements:
                    headline = element.get_text(strip=True)
                    if headline and len(headline) > 10:  # Filter out very short text
                        headlines.append(headline)
            
            # Remove duplicates while preserving order
            seen = set()
            unique_headlines = []
            for headline in headlines:
                if headline not in seen:
                    seen.add(headline)
                    unique_headlines.append(headline)
            
            return unique_headlines[:20]  # Return top 20 headlines
            
        except requests.RequestException as e:
            print(f"Error fetching BBC News: {e}")
            return []
    
    def scrape_india_today(self):
        """Scrape headlines from India Today"""
        url = "https://www.indiatoday.in"
        headlines = []
        
        try:
            print(f"Fetching headlines from India Today...")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # India Today headline selectors
            selectors = [
                '.detail h2 a',
                '.detail h3 a',
                '.story__headline a',
                '.catagory-listing h2 a',
                '.catagory-listing h3 a',
                'h2.heading a',
                'h3.heading a',
                '.B1S3_content__wrap__9mSB6 h2 a',
                '.B1S3_content__wrap__9mSB6 h3 a',
                'a[data-vars-link-name]'
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                for element in elements:
                    headline = element.get_text(strip=True)
                    if headline and len(headline) > 10 and 'Advertisement' not in headline:
                        headlines.append(headline)
            
            # Remove duplicates
            seen = set()
            unique_headlines = []
            for headline in headlines:
                if headline not in seen:
                    seen.add(headline)
                    unique_headlines.append(headline)
            
            return unique_headlines[:15]  # Return top 15 headlines
            
        except requests.RequestException as e:
            print(f"Error fetching India Today: {e}")
            return []
    
    def scrape_ndtv(self):
        """Scrape headlines from NDTV"""
        url = "https://www.ndtv.com"
        headlines = []
        
        try:
            print(f"Fetching headlines from NDTV...")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # NDTV headline selectors
            selectors = [
                '.news_Itm h2 a',
                '.news_Itm h3 a',
                '.story-list h2 a',
                '.story-list h3 a',
                '.main-news h2 a',
                '.main-news h3 a',
                '.story__title a',
                '.story-title a',
                'h2.story-title a',
                'h3.story-title a',
                '.story_overlay h2 a',
                '.story_overlay h3 a'
            ]
            
            for selector in selectors:
                elements = soup.select(selector)
                for element in elements:
                    headline = element.get_text(strip=True)
                    if headline and len(headline) > 10 and 'Advertisement' not in headline:
                        headlines.append(headline)
            
            # Remove duplicates
            seen = set()
            unique_headlines = []
            for headline in headlines:
                if headline not in seen:
                    seen.add(headline)
                    unique_headlines.append(headline)
            
            return unique_headlines[:20]  # Return top 20 headlines
            
        except requests.RequestException as e:
            print(f"Error fetching NDTV: {e}")
            return []
    
    def save_headlines_to_file(self, headlines, filename="news_headlines.txt"):
        """Save headlines to a text file"""
        try:
            # Get current working directory
            import os
            current_dir = os.getcwd()
            full_path = os.path.join(current_dir, filename)
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            print(f"📁 Attempting to save file to: {full_path}")
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"News Headlines - Scraped on {timestamp}\n")
                f.write("=" * 50 + "\n\n")
                
                for i, headline in enumerate(headlines, 1):
                    f.write(f"{i:2d}. {headline}\n")
                
                f.write(f"\n\nTotal Headlines: {len(headlines)}\n")
            
            # Verify file was created
            if os.path.exists(filename):
                file_size = os.path.getsize(filename)
                print(f"\n" + "="*60)
                print(f"🎉 FILE SUCCESSFULLY SAVED! 🎉")
                print(f"="*60)
                print(f"📄 File Name: {filename}")
                print(f"📂 Full Path: {full_path}")
                print(f"📊 File Size: {file_size} bytes")
                print(f"📰 Headlines Count: {len(headlines)}")
                print(f"="*60)
                
                # Show file contents preview
                print(f"\n📖 File Content Preview:")
                print("-" * 40)
                with open(filename, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f):
                        if i < 4:
                            print(f"   {line.strip()}")
                        else:
                            break
                print("-" * 40)
                print(f"💡 TIP: Look for '{filename}' in your VS Code Explorer panel!")
            else:
                print(f"❌ ERROR: File was not created at {full_path}")
            
        except PermissionError:
            print(f"❌ PERMISSION ERROR: Cannot write to {filename}")
            print("💡 Try running VS Code as administrator or save to a different location")
            
            # Try saving to desktop as backup
            try:
                import os
                desktop = os.path.join(os.path.expanduser("~"), "Desktop")
                backup_file = os.path.join(desktop, filename)
                print(f"🔄 Trying to save to Desktop: {backup_file}")
                
                with open(backup_file, 'w', encoding='utf-8') as f:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    f.write(f"News Headlines - Scraped on {timestamp}\n")
                    f.write("=" * 50 + "\n\n")
                    
                    for i, headline in enumerate(headlines, 1):
                        f.write(f"{i:2d}. {headline}\n")
                    
                    f.write(f"\n\nTotal Headlines: {len(headlines)}\n")
                
                print(f"✅ Backup saved to Desktop: {backup_file}")
                
            except Exception as backup_error:
                print(f"❌ Backup save also failed: {backup_error}")
                
        except IOError as e:
            print(f"❌ FILE I/O ERROR: {e}")
            print("💡 Possible solutions:")
            print("   • Check if the folder exists and you have write permissions")
            print("   • Try closing any programs that might be using the file")
            print("   • Run VS Code as administrator")
            
        except Exception as e:
            print(f"❌ UNEXPECTED ERROR: {e}")
            print("💡 Please check your file system permissions")
    
    def scrape_all_sources(self):
        """Scrape headlines from multiple sources"""
        all_headlines = []
        sources = []
        
        # Scrape BBC News
        bbc_headlines = self.scrape_bbc_news()
        if bbc_headlines:
            all_headlines.extend([f"[BBC] {headline}" for headline in bbc_headlines])
            sources.append(f"BBC News: {len(bbc_headlines)} headlines")
        
        time.sleep(1)  # Be respectful with requests
        
        # Scrape India Today
        india_today_headlines = self.scrape_india_today()
        if india_today_headlines:
            all_headlines.extend([f"[India Today] {headline}" for headline in india_today_headlines])
            sources.append(f"India Today: {len(india_today_headlines)} headlines")
        
        time.sleep(1)  # Be respectful with requests
        
        # Scrape NDTV
        ndtv_headlines = self.scrape_ndtv()
        if ndtv_headlines:
            all_headlines.extend([f"[NDTV] {headline}" for headline in ndtv_headlines])
            sources.append(f"NDTV: {len(ndtv_headlines)} headlines")
        
        return all_headlines, sources

def main():
    """Main function to run the news scraper"""
    print("🗞️  News Headlines Web Scraper")
    print("=" * 40)
    
    scraper = NewsHeadlineScraper()
    
    try:
        # Scrape headlines from all sources
        headlines, sources = scraper.scrape_all_sources()
        
        if headlines:
            print(f"\n📊 Scraping Summary:")
            for source in sources:
                print(f"   • {source}")
            
            # Create filename with timestamp
            filename = f"news_headlines_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            print(f"\n💾 Saving headlines to: {filename}")
            
            # Save headlines to file
            scraper.save_headlines_to_file(headlines, filename)
            
            # Display first few headlines
            print(f"\n📰 Preview of scraped headlines:")
            for i, headline in enumerate(headlines[:5], 1):
                print(f"   {i}. {headline}")
            
            if len(headlines) > 5:
                print(f"   ... and {len(headlines) - 5} more headlines")
                
            # Additional file location info
            import os
            current_dir = os.getcwd()
            print(f"\n" + "🔍" * 20)
            print(f"📁 YOUR FILE IS SAVED HERE:")
            print(f"🔍" * 20)
            print(f"📂 Folder: {current_dir}")
            print(f"📄 File: {filename}")
            print(f"💻 How to find it:")
            print(f"   1. Look in VS Code Explorer (left panel)")
            print(f"   2. Or open File Explorer and go to above folder")
            print(f"   3. Or double-click the file in VS Code to open it")
            print(f"🔍" * 20)
                
        else:
            print("❌ No headlines were scraped. Please check your internet connection.")
            print("🔍 This could happen if:")
            print("   • Internet connection is slow or unavailable")
            print("   • News websites have changed their structure")
            print("   • Websites are blocking automated requests")
            
    except KeyboardInterrupt:
        print("\n⚠️  Scraping interrupted by user")
    except Exception as e:
        print(f"❌ An error occurred: {e}")
        print("💡 Try running the script again or check your internet connection")

if __name__ == "__main__":
    main()