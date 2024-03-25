from block import Block


class DodoCoin:
    def __init__(self):
        self.mem_pool = []
        self._genesis_block = None
        self.wallets = {}
        self.__create_genesis_block()


    def __create_genesis_block(self):
        self._genesis_block = Block(index=0, transactions=[], previous_block_hash=0, difficulty_level=1,
                              metadata='The Times 03/Jan/2009 Chancellor on brink of second bailout for banks Genesis '
                                       'block using same string as bitcoin!')
        self._genesis_block.generate_hash()

    @property
    def genesis_block(self):
        return self._genesis_block

    def register_wallet(self, friendly_name, public_key):
        self.wallets[friendly_name] = public_key

    def list_wallets(self):
        for key, value in self.wallets.items():
            print(f"{key} - {value}")

    def list_pending_transactions(self):
        for transaction in self.mem_pool:
            print(transaction)


if __name__ == "__main__":
    from dodocoin_2.node import Node
    from dodocoin_2.wallet import Wallet

    dodo = DodoCoin()
    node_1 = Node(dodo)

    sunil_wallet = Wallet("Sunil")
    harsh_wallet = Wallet("Harsh")

    dodo.register_wallet(sunil_wallet.user, sunil_wallet.public_key)
    dodo.register_wallet(harsh_wallet.user, harsh_wallet.public_key)
    dodo.list_wallets()

    transaction = sunil_wallet.initiate_transaction(harsh_wallet.user, 20)
    node_1.add_new_transaction(transaction)
    transaction = sunil_wallet.initiate_transaction(harsh_wallet.user, 30)
    node_1.add_new_transaction(transaction)
    dodo.list_pending_transactions()