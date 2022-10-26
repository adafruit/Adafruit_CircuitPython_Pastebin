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
    from adafruit_pastebin import SupportsStr  # pylint: disable=ungrouped-imports
except ImportError:
    pass


POST_URL = "http://pastebin.com/api/api_post.php"


# pylint: disable=too-few-public-methods
class PrivacySetting:
    """
    Enum-like class for privacy settings.

    Valid options are:

    * PUBLIC
    * UNLISTED
    * PRIVATE

    """

    PUBLIC = "0"
    UNLISTED = "1"
    PRIVATE = "2"


# pylint: disable=too-few-public-methods
class ExpirationSetting:
    """
    Enum-like class for expiration settings.

    Valid options are:

    * NEVER
    * TEN_MINUTES
    * ONE_HOUR
    * ONE_DAY
    * ONE_WEEK
    * TWO_WEEKS
    * ONE_MONTH
    * SIX_MONTHS
    * ONE_YEAR

    """

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
    """
    Pastebin API for PasteBin.com.

    :param Session session: An :py:class:~`adafruit_requests.Session`
        to use for web connectiviy
    :param str auth_key: The `PasteBin.com dev key <https://pastebin.com/doc_api#1>`_
        to use for API accessibilty
    """

    def paste(
        self,
        content: SupportsStr,
        *,
        name: Optional[str] = None,
        content_format: Optional[str] = None,
        privacy: str = PrivacySetting.PUBLIC,
        expiration: str = ExpirationSetting.NEVER,
    ) -> str:
        """
        Paste content to PasteBin.com and return the URL of the new paste.

        :param content: Any string (or object that can be converted to a string)
            to paste
        :param str|None name: (Optional) A name for paste
        :param str|None content_format: (Optional) The formatting of the pasted content;
            valid formats can be found `in the PasteBin.com API docs
            <https://pastebin.com/doc_api#5>`_
        :param str privacy: (Optional) The privacy setting of the paste, which must be a
            valid option from :py:class:`~adafruit_pastebin.pastebin.PrivacySetting`;
            default is public
        :param str expiration: (Optional) When the paste will expire and be deleted,
            which must be a valid option from
            :py:class:`~adafruit_pastebin.pastebin.ExpirationSetting`; default is never
        """

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
