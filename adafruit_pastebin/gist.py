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
    """Pastebin API for GitHub Gists"""

    def paste(
        self,
        content: SupportsStr,
        *,
        filename: str = "My Gist",
        description: Optional[str] = None,
        public: bool = False,
    ) -> str:
        """Paste content as a GitHub Gist"""

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
        except KeyError:
            error_message = json_response["message"]
        raise RuntimeError(error_message)
