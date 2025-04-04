const hre = require("hardhat");

async function main() {
  const initialSupply = hre.ethers.parseUnits("10000000", 18); // 10 million RNX with 18 decimals

  const Royalnova = await hre.ethers.getContractFactory("RoyalnovaToken");
  const rnx = await Royalnova.deploy(initialSupply);

  await rnx.waitForDeployment();

  console.log("RoyalnovaToken deployed to:", await rnx.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});

