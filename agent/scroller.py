# scroller.py
# handles scrolling logic

from selenium.webdriver.common.action_chains import ActionChains
import time


class Scroller:
    """
    class to handle scrolling actions
    Responsibilities:
    - scroll by step (pixels, delay)
    - support pause/resume
    - change speed dynamically
    """
    SPEEDS = {
        "slow":   (1, 0.025),   # ~40px/sec, relaxed crawl
        "medium": (4, 0.018),   # ~220px/sec, balanced & readable
        "fast":   (15, 0.008)   # ~1900px/sec, smooth glide
    }


    def __init__(self, driver, speed: str = "slow"):
        """
        initialize with driver and default speed
        speed presets: slow / medium / fast
        """
        self.driver = driver
        self.speed = speed
        self.pixels, self.delay = self.SPEEDS.get(speed, self.SPEEDS["medium"])
        

        #initial 
      


        #paused 
        self.paused = False


    def scroll_step(self, paused=False):
        """
        Perform one scroll step and return True if more scrolling is possible
        Args:
            paused: External pause state to override internal paused state
        """
        if paused or self.paused:
            return True  # stay on current page while paused
        
        current_scroll = self.driver.execute_script("return window.pageYOffset")
        page_height = self.driver.execute_script("return document.body.scrollHeight")
        window_height = self.driver.execute_script("return window.innerHeight")
        
        # check if we've reached the bottom
        if current_scroll + window_height >= page_height - 10:  # 10px tolerance
            return False  # reached end of page
        
        # perform scroll
        self.driver.execute_script(f"window.scrollBy(0, {self.pixels});")
        time.sleep(self.delay)
        return True
        
    def start(self):
        """
        Legacy method - begin scrolling until end of page (kept for compatibility)
        """
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        current_height = 0

        while current_height < last_height:
            if not self.paused:
                self.driver.execute_script(f"window.scrollBy(0, {self.pixels});")
                time.sleep(self.delay)
                current_height += self.pixels
                # update last height in case page dynamically loads content
                last_height = self.driver.execute_script("return document.body.scrollHeight")
            else:
                time.sleep(0.1)  # wait while paused

    def pause(self):
        """
        pause scrolling
        """
        self.paused = True
        

    def resume(self):
        """
        resume scrolling
        """
        self.paused = False
        

    def change_speed(self, speed: str):
        """
        update scroll speed on the fly
        """
        if speed in self.SPEEDS:
            self.speed = speed
            self.pixels, self.delay = self.SPEEDS[speed]
        else:
            print(f"Speed '{speed}' not recognized. Using current speed.")

