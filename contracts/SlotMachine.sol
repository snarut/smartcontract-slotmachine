// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract SlotMachine is Ownable {
    IERC20 public slotChip;
    address payable[] public players;
    mapping(address => uint256) public playersBet;

    address[] public allowedTokens;
    mapping(address => address) public tokenPriceFeedMapping;

    constructor(address _slotChipAddress) {
        slotChip = IERC20(_slotChipAddress);
    }

    function getChip(uint256 _amount, address _token) public {
        require(_amount > 0, "Amount must be more than 0.");
        require(tokenIsAllowed(_token), "Token is not allowed");

        IERC20(_token).transferFrom(msg.sender, address(this), _amount);
        slotChip.transfer(msg.sender, _amount);
    }

    function addAllowedTokens(address _token) public onlyOwner {
        allowedTokens.push(_token);
    }

    function setPriceFeedContract(address _token, address _priceFeed) public onlyOwner {
        tokenPriceFeedMapping[_token] = _priceFeed;
    }

    function tokenIsAllowed(address _token) public returns (bool) {
        for(uint256 i=0; i < allowedTokens.length; i++) {
            if (allowedTokens[i] == _token) {
                return true;
            }
        }
        return false;
    }
}