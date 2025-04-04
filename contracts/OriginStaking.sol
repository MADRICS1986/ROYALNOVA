// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import "./openzeppelin/token/ERC20/IERC20.sol";
import "./openzeppelin/access/Ownable.sol";

contract OriginStaking is Ownable {
    IERC20 public token;

    struct Stake {
        uint256 amount;
        uint256 startTime;
    }

    mapping(address => Stake) private stakes;

    uint256 public rewardRate = 10; // 10% annual reward

    event Staked(address indexed user, uint256 amount);
    event Unstaked(address indexed user, uint256 amount);
    event RewardClaimed(address indexed user, uint256 reward);

    // ✅ Proper constructor with token and owner initialization
    constructor(address _token) Ownable(msg.sender) {
        token = IERC20(_token);
    }

    function stake(uint256 amount) external {
        require(amount > 0, "Cannot stake 0 tokens");
        require(token.transferFrom(msg.sender, address(this), amount), "Transfer failed");

        if (stakes[msg.sender].amount > 0) {
            uint256 reward = calculateReward(msg.sender);
            token.transfer(msg.sender, reward);
            emit RewardClaimed(msg.sender, reward);
        }

        stakes[msg.sender].amount += amount;
        stakes[msg.sender].startTime = block.timestamp;

        emit Staked(msg.sender, amount);
    }

    function unstake() external {
        require(stakes[msg.sender].amount > 0, "No tokens staked");

        uint256 amount = stakes[msg.sender].amount;
        uint256 reward = calculateReward(msg.sender);

        delete stakes[msg.sender];

        token.transfer(msg.sender, amount + reward);

        emit Unstaked(msg.sender, amount);
        emit RewardClaimed(msg.sender, reward);
    }

    function calculateReward(address staker) public view returns (uint256) {
        Stake memory userStake = stakes[staker];
        if (userStake.amount == 0) return 0;

        uint256 stakingDuration = block.timestamp - userStake.startTime;
        uint256 reward = (userStake.amount * rewardRate * stakingDuration) / (365 days * 100);

        return reward;
    }

    // ✅ Getter function for external stake access
    function getStake(address staker) external view returns (uint256 amount, uint256 startTime) {
        Stake memory userStake = stakes[staker];
        return (userStake.amount, userStake.startTime);
    }
}

