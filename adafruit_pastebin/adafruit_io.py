# SPDX-FileCopyrightText: Copyright (c) 2022 Alec Delaney for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_pastebin.adafruit_io`
===============================

Pastebin API for Adafuit IO


* Author(s): Alec Delaney

"""

import json
from adafruit_pastebin import _Pastebin

try:
    import typing  # pylint: disable=unused-import
    from adafruit_pastebin import SupportsStr
    from adafruit_requests import Session
except ImportError:
    pass

POST_URL = "https://io.adafruit.com/api/v2/{username}/feeds/{feed_key}/data"


class AIOPastebin(_Pastebin):
    """
    Pastebin API for Adafruit IO.

    :param Session session: An :py:class:~`adafruit_requests.Session`
        to use for web connectiviy
    :param str auth_key: The Adafruit IO key to use for authentication
    :param str username: The username associated with the ``auth_key``
    :param str feed_key: The feed key of the feed to use for pasting
    """

    def __init__(
        self, session: Session, auth_key: str, *, username: str, feed_key: str
    ) -> None:
        super().__init__(session, auth_key)
        self._username = username
        self._feed_key = feed_key
        self._post_url = (
            f"https://io.adafruit.com/api/v2/{username}/feeds/{feed_key}/data"
        )

    def paste(
        self,
        content: SupportsStr,
    ) -> str:
        """
        Paste content to Adafruit IO and returns the URL of the feed.

        :param content: Any string (or object that can be converted to a string)
            to paste
        """

        payload = {
            "value": str(content),
        }

        headers = {
            "X-AIO-Key": self._auth_key,
        }

        response = self._session.post(self._post_url, json=payload, headers=headers)
        response_json = json.loads(response.text)

        if "error" in response_json:
            raise RuntimeError("Could not paste the information")

        return f"https://io.adafruit.com/{self._username}/feeds/{self._feed_key}"
