// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "./openzeppelin/token/ERC20/ERC20.sol";
import "./openzeppelin/access/Ownable.sol";

contract OriginToken is ERC20, Ownable {
    uint8 private _decimals;

    constructor(
        string memory name,
        string memory symbol,
        uint8 decimalsValue,               // Renamed to avoid shadowing
        uint256 initialSupply
    ) ERC20(name, symbol) Ownable(msg.sender) {
        _decimals = decimalsValue;         // Store the decimals value
        _mint(msg.sender, initialSupply);
    }

    function decimals() public view override returns (uint8) {
        return _decimals;                  // Return the correct value
    }
}

