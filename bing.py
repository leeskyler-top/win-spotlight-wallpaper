import datetime
import os
import json
import requests


def get_wallpaper(start_idx, end_idx):
    os.makedirs('./imgs', exist_ok=True)
    for idx in range(start_idx, end_idx + 1):
        api_url = f"https://www.bing.com/HPImageArchive.aspx?format=js&mbl=1&idx={idx}&n=1&cc=us"
        response = requests.get(api_url).json()
        img_url = f"https://www.bing.com{response['images'][0]['url']}"
        img_data = requests.get(img_url).content
        img_filename = f"./imgs/bing_wallpaper_{idx}_{str(datetime.datetime.now().year)}_{str(datetime.datetime.now().month)}_{str(datetime.datetime.now().day)}.jpg"
        with open(img_filename, 'wb') as img_file:
            img_file.write(img_data)
        print(f"Image {idx} saved as {img_filename}")

if __name__ == "__main__":
    get_wallpaper(1, 1)
