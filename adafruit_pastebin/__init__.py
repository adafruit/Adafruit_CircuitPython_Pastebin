# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2022 Alec Delaney for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_pastebin`
===================

CircuitPython library for interacting with online pastebin services


* Author(s): Alec Delaney

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

"""

try:
    from typing import List
    from typing_extensions import Protocol
    from adafruit_requests import Session

    class SupportsStr(Protocol):
        """Protocol type for anything that supports the `str()` method"""

        def __str__(self) -> str:  # pylint: disable=invalid-str-returned
            ...

except ImportError:
    pass

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_Pastebin.git"


# pylint: disable=too-few-public-methods
class _Pastebin:
    """
    Generic paste bin class

    TODO: Add more details
    """

    def __init__(self, session: Session, auth_key: str) -> None:
        self._session = session
        self._auth_key = auth_key
