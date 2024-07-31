import os
import requests
from bs4 import BeautifulSoup
import concurrent.futures  # For multithreading

# Function to check and create the wallpapers directory
def check_path():
    if not os.path.exists("./wallpapers"):
        os.makedirs("./wallpapers")

# Function to request the home page
def req_home_page():
    global ua
    req = requests.get('https://windows10spotlight.com/', headers={'User-Agent': ua})
    return req.text

# Function to request the number of post pages
def req_post_pages(html_content):
    soup = BeautifulSoup(html_content, 'lxml')
    page_nums = []
    for link in soup.find_all('a', class_='page-numbers'):
        try:
            # Remove commas from the number and convert to integer
            page_number = int(link.text.replace(',', ''))
            page_nums.append(page_number)
        except ValueError:
            continue
    return max(page_nums)

# Function to request a single page and extract hrefs
def req_single_page(page):
    global ua
    if page <= 1:
        link = "https://windows10spotlight.com/"
    else:
        link = "https://windows10spotlight.com/page/" + str(page)
    print("Requesting Page " + str(page))
    req = requests.get(link, headers={'User-Agent': ua})
    soup = BeautifulSoup(req.text, 'html.parser')
    links = soup.find_all('a', class_=['anons-thumbnail', 'show'])
    hrefs = [link.get('href') for link in links]
    return hrefs

# Function to get image links from a page
def get_imgs_page(url):
    req = requests.get(url, headers={'User-Agent': ua})
    soup = BeautifulSoup(req.text, 'html.parser')
    img_tags = soup.find_all('img')
    desired_links = []

    for img_tag in img_tags:
        srcset = img_tag.get('srcset', '')
        image_links = srcset.split(',')
        for image in image_links:
            if len(image.strip().split(' ')) == 2:
                url, width = image.strip().split(' ')
                if width == '1920w':
                    desired_links.append(url)
            else:
                continue

    return desired_links

# Function to download and save the image
def download_image(url):
    filename = os.path.basename(url)
    file_path = os.path.join("./wallpapers", filename)
    try:
        req = requests.get(url, headers={'User-Agent': ua}, timeout=10)
        if req.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(req.content)
            print(f"Downloaded and saved: {filename}")
        else:
            print(f"Failed to download: {url} - Status code: {req.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Exception occurred while downloading {url}: {e}")

# Main execution
if __name__ == '__main__':
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"

    check_path()
    home_page = req_home_page()
    pages = req_post_pages(home_page)
    imgs_url = []
    for page in range(1, pages + 1):
        hrefs = req_single_page(page)
        for href in hrefs:
            imgs = get_imgs_page(href)
            imgs_url.extend(imgs)

    # Use ThreadPoolExecutor for multithreaded downloading
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Submit the download tasks to the executor
        future_to_url = {executor.submit(download_image, url): url for url in imgs_url}

        # Check the completed tasks
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                future.result()  # Get the result of the future
            except Exception as e:
                print(f"Error occurred for {url}: {e}")
