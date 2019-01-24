# proxy-tool

This multi-threaded proxy tool will quickly scrape proxies and check them against https://www.google.com for response .
Working proxies will be saved into a new file which is named by the current date for an easy daily proxy scraping .

```
usage : proxy_tool.py
```
<b>Additional flags:</b>
```
[-u] [--url] - the url to check proxies against       # default https://www.google.com
[-m] [--max] - maximum proxies to scrape              # default 800
[-t] [--timeout] - set proxy timeout limit            # default 8
[-st] [--set-threads] - set number of thread to run   # default 30
```

<b> Requirements: </b>
```
bs4
requests
```
