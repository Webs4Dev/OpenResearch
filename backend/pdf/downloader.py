import requests


def download_pdf(url:str,save_path:str):

    response = requests.get(url,timeout=20)
    response.raise_for_status()

    with open(save_path,"wb") as f:
        f.write(response.content)

    return save_path