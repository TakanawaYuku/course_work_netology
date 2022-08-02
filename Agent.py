import requests
import os
import json
import time
import random as rnd


class Social:

    @staticmethod
    def __folder_creation(base_path, path):
        file_path = os.path.join(base_path, path)
        if not os.path.isdir(file_path):
            os.mkdir(file_path)
        return file_path

    @staticmethod
    def _path_normalizer(name_path):
        symbol_no = rf"""*:'"%!@?$/\\|&<>+.)("""
        name = '_'.join(name_path.split()).strip(symbol_no)
        for s in symbol_no:
            if s in name:
                name = name.replace(s, '_')
        return name

    def files_downloader(self, file_dir: str):
        file_path_start = self.__folder_creation(os.getcwd(), file_dir)
        dict_foto_info = {}
        for title, value in self.photos_info().items():
            file_path = self.__folder_creation(file_path_start, title)
            print(f"Загружаем файлы в директорию >>> {file_path}:")
            time.sleep(rnd.randint(1, 5))
            list_value = []

            for info in value:
                file_name = os.path.join(file_path, info['file_name'])
                response = requests.get(info['url'])
                print(f"'{info['file_name']}' ")
                with open(file_name, 'wb') as f:
                    f.write(response.content)

                list_value.append({
                    'file_name': info['file_name'],
                    'size': info['size']
                })

            dict_foto_info[title] = list_value

        file_name_json = os.path.join(file_path_start, f"{file_dir}.json")
        print(f"Загружаем файл '{file_dir}.json' в >>> {file_path_start}")
        with open(file_name_json, 'w', encoding="utf-8") as f:
            json.dump(dict_foto_info, f, indent=2, ensure_ascii=False)
        print("=" * 50)
