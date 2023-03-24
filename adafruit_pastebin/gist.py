# SPDX-FileCopyrightText: Copyright (c) 2022 Alec Delaney for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_pastebin.gist`
========================

Pastebin API for GitHub Gists


* Author(s): Alec Delaney

"""

import json
from adafruit_pastebin import _Pastebin

try:
    from typing import Optional
    from adafruit_pastebin import SupportsStr
except ImportError:
    pass

POST_URL = "https://api.github.com/gists"


class Gist(_Pastebin):
    """
    Pastebin API for GitHub Gists.

    :param Session session: An :py:class:~`adafruit_requests.Session`
        to use for web connectiviy
    :param str auth_key: The `GitHub Personal Access Token
        <https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token>`_
        to use for authentication
    """

    def paste(
        self,
        content: SupportsStr,
        *,
        filename: str = "My Gist",
        description: Optional[str] = None,
        public: bool = False,
    ) -> str:
        """
        Paste content as a GitHub Gist and return the URL of the new gist.

        :param content: Any string (or object that can be converted to a string)
            to paste
        :param str filename: (Optional) A filename for the gist content
        :param str|None description: (Optional) A description for the gist
        :param bool public: Whether the gist should be public (``True``) or
            private (``False``)
        """

        headers = {
            "Accept": "applciation/vnd.github+json",
            "Authorization": f"Bearer {self._auth_key}",
        }

        data = {"public": public, "files": {filename: {"content": str(content)}}}

        if description is not None:
            data["description"] = description

        response = self._session.post(POST_URL, headers=headers, data=json.dumps(data))

        json_response = json.loads(response.text)
        try:
            return json_response["html_url"]
        except KeyError as err:
            error_message = json_response["message"]
            raise RuntimeError(error_message) from err
