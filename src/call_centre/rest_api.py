import asyncio
import copy
import logging
import time
from datetime import datetime
from pathlib import Path

import requests
from fastapi import APIRouter, Form

from call_centre.services.gpts import GPTS
from call_centre.storages.local import LocalStorages
from call_centre.utils.constant import TIMESTAMP_FORMAT
from call_centre.utils.message import Message
from call_centre.utils.stt import STT
from call_centre.utils.utils import process_messages

BASE_DIR = Path(__file__).parent.parent

logger = logging.getLogger(f'{__name__}  {__name__}')
gpt = GPTS()
stt = STT()
file = LocalStorages()
router = APIRouter()
all_messages = []
_res = [
    '''1. Greeting: Yes\n
2. Self-introduction: No\n
3. Closing phrase: No\n
4. Statement before verifying information: No\n
5. Re-verification of registrant's identity before registration: No\n
6. Verification of the mobile phone number for registration: No\n
7. Verification of personal details of the customer: No\n
8. Inquiry about whether IDD roaming service is needed: No\n
9. Remind the customer to take a survey - NPS: No\n
10. Provide the customer with ways to inquire and contact: No
'''.strip(),
    '''
    1. Greeting: Yes\n
    2. Self-introduction: Yes\n
    3. Closing phrase: No\n
    4. Statement before verifying information: No\n
    5. Re-verification of registrant's identity before registration: No\n
    6. Verification of the mobile phone number for registration: Yes\n
    7. Verification of personal details of the customer: Yes\n
    8. Inquiry about whether IDD roaming service is needed: No\n
    9. Remind the customer to take a survey - NPS: No\n
    10. Provide the customer with ways to inquire and contact: Yes
    '''.strip()
]


@router.get('/')
async def hello_world():
    """
    hello world
    :return:
    """
    return Message(
        message='Hello World',
    )


@router.post('/chatCompletion/')
async def chat_completion(
        content: str = Form(),
):
    """
    chat completion
    :param content:
    :return:
    """
    start_time = time.time()
    res = await gpt.ask(
        question=content
    )
    _msg = copy.deepcopy(res)
    all_messages.extend(_msg[-2:])
    return Message(
        message='Chat completion successful',
        data=all_messages,
        response_time=time.time() - start_time,
    )


@router.post('/analyse/')
async def analyse(
        audio: str = Form(),
        content: str = Form(),
):
    """
    chat completion
    :param language:
    :param content:
    :param audio:
    :param temperature:
    :return:
    """
    current_time = datetime.now()
    start_time = time.time()
    # save audio file
    save_path = BASE_DIR / 'input' / f'{current_time.strftime(TIMESTAMP_FORMAT)}ask.wav'
    save_path.parent.mkdir(parents=True, exist_ok=True)
    download_audio(url=audio, local_filename=save_path)
    if '98107680.mp3' in audio:
        await asyncio.sleep(10)
    # data = await audio.read()
    # await file.save(save_path, data)
    # stt transcribe audio
    audio_content = await stt.transcribe_audio(save_path)
    # chat gpt step
    res = await gpt.custom_chat_completions(
        question=content,
        audio_content=audio_content,
    )
    all_messages.extend(res[-2:])
    processed_messages = process_messages(all_messages)
    return Message(
        message='Chat completion successful',
        data=processed_messages,
        response_time=time.time() - start_time,
    )


@router.get('/temperature/')
def get_temperature():
    """
    get temperature
    :return:
    """
    return gpt.temperature


@router.post('/temperature/')
def update_temperature(
        temperature: float = Form(description='Modify temperature')
):
    """
    Modify temperature
    :param temperature:
    :return:
    """
    return gpt.update_temperature(temperature)


@router.get('/prompts/')
def get_prompt():
    """
    get prompt
    :return:
    """
    return gpt.prompts


@router.post('/prompts/')
def update_prompt(
        prompt: str = Form(description='Modify prompts')
):
    """
    Modify prompts
    :param prompt:
    :return:
    """
    return gpt.update_prompts(prompt)


@router.get('/messages/')
def get_messages():
    return all_messages


@router.get('/initMessages/')
def init_messages():
    """
    init messages
    :return:
    """
    global all_messages
    all_messages = [
    ]
    gpt.init_messages_context()


def download_audio(url, local_filename):
    with requests.get(url, stream=True) as response:
        response.raise_for_status()  # 确保请求成功
        with open(local_filename, 'wb') as _f:
            for chunk in response.iter_content(chunk_size=8192):
                _f.write(chunk)
    print(f"Downloaded {local_filename}")
