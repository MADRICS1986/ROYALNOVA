const hre = require("hardhat");

async function main() {
  const tokenAddress = "0xe7f1725e7734ce288f8367e1bb143e90bb3f0512"; // RNX Token

  const OriginStaking = await hre.ethers.getContractFactory("OriginStaking");
  const staking = await OriginStaking.deploy(tokenAddress);

  await staking.waitForDeployment(); // ✅ replaces .deployed()

  console.log(`OriginStaking deployed to: ${staking.target}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

