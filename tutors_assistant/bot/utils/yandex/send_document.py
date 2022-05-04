import logging

import httpx
from httpx import Response

from logger_conf import handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


async def yandex_disk_send_documents(
    token: str, folder_path: str = "", file_path: str = ""
):
    """
    Отправка документов на яндекс диск
    """
    load_documents_url = "https://cloud-api.yandex.net/v1/disk/resources/upload"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"OAuth {token}",
    }
    path = f"{folder_path}{file_path.split('/')[-1]}"
    async with httpx.AsyncClient() as client:
        response: Response = await client.get(
            url=load_documents_url,
            headers=headers,
            params={"path": path, "overwrite": False},
        )
        logger.info(
            f"yandex_disk_send_documents: "
            f"status= {response.status_code}"
            f"response= {response.json()}"
        )
        res_json = response.json()
        with open(file_path, "rb") as file:
            response: Response = await client.put(
                url=res_json["href"], files={"file": file}
            )

    return response
