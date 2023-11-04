from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from pathlib import Path
import json
from datetime import datetime

from filelist_api.settings import BASE_DIR
from config import DIR


def file_list(request):
    data_path = BASE_DIR.joinpath(DIR)
    if not data_path.is_dir():
        data_path = Path(DIR)
    try:
        files = [x for x in data_path.iterdir() if x.is_file()]
    except FileNotFoundError:
        return HttpResponse(f'Requsted path does not exist ({DIR})')

    file_info_list = []

    for file in files:
        file_info_list.append({
            "name": file.stem,
            "type": file.suffix,
            "time": datetime.fromtimestamp(file.stat().st_mtime).strftime(
                            "%d/%m/%Y, %H:%M:%S")
        })

    return JsonResponse({"data": file_info_list}, safe=False, 
                        json_dumps_params={'ensure_ascii': False, 'indent': 2})