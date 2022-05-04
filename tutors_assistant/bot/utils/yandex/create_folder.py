import logging

import httpx
from httpx import Response

from logger_conf import handler

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


async def yandex_disk_create_folder(path: str, token: str) -> Response:
    """
    Создание папки на яндекс диске
    """

    create_folder_url = "https://cloud-api.yandex.net/v1/disk/resources"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"OAuth {token}",
    }

    async with httpx.AsyncClient() as client:
        response: Response = await client.put(
            url=create_folder_url,
            params={"path": path},
            headers=headers,
        )
        logger.info(
            f"yandex_disk_create_folder: "
            f"status= {response.status_code}"
            f"response= {response.json()}"
        )

    return response
