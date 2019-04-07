#!/usr/bin/env python3
from lightning import Plugin, Millisatoshi
import requests
import json

# Simple plugin to get a work from a wordserv server.

plugin = Plugin()

@plugin.method("getword")
def getword(plugin, url="http://127.0.0.1:5000", max: Millisatoshi=Millisatoshi(24)):
    """Pay for a 24-byte word from a lightning word server.
    """
    r = requests.get(url)
    inv = r.content.decode()
    # Check amount!
    decode = plugin.rpc.decodepay(inv)
    amount = decode['amount_msat']
    if amount > max:
        raise ValueError("Amount {} is too large".format(amount))
    preimage = plugin.rpc.pay(inv)['payment_preimage']
    b = bytes.fromhex(preimage)
    return {'description': decode['description'], 'words': b[8:].decode()}
    

@plugin.init()
def init(options, configuration, plugin):
    plugin.log("Plugin getword.py initialized")

plugin.run()
