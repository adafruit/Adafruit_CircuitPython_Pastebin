# SPDX-FileCopyrightText: Copyright (c) 2022 Alec Delaney for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

import ssl
import socket
import adafruit_requests as requests
from adafruit_pastebin.gist import Gist

from settings import secrets
devkey = secrets["auth_key"]

session = requests.Session(socket, ssl_context=ssl.create_default_context())

pastebin = Gist(session, devkey)
paste_url = pastebin.paste(
    "This is a test paste!",
    filename="test.txt",
)
print(paste_url)