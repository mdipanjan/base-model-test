import hypersync
import asyncio
import json
from hypersync import BlockField, JoinMode, TransactionField, LogField, ClientConfig, TransactionSelection
from prisma import Prisma
from datetime import datetime

async def main():

    db = Prisma()
    await db.connect()

    client = hypersync.HypersyncClient(ClientConfig(
        url="https://base.hypersync.xyz",
    ))
    height = await client.get_height()


    # The query to run
    query = hypersync.Query(
        from_block =  height - 1000000,
        to_block = height,
        include_all_blocks=True,
        join_mode=JoinMode.JOIN_ALL,
        transactions=[TransactionSelection()],
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
            transaction=[
                TransactionField.BLOCK_NUMBER,
                TransactionField.HASH,
                TransactionField.FROM,
                TransactionField.TO,
                TransactionField.VALUE,
                TransactionField.GAS,
                TransactionField.GAS_PRICE,
                TransactionField.EFFECTIVE_GAS_PRICE,
                TransactionField.MAX_PRIORITY_FEE_PER_GAS,
                TransactionField.INPUT,
                TransactionField.NONCE,
                TransactionField.MAX_FEE_PER_GAS,
                TransactionField.CUMULATIVE_GAS_USED,
                TransactionField.GAS_USED,
                TransactionField.CHAIN_ID,
                TransactionField.STATUS,
                TransactionField.TRANSACTION_INDEX,
                TransactionField.BLOCK_HASH
                
            ],
            
       
        ),
        
    )

    print("Running the query...")
    config = hypersync.StreamConfig(
        hex_output=hypersync.HexOutput.PREFIXED,
        batch_size=1000000,
    )
   


    await client.collect_parquet("data", query, config)


  

asyncio.run(main())
