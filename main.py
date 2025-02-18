import hypersync
import asyncio
import json
import time
import logging
import datetime
from hypersync import BlockField, JoinMode, TransactionField, LogField, ClientConfig, TransactionSelection
from prisma import Prisma
from datetime import datetime
from tqdm.auto import tqdm

# Set up logging
logger = logging.getLogger(__name__)
fmt = "%(filename)-20s:%(lineno)-4d %(asctime)s %(message)s"
logging.basicConfig(level=logging.INFO, format=fmt,
                   handlers=[logging.StreamHandler()])

async def main():
    db = Prisma()
    await db.connect()

    client = hypersync.HypersyncClient(ClientConfig(
        url="https://base.hypersync.xyz",
    ))  
    height = await client.get_height()
    start_block = height - 80000
    total_blocks = height - start_block

    # The query to run
    query = hypersync.Query(
        from_block=start_block,
        to_block=height,
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

    print(f"Starting the stream from block {start_block} to {height}...")
    start_time = time.time()
    
    config = hypersync.StreamConfig(
        hex_output=hypersync.HexOutput.PREFIXED,
        batch_size=1000000,
    )

    # Start the stream
    receiver = await client.stream(query, config)
    
    total_processed_blocks = 0
    total_transactions = 0

    with tqdm(total=total_blocks, desc="Processing blocks", unit="blocks") as pbar:
        while True:
            res = await receiver.recv()
            
            # exit if the stream finished
            if res is None:
                break

            blocks_in_batch = len(res.data.blocks)
            total_processed_blocks += blocks_in_batch
            total_transactions += len(res.data.transactions)

            # Update progress bar
            pbar.update(blocks_in_batch)
            pbar.set_postfix({
                "Current height": res.next_block,
                "Transactions": total_transactions
            })

    # Store the data in parquet format after streaming is complete
    await client.collect_parquet("data", query, config)

    end_time = time.time()
    duration = end_time - start_time

    print("\nStream completed!")
    print(f"Total time taken: {duration:.2f} seconds")
    print(f"Total blocks processed: {total_processed_blocks}")
    print(f"Total transactions processed: {total_transactions}")

    await db.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
