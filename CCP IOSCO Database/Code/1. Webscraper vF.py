import requests
import time
from bs4 import BeautifulSoup
from urllib.parse import urljoin, unquote_plus
import os
import re
import zipfile
import io
start_time = time.time()
def clean_filename(filename):
    invalid_chars = "<>:*?\"|\\/"
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    return unquote_plus(filename)  

def download_and_extract_zip(zip_content, download_dir, filename_prefix=""):
    with zipfile.ZipFile(io.BytesIO(zip_content)) as thezip:
        for zipinfo in thezip.infolist():
            extracted_filename = clean_filename(zipinfo.filename)
            final_path = os.path.join(download_dir, f"{filename_prefix}{extracted_filename}")
            thezip.extract(zipinfo, download_dir)
            os.rename(os.path.join(download_dir, zipinfo.filename), final_path)
            print(f"File extracted and saved as: {final_path}")

def download_files(url, download_dir, company_name):
    company_folder = os.path.join(download_dir, company_name)
    os.makedirs(company_folder, exist_ok=True)
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    base_url_for_downloads = url
    if 'kdpwccp.pl' in url:
        base_url_for_downloads = 'https://www.kdpwccp.pl/'
    elif 'ecc.de' in url:
        base_url_for_downloads = 'https://www.ecc.de/'

    
    links = soup.find_all("a", href=True)

   
    if 'skdd-ccp.hr' in url:
        pattern = re.compile(r'IOSCO \d{4} Q[1-4]')
        links = [link for link in links if pattern.search(link.text)]
    
    for link in links:
        href = link.get("href")
        if "xlsx" in href or "zip" in href or 'skdd-ccp.hr' in url:
            absolute_url = urljoin(base_url_for_downloads, href)
            
            time.sleep(3)
            
            head_response = requests.head(absolute_url)
            content_length = head_response.headers.get('Content-Length')
            
            if content_length and int(content_length) > 3145728:  # Skip if over 3 MB to reduce script time
                print(f"File skipped due to size limit: {absolute_url} (Size: {content_length} bytes)")
                continue
            
            file_size_message = "Size: {content_length} bytes" if content_length else "Size unknown, assumed to fit"
            filename = f"{clean_filename(link.text)}.xlsx" if 'skdd-ccp.hr' in url else clean_filename(href.split("/")[-1])
            download_path = os.path.join(company_folder, filename)
            
            if not os.path.exists(download_path):
                print(f"Downloading: {absolute_url} ({file_size_message})")
                try:
                    file_response = requests.get(absolute_url, stream=True)
                    if "zip" in filename:
                        print(f"ZIP file detected. Downloading and extracting: {filename}")
                        download_and_extract_zip(file_response.content, company_folder)
                    else:
                        with open(download_path, "wb") as file:
                            for chunk in file_response.iter_content(chunk_size=3145728):
                                file.write(chunk)
                        print(f"File downloaded: {filename}")
                except requests.RequestException as e:
                    print(f"Download failed for {absolute_url}: {e}")
            else:
                print(f"File already exists: {filename}")


specific_folder = r"C:\{Your Path}\CCP IOSCO Database\Raw Data"

#Nasdaq,Keler and Athex can not be scraped via Beautiful Soup.
urls_and_companies = [
    
    
    ("https://clear.cboe.com/europe/resources/documentation/public_disclosures/", "CBOE Clear"),
    ("https://www.kdpwccp.pl/en/cpmi-iosco-principles-for-financial-market-infrastructures.html", "KDPW"),
    ("https://www.eurex.com/ec-en/find/about-us/regulatory-standards", "Eurex AG"),
    ("https://www.euronext.com/en/post-trade/euronext-clearing/about/statistics", "Euronext"),
    ("https://www.lch.com/resources/ccp-disclosures", "LCH"),
    ("https://www.ecc.de/en/downloads", "European Commodity Clearing"),
    #("https://www.kelerkszf.hu/Dokumentumt%C3%A1r/CPMI%20IOSCO%20K%C3%B6zz%C3%A9t%C3%A9telek/", "Keler"),
    ("https://www.ccpa.at/downloads/downloads-allgemeines/", "CCP Austria"),
    ("https://www.bmeclearing.es/ing/Regulations/CPMI-IOSCO","BME Clearing"),
    ("https://www.omiclear.pt/en/periodic-reports","OMI Clearing"),
    ("https://www.ice.com/clearing/quarterly-clearing-disclosures", "ICE Clear"),
    #("https://www.athexgroup.gr/stocks1/-/asset_publisher/3BuDj4DceKYP/content/ypochreose-demosiopoieses?controlPanelCategory=portlet_101_INSTANCE_3BuDj4DceKYP","Athex"),
    ("https://www.skdd-ccp.hr/portal/f?p=100:1", "SKDD"),
    #("https://www.nasdaq.com/solutions/about-nasdaq-clearing", "NASDAQ")
    
]

for url, company in urls_and_companies:
    download_files(url, specific_folder, company)

print(f"The script took {time.time() - start_time:.2f} seconds to be completed.")
