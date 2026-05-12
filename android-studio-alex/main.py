import json
import urllib.request
from bs4 import BeautifulSoup

url_to_fetch = "https://developer.android.com/studio"
req = urllib.request.Request(url_to_fetch, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as response:
    page_content = response.read().decode('utf-8')

soup = BeautifulSoup(page_content, 'html.parser')
download_table = soup.find("table", class_="download")
output_data = {}

if download_table:
    rows = download_table.find("tbody").find_all("tr") if download_table.find("tbody") else download_table.find_all("tr")
    for row in rows[1:]:
        columns = row.find_all("td")
        platform = columns[0].get_text(separator=" ").strip()
        if "Linux" in platform:
            button = columns[1].find("button")
            if not button:
                continue
            file_name = button.get_text(strip=True)
            file_size = columns[2].get_text(strip=True)
            sha_checksum = columns[3].get_text(strip=True)

            # Extract the download URL from the modal dialog link
            dialog_id = button.get("data-modal-dialog-id", "")
            download_link = soup.find("a", id=f"agree-button__{dialog_id}")
            url = download_link.get("href", "") if download_link else ""

            # Extract version from the URL path (e.g., .../ide-zips/2025.3.2.6/...)
            version = url.split("/")[-2] if url else file_name.split("-")[2]

            output_data = {
                "platform": platform,
                "version": version,
                "url": url,
                "fsize": file_size,
                "sha256": sha_checksum
            }

if output_data:
    print(json.dumps(output_data, indent=4))
else:
    print("Linux download data not found.")
