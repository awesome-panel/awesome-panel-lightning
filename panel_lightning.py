"""The panel_lightning module provides the `LitPanelPage` that makes it easy
to add a Panel page to your `LightningFlow`.
"""
from __future__ import annotations

import pathlib
from types import ModuleType
from typing import Callable, Dict, Union

import lightning_app as lapp
import panel as pn
from bokeh.application.handlers import code
from bokeh.server.server import Server
from lightning_app.core import constants

Page = Union[Callable[[], pn.viewable.Viewable], str, pathlib.Path]


class _CodeRunnerWithFastInitialResponse(code.CodeRunner):
    """Helper class to provide a fast initial response to the lightning.ai server

    C.f. https://github.com/Lightning-AI/lightning/issues/13335
    """

    _is_patched = False
    _initial_response = True

    def run(self, module: ModuleType, post_check: Callable[[], None] | None = None) -> None:
        """Patches the code.CodeRunner to provide a fast initial response"""
        if self._initial_response:
            pn.pane.HTML("<h1>Fast Initial Response. Please reload the page.</h1>").servable()
            self._initial_response = False
        else:
            super().run(module, post_check)

    @classmethod
    def patch(cls):
        """Patches the Panel server to provide a fast initial response from pages created via
        .py and .ipynb files."""
        if not cls._is_patched:
            cls._is_patched = True
            code.CodeRunner = _CodeRunnerWithFastInitialResponse


class _PageWithFastInitialResponse:  # pylint: disable=too-few-public-methods
    """Helper class to provide a fast initial response to the Lightning.AI server

    C.f. https://github.com/Lightning-AI/lightning/issues/13335
    """

    def __init__(self, page: Callable[[], pn.viewable.Viewable]):
        """Wraps the page function to provide a fast initial response

        Args:
            page (Callable[[], pn.viewable.Viewable]): A function returning a Panel viewable
        """
        self._initial_response = True
        self._page = page

    def get(self):
        """Runs the page function and returns the result.

        The first time the get function is a run a fast page function is run
        """
        if self._initial_response:
            self._initial_response = False
            return pn.pane.HTML("<h1>Fast Initial Response</h1>")

        return self._page()


class LitPanelPage(lapp.LightningWork):
    """Can serve a single page Panel app"""

    def __init__(self, page: Page, **params):
        """Can serve a single page Panel app

        Args:
            page (Page):
                A function returning a Panel `Viewable` or the path of a file containing a
                Panel application.
        """
        if isinstance(page, (str, pathlib.Path)):
            _CodeRunnerWithFastInitialResponse.patch()
            page = str(page)
            self._page = page
        else:
            self._page = _PageWithFastInitialResponse(page=page).get

        self._server: Union[None, Server] = None

        super().__init__(**params)

    def run(self, *args, **kwargs):
        """Starts the server and serves the page"""
        print("websocket_origin", self.websocket_origin)
        self._server = pn.serve(
            {"/": self._page},
            port=self.port,
            address=self.host,
            websocket_origin=self.websocket_origin,
            show=False,
        )

    def stop(self):
        """Stops the server"""
        if self._server:
            self._server.stop()

    def get_tab(self, name: str) -> Dict[str, str | "LitPanelPage"]:
        """Returns a *tab* definition to be included in the layout of a LightingFlow"""
        return {"name": name, "content": self}

    @property
    def websocket_origin(self) -> str:
        """Returns"""
        host = constants.APP_SERVER_HOST.replace("http://", "").replace("https://", "")
        if host != "127.0.0.1":
            host = "*." + host.split(".")[-1]
        return host + ":" + str(self.port)
