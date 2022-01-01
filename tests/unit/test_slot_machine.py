from os import access
from brownie import network, exceptions
import pytest
from scripts.helpful_scripts import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract
from scripts.deploy import deploy_slot_machine

def test_set_price_feed_contract():
    #arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("test on local network only")
    account = get_account()
    non_owner = get_account(index=1)
    slot_machine, slot_chip = deploy_slot_machine()
    dai_token = get_contract("dai_token")

    #act
    price_feed_address = get_contract("dai_usd_price_feed")
    slot_machine.setPriceFeedContract(dai_token.address, price_feed_address, {"from": account})

    #assert
    assert slot_machine.tokenPriceFeedMapping(dai_token.address) == price_feed_address
    with pytest.raises(exceptions.VirtualMachineError):
        slot_machine.setPriceFeedContract(dai_token.address, price_feed_address, {"from": non_owner})

def test_get_slot_chip(amount_deposit):
    #arrange
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("test on local network only")
    account = get_account()
    slot_machine, slot_chip = deploy_slot_machine()
    dai_token = get_contract("dai_token")

    #act
    dai_token.approve(slot_machine.address, amount_deposit, {"from": account})
    slot_machine.getChip(amount_deposit, dai_token.address, {"from": account})

    #assert
    slot_chip.balanceOf(account, {"from": account}) > 0 
