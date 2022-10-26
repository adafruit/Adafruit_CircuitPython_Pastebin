# SPDX-FileCopyrightText: Copyright (c) 2022 Alec Delaney for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_pastebin.pastebin`
============================

Pastebin API for PasteBin.com


* Author(s): Alec Delaney

"""

from adafruit_pastebin import _Pastebin

try:
    from typing import Optional
    from typing_extensions import Literal
    from adafruit_pastebin import SupportsStr  # pylint: disable=ungrouped-imports
except ImportError:
    pass


POST_URL = "http://pastebin.com/api/api_post.php"


# pylint: disable=too-few-public-methods
class PrivacySetting:
    """Privacy settings"""

    PUBLIC = "0"
    UNLISTED = "1"
    PRIVATE = "2"


# pylint: disable=too-few-public-methods
class ExpirationSetting:
    """Expiration settings"""

    NEVER = "N"
    TEN_MINUTES = "10M"
    ONE_HOUR = "1H"
    ONE_DAY = "1D"
    ONE_WEEK = "1W"
    TWO_WEEKS = "2W"
    ONE_MONTH = "1M"
    SIX_MONTHS = "6M"
    ONE_YEAR = "1Y"


class PasteBin(_Pastebin):
    """Pastebin API for PasteBin.com"""

    def paste(
        self,
        content: SupportsStr,
        *,
        name: Optional[str] = None,
        content_format: Optional[str] = None,
        privacy: Literal["0", "1", "2"] = PrivacySetting.PUBLIC,
        expiration: str = ExpirationSetting.NEVER,
    ) -> str:
        """Paste content to PasteBin.com"""

        data = {
            "api_dev_key": self._auth_key,
            "api_option": "paste",
            "api_paste_code": str(content),
            "api_paste_private": privacy,
            "api_paste_expire_date": expiration,
        }
        if name is not None:
            data["api_paste_name"] = name
        if content_format is not None:
            data["api_paste_format"] = content_format

        response = self._session.post(POST_URL, data=data)
        if not response.text.startswith("http"):
            raise RuntimeError(response.text)

        return response.text
