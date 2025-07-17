# from pymodbus.client import ModbusTcpClient
from pymodbus.client.sync import ModbusTcpClient

from pymodbus.exceptions import ModbusException

# Modbus data configuration
MODBUS_DATA = {
    "MODBUS1": {"FUNCCODE": 3, "OFFSET": 0, "STARTREG": 30000, "NUMREGS": 25, "REGDATA": [21333, 20018, 12336, 12333, 14411, 21580, 11597, 12288, 0, 0, 0, 0, 0, 0, 0, 18518, 12848, 13616, 12592, 12340, 14640, 0, 0, 0, 0]},
    "MODBUS2": {"FUNCCODE": 3, "OFFSET": 0, "STARTREG": 30071, "NUMREGS": 12, "REGDATA": [2, 2, 0, 8000, 0, 8800, 0, 8800, 0, 5280, 65535, 60256]},
    "MODBUS3": {"FUNCCODE": 3, "OFFSET": 0, "STARTREG": 32000, "NUMREGS": 60, "REGDATA": [6, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 21136, 4499, 387, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
    "MODBUS4": {"FUNCCODE": 3, "OFFSET": 0, "STARTREG": 32060, "NUMREGS": 60, "REGDATA": [0, 0, 0, 0, 0, 1741, 4023, 4056, 4036, 2317, 2328, 2350, 0, 2438, 0, 2426, 0, 2446, 0, 3977, 0, 1696, 65535, 65533, 1000, 5018, 9741, 450, 3000, 512, 0, 26282, 61018, 65535, 65535, 0, 942, 0, 0, 0, 0, 0, 0, 0, 0, 0, 45, 28829, 46, 49302, 26282, 62803, 0, 193, 0, 646, 0, 646, 7, 37004]},
    "MODBUS5": {"FUNCCODE": 3, "OFFSET": 0, "STARTREG": 37100, "NUMREGS": 39, "REGDATA": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32767, 65535, 32767, 65535, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]},
    "MODBUS6": {"FUNCCODE": 3, "OFFSET": 0, "STARTREG": 40000, "NUMREGS": 2, "REGDATA": [26282, 62811]}
}

def write_modbus_data(client, slave_id, data):
    try:
        for modbus_block, params in data.items():
            start_reg = params["STARTREG"]  # Adjust for 0-based addressing
            reg_data = params["REGDATA"]
            num_regs = params["NUMREGS"]
            print(f"Writing to {modbus_block} (Slave ID: {slave_id}, Start Register: {params['STARTREG']}, Number of Registers: {num_regs})")
            
            # Write multiple registers using function code 16 (Preset Multiple Registers)
            result = client.write_registers(start_reg, reg_data, unit=slave_id)
            if result.isError():
                print(f"Error writing to {modbus_block}: {result}")
            else:
                print(f"Successfully wrote to {modbus_block}")
    except ModbusException as e:
        print(f"Modbus error: {e}")
    except Exception as e:
        print(f"General error: {e}")

def main():
    # Connect to Modbus TCP server
    client = ModbusTcpClient('127.0.0.1', port=502)
    try:
        if not client.connect():
            print("Failed to connect to Modbus server")
            return
        
        # Write to slave ID 1
        print("Writing to Slave ID 1...")
        write_modbus_data(client, 1, MODBUS_DATA)
        
        # Write to slave ID 2
        print("\nWriting to Slave ID 2...")
        write_modbus_data(client, 2, MODBUS_DATA)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()