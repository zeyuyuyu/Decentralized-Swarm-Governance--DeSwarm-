import hashlib
import random
import json
from typing import List, Dict

class Block:
    def __init__(self, index: int, timestamp: float, data: Dict, previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

class BlockChain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []
        self.nodes = set()

    def create_genesis_block(self) -> Block:
        return Block(0, 0.0, {}, '0')

    def add_block(self, block: Block) -> bool:
        if self.is_valid_block(block):
            self.chain.append(block)
            self.pending_transactions = []
            return True
        return False

    def is_valid_block(self, block: Block) -> bool:
        if block.index != len(self.chain):
            return False
        if block.previous_hash != self.chain[-1].hash:
            return False
        if block.hash != block.calculate_hash():
            return False
        return True

    def add_transaction(self, transaction: Dict) -> bool:
        self.pending_transactions.append(transaction)
        return True

    def mine_block(self, miner_address: str) -> Block:
        block = Block(len(self.chain), time.time(), self.pending_transactions, self.chain[-1].hash)
        if self.add_block(block):
            self.reward_miner(miner_address)
            return block
        return None

    def reward_miner(self, miner_address: str) -> bool:
        reward_transaction = {
            'from': 'system',
            'to': miner_address,
            'amount': 10
        }
        self.add_transaction(reward_transaction)
        return True

    def consensus(self) -> bool:
        longest_chain = self.chain
        for node in self.nodes:
            if len(node.chain) > len(longest_chain):
                longest_chain = node.chain
        if len(longest_chain) > len(self.chain):
            self.chain = longest_chain
            return True
        return False

    def add_node(self, node_address: str) -> bool:
        self.nodes.add(node_address)
        return True

    def vote(self, voter_address: str, proposal: str, vote: bool) -> bool:
        transaction = {
            'from': voter_address,
            'proposal': proposal,
            'vote': vote
        }
        self.add_transaction(transaction)
        return True

    def tally_votes(self, proposal: str) -> Dict[bool, int]:
        vote_counts = {}
        for tx in self.pending_transactions:
            if tx['proposal'] == proposal:
                vote_counts[tx['vote']] = vote_counts.get(tx['vote'], 0) + 1
        return vote_counts

    def finalize_proposal(self, proposal: str) -> bool:
        vote_counts = self.tally_votes(proposal)
        if max(vote_counts.values()) > sum(vote_counts.values()) / 2:
            self.mine_block({'proposal': proposal, 'result': max(vote_counts, key=vote_counts.get)})
            return True
        return False
