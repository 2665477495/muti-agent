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
        self.address, self.private_key = self.generate_key_pair()
        self.balance = balance

    def generate_key_pair(self):
        key_pair = RSA.generate(2048)
        private_key = PKCS1_v1_5.new(key_pair)
        public_key = key_pair.publickey()
        return (public_key.exportKey(), private_key)

    def send(self, recipient, amount, fee):
        if self.balance >= amount + fee:
            transaction = Transaction(self.address, recipient, amount, fee)
            transaction.sign(self.private_key)
            if transaction.is_valid():
                self.balance -= amount + fee
                recipient.receive(amount)
                transaction_pool.add_transaction(transaction)
                return True
        return False

    def receive(self, amount):
        self.balance += amount

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
# 进行 100 次交易模拟
for i in range(100):
    # 选择两个钱包对象进行交易
    wallets = economic_rule.select_wallets(2)
    sender = wallets[0]
    recipient = wallets[1]
    # 生成交易金额和手续费
    max_amount = min(sender.balance - transaction_rule.min_fee, recipient.balance)
    if max_amount <= 0:
        continue
    amount = random.randint(1, max_amount)
    fee = random.uniform(transaction_rule.min_fee, transaction_rule.max_fee)
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

