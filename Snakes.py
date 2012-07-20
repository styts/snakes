#!/usr/bin/env python
import sys
sys.path.append("src")

from engine.app import App

app = App()
while app.is_running:
    app.process()
