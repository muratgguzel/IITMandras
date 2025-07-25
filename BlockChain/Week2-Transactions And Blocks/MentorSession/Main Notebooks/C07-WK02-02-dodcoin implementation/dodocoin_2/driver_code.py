from blockchain import DodoCoin
from wallet import Wallet
from node import Node

dodo = DodoCoin()

node_1 = Node(dodo)

peter_wallet = Wallet('Peter')
tony_wallet = Wallet('Tony')
strange_wallet = Wallet('Strange')
bruce_wallet = Wallet('Bruce')
steve_wallet = Wallet('Steve')
carol_wallet = Wallet('Carol')
scarlet_wallet = Wallet('Scarlet')
nebula_wallet = Wallet('Nebula')
natasha_wallet = Wallet("Natasha")
shuri_wallet = Wallet('Shuri')

# Register each wallet with Blockchain
dodo.register_wallet(peter_wallet.user, peter_wallet.public_key)
dodo.register_wallet(tony_wallet.user, tony_wallet.public_key)
dodo.register_wallet(strange_wallet.user, strange_wallet.public_key)
dodo.register_wallet(bruce_wallet.user, bruce_wallet.public_key)
dodo.register_wallet(steve_wallet.user, steve_wallet.public_key)
dodo.register_wallet(carol_wallet.user, carol_wallet.public_key)
dodo.register_wallet(scarlet_wallet.user, scarlet_wallet.public_key)
dodo.register_wallet(nebula_wallet.user, nebula_wallet.public_key)
dodo.register_wallet(natasha_wallet.user, natasha_wallet.public_key)
dodo.register_wallet(shuri_wallet.user, shuri_wallet.public_key)

# Show list of registered wallets.
print("\nList of registered wallets.")
dodo.list_wallets()

transaction = peter_wallet.initiate_transaction(tony_wallet.user, 20)
node_1.add_new_transaction(transaction)
transaction = peter_wallet.initiate_transaction(bruce_wallet.user, 25)
node_1.add_new_transaction(transaction)
transaction = tony_wallet.initiate_transaction(bruce_wallet.user, 50)
node_1.add_new_transaction(transaction)
transaction = bruce_wallet.initiate_transaction(peter_wallet.user, 50)
node_1.add_new_transaction(transaction)
print("\nList of pending transactions.")
dodo.list_pending_transactions()
node_1.create_new_block()

transaction = scarlet_wallet.initiate_transaction(peter_wallet.user, 25)
node_1.add_new_transaction(transaction)
transaction = carol_wallet.initiate_transaction(steve_wallet.user, 50)
node_1.add_new_transaction(transaction)
transaction = steve_wallet.initiate_transaction(bruce_wallet.user, 50)
node_1.add_new_transaction(transaction)

node_1.create_new_block()
print("\nPrinting blockchain.")
node_1.show_chain()


