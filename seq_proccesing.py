"""
sequentially download pics from unsplash.com
and convert them to Black & White by creating a copy
"""
import requests
import os
import time
from PIL import Image
from comp.url_file import splash_imgs
from comp.gen_functions import log_time


class PicProcessor:
    def __init__(self):
        self.__folder_path = 'pics'
        self._list_links = None
        self.downloaded_pics_paths = []

        open('performance_time.txt', 'w').close()
        self.__prepare_pic_folder()


    def __prepare_pic_folder(self):
        if not os.path.isdir(self.__folder_path):
            os.mkdir(self.__folder_path)

    def set_links(self, lst_links):
        self._list_links = lst_links

    def done_downloading(self, pic_link):
        self.downloaded_pics_paths.append(pic_link)

    def download_pics(self):
        """
        download pics and save them using custom names
        """
        for pic_link in self._list_links:
            img_content = requests.get(pic_link).content
            img_name = pic_link.split('/')[3][:12]
            img_name = os.path.join(self.__folder_path, f'{img_name}.jpg')

            with open(img_name, 'wb') as img:
                img.write(img_content)
                self.done_downloading(img_name)

    def convert_to_bw(self):
        """
        convert the pics to B&W by creating new file for this
        """
        for processed_pic_link in self.downloaded_pics_paths:
            img_opened = Image.open(processed_pic_link)
            img_opened = img_opened.convert('L')
            new_pic_name = processed_pic_link.split(".")[0]
            img_opened.save(f'{new_pic_name}_converted.jpg')


# TESTING THE CLASS AND ITS PERF

test_processor = PicProcessor()
test_processor.set_links(splash_imgs)

for _ in range(10):
    # downloading phase
    start_time = time.perf_counter()
    test_processor.download_pics()
    end_time = time.perf_counter()
    download_time = round(end_time - start_time, 2)

    # converting phase
    start_time = time.perf_counter()
    test_processor.convert_to_bw()
    end_time = time.perf_counter()
    converting_time = round(end_time - start_time, 2)

    # outcome
    log_time(download_time, converting_time, 'seq')
    print('One Full Cycle Done.')
