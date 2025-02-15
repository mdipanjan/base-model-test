import hypersync
import asyncio
import json
from hypersync import BlockField, JoinMode, TransactionField, LogField, ClientConfig
from prisma import Prisma
from datetime import datetime

async def main():

    db = Prisma()
    await db.connect()

    client = hypersync.HypersyncClient(ClientConfig())

    # The query to run
    query = hypersync.Query(
        from_block=20224332,
        to_block=20224333,
        include_all_blocks=True,
        join_mode=JoinMode.JOIN_ALL,
        field_selection=hypersync.FieldSelection(
            block=[
                BlockField.NUMBER,
                BlockField.TIMESTAMP, 
                BlockField.HASH,
                BlockField.PARENT_HASH,
                BlockField.NONCE,
                BlockField.SHA3_UNCLES,
                BlockField.LOGS_BLOOM,
                BlockField.TRANSACTIONS_ROOT,
                BlockField.STATE_ROOT,
                BlockField.RECEIPTS_ROOT,
                BlockField.MINER,
                BlockField.DIFFICULTY,
                BlockField.TOTAL_DIFFICULTY,
                BlockField.EXTRA_DATA,
                BlockField.SIZE,
                BlockField.GAS_LIMIT,
                BlockField.GAS_USED,
                BlockField.BASE_FEE_PER_GAS,
                BlockField.BLOB_GAS_USED,
                BlockField.EXCESS_BLOB_GAS,
                BlockField.PARENT_BEACON_BLOCK_ROOT,
                BlockField.WITHDRAWALS_ROOT,
                BlockField.WITHDRAWALS,
                BlockField.L1_BLOCK_NUMBER,
                BlockField.SEND_COUNT,
                BlockField.SEND_ROOT,
                BlockField.MIX_HASH,
            ],
        ),
    )

    print("Running the query...")

    res = await client.get(query)

    print(f"Ran the query once. Next block to query is {res.next_block}")

    def safe_hex_to_int(value):
        """Convert hex string to integer safely"""
        if value is None:
            return None
        try:
            return int(value, 16) if isinstance(value, str) and value.startswith("0x") else int(value)
        except ValueError:
            return None
    def safe_hex_to_str(value):
        """Convert hex string to a string representation of an integer safely"""
        if value is None:
            return None
        try:
            return str(int(value, 16)) if isinstance(value, str) and value.startswith("0x") else str(value)
        except ValueError:
            return None
    def safe_large_number(value):
        """Ensure large numbers are stored as strings to prevent overflow"""
        if value is None:
            return None
        try:
            return str(value)  # Convert to string to avoid BigInt overflow
        except ValueError:
            return None




    for block in res.data.blocks:
        print(f"Inserting Block {block.number} into database...")
        print(block.timestamp)
        # withdrawals_list = [
        #     {
        #         "index": withdrawal.index,
        #         "validator_index": withdrawal.validator_index,
        #         "address": withdrawal.address,
        #         "amount": safe_hex_to_int(withdrawal.amount),
        #     }
        #     for withdrawal in block.withdrawals
        # ] if block.withdrawals else None

        # withdrawals_json = json.dumps(withdrawals_list) if withdrawals_list else None

        # difficulty = safe_hex_to_str(block.difficulty)
        # total_difficulty = safe_hex_to_str(block.total_difficulty)
        # size = safe_hex_to_str(block.size)
        # gas_limit = safe_hex_to_str(block.gas_limit)
        # gas_used = safe_hex_to_str(block.gas_used)
        # base_fee_per_gas = safe_hex_to_str(block.base_fee_per_gas)
        # blob_gas_used = safe_hex_to_str(block.blob_gas_used)
        # excess_blob_gas = safe_hex_to_str(block.excess_blob_gas)
        # l1_block_number = safe_hex_to_str(block.l1_block_number)
        
        send_count = safe_large_number(block.send_count)
        timestamp_int = int(block.timestamp, 16) if isinstance(block.timestamp, str) and block.timestamp.startswith("0x") else block.timestamp
        timestamp_dt = datetime.utcfromtimestamp(timestamp_int)
        size_int = int(block.size, 16) if isinstance(block.size, str) and block.size.startswith("0x") else block.size
        base_fee_per_gas_int = int(block.base_fee_per_gas, 16) if isinstance(block.base_fee_per_gas, str) and block.base_fee_per_gas.startswith("0x") else block.base_fee_per_gas
        gas_used_int = int(block.gas_used, 16) if isinstance(block.gas_used, str) and block.gas_used.startswith("0x") else block.gas_used
        gas_limit_int = int(block.gas_limit, 16) if isinstance(block.gas_limit, str) and block.gas_limit.startswith("0x") else block.gas_limit
        blob_gas_used_int = int(block.blob_gas_used, 16) if isinstance(block.blob_gas_used, str) and block.blob_gas_used.startswith("0x") else block.blob_gas_used
        excess_blob_gas_int = int(block.excess_blob_gas, 16) if isinstance(block.excess_blob_gas, str) and block.excess_blob_gas.startswith("0x") else block.excess_blob_gas
        
        # send_count = int(block.send_count, 16) if isinstance(block.send_count, str) and block.send_count.startswith("0x") else block.send_count

        await db.block.create(
            data={
                'number': str(block.number),
                'hash': block.hash,
                'parent_hash': block.parent_hash,
                'nonce': block.nonce,   
                'sha3_uncles': block.sha3_uncles,
                'transactions_root': block.transactions_root,
                'state_root': block.state_root,                'miner': block.miner,                
                'extra_data': block.extra_data,
                'size': size_int,
                'gas_limit': gas_limit_int,
                'gas_used': gas_used_int,
                'timestamp': timestamp_dt,  # ✅ Now in correct DateTime format
                'base_fee_per_gas': base_fee_per_gas_int,
                'blob_gas_used': blob_gas_used_int,
                'excess_blob_gas': excess_blob_gas_int, 
                'send_count': send_count,
                'send_root': block.send_root,
                'mix_hash': block.mix_hash,
                # 'logs_bloom': block.logs_bloom,
                # 'receipts_root': block.receipts_root,
                # 'parent_beacon_block_root': block.parent_beacon_block_root,
                # 'withdrawals_root': block.withdrawals_root,
                # 'withdrawals': withdrawals_json,  # Store as JSON
                # 'l1_block_number': str(block.l1_block_number) if block.l1_block_number else None,
                # 'difficulty': str(block.difficulty),  # Convert BigInt fields to str
                # 'total_difficulty': str(block.total_difficulty),  # Convert BigInt fields to str

            }
        )


    print(f"Inserted {len(res.data.blocks)} blocks into the database.")
    
    await db.disconnect()

asyncio.run(main())
