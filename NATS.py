import asyncio
import json
import time
from nats.aio.client import Client as NATS
from pymodbus.client.sync import ModbusTcpClient
import os

CONFIG_FILE = "config.json"
seed_path = os.path.join(os.path.dirname(__file__), 'a.nkey')

def read_modbus(ip, port, addr, funccode, offset, startreg, numregs):
    client = ModbusTcpClient(ip, port=port, timeout=10)
    if not client.connect():
        return None

    real_start = startreg + offset
    result = None
    try:
        if funccode == 3:
            result = client.read_holding_registers(real_start, numregs, unit=addr)
        elif funccode == 4:
            result = client.read_input_registers(real_start, numregs, unit=addr)
        else:
            print(f"❌ Unsupported FUNCCODE: {funccode}")
    except Exception as e:
        print(f"❌ Modbus error: {e}")

    client.close()
    if result and hasattr(result, "registers"):
        return result.registers
    return None

async def error_cb(e):
    print("❌ Lỗi NATS:", str(e))

async def run():
    print("#####    STARTING    ####")
    with open(CONFIG_FILE, "r") as f:
        devices = json.load(f)

    nc = NATS()
    await nc.connect(
        servers=["nats://113.164.234.227:4222"],
        nkeys_seed=seed_path,
        error_cb=error_cb
    )

    while True:
        for dev in devices:
            serial = dev["serial"]
            pvid = dev["pvid"]
            ip = dev.get("ip", "127.0.0.1")
            port = dev.get("port", 502)
            addr = dev.get("modbus_addr", 1)
            modbus_groups = dev.get("modbus_groups", [])
            payload = {
                "PVID": pvid,
                "PTYPE": "DATA",
                "ITYPE": "HUAWEI1",
                "UTS": time.time()
            }

            for group in modbus_groups:
                name = group["name"]
                startreg = group["start"]
                numregs = group["count"]
                funccode = group.get("funccode", 3)
                offset = group.get("offset", 0)

                regs = read_modbus(ip, port, addr, funccode, offset, startreg, numregs)
                payload[name] = {
                    "FUNCCODE": funccode,
                    "OFFSET": offset,
                    "STARTREG": startreg,
                    "NUMREGS": numregs,
                    "REGDATA": regs if regs else []
                }

            channel_pub = f"raw_pvdata.{serial}"
            await nc.publish(channel_pub, json.dumps(payload).encode())
            print(f"📤 Gửi dữ liệu lên {channel_pub}")
            time.sleep(0.1)

        await asyncio.sleep(30)  # Gửi mỗi 5s

asyncio.run(run())
