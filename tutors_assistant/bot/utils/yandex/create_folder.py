import os

import httpx
from httpx import Response


async def yandex_disk_create_folder(path: str) -> Response:
    """
    Создание папки на яндекс диске
    """

    create_folder_url = "https://cloud-api.yandex.net/v1/disk/resources"

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"OAuth {os.getenv('YANDEX_DISK_TOKEN')}",
    }

    async with httpx.AsyncClient() as client:
        response = await client.put(
            url=create_folder_url,
            params={"path": path},
            headers=headers,
        )

    return response
