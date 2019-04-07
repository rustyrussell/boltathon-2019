#!/usr/bin/env python3

# A plugin for c-lightning which provides a simple invoice web service
# to reveal a phrase when paid.

# Trivial extensions include:
#  Make it reveal the nth phrase, depending on how many have already been revealed.
#  Have an option or even rpc call to set or add what backend text files to serve.
#
# Note: every node in the path also gets this preimage; you might want
# to combine it with something in the invoice description itself
# (which, also should be served over https not http!)
from lightning import Plugin
from flask import Flask
import threading
import os
import secrets

app = Flask(__name__)
app.debug = False

@app.route('/')
def serve_invoice():
    # Label is an internal thing which needs to be unique: for serious
    # systems this ensures that we can determine whether invoice
    # creation succeeded or not if we crashed during.  We don't care
    # that much!
    randomness = secrets.token_hex(8)
    invoice = plugin.rpc.invoice(msatoshi=24, label=randomness, description='Test invoice',
                                 preimage=randomness+bytes('An unexpected surprise!!', encoding='utf8').hex())
    return invoice['bolt11']

plugin = Plugin()

@plugin.init()
def init(options, configuration, plugin):
    threading.Thread(target=app.run, daemon=True).start()
    plugin.log("Plugin plugin.py initialized")

plugin.run()
