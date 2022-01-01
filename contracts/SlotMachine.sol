// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

contract SlotMachine is Ownable {
    IERC20 public slotChip;
    address payable[] public players;
    mapping(address => uint256) public playersBet; // amount of slotchip player betting in current round

    address[] public allowedTokens;
    mapping(address => address) public tokenPriceFeedMapping;

    enum ReelSymbol {
        One, Two, Three, Four, Five, Six, Seven, Eight, Nine, Bar
    }

    constructor(address _slotChipAddress) {
        slotChip = IERC20(_slotChipAddress);
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

    function getChip(uint256 _amount, address _token) public {
        require(_amount > 0, "Amount must be more than 0.");
        require(tokenIsAllowed(_token), "Token is not allowed");

        IERC20(_token).transferFrom(msg.sender, address(this), _amount);
        // convert _amount to USD
        (uint256 price, uint256 decimals) = getTokenUSDValue(_token);
        uint256 amountInUSD = _amount*price/10**decimals;
        slotChip.transfer(msg.sender, amountInUSD);
    }

    function getTokenUSDValue(address _token) public view returns (uint256, uint256) {
        address priceFeedAddress = tokenPriceFeedMapping[_token];
        AggregatorV3Interface priceFeed = AggregatorV3Interface(priceFeedAddress);
        (,int256 price,,, ) = priceFeed.latestRoundData();
        uint256 decimals = priceFeed.decimals();
        return (uint256(price), decimals);
    }

    function spin(uint _amount) public returns (uint256, uint256, uint256, bool) {
        require(_amount > 0, "Amount must be more than 0");
        require(_amount <= slotChip.balanceOf(msg.sender), "Not enough slot chips");
        // transfer amount to contract
        slotChip.transferFrom(msg.sender, address(this), _amount);
        // update value in playersBalance and playersBet
        playersBet[msg.sender] = _amount;

        //pick random number
        uint256 nounce = 0;
        uint256 balance = slotChip.balanceOf(msg.sender);
        uint256 rand1 = uint256(keccak256(abi.encodePacked(block.timestamp, balance, nounce))) % 10;
        uint256 rand2 = uint256(keccak256(abi.encodePacked(block.timestamp, balance, nounce+1))) % 10;
        uint256 rand3 = uint256(keccak256(abi.encodePacked(block.timestamp, balance, nounce+2))) % 10;

        bool win = false;
        if (rand1 == rand2 && rand2 == rand3) { // winning
            slotChip.transfer(msg.sender, _amount + (_amount * 10));
            win = true;
        }

        return (rand1, rand2, rand3, win);
    }
}