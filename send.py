import asyncio
import json
import time
from nats.aio.client import Client as NATS

NATS_SERVER = "nats://113.164.234.227:4222"
CHANNEL_PUB = "raw_pvdata.HV2160135605"
NKEY_SEED_FILE = "a.nkey"  # ⚠️ Chỉ chứa dòng SU..., không có BEGIN/END

# Payload cố định
payload = {
    "PVID": "HV2160135605",
    "PTYPE": "DATA",
    "ITYPE": "HUAWEI1",
    "UTS": time.time(),
    "MODBUS1": {
        "FUNCCODE": 3, "OFFSET": 0, "STARTREG": 30000, "NUMREGS": 25,
        "REGDATA": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    },
    "MODBUS2": {
        "FUNCCODE": 3, "OFFSET": 0, "STARTREG": 30071, "NUMREGS": 12,
        "REGDATA": [2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    },
    "MODBUS3": {
        "FUNCCODE": 3, "OFFSET": 0, "STARTREG": 32000, "NUMREGS": 60,
        "REGDATA": [6, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    },
    "MODBUS4": {
        "FUNCCODE": 3, "OFFSET": 0, "STARTREG": 32060, "NUMREGS": 60,
        "REGDATA": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1000, 5018, 9741, 450, 3000, 512, 0, 26282, 61018, 65535, 65535, 0, 942, 0, 0, 0, 0, 0, 0, 0, 0, 0, 45, 28829, 46, 49302, 26282, 62803, 0, 193, 0, 646, 0, 646, 7, 37004]
    },
    "MODBUS5": {
        "FUNCCODE": 3, "OFFSET": 0, "STARTREG": 37100, "NUMREGS": 39,
        "REGDATA": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]
    },
    "MODBUS6": {
        "FUNCCODE": 3, "OFFSET": 0, "STARTREG": 40000, "NUMREGS": 2,
        "REGDATA": [0, 0]
    }
}

async def error_cb(e):
    print("❌ Lỗi kết nối:", e)

async def run():
    nc = NATS()
    await nc.connect(
        servers=[NATS_SERVER],
        nkeys_seed=NKEY_SEED_FILE,
        error_cb=error_cb
    )

    while True:
        payload["UTS"] = int(time.time())
        print(int(time.time()))
        await nc.publish(CHANNEL_PUB, json.dumps(payload).encode())
        print(f"✅ [{time.strftime('%X')}] Gửi bản tin cố định tới {CHANNEL_PUB}")
        await asyncio.sleep(10)

asyncio.run(run())
