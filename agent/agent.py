# ==============================
# agent.py
# controls the flow:
#   - open browser
#   - search google
#   - visit first 5 links
#   - delegate scrolling
#   - track stats
#   - update dashboard
# ==============================


import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import threading   # to run keyboard listener in background
import keyboard    # type: ignore # capture key presses

from agent.scroller import Scroller
from agent.tracker import SessionTracker
from agent.dashboard import Dashboard

class BrowserAgent:
    """
    TODO: class representing the main agent
    Responsibilities:
    - search google
    - manage navigation between links
    - control scrolling state
    - interact with dashboard + tracker
    """

    def __init__(self):
        """
        Initialize webdriver, tracker, dashboard with anti-detection measures
        """
        # setup Chrome options for fast browsing (optimized for speed)
        chrome_options = Options()
        # core performance optimizations
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")  # much faster loading
        chrome_options.add_argument("--no-first-run")
        chrome_options.add_argument("--disable-default-apps")
        chrome_options.add_argument("--disable-background-timer-throttling")
        chrome_options.add_argument("--disable-renderer-backgrounding")
        chrome_options.add_argument("--disable-backgrounding-occluded-windows")
        chrome_options.add_argument("--disable-client-side-phishing-detection")
        chrome_options.add_argument("--disable-sync")
        chrome_options.add_argument("--disable-translate")
        chrome_options.add_argument("--hide-scrollbars")
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--start-maximized") 
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # set preferences for additional stealth ye clocking notif & geoloc
        prefs = {
            "profile.default_content_setting_values": {
                "notifications": 2,  
                "geolocation": 2,     
            }
        }
        chrome_options.add_experimental_option("prefs", prefs)
        
        # random user agents to avoid detection (captcha gng ://)
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        ]
        chrome_options.add_argument(f"--user-agent={random.choice(user_agents)}")
        
        # initialize driver with options
        self.driver = webdriver.Chrome(options=chrome_options)
        
        self.driver.maximize_window()
        
        # execute script to remove webdriver property
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        self.tracker = SessionTracker()
        self.dashboard = Dashboard()
        
        # flags
        self.current_speed = "slow"    
        self.paused = False               
        self.next_site_flag = False       
        self.prev_site_flag = False       
        self.quit_flag = False            


    def search_duckduckgo(self, query: str):
        """
        Fast search using DuckDuckGo (no CAPTCHA, privacy-focused)
        """
        try:
            print("[INFO] Using DuckDuckGo search (faster, no CAPTCHA)")
            self.driver.get(f"https://duckduckgo.com/?q={query.replace(' ', '+')}&ia=web")
            
            # wait for results - DuckDuckGo is much faster ngl
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'article h2 a')))
            
            
            results = self.driver.find_elements(By.CSS_SELECTOR, 'article h2 a')  #chrome h3 a
            
            links = []
            for r in results[:5]:
                try:
                    href = r.get_attribute('href')
                    if href and href.startswith('http') and 'duckduckgo.com' not in href:
                        links.append(href)
                except Exception as e:
                    continue
            
            if links:
                print(f"[SUCCESS] Found {len(links)} valid links from DuckDuckGo")
                return links
            else:
                print("[WARNING] No valid links found on DuckDuckGo")
                return []
                
        except Exception as e:
            print(f"[ERROR] DuckDuckGo search failed: {e}")
            return []
    
    def search_bing(self, query: str):
        """
        Fallback search using Bing (usually more lenient than Google)
        """
        try:
            print("[INFO] Using Bing search as fallback")
            self.driver.get(f"https://www.bing.com/search?q={query.replace(' ', '+')}")
            
           
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h2 a')))
            
          
            results = self.driver.find_elements(By.CSS_SELECTOR, 'h2 a')
            
            links = []
            for r in results[:5]:
                try:
                    href = r.get_attribute('href')
                    if href and href.startswith('http') and 'bing.com' not in href and 'microsoft.com' not in href:
                        links.append(href)
                except Exception as e:
                    continue
            
            if links:
                print(f"[SUCCESS] Found {len(links)} valid links from Bing")
                return links
            else:
                print("[WARNING] No valid links found on Bing")
                return []
                
        except Exception as e:
            print(f"[ERROR] Bing search failed: {e}")
            return []
    
    def search(self, query: str, max_retries: int = 1):
        """
        Fast multi-engine search with fallbacks (DuckDuckGo -> Bing -> Google)
        Prioritizes speed over stealth for better user experience
        """
        # try DuckDuckGo first 
        links = self.search_duckduckgo(query)
        if links:
            return links
        
        # try Bing as fallback
        links = self.search_bing(query)
        if links:
            return links
        
        # last resort fam: simplified Google search (single attempt)
        print("[INFO] Using Google search")
        try:
            self.driver.get(f"https://www.google.com/search?q={query.replace(' ', '+')}")
            
            # quick wait and check for CAPTCHA
            time.sleep(2)
            page_source = self.driver.page_source.lower()
            if "unusual traffic" in page_source or "captcha" in page_source:
                print("[WARNING] Google CAPTCHA detected. Skipping Google search.")
                return []
            
            # quick result extraction
            wait = WebDriverWait(self.driver, 5)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a h3')))
            results = self.driver.find_elements(By.CSS_SELECTOR, 'a h3')
            
            links = []
            for r in results[:5]:
                try:
                    parent = r.find_element(By.XPATH, '..')
                    href = parent.get_attribute('href')
                    if href and href.startswith('http') and 'google.com' not in href:
                        links.append(href)
                except:
                    continue
            
            if links:
                print(f"[SUCCESS] Found {len(links)} valid links from Google")
                return links
                
        except Exception as e:
            print(f"[ERROR] Google search failed: {e}")
        
        # If all searches fail, provide demo links
        print("[WARNING] All search engines failed. Using demo links.")
        return self.get_demo_links()
    

    #testing only -- fast demo mode
    def get_demo_links(self):
        """
        Fallback demo links for testing when search fails
        """
        demo_links = [
            "https://news.ycombinator.com",
            "https://www.bbc.com/news",
            "https://www.reddit.com",
            "https://stackoverflow.com",
            "https://www.wikipedia.org"
        ]
        print(f"[INFO] Using {len(demo_links)} demo websites")
        return demo_links
    
    def run_fast_demo(self, query: str):
        """
        Fast demo mode - skip search, use popular websites directly
        """
        print("\n" + "=" * 60)
        print("         assa - fast mode testing")
        print("=" * 60)
        print(f"[INFO] Demo query: '{query}'")
        print("[INFO] Skipping search, using popular websites...")
        print("[INFO] Starting keyboard listener...")
        print("[INFO] Browser ready!\n")
        
        self.start_keyboard_listener()
        links = self.get_demo_links()
        
        # use same main loop as regular run
        for index, link in enumerate(links, 1):
            if self.quit_flag:
                break

            self.driver.get(link)
            self.tracker.start_site(link)
            scroller = Scroller(self.driver, self.current_speed)

            scrolling_active = True
            while scrolling_active:
                status = "PAUSED" if self.paused else "SCROLLING"
                self.dashboard.show_status(index, len(links), link, self.current_speed, status)

                if self.next_site_flag:
                    self.next_site_flag = False
                    break
                if self.prev_site_flag:
                    self.prev_site_flag = False
                    index = max(0, index - 2)
                    break
                if self.quit_flag:
                    break

                if self.paused:
                    time.sleep(0.1)
                    continue

                scroller.change_speed(self.current_speed)
                can_scroll_more = scroller.scroll_step(self.paused)
                
                if not can_scroll_more:
                    self.dashboard.show_status(index, len(links), link, self.current_speed, "END OF PAGE")
                    time.sleep(2)
                    scrolling_active = False
                    break
                    
                time.sleep(0.002)

            self.tracker.end_site()

        self.dashboard.show_summary(self.tracker.get_summary())
        self.cleanup()

       
       
    def run(self, query: str):
        """
        Main execution loop for browser automation
        1. call search()
        2. iterate through links
        3. open site, scroll with Scroller
        4. record stats with Tracker
        5. update Dashboard
        """
        # show startup message
        print("\n" + "=" * 60)
        print("    automated scrolling search agent - initializing")
        print("=" * 60)
        print(f"[INFO] Search query: '{query}'")
        print("[INFO] Starting keyboard listener...")
        print("[INFO] Launching browser...\n")
        
        self.start_keyboard_listener()
        links = self.search(query)
        for index, link in enumerate(links, 1):
            # 3a. check quit flag before opening
            if self.quit_flag:
                break

            # 3b. open link in selenium driver
            self.driver.get(link)

            # 4. start tracking the site
            self.tracker.start_site(link)

            # 5. initialize scroller for this page
            scroller = Scroller(self.driver, self.current_speed)

            # 6. scrolling loop (step by step)
            scrolling_active = True
            while scrolling_active:
                # 6a. update dashboard with current status
                status = "PAUSED" if self.paused else "SCROLLING"
                self.dashboard.show_status(index, len(links), link, self.current_speed, status)

                # 6b. check flags for next / prev / quit
                if self.next_site_flag:
                    self.next_site_flag = False
                    break
                if self.prev_site_flag:
                    self.prev_site_flag = False
                    index = max(0, index - 2)  # go back one site in loop
                    break
                if self.quit_flag:
                    break

                # 6c. if paused, just wait and continue loop
                if self.paused:
                    time.sleep(0.1)
                    continue

                # 6d. dynamically update scroller speed
                scroller.change_speed(self.current_speed)

                # 6e. perform one scroll step (pass pause state)
                can_scroll_more = scroller.scroll_step(self.paused)
                
                # 6f. if we've reached the end of the page, automatically go to next site
                if not can_scroll_more:
                    self.dashboard.show_status(index, len(links), link, self.current_speed, "END OF PAGE")
                    time.sleep(2)  # Brief pause before moving to next site
                    scrolling_active = False
                    break
                    
                # Small delay to prevent excessive CPU usage
                time.sleep(0.002)

            # 7. end tracking this site
            self.tracker.end_site()

        # 8. after all sites or quit, show final summary
        self.dashboard.show_summary(self.tracker.get_summary())
        
        # 9. cleanup
        self.cleanup()

    def start_keyboard_listener(self):
        """
        Start a background thread to listen for keyboard input:
        - 1,2,3 → change speed
        - p → pause/resume
        - n → next site
        - b → previous site
        - q → quit
        """
        def on_key_event(e):
            # only process key down events to avoid double triggers
            if e.event_type == keyboard.KEY_DOWN:
                if e.name == "1":
                    self.current_speed = "slow"
                elif e.name == "2":
                    self.current_speed = "medium"
                elif e.name == "3":
                    self.current_speed = "fast"
                elif e.name == "p":
                    self.paused = not self.paused
                elif e.name == "n":
                    self.next_site_flag = True
                elif e.name == "b":
                    self.prev_site_flag = True
                elif e.name == "q":
                    self.quit_flag = True

        # use hook instead of on_press for better reliability
        listener_thread = threading.Thread(target=lambda: keyboard.hook(on_key_event), daemon=True) #.on_press(on_key_event)
        listener_thread.start()
    
    def cleanup(self):
        """
        Clean up browser and stop dashboard
        """
        try:
            if hasattr(self, 'driver') and self.driver:
                self.driver.quit()
                print("[INFO] Browser closed successfully")
        except Exception as e:
            print(f"[WARNING] Error closing browser: {e}")
        
        try:
            if hasattr(self, 'dashboard') and self.dashboard and self.dashboard.live:
                self.dashboard.live.stop()
        except Exception as e:
            print(f"[WARNING] Error stopping dashboard: {e}")
