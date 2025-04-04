// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/utils/Counters.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract RoyalnovaDAO is Ownable {
    using Counters for Counters.Counter;

    struct Proposal {
        string description;
        uint256 votesFor;
        uint256 votesAgainst;
        uint256 deadline;
        bool executed;
    }

    mapping(uint256 => Proposal) public proposals;
    mapping(address => mapping(uint256 => bool)) public hasVoted;
    Counters.Counter private proposalIdCounter;
    IERC20 public immutable RNX;

    event ProposalCreated(uint256 proposalId, string description, uint256 deadline);
    event Voted(uint256 proposalId, address voter, bool support);
    event ProposalExecuted(uint256 proposalId, bool passed);

    constructor(IERC20 _RNX) {
        RNX = _RNX;
    }

    function createProposal(string memory _description, uint256 _duration) external onlyOwner {
        uint256 proposalId = proposalIdCounter.current();
        proposalIdCounter.increment();
        
        proposals[proposalId] = Proposal({
            description: _description,
            votesFor: 0,
            votesAgainst: 0,
            deadline: block.timestamp + _duration,
            executed: false
        });
        
        emit ProposalCreated(proposalId, _description, block.timestamp + _duration);
    }

    function vote(uint256 _proposalId, bool _support) external {
        Proposal storage proposal = proposals[_proposalId];
        require(block.timestamp < proposal.deadline, "Voting period over");
        require(!hasVoted[msg.sender][_proposalId], "Already voted");
        
        uint256 votingPower = RNX.balanceOf(msg.sender);
        require(votingPower > 0, "No voting power");
        
        if (_support) {
            proposal.votesFor += votingPower;
        } else {
            proposal.votesAgainst += votingPower;
        }
        
        hasVoted[msg.sender][_proposalId] = true;
        emit Voted(_proposalId, msg.sender, _support);
    }

    function executeProposal(uint256 _proposalId) external onlyOwner {
        Proposal storage proposal = proposals[_proposalId];
        require(block.timestamp >= proposal.deadline, "Voting still ongoing");
        require(!proposal.executed, "Proposal already executed");
        
        bool passed = proposal.votesFor > proposal.votesAgainst;
        proposal.executed = true;
        
        emit ProposalExecuted(_proposalId, passed);
    }
}
