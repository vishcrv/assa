# ==============================
# tracker.py
# logs sites visited and time spent
# ==============================

import time


class SessionTracker:
    """
    TODO: tracks session stats
    Responsibilities:
    - record start/end time for each site
    - compute total time spent
    - return summary for dashboard
    """

    def __init__(self):
        self.records = []
        self.current_site = None
        self.start_time = None

    def start_site(self, url: str):
        """
        TODO: record start time for a site
        """
        self.current_site = url
        self.start_time = time.time()  # record start time

    def end_site(self):
        """
        TODO: record end time, compute duration
        """
        if self.current_site is None or self.start_time is None:
            return

        end_time = time.time()
        duration = end_time - self.start_time
        minutes = int(duration // 60)
        seconds = int(duration % 60)
        time_str = f"{minutes}m {seconds}s"

        self.records.append({
            "url": self.current_site,
            "time_spent": time_str
        })

        # reset current site
        self.current_site = None
        self.start_time = None

    def get_summary(self):
        """
        TODO: return list of sites + durations
        """
        return self.records
