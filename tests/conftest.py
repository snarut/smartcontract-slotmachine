import pytest
from web3 import Web3

@pytest.fixture
def amount_deposit():
    return Web3.toWei(10, "ether")