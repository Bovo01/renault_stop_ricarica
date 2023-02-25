from typing import Union
from datetime import datetime


def log(filename: str, STRING_FORMAT: str, e: Union[BaseException, str]):
    with open(f'logs/{filename}.log', 'a') as f:
        f.write(f"{datetime.now().strftime(STRING_FORMAT)} - {str(e)}\n")