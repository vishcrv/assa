# assa - automated searching scrolling agent

## Overview
an automated browser tool that searches the web and scrolls through websites with real-time keyboard controls. Built with Selenium WebDriver, Rich terminal UI, and multi-engine search fallbacks.

---

## Setup Instructions

### 1. Clone the Repository
```sh
git clone https://github.com/vishcrv/assa.git
cd assa
```

### 2. Create and Activate Python Environment
```sh
# Using venv (recommended)
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Install Chrome Browser
Ensure Google Chrome is installed on your system:
- **Windows**: Download from [chrome.google.com](https://chrome.google.com)
- **Linux**: 
  ```sh
  # Ubuntu/Debian
  sudo apt update && sudo apt install google-chrome-stable
  
  # CentOS/RHEL
  sudo yum install google-chrome-stable
  ```

---

## Running the Application

### Basic Usage
```sh
python main.py "search term"
```

### Fast Demo Mode (Recommended for Testing)
```sh
python main.py --fast "test"
```

---

## Terminal Screenshots

### Application Startup
<img width="1360" height="715" alt="image" src="https://github.com/user-attachments/assets/b5940738-c2d4-4434-b3dc-4b8d761bf88d" />



### Main Interface
<img width="1365" height="720" alt="image" src="https://github.com/user-attachments/assets/b32b8015-26e3-4f13-af0b-7e7677ff10b1" />


### Session Summary
<img width="1365" height="716" alt="image" src="https://github.com/user-attachments/assets/ffd54c3f-cf9d-40b7-bfb5-3ab4d3df29d9" />


---

## Controls

| Key | Action |
|-----|--------|
| `1` | Slow scrolling speed |
| `2` | Medium scrolling speed |
| `3` | Fast scrolling speed |
| `p` | Pause/Resume scrolling |
| `n` | Skip to next website |
| `b` | Go to previous website |
| `q` | Quit application |

---

## Dependencies

### Core Packages
```
selenium>=4.15.0    # Browser automation
keyboard>=0.13.5    # Global hotkey detection
rich>=13.7.0        # Terminal UI components
```

### System Requirements
- **Python**: 3.8+
- **Chrome Browser**: Latest version
- **ChromeDriver**: Auto-managed by Selenium

---

## Project Structure
```
assa/
├── main.py              # Entry point
├── agent/
│   ├── __init__.py
│   ├── agent.py         # Main browser controller
│   ├── scroller.py      # Scrolling logic
│   ├── dashboard.py     # Terminal UI
│   └── tracker.py       # Session tracking
├── requirements.txt     # Dependencies
└── README.md
```

---

## Search Engine Fallbacks
The application uses multiple search engines with automatic fallbacks:

1. **DuckDuckGo** (Primary) - Fast, no CAPTCHA
2. **Bing** (Fallback) - More lenient than Google
3. **Google** (Last Resort) - May encounter CAPTCHAs
4. **Demo Sites** (Final Fallback) - Popular websites for testing

---

## Troubleshooting

### Chrome Driver Issues
```sh
# Update Chrome to latest version
# ChromeDriver is managed automatically by Selenium 4.x
```

### Permission Errors (Linux)
```sh
# Grant execute permissions
chmod +x main.py

# If keyboard access issues
sudo python main.py "search term"
```

### Module Not Found Errors
```sh
# Ensure virtual environment is activated
pip install -r requirements.txt

# Check installation
pip list | grep -E "(selenium|keyboard|rich)"
```

### Browser Won't Start
- **Windows**: Ensure Chrome is installed in default location
- **Linux**: Install Chrome using package manager
- **All Systems**: Close existing Chrome instances

### Keys Not Responding
- Ensure terminal window has focus
- Try running with administrator/sudo privileges
- Press keys once (avoid rapid pressing)

---

## Platform-Specific Notes

### Windows
- Run in PowerShell or Command Prompt
- May require administrator privileges for global hotkeys
- Chrome typically installed in `C:\Program Files\Google\Chrome\`

### Linux
- Requires X11 display server for GUI
- May need `sudo` for keyboard access
- Install Chrome via package manager for best compatibility

### macOS
- Install Chrome from official website
- Grant accessibility permissions if prompted
- Use Terminal.app or iTerm2

---
