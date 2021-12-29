from brownie import SlotMachine, SlotChip, network, config
from scripts.helpful_scripts import get_account, get_contract

def deploy_slot_machine():
    account = get_account()
    slot_chip = SlotChip.deploy({"from": account})
    slot_machine = SlotMachine.deploy(slot_chip.address,  {"from": account})
    transfer_slot_chip_tx = slot_chip.transfer(slot_machine.address, slot_chip.totalSupply())
    transfer_slot_chip_tx.wait(1)
    print(f"SlotMachine deployed at {slot_machine.address}")

    dai_token = get_contract("dai_token")
    dict_of_tokens_and_its_price_feed = {
        dai_token: get_contract("dai_usd_price_feed"),
    }
    add_allowed_tokens(slot_machine, dict_of_tokens_and_its_price_feed, account)

    return slot_machine, slot_chip

def add_allowed_tokens(slot_machine, dict_of_tokens_and_its_price_feed, account):
    for token in dict_of_tokens_and_its_price_feed:
        add_token_tx = slot_machine.addAllowedTokens(token.address, {"from": account})
        add_token_tx.wait(1)
        set_pf_tx = slot_machine.setPriceFeedContract(token.address, dict_of_tokens_and_its_price_feed[token], {"from": account})
        set_pf_tx.wait(1)

def main():
    deploy_slot_machine()