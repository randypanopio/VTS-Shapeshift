import subprocess, webbrowser, sys

def open_url_browser(url):
    if sys.platform == 'darwin':    # in case of OS X
        subprocess.Popen(['open', url])
    else:
        webbrowser.open_new_tab(url)