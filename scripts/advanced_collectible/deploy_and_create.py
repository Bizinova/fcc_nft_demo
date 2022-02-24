from scripts.helpful_scripts import (
    fund_with_link,
    get_account,
    OPENSEA_URL,
    config,
    network,
    get_contract,
)
from brownie import AdvancedCollectible, network, config


def deploy_and_create():
    # grab account
    account = get_account()
    # Deploy contract
    # OpenSea only works with Rinkeby
    advanced_collectible = AdvancedCollectible.deploy(
        get_contract("vrfCoordinator"),
        get_contract("linkToken"),
        config["networks"][network.show_active()]["keyhash"],
        config["networks"][network.show_active()]["fee"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    # Fund contract with Link
    fund_with_link(advanced_collectible.address)
    # Create collectible
    creating_tx = advanced_collectible.createCollectible({"from": account})
    creating_tx.wait(1)
    print("New token has been created")
    return advanced_collectible, creating_tx


def main():
    deploy_and_create()
