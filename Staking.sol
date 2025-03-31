// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IERC20 {
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    function balanceOf(address account) external view returns (uint256);
}

contract RoyalnovaStaking {
    IERC20 public rnxToken;
    uint256 public stakingDuration = 30 days; // Staking lock period
    uint256 public rewardRate = 10; // 10% reward rate per staking period

    struct Stake {
        uint256 amount;
        uint256 timestamp;
    }

    mapping(address => Stake) public stakes;

    event Staked(address indexed user, uint256 amount, uint256 timestamp);
    event Unstaked(address indexed user, uint256 amount, uint256 timestamp);
    event RewardClaimed(address indexed user, uint256 reward);

    constructor(address _rnxToken) {
        rnxToken = IERC20(_rnxToken);
    }

    // Stake RNX tokens
    function stake(uint256 amount) external {
        require(amount > 0, "Amount must be greater than zero");
        require(rnxToken.transferFrom(msg.sender, address(this), amount), "Transfer failed");

        Stake storage stakeData = stakes[msg.sender];
        stakeData.amount += amount;
        stakeData.timestamp = block.timestamp;

        emit Staked(msg.sender, amount, block.timestamp);
    }

    // Unstake RNX tokens
    function unstake() external {
        Stake storage stakeData = stakes[msg.sender];
        require(stakeData.amount > 0, "No tokens to unstake");
        require(block.timestamp >= stakeData.timestamp + stakingDuration, "Staking period has not ended");

        uint256 amount = stakeData.amount;
        stakeData.amount = 0;

        require(rnxToken.transferFrom(address(this), msg.sender, amount), "Transfer failed");
        emit Unstaked(msg.sender, amount, block.timestamp);
    }

    // Calculate rewards for a user
    function calculateRewards(address user) public view returns (uint256) {
        Stake storage stakeData = stakes[user];
        uint256 stakingTime = block.timestamp - stakeData.timestamp;
        uint256 reward = (stakeData.amount * rewardRate * stakingTime) / (stakingDuration * 100);
        return reward;
    }

    // Claim rewards for staking
    function claimRewards() external {
        uint256 reward = calculateRewards(msg.sender);
        require(reward > 0, "No rewards available");

        stakes[msg.sender].timestamp = block.timestamp; // Reset the staking time
        require(rnxToken.transferFrom(address(this), msg.sender, reward), "Reward transfer failed");

        emit RewardClaimed(msg.sender, reward);
    }
}
