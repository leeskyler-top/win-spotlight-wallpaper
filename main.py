import os
import shutil
import sys
from PIL import Image
import platform


def os_release():
    # Check if the operating system is Windows
    if platform.system() != "Windows":
        print("Not Windows")
        sys.exit(1)
    else:
        return platform.release()


def check_path():
    if not os.path.exists("./imgs"):
        os.makedirs("./imgs")


def get_image_type(image_path):
    # Open the image and return its format
    with Image.open(image_path) as img:
        return img.format.lower()


def is_large_image(image_path, min_width=1920, min_height=1080):
    # Check if the image dimensions are larger than or equal to the specified minimum
    with Image.open(image_path) as img:
        width, height = img.size
        return width >= min_width and height >= min_height


def copy_file(path):
    global width, height
    print(os.listdir(path))
    for img in os.listdir(path):
        src_img = os.path.join(path, img)
        if is_large_image(src_img, width, height):
            current_img_type = get_image_type(src_img)
            dest_file = os.path.join("./imgs", f"{img}.{current_img_type}")
            if not os.path.exists(dest_file):
                shutil.copy2(src_img, dest_file)

if __name__ == "__main__":
    path = f"C:\\Users\\{os.getlogin()}\\AppData\\Local\\Packages\\Microsoft.Windows.ContentDeliveryManager_cw5n1h2txyewy\\LocalState\\Assets"
    win11_wallpaper_path = f"C:\\Users\\{os.getlogin()}\\AppData\\Roaming\\Microsoft\\Windows\\Themes\\CachedFiles"

    # Min Width and Min Height
    width = 1920
    height = 1080

    ver = os_release()
    check_path()
    copy_file(path)
    if ver == "11":
        copy_file(win11_wallpaper_path)
