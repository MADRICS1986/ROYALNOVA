// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "forge-std/Test.sol";
import "../src/RoyalnovaToken.sol";

contract RoyalnovaTokenTest is Test {
    RoyalnovaToken public token;
    address public owner = address(0x1);
    address public recipient = address(0x2);
    address public spender = address(0x3);

    /// @dev Deploys the token contract before each test
    function setUp() public {
        token = new RoyalnovaToken(owner);
        
        // ✅ Transfer 5,000 tokens to recipient
        vm.startPrank(owner);
        token.transfer(recipient, 5_000 * 10 ** token.decimals());
        vm.stopPrank();
    }

    /// @dev Test the initial supply
    function testInitialSupply() public {
        uint256 initialSupply = 1_000_000 * 10 ** token.decimals();
        uint256 expectedOwnerBalance = initialSupply - (5_000 * 10 ** token.decimals());

        assertEq(
            token.balanceOf(owner),
            expectedOwnerBalance,
            "Owner balance should match after setup transfer."
        );
        
        assertEq(
            token.balanceOf(recipient),
            5_000 * 10 ** token.decimals(),
            "Recipient should have 5,000 tokens."
        );
    }

    /// @dev Test token approval functionality
    function testApproval() public {
        vm.startPrank(owner);
        token.approve(spender, 5_000 * 10 ** token.decimals());
        
        assertEq(
            token.allowance(owner, spender),
            5_000 * 10 ** token.decimals(),
            "Spender should be approved for 5,000 tokens."
        );

        vm.stopPrank();
    }

    /// @dev Test token transfer functionality
    function testTransfer() public {
        vm.startPrank(recipient);

        // ✅ Transfer 500 tokens back from recipient to owner
        token.transfer(owner, 500 * 10 ** token.decimals());

        uint256 expectedRecipientBalance = (5_000 * 10 ** token.decimals()) - (500 * 10 ** token.decimals());
        uint256 expectedOwnerBalance = (1_000_000 * 10 ** token.decimals()) - (5_000 * 10 ** token.decimals()) + (500 * 10 ** token.decimals());

        assertEq(
            token.balanceOf(recipient),
            expectedRecipientBalance,
            "Recipient balance should decrease by 500 tokens."
        );

        assertEq(
            token.balanceOf(owner),
            expectedOwnerBalance,
            "Owner balance should increase by 500 tokens."
        );

        vm.stopPrank();
    }
}

