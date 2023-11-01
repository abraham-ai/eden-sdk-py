import asyncio
import httpx
from aiofiles import open as aio_open
import eden



import time
import eden
from . import utils


def create(name, description):
    return utils.post("/collections/create", {
        "name": name,
        "description": description
    })


def get(collectionId):
    result = utils.get("/collections/" + collectionId)
    return result["collection"]


def addcreations(collectionId, creationIds):
    return utils.post("/collections/addcreations", {
        "collectionId": collectionId,
        "creationIds": creationIds
    })
