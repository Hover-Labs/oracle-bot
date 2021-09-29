import requests
import os
from pytezos import pytezos
from datetime import datetime, timedelta
from apscheduler.schedulers.blocking import BlockingScheduler

HARBINGER_ORACLE = 'KT1AdbYiPYb5hDuEuVrfxmFehtnBCXv4Np7r'
DISCORD_WEBHOOK = os.environ['DISCORD_WEBHOOK']

def check():
    client = pytezos.using(shell='https://mainnet.api.tez.ie')

    contract = client.contract(HARBINGER_ORACLE)

    ts = contract.storage['assetMap']['XTZ-USD']()['lastUpdateTime']

    current_oracle_update_age = datetime.utcnow() - datetime.fromtimestamp(ts)

    if current_oracle_update_age > timedelta(minutes=25):
        requests.post(DISCORD_WEBHOOK, json={
            "content": ":warning: The oracle is > 25 minutes out of date! Please ensure there's a poster update or visit <https://harbinger.live> to update Kolibri manually (if possible)!"
        })
        print("[{}] Over 25 mins!".format(datetime.now()))
    elif current_oracle_update_age > timedelta(minutes=30):
        requests.post(DISCORD_WEBHOOK, json={
            "content": ":no_entry: <@&819726924440010843> **The oracle is now > 30 minutes out of date.** Minting new kUSD, liquidating ovens, and withdrawing from ovens has been disabled in the protocol. Please update the oracle to restore functionality (though likely there's an outage at coinbase outside anyone else's control)."
        })
        print("[{}] Over 30 mins!".format(datetime.now()))
    else:
        # Clear microseconds
        current_oracle_update_age -= timedelta(microseconds=current_oracle_update_age.microseconds)
        print("[{}] Latest update is from {} ago, no need to alert...".format(datetime.now(), current_oracle_update_age))

scheduler = BlockingScheduler()
scheduler.add_job(check, 'interval', minutes=5, next_run_time=datetime.now())

try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    pass
