import hypersync
import asyncio
from hypersync import BlockField, JoinMode, TransactionField, LogField, ClientConfig

async def main():
    client = hypersync.HypersyncClient(ClientConfig())

    # The query to run
    query = hypersync.Query(
        # only get block 20224332
		from_block=20224332,
        to_block=20224333,
        include_all_blocks=True,
        join_mode=JoinMode.JOIN_ALL,
        field_selection=hypersync.FieldSelection(
            block=[
                BlockField.NUMBER,
                BlockField.TIMESTAMP, 
                BlockField.HASH,
                BlockField.NONCE,
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
                BlockField.UNCLES,
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
                TransactionField.GAS_PRICE,
                TransactionField.GAS_USED,			]
		),

    )

    print("Running the query...")

    # Run the query once, the query is automatically paginated so it will return when it reaches some limit (time, response size etc.)
    # there is a next_block field on the response object so we can set the from_block of our query to this value and continue our query until
    # res.next_block is equal to res.archive_height or query.to_block in case we specified an end block.
    res = await client.get(query)

    print(f"Ran the query once.  Next block to query is {res.next_block}")
    for block in res.data.blocks:
        print("Block Details:")
        print(block.number)
        print(block.hash)
        print(block.parent_hash)
        print(block.nonce)
        print(block.sha3_uncles)
        print(block.logs_bloom)
        print(block.transactions_root)
        print(block.state_root)
        print(block.receipts_root)
        print(block.miner)
        print(block.difficulty)
        print(block.total_difficulty)
        print(block.extra_data)
        print(block.size)
        print(block.gas_limit)
        print(block.gas_used)
        print(block.timestamp)
        print(block.uncles)
        print(block.base_fee_per_gas)
        print(block.blob_gas_used)
        print(block.excess_blob_gas)
        print(block.parent_beacon_block_root)
        print(block.withdrawals_root)
        print(block.withdrawals)
        print(block.l1_block_number)
        print(block.send_count)
        print(block.send_root)
        print(block.mix_hash)
        print(block)
    print(len(res.data.transactions))
    print(len(res.data.logs))

asyncio.run(main())