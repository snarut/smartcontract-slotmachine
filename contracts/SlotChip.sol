// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

// TO DO:
// - Should this be pre-minted or only mint when player deposit

contract SlotChip is ERC20 {
    constructor() public ERC20("Slot Chip", "SLC") {
        
        _mint(msg.sender, 1000000 * 10**18);
    }
}