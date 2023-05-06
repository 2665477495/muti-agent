class CryptoCurrency:
    def __init__(self, name, symbol, total_supply, unit):
        self.name = name              # 货币名称
        self.symbol = symbol          # 货币符号
        self.total_supply = total_supply  # 初始发行量
        self.unit = unit              # 货币单位

class Account:
    def __init__(self):
        self.public_key = None        # 公钥
        self.private_key = None       # 私钥
        self.address = None           # 地址
        self.balance = 0              # 余额

class Transaction:
    def __init__(self, sender, recipient, amount, fee):
        self.sender = sender          # 付款方
        self.recipient = recipient    # 收款方
        self.amount = amount          # 交易金额
        self.fee = fee                # 手续费

import hashlib
import time

class Block:
    def __init__(self, data, prev_hash):
        self.timestamp = time.time()         # 时间戳
        self.data = data                     # 区块数据
        self.prev_hash = prev_hash           # 前一个区块的哈希值
        self.nonce = 0                       # 随机数
        self.hash = self.calculate_hash()    # 当前区块的哈希值

    def calculate_hash(self):
        data = str(self.timestamp) + str(self.data) + str(self.prev_hash) + str(self.nonce)
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def mine_block(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2

    def create_genesis_block(self):
        return Block("Genesis Block", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.prev_hash = self.get_latest_block().hash
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            prev_block = self.chain[i - 1]
            curr_block = self.chain[i]
            if curr_block.hash != curr_block.calculate_hash() or curr_block.prev_hash != prev_block.hash:
                return True
