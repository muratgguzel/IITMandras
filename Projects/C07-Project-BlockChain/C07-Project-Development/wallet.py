import json

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization


# Provides an interface to a user to participate in Dodocoin network
# It provides private and public keys to a user.
class Wallet:
    # Problem Statement 1.a
    # Add a new default parameter generate_key
    def __init__(self, user, node=None, generate_key=True):
        self.user = user
        self.__private_key = ''
        self.public_key = ''
        self.associated_node = node  # New attribute. Set during wallet creation. Or explicitly associated with a node

        # Problem Statement 1.a: Add new protected instance variable _generate_key
        self._generate_key = generate_key
        self.__generate_keys()

    def __generate_keys(self):
        # Problem Statement 1.a.i
        # Check if the _generate_key is True or not

        if (self._generate_key == True):
            self.__private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
            self.public_key = self.__private_key.public_key()
            # filename = self.user + "_private_key.pem"
            filename_new_private_key = self.user + "_private_key.pem"
            # def serialize_private_key_to_file(self, filename):
            # Serialize to file private key
            self.serialize_private_key_to_file(filename_new_private_key)
            # Serialize to file public key
            filename_new_public_key = self.user + "_public_key.pem"
            self.serialize_public_key_to_file(filename_new_public_key)
        #Getting keys from existing
        else:
            filename_private_key = self.user + "_private_key.pem"
            self.deserialize_private_key_from_file(filename_private_key)
            filename_public_key=self.user + "_public_key.pem"
            self.deserialize_public_key_from_file(filename_public_key)

    def initiate_transaction(self, receiver, coins):
        
        # Problem Statement 1.b
        # Check whether __private_key is valid or not
        if not self.__private_key:
            print("Private key not found. Transaction cannot be initiated")
            return
        
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
        # c. transaction. Now we are sending encrypted message
        new_transaction = {'sender': self.user,
                           "signature": signature,
                           "transaction_bytes": transaction_jsonified_to_bytes}
        # return new_transaction
        # Instead of returning the transaction, it will be passed to the associated node for validation.
        if self.associated_node:
            self.associated_node.add_new_transaction(new_transaction)
        else:
            return new_transaction
        
    def serialize_private_key(self):
        private_key_pem = self.__private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                           format=serialization.PrivateFormat.PKCS8,
                                                           encryption_algorithm=serialization.NoEncryption())

        filename = self.user + "_private_key.pem"
        with open(filename, 'wb') as fhandle:
            fhandle.write(private_key_pem)

    def serialize_public_key(self):
        public_key_pem = self.public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                      format=serialization.PublicFormat.SubjectPublicKeyInfo)

        filename = self.user + "_public_key.pem"
        with open(filename, 'wb') as fhandle:
            fhandle.write(public_key_pem)

    def deserialize_private_key(self):
        filename = self.user + "_private_key.pem"
        with open(filename, "rb") as fhandle:
            # Problem Statement 1.a.iii
            # Change the code below to initialise the private instance variable __private_key
            self.__private_key = serialization.load_pem_private_key(
                fhandle.read(),
                password=None
            )
            user=self.user
            Privatekey=self.__private_key
            print(f"{user}'s Deserialized Private Key = {Privatekey}")


    def deserialize_public_key(self):
        filename = self.user + "_public_key.pem"
        with open(filename, "rb") as fhandle:
            self.public_key = serialization.load_pem_public_key(
                fhandle.read()
            )
            user = self.user
            PublicKey = self.public_key
            print(f"{user}'s Deserialized Public Key = {PublicKey}")

    # Problem Statement 1.c.i
    # The function will accept a parameter “filename”
    # Use this filename to serialize the private key
    def serialize_private_key_to_file(self, filename):
        private_key_pem = self.__private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                           format=serialization.PrivateFormat.PKCS8,
                                                           encryption_algorithm=serialization.NoEncryption())

        with open(filename, 'wb') as fhandle:
            fhandle.write(private_key_pem)

    # Problem Statement 1.c.i
    # The function will accept a parameter “filename”
    # Use this filename to deserialize the private key
    def deserialize_private_key_from_file(self, filename):
        with open(filename, "rb") as fhandle:
            # Problem Statement 1.a.iii
            # Change the code below to initialise the private instance variable __private_key
            self.__private_key = serialization.load_pem_private_key(
                fhandle.read(),
                password=None
            )
            user = self.user
            Privatekey = self.__private_key
            print(f"{user}'s Deserialized Private Key = {Privatekey}")


        # Problem Statement 1.c.ii

    # The function will accept a parameter “filename”
    # Use this filename to serialize the public key
    def serialize_public_key_to_file(self, filename):
        public_key_pem = self.public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                      format=serialization.PublicFormat.SubjectPublicKeyInfo)

        with open(filename, 'wb') as fhandle:
            fhandle.write(public_key_pem)

    # Problem Statement 1.c.ii
    # The function will accept a parameter “filename”.
    # Use this filename to deserialize the public key
    def deserialize_public_key_from_file(self, filename):
          with open(filename, "rb") as fhandle:
            self.public_key = serialization.load_pem_public_key(
                fhandle.read()
            )
            user = self.user
            PublicKey = self.public_key
            print(f"{user}'s Deserialized Public Key = {PublicKey}")

    def assocate_with_node(self, node):
        self.associated_node = node


if __name__ == "__main__":
    from blockchain import DodoCoin
    from node import Node

    dodo = DodoCoin()
    node_1 = Node("Node_1", dodo)

    # Problem Statement 1.a 
    # Argument generate_key can be added 
    sunil_wallet = Wallet('Sunil', node_1)
    harsh_wallet = Wallet('Harsh', node_1)
    dodo.register_wallet(sunil_wallet.user, sunil_wallet.public_key)
    dodo.register_wallet(harsh_wallet.user, harsh_wallet.public_key)

    sunil_wallet.initiate_transaction("Harsh", 50)
    sunil_wallet.initiate_transaction("Harsh", 20)
    dodo.list_pending_transactions()

    sunil_wallet.serialize_private_key()
    sunil_wallet.deserialize_private_key()
    sunil_wallet.serialize_public_key()
    sunil_wallet.deserialize_public_key()
