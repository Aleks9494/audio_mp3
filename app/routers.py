import io
import logging
import os.path
import aiofiles
import uuid
from typing import Union
from pydantic import UUID4
from pydub import AudioSegment
from fastapi import (
    APIRouter,
    File,
    UploadFile,
    Form,
    Depends
)
from fastapi.responses import (
    StreamingResponse,
    JSONResponse
)
from sqlalchemy.orm import Session
from app.base import get_session
from app.models import (
    User,
    Song
)
from app.schemas import (
    UserCreate,
    UserResponse,
    SongResponse,
    SongDB
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix='/api/v1')


@router.post("/create_user", response_model=UserResponse, status_code=201)
async def create_user(
        user: UserCreate,
        db_session: Session = Depends(get_session)
) -> Union[UserResponse, JSONResponse]:
    token = uuid.uuid4()

    try:
        user_db = User(
            user_token=token,
            username=user.username,
        )
        db_session.add(user_db)
        db_session.commit()
        db_session.refresh(user_db)
    except Exception as e:
        db_session.rollback()
        return JSONResponse(content=f"Error with DB, cause {str(e)}", status_code=400)

    return UserResponse(id=user_db.id, token=user_db.user_token)


@router.post("/upload_wav", response_model=SongResponse)
async def upload_wav(
        file: UploadFile = File(...),
        user_id: int = Form(...),
        user_token: UUID4 = Form(...),
        db_session: Session = Depends(get_session)
) -> Union[SongResponse, JSONResponse]:

    user = db_session.query(User).filter(User.id == user_id, User.user_token == user_token).first()
    if not user:
        return JSONResponse(content='User not found', status_code=404)

    name = file.filename
    filename, file_extension = os.path.splitext(name)

    if file_extension != '.wav':
        return JSONResponse(content='File isn`t a wav extension', status_code=400)

    root_path = "/data"
    if os.path.exists(root_path):
        names_of_files = os.listdir(root_path)
    else:
        return JSONResponse(content='Folder for converting files not found', status_code=404)

    count = 1

    while name in names_of_files:
        name = filename + f"({count})" + file_extension
        count += 1

    os.umask(0)
    async with aiofiles.open(f"{root_path}/{name}", 'wb') as out_file:
        while content := await file.read(1024):
            await out_file.write(content)

    try:
        src = f"{root_path}/{name}"
        name_without_extension, file_extension = os.path.splitext(name)
        dst = f"{root_path}/{name_without_extension}.mp3"

        sound = AudioSegment.from_mp3(src)
        sound.export(dst, format="wav")

        uuid_for_song = uuid.uuid4()
    except Exception as e:
        return JSONResponse(content=f"Error with converting to mp3, cause: {str(e)}", status_code=400)

    if os.path.exists(f"{root_path}/{name_without_extension}.mp3"):
        async with aiofiles.open(f"{root_path}/{name_without_extension}.mp3", 'rb') as out_file:
            content = await out_file.read()
    else:
        return JSONResponse(content="Error with converting to mp3", status_code=400)

    try:
        song = Song(
            uuid_key=uuid_for_song,
            song=content,
            user_id=user_id,
            name=name_without_extension
        )
        db_session.add(song)
        db_session.commit()
        db_session.refresh(song)
    except Exception as e:
        db_session.rollback()
        return JSONResponse(content=f"Error with DB, cause {str(e)}", status_code=400)

    os.remove(f"{root_path}/{name_without_extension}.mp3")
    os.remove(f"{root_path}/{name}")

    return SongResponse(url=f"http://0.0.0.0:8010/api/v1/record?id={uuid_for_song}&user={user_id}")


@router.get("/record", response_model=None)
async def download_song(
        id: UUID4,
        user: int,
        db_session: Session = Depends(get_session)
) -> Union[StreamingResponse, JSONResponse]:
    song_from_db = db_session.query(Song).filter(Song.uuid_key == id, Song.user_id == user).first()
    if not song_from_db:
        return JSONResponse(content='Song not found', status_code=404)

    song = SongDB.from_orm(song_from_db)

    file_bytesio = io.BytesIO(song.song)
    response = StreamingResponse(file_bytesio, media_type="audio/mp3")
    response.headers["Content-Disposition"] = f"attachment; filename={song.name}.mp3"
    response.headers["content-type"] = "multipart/form-data"

    return response
