from scripts.helpful_scripts import (
    get_account,
    OPENSEA_URL,
    fund_with_link,
)
from brownie import AdvancedCollectible, network, config
from web3 import Web3


def create_collectible():
    # grab account
    account = get_account()
    advanced_collectible = AdvancedCollectible[-1]
    fund_with_link(advanced_collectible.address, amount=Web3.toWei(0.1, "ether"))
    creation_tx = advanced_collectible.createCollectible({"from": account})
    creation_tx.wait(1)
    print("Collectible created!")


def main():
    create_collectible()
