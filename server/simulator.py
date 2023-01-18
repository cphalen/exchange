import time
import os

debug = os.environ.get("EXCHANGE_SERVER_DEBUG", True)

class Simulator:
    def __init__(self, username, bot, ob):
        self.username = username
        self.bot = bot
        self.ob = ob

    def tick(self):
        # TODO:
        #   1) Generate order from agent (unless at max orders)
        #   2) Call the corresponding buy or sell function provided by client
        #   3) Attempt to resolve orders
        pass

    def run(self):
        if debug:
            print("Beginning 60 second simulation")

        # we do 60 runs of a 1 second interval of running the loop
        for i in range(60):
            end = time.time() + 1
            while time.time() < end:
                self.tick()

        if debug:
            print("Ending simulation")

        return self.ob.get_payout(self.username)
