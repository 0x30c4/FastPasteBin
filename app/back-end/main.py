#!/usr/bin/env python3
from uvicorn import run, logging
from fastapi_sqlalchemy import DBSessionMiddleware, db
from aiofiles import open as aio_open
from os import environ
from os.path import join
from uuid import uuid4
from typing import Union
from fastapi import (
                     FastAPI,
                     UploadFile,
                     File,
                     status,
                     HTTPException,
                     Request,
)
from starlette.responses import RedirectResponse
from db.models import Bindata as ModelBinData
from configs.config import (
                            title,
                            db_url,
                            BIN_UPLOAD,
                            APP_URL,
                            APP_URL_INDEX,
                            APP_URL_UBIN,
                            LOG_INI,
                            version,
                            terms_of_service,
                            contact,
                            license_info,
                            description,
                            help_text
)

app = FastAPI(
                title=title,
                description=description,
                version=version,
                terms_of_service=terms_of_service,
                contact=contact,
                license_info=license_info,
                openapi_url="/api/openapi.json",
                docs_url="/api/docs"
             )


app.add_middleware(DBSessionMiddleware, db_url=db_url)


async def write_to_file(file, uuid):
    # Write the paste to the disk
    try:
        # creating the file name with full path
        file_path = join(BIN_UPLOAD, uuid)
        async with aio_open(file_path, "wb") as out_file:
            while content := await file.read(1024):
                await out_file.write(content)
    except Exception as e:
        logging.logging.error(e)
        raise HTTPException(status_code=status
                            .HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Couldn't Save The File!")
    return True


@app.get("/", status_code=status.HTTP_301_MOVED_PERMANENTLY)
async def index(request: Request) -> RedirectResponse:
    """
    This page just redirects browser client's to the WEB front end.
    """
    # If the client is requesting from a terminal then return
    # the help menu
    if "curl" in request.headers.get("user-agent"):
        return help_text
    return RedirectResponse(url=join(APP_URL, APP_URL_INDEX))


@app.post("/", status_code=status.HTTP_201_CREATED)
async def paste_bin(
    request: Request,
    file: UploadFile = File(None),
    meta_data: str = "",
    is_tmp: bool = False,
    rf: str = "url",
) -> Union[dict, str]:

    """
    This is the main Paste Bin end point that handels new pastes.
    """

    # if file is None raise error 415
    if file is None:
        logging.logging.error("No Data Was Pasted!")
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                            detail="No data was Pasted!")

    # if no content length was providerd with the request
    # then raise 411 length required error
    if "content-length" not in request.headers:
        logging.logging.error("No Content-Length Header!")
        raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED,
                            detail="No Content-Length Header!")

    # creating a uniq 32 char uuid version 4
    gen_uuid = uuid4().hex
    # if write opatarion is successfull then put the related
    # data to the paste to the db.
    if await write_to_file(file, gen_uuid):

        image_db = ModelBinData(
            uuid=gen_uuid, meta_data=meta_data,
            is_tmp=is_tmp
        )
        db.session.add(image_db)
        db.session.commit()

        rf.lower()
        ret_obj = None
        # building the paste url with the gen_uuid
        resp_url = join(APP_URL, APP_URL_UBIN, gen_uuid)
        # if the user want's json response then return
        # json else by default return just the paste url.
        if rf == "json":
            ret_obj = {
                "uuid": gen_uuid,
                "meta_data": meta_data,
                "is_tmp": is_tmp,
                "url": resp_url
            }
        elif rf == "url":
            ret_obj = resp_url

        return ret_obj

    # if the writing paste to the disk fails then return a empty response.
    return {}

if __name__ == "__main__":
    port = int(environ.get("PORT", default=5000))
    workers = int(environ.get("WORKERS", default=1))
    host = environ.get("HOST", default="0.0.0.0")
    log_level = environ.get("LOG_LEVEL", default="info")

    reload = int(environ.get("RELOAD", default="1"))

    run(
        "main:app", host=host, port=port,
        log_level=log_level, workers=workers,
        reload=reload, log_config=LOG_INI
    )
