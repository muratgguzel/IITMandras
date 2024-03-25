import json

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding


class Wallet:
    def __init__(self, user):
        self.user = user
        self.__private_key = ''
        self.public_key = ''
        self.__generate_keys()

    def __generate_keys(self):
        self.__private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        self.public_key = self.__private_key.public_key()

    def initiate_transaction(self, receiver, coins):
        transaction = {'sender': self.user, "receiver": receiver, "coins": coins}

        # This function digitally signs a transaction.
        # This has the following steps
        # 1. We convert the dictionary which contains transaction details to a string
        # For this we convert this to a JSON string.
        transaction_jsonified = json.dumps(transaction)
        # print(transaction_jsonified)
        # 2. Change this string to a byte stream. Call the function encode() to encode the string in utf-8 format
        transaction_jsonified_to_bytes = transaction_jsonified.encode()
        # print(transaction_jsonified_to_bytes)
        # 3. Digitally sign the transaction
        signature = self.__private_key.sign(transaction_jsonified_to_bytes,
                                            padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                                        salt_length=padding.PSS.MAX_LENGTH),
                                            hashes.SHA256())
        # 4. Structure the information and pass is back to the caller.
        # This structure will be passed to node for verification.
        # On successful verification, this transaction will be added to the mem_pool
        # a. Sender details. We will use this to pick the public key of sender and validate the transaction
        # b. Signature. Of the transaction
        # c. transaction. Here we are sending transaction data as plain text

        new_transaction = {'sender': self.user,
                           "signature": signature,
                           "transaction_bytes": transaction_jsonified_to_bytes}
        return new_transaction


if __name__ == "__main__":
    test_wallet = Wallet("Test")
    print(test_wallet.public_key)

    transaction = test_wallet.initiate_transaction("Sunil", 50)
    print(transaction)

