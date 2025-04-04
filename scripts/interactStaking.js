const { ethers } = require("hardhat");

async function main() {
  console.log("✅ Hardhat + Ethers is working!");
  const accounts = await ethers.getSigners();
  console.log("First account:", accounts[0].address);
}

main().catch((error) => {
  console.error("❌ ERROR:", error);
  process.exitCode = 1;
});

