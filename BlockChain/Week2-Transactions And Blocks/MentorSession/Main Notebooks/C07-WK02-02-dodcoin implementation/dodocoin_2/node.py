from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
import json

from block import Block


class Node:
    def __init__(self, dodocoin):
        self.cryptocurrency = dodocoin
        self._chain = []
        self._get_chain()

    def _get_chain(self):
        self._chain.append(self.cryptocurrency.genesis_block)

    def __str__(self):
        return f'Chain:\n{self._chain}'

    def create_new_block(self):
        new_block = Block(index=len(self._chain), transactions=self.cryptocurrency.mem_pool,
                          previous_block_hash=self._chain[-1].block_hash, metadata='')

        new_block.generate_hash()
        self._chain.append(new_block)
        self.cryptocurrency.mem_pool = []
        return new_block

    def show_chain(self):
        for chain_block in self._chain:
            print(chain_block)

    def add_new_transaction(self, transaction):
        try:
            self._validate_transaction(transaction)
        except InvalidSignature as e:
            print("Invalid signature. Cannot add this transaction")
            return

        if self._validate_receiver(transaction):
            transaction_bytes = transaction['transaction_bytes']
            transaction_data = json.loads(transaction_bytes)
            self.cryptocurrency.mem_pool.append(transaction_data)

    def _validate_transaction(self, transaction):
        sender_public_key = self.cryptocurrency.wallets[transaction['sender']]
        signature = transaction['signature']
        transaction_bytes = transaction['transaction_bytes']
        sender_public_key.verify(signature, transaction_bytes,
                                 padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                                 hashes.SHA256())

    def _validate_receiver(self, transaction):
        transaction_bytes = transaction['transaction_bytes']
        transaction_data = json.loads(transaction_bytes)
        # print(transaction_data)
        if transaction_data['receiver'] in self.cryptocurrency.wallets:
            return True
        return False

if __name__ == "__main__":
    from blockchain import DodoCoin
    from wallet import Wallet

    dodo = DodoCoin()
    node_1 = Node(dodo)
    node_1.show_chain()

    sunil_wallet = Wallet("Sunil")
    harsh_wallet = Wallet("Harsh")

    dodo.register_wallet(sunil_wallet.user, sunil_wallet.public_key)
    dodo.register_wallet(harsh_wallet.user, harsh_wallet.public_key)

    transaction = sunil_wallet.initiate_transaction(harsh_wallet.user, 20)
    node_1.add_new_transaction(transaction)
    transaction = sunil_wallet.initiate_transaction(harsh_wallet.user, 30)
    node_1.add_new_transaction(transaction)
    dodo.list_pending_transactions()
    node_1.create_new_block()
    node_1.show_chain()