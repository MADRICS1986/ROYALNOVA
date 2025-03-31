// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract RoyalnovaToken is ERC20 {
    constructor(address owner) ERC20("Royalnova Token", "RNX") {
        uint256 supply = 1_000_000 * 10 ** decimals();   // ✅ Correct total supply with decimals
        _mint(owner, supply);
    }
}

