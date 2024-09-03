from bs4 import BeautifulSoup
import requests
import pandas as pd

# List of website URLs to scrape
websites = [
    "https://blackswan.ch/detail/A32BBF",
    "https://blackswan.ch/detail/A1180D",
    "https://blackswan.ch/detail/A97DF6",
    "https://blackswan.ch/detail/A88D8D",
    "https://blackswan.ch/detail/4D239E",
    "https://blackswan.ch/detail/E06457",
    "https://blackswan.ch/detail/A04B0A",
    "https://blackswan.ch/detail/A951D6",
    "https://blackswan.ch/detail/A8945D",
    "https://blackswan.ch/detail/A19985"
]

# Initialize a list to hold the results
results = []

# Loop through each website in the list
for website in websites:
    result = requests.get(website)
    content = result.text

    # Parse the HTML content using BeautifulSoup with lxml parser
    soup = BeautifulSoup(content, "lxml")

    # Find the specific article by ID
    box = soup.find("article", id="post-721")

    if box:
        # Scrape the 'registration' span
        registration = box.find("div",style="font-weight: bold; font-size:20px;").get_text()

        # Scrape the first 'div' with class 'tooltip' and get the first six characters, capitalized
        hex_all = box.find("div", class_="tooltip").get_text()
        hex_value = hex_all[:6].upper()

        # Scrape the third 'div' with class 'nicebox'
        all_nicebox = box.find_all("div", class_="nicebox")
        if len(all_nicebox) > 2:  # Ensure there are at least 3 nicebox divs
            third_nicebox = all_nicebox[2]  # Access the third 'nicebox' div

            # Find the third 'div' inside the third 'nicebox'
            all_div = third_nicebox.find_all("div")
            if len(all_div) > 3:  # Ensure there are at least 3 divs inside
                last_div = all_div[3].get_text()  # Get the text of the third div
            else:
                last_div = "Inner div not found"
        else:
            last_div = "Outer div not found"

        # Store the results for this website
        results.append({
            "Website": website,
            "Registration": registration,
            "Hex Value": hex_value,
            "Last Seen": last_div
        })

# Convert the results to a DataFrame
df = pd.DataFrame(results)

# Define the filename with today's date
filename = "scraping_results_hex.xlsx"

# Write the DataFrame to an Excel file
df.to_excel(filename, index=False)

print(f"Results have been written to {filename}")
