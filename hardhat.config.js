require("@nomicfoundation/hardhat-toolbox");
require("@nomicfoundation/hardhat-ethers"); 

module.exports = {
  solidity: {
    compilers: [
      { version: "0.8.28" },
      { version: "0.8.20" },
      { version: "0.8.8" },
      { version: "0.8.4" },
      { version: "0.8.2" },
      { version: "0.8.1" }
    ]
  }
};

