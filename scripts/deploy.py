from brownie import SlotMachine, SlotChip, network, config
from scripts.helpful_scripts import get_account, get_contract
from web3 import Web3

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

    approve_tx = dai_token.approve(slot_machine.address, Web3.toWei(100, "ether"), {"from": account})
    approve_tx.wait(1)
    get_chip_tx = slot_machine.getChip(100, dai_token.address, {"from": account})
    get_chip_tx.wait(1)
    chip_received = slot_chip.balanceOf(account, {"from": account})
    print(f"Got slot chip: {chip_received}")
    slot_chip.approve(slot_machine.address, chip_received, {"from": account})

    while True:
        spin_tx = slot_machine.spin(1, {"from": account})
        spin_tx.wait(1)
        values = spin_tx.return_value
        win = values[3]
        current_chip = slot_chip.balanceOf(account, {"from": account})
        print(f"{values[0]} {values[1]} {values[2]}")
        if win:
            print(f"You won!!! Your balance is {current_chip}")
            break
        else:
            print(f"Sorry, you lose. Your balance is {current_chip}")
            if current_chip <= 0:
                break



    return slot_machine, slot_chip

def add_allowed_tokens(slot_machine, dict_of_tokens_and_its_price_feed, account):
    for token in dict_of_tokens_and_its_price_feed:
        add_token_tx = slot_machine.addAllowedTokens(token.address, {"from": account})
        add_token_tx.wait(1)
        set_pf_tx = slot_machine.setPriceFeedContract(token.address, dict_of_tokens_and_its_price_feed[token], {"from": account})
        set_pf_tx.wait(1)

def main():
    deploy_slot_machine()