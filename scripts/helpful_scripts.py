from brownie import network, config, accounts, Contract, VRFCoordinatorMock, LinkToken

FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev2"]
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local-two"]
OPENSEA_URL = "https://testnets.opensea.io/assets/{}/{}"
BREED_MAPPING = {0: "PUG", 1: "SHIBA_INU", 2: "ST_BERNARD"}


def get_breed(breed_number):
    return BREED_MAPPING[breed_number]


def get_account(index=None, id=None):
    # method 1 - local chain: accounts[0]
    # method 2 - env variable: accounts.add("env")
    # method 3 - cmd line native: accounts.load("id")
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "vrfCoordinator": VRFCoordinatorMock,
    "linkToken": LinkToken,
}


def get_contract(contract_name):
    """ "This function will grab the contract addresses from the brownie config
    if defined, otherwise, it will deploy a mock version of that contract, and return
    that mock contract.

        Args:
            contract_name (string)

        Returns:
            brownie.network.contract.ProjectContract: the most recently deployed
            version of this contract.

    """
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            # MockV3Aggregator.length which checks if a mock has prev been deployed
            deploy_mocks()
        contract = contract_type[-1]
        # MockV3Aggregator[-1], aka get most recent version of deployed contract
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # address: shown above
        # abi: VRFCoordinatorMock.abi
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
    return contract


def deploy_mocks():
    """
    Use this script if you want to deploy mocks to a testnet
    """
    print(f"The active network is {network.show_active()}")
    print("Deploying mocks...")
    account = get_account()
    print("Deploying Mock Link Token")
    link_token = LinkToken.deploy({"from": account})
    print(f"Link Token deployed to {link_token.address}")
    print("Deploying Mock Link Token")
    vrf_coordinator = VRFCoordinatorMock.deploy(LinkToken[-1], {"from": account})
    print(f"Link Token deployed to {link_token.address}")
    print("Deployed!")


def fund_with_link(
    contract_address, account=None, link_token=None, amount=10_000_000_000_000_000_000
):  # 0.1 Link
    # use the account passed thru, otherwise get_account
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("linkToken")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    # another way to create contracts and interact, don't need deploy contract cause interfaces compiles ABI
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print(f"Funded Contract {contract_address} with link!")
    return tx
