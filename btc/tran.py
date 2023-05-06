from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import random

class Transaction:
    def __init__(self, sender, recipient, amount, fee):
        self.sender = sender          # 付款方
        self.recipient = recipient    # 收款方
        self.amount = amount          # 交易金额
        self.fee = fee                # 手续费

class TransactionRule:
    def __init__(self, max_amount, max_fee):
        self.max_amount = max_amount    # 单笔交易最大金额
        self.max_fee = max_fee          # 单笔交易最大手续费

    def is_valid_transaction(self, transaction):
        if transaction.amount > self.max_amount or transaction.fee > self.max_fee:
            return False
        return True

class EconomicRule:
    def __init__(self, wallets):
        self.wallets = wallets

    def select_wallets(self, num):
        wallets = sorted(self.wallets, key=lambda x: x.balance, reverse=True)
        return wallets[:num]

class TransactionPool:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def get_transactions(self):
        return self.transactions

class Wallet:
    def __init__(self, balance):
        self.private_key, self.public_key = self.generate_keys()
        self.address = self.get_address(self.public_key)
        self.balance = balance

    def generate_keys(self):
        rsa_key = RSA.generate(1024)
        private_key = rsa_key.export_key()
        public_key = rsa_key.publickey().export_key()
        return private_key, public_key

    def get_address(self, public_key):
        sha256_hash = SHA256.new(public_key)
        return sha256_hash.hexdigest()

    def sign_transaction(self, transaction):
        signer = PKCS1_v1_5.new(RSA.import_key(self.private_key))
        h = SHA256.new(str(transaction.sender).encode() + str(transaction.recipient).encode() +
                       str(transaction.amount).encode() + str(transaction.fee).encode())
        signature = signer.sign(h)
        return signature

    def verify_transaction(self, transaction):
        pubkey = RSA.import_key(self.public_key)
        rsa = PKCS1_v1_5.new(pubkey)
        h = SHA256.new(str(transaction.sender).encode() + str(transaction.recipient).encode() +
                       str(transaction.amount).encode() + str(transaction.fee).encode())
        try:
            rsa.verify(h, transaction.signature)
            return True
        except:
            return False

    def send(self, recipient, amount, fee):
        transaction = Transaction(self.address, recipient, amount, fee)
        if not transaction_rule.is_valid_transaction(transaction):
            return False
        if self.balance < amount + fee:
            return False
        transaction.signature = self.sign_transaction(transaction)
        transaction_pool.add_transaction(transaction)
        self.balance -= amount + fee
        return True

    def receive(self, transaction):
        if self.verify_transaction(transaction):
            if transaction.recipient == self.address:
                self.balance += transaction.amount
                return True
        return False

# 创建 5 个钱包对象，分别有不同的初始资产分布
wallet1 = Wallet(1000)
wallet2 = Wallet(500)
wallet3 = Wallet(300)
wallet4 = Wallet(200)
wallet5 = Wallet(100)

# 创建交易规则和经济学规则对象
transaction_rule = TransactionRule(100, 0.1)
economic_rule = EconomicRule([wallet1, wallet2, wallet3, wallet4, wallet5])

# 创建交易池对象
transaction_pool = TransactionPool()

# 进行 100 次交易模拟
for i in range(100):
    # 选择两个钱包对象进行交易
    wallets = economic_rule.select_wallets(2)
    sender = wallets[0]
    recipient = wallets[1]
    amount = random.randint(1, 100)
    fee = random.uniform(0.01, 0.1)
    # 发送交易
    if sender.send(recipient.address, amount, fee):
        print("Transaction sent:", sender.balance, recipient.balance)
    else:
        print("Invalid transaction")

# 输出每个钱包对象的最终资产余额
print("Wallet 1 balance:", wallet1.balance)
print("Wallet 2 balance:", wallet2.balance)
print("Wallet 3 balance:", wallet3.balance)
print("Wallet 4 balance:", wallet4.balance)
print("Wallet 5 balance:", wallet5.balance)

