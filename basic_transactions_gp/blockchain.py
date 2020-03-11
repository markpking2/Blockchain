# Paste your version of blockchain.py from the client_mining_p
# folder here

import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request
from flask_cors import CORS


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Create a new Block in the Blockchain

        A block should have:
        * Index
        * Timestamp
        * List of current transactions
        * The proof used to mine this block
        * The hash of the previous block

        :param proof: <int> The proof given by the Proof of Work algorithm
        :param previous_hash: (Optional) <str> Hash of previous Block
        :return: <dict> New Block
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1])
        }

        # Reset the current list of transactions
        self.current_transactions = []

        # Append the block to the chain
        self.chain.append(block)

        # Return the new block
        return block

    def hash(self, block):
        """
        Creates a SHA-256 hash of a Block

        :param block": <dict> Block
        "return": <str>
        """

        # Use json.dumps to convert json into a string
        # Use hashlib.sha256 to create a hash
        # It requires a `bytes-like` object, which is what
        # .encode() does.
        # It converts the Python string into a byte string.
        # We must make sure that the Dictionary is Ordered,
        # or we'll have inconsistent hashes

        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        hash_object = hashlib.sha256(block_string)
        hash_string = hash_object.hexdigest()

        # By itself, the sha256 function returns the hash in a raw string
        # that will likely include escaped characters.
        # This can be hard to read, but .hexdigest() converts the
        # hash to a string of hexadecimal characters, which is
        # easier to work with and understand

        return hash_string

    def new_transaction(self, sender, recipient, amount):
        # Create a method in the `Blockchain` class called `new_transaction` that adds a new transaction to the list of transactions:

        #   :param sender: <str> Address of the Recipient
        #   :param recipient: <str> Address of the Recipient
        #   :param amount: <int> Amount
        #   :return: <int> The index of the `block` that will hold this transaction
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }

        self.current_transactions.append(transaction)
        index = len(self.chain) + 1

        return index

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def valid_proof(block_string, proof):
        """
        Validates the Proof:  Does hash(block_string, proof) contain 3
        leading zeroes?  Return true if the proof is valid
        :param block_string: <string> The stringified block to use to
        check in combination with `proof`
        :param proof: <int?> The value that when combined with the
        stringified previous block results in a hash that has the
        correct number of leading zeroes.
        :return: True if the resulting hash is a valid proof, False otherwise
        """
        # return True or False
        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:5] == '0' * 5


# Instantiate our Node
app = Flask(__name__)
cors = CORS(app)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['POST'])
def mine():
    # Modify the `mine` endpoint to create a reward via a `new_transaction`
    # for mining a block:

    #     * The sender is "0" to signify that this node created a new coin
    #     * The recipient is the id of the miner
    #     * The amount is 1 coin as a reward for mining the next block

    data = request.get_json()
    # print(data)

    required_properties = ['id', 'proof']

    if all(k in data for k in required_properties):
        string_object = json.dumps(blockchain.last_block, sort_keys=True)
        if blockchain.valid_proof(string_object, data['proof']):
            blockchain.new_transaction('0', data['id'], 1)

            previous_hash = blockchain.hash(blockchain.last_block)
            block = blockchain.new_block(data['proof'], previous_hash)

            response = {
                'message': 'New Block Forged',
                'index': block['index'],
                'transactions': block['transactions'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']
            }

            return jsonify(response), 200
        else:
            response = {'message': 'Proof is invalid or already submitted'}
    else:
        response = {'message': 'Please submit both proof and id'}

    return jsonify(response), 400


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/last_block', methods=['GET'])
def last_block():
    return jsonify(blockchain.last_block), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    #   * use `request.get_json()` to pull the data out of the POST
    #   * check that 'sender', 'recipient', and 'amount' are present
    #       * return a 400 error using `jsonify(response)` with a 'message'
    #   * upon success, return a 'message' indicating index of the block
    #     containing the transaction
    data = request.get_json()
    print(data)

    required_properties = ['sender', 'recipient', 'amount']

    if all(k in data for k in required_properties):
        index = blockchain.new_transaction(
            data['sender'], data['recipient'], data['amount'])

        response = {
            'message': f'Transaction added to block {index}'}
        return jsonify(response), 201
    else:
        response = {'message': 'Please submit sender, recipient, and amount'}

    return jsonify(response), 400


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
