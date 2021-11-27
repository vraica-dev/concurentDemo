"""
downloading and converting pics to B&W using concurency
both threading and multiprocessing
"""
import requests
import os
import time
from PIL import Image
import concurrent.futures
from comp.url_file import splash_imgs
from comp.gen_functions import log_time


class PicProcessorConcurent:
    def __init__(self):
        self.__folder_path = 'pics'
        self._list_links = None
        self.downloaded_pics_paths = []

        open('performance_time_conc.txt', 'w').close()
        self.__prepare_pic_folder()

    def __prepare_pic_folder(self):
        if not os.path.isdir(self.__folder_path):
            os.mkdir(self.__folder_path)

    def set_links(self, lst_links):
        self._list_links = lst_links

    def done_downloading(self, pic_link):
        self.downloaded_pics_paths.append(pic_link)

    def _download_pic(self, pic_link):
        """
        downloads one picture based on link and saves it
        """
        img_content = requests.get(pic_link).content
        img_name = pic_link.split('/')[3][:12]
        img_name = os.path.join(self.__folder_path, f'{img_name}.jpg')

        with open(img_name, 'wb') as img:
            img.write(img_content)
            self.done_downloading(img_name)

    def _convert_bw(self, processed_pic_link):
        """
        converts one picture to B&W and saves it with a new name
        """
        img_opened = Image.open(processed_pic_link)
        img_opened = img_opened.convert('L')
        new_pic_name = processed_pic_link.split(".")[0]
        img_opened.save(f'{new_pic_name}_converted.jpg')

    def download_all_pics(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = [executor.submit(self._download_pic, pic_link) for pic_link in self._list_links]

    def convert_all_pics(self):
        with concurrent.futures.ProcessPoolExecutor() as proc_executor:
            future = proc_executor.map(self._convert_bw, self.downloaded_pics_paths)


# TESTING

if __name__ == '__main__':

    cProcesor = PicProcessorConcurent()
    cProcesor.set_links(splash_imgs)

    for _ in range(10):
        start_time = time.perf_counter()
        cProcesor.download_all_pics()
        end_time = time.perf_counter()
        download_time = round(end_time - start_time, 2)

        start_time = time.perf_counter()
        cProcesor.convert_all_pics()
        end_time = time.perf_counter()
        converting_time = round(end_time - start_time, 2)

        log_time(download_time, converting_time, 'conccurent')
        print('One full cycle done in concurency.')