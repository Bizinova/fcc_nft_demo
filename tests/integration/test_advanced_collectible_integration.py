from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    get_contract,
)
from brownie import AdvancedCollectible, network
import pytest
import time
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
from scripts.advanced_collectible.create_collectible import create_collectible


def test_can_create_advanced_collectible_integration():
    # deploy contract
    # create an NFT
    # get a random breed back
    # Arrange
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Only for integration testing")
    # Act
    advanced_collectible, creation_tx = deploy_and_create()
    time.sleep(60)
    # Assert
    assert advanced_collectible.tokenCounter() == 1
