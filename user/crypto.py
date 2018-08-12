import binascii
import datetime
import logging
import sys

import maya

from nucypher.characters import Alice, Bob, Ursula
from nucypher.data_sources import DataSource
# This is already running in another process.
from nucypher.network.middleware import RestMiddleware
from umbral.keys import UmbralPublicKey


def get_seed():
    teacher_dht_port = 3500
    teacher_rest_port = int(teacher_dht_port) + 100
    with open("examples-runtime-cruft/node-metadata-{}".format(teacher_rest_port), "r") as f:
        f.seek(0)
        teacher_bytes = binascii.unhexlify(f.read())
    URSULA = Ursula.from_bytes(teacher_bytes, federated_only=True)
    print("Will learn from {}".format(URSULA))

    return URSULA


def get_alice():
    return  Alice(network_middleware=RestMiddleware(),
          known_nodes=(get_seed(),),  # in lieu of seed nodes
          federated_only=True,
          always_be_learning=True)  # TODO: 289

def get_bob():
    return  Bob(known_nodes=(get_seed(),), federated_only=True, always_be_learning=True)




