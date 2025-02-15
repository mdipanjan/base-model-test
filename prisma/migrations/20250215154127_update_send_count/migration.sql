-- CreateTable
CREATE TABLE "Block" (
    "number" BIGINT NOT NULL,
    "hash" TEXT NOT NULL,
    "parent_hash" TEXT,
    "nonce" TEXT,
    "sha3_uncles" TEXT,
    "logs_bloom" TEXT,
    "transactions_root" TEXT,
    "state_root" TEXT,
    "receipts_root" TEXT,
    "miner" TEXT,
    "difficulty" BIGINT,
    "total_difficulty" BIGINT,
    "extra_data" TEXT,
    "size" BIGINT,
    "gas_limit" BIGINT,
    "gas_used" BIGINT,
    "timestamp" TIMESTAMP(3),
    "base_fee_per_gas" BIGINT,
    "blob_gas_used" BIGINT,
    "excess_blob_gas" BIGINT,
    "parent_beacon_block_root" TEXT,
    "withdrawals_root" TEXT,
    "withdrawals" JSONB,
    "l1_block_number" BIGINT,
    "send_count" TEXT,
    "send_root" TEXT,
    "mix_hash" TEXT,

    CONSTRAINT "Block_pkey" PRIMARY KEY ("number")
);

-- CreateIndex
CREATE UNIQUE INDEX "Block_hash_key" ON "Block"("hash");
