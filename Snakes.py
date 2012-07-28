#!/usr/bin/env python
import sys
sys.path.append("src")

#import gc
#gc.disable()
#gc.set_debug(gc.DEBUG_STATS)

from engine.app import App

app = App()
while app.is_running:
    app.process()
