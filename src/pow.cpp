// Copyright (c) 2010-2024 Royalnova developers
// Distributed under the MIT software license.

#include <chain.h>
#include <chainparams.h>
#include <consensus/params.h>
#include <logging.h>
#include <pow.h>
#include <primitives/block.h>
#include <uint256.h>
#include <arith_uint256.h>
#include "common/system.h"
#include <validation.h>

// Difficulty adjustment algorithm for Royalnova (RNX)
unsigned int GetNextWorkRequired(const CBlockIndex* pindexLast, const CBlockHeader* pblock, const Consensus::Params& params)
{
    assert(pindexLast != nullptr);

    int nHeightFirst = pindexLast->nHeight - (params.DifficultyAdjustmentInterval() - 1);
    assert(nHeightFirst >= 0);

    const CBlockIndex* pindexFirst = pindexLast->GetAncestor(nHeightFirst);
    assert(pindexFirst);

    return CalculateNextWorkRequired(pindexLast, pindexFirst->GetBlockTime(), params);
}

// Calculates new difficulty based on past blocks
unsigned int CalculateNextWorkRequired(const CBlockIndex* pindexLast, int64_t nFirstBlockTime, const Consensus::Params& params)
{
    assert(pindexLast != nullptr);

    // Limit adjustment step
    int64_t nActualTimespan = pindexLast->GetBlockTime() - nFirstBlockTime;
    int64_t nTargetTimespan = params.nPowTargetTimespan;

    // Adjust difficulty within bounds
    if (nActualTimespan < nTargetTimespan / 4)
        nActualTimespan = nTargetTimespan / 4;
    if (nActualTimespan > nTargetTimespan * 4)
        nActualTimespan = nTargetTimespan * 4;

    // Retarget
    arith_uint256 bnNew;
    bnNew.SetCompact(pindexLast->nBits);
    bnNew *= nActualTimespan;
    bnNew /= nTargetTimespan;

    // Ensure difficulty does not exceed max target
    if (bnNew > UintToArith256(params.powLimit))
        bnNew = UintToArith256(params.powLimit);

    return bnNew.GetCompact();
}

// Checks if a block satisfies proof-of-work requirement
bool CheckProofOfWork(uint256 hash, unsigned int nBits, const Consensus::Params& params)
{
    bool fNegative;
    bool fOverflow;
    arith_uint256 bnTarget;

    bnTarget.SetCompact(nBits, &fNegative, &fOverflow);

    // Check range
    if (fNegative || bnTarget == 0 || fOverflow || bnTarget > UintToArith256(params.powLimit))
        return false;

    // Check proof of work
    if (UintToArith256(hash) > bnTarget)
        return false;

    return true;
}

std::optional<arith_uint256> DeriveTarget(unsigned int nBits, const uint256 pow_limit) {
    arith_uint256 target;
    bool fNegative;
    bool fOverflow;
    
    target.SetCompact(nBits, &fNegative, &fOverflow);

    if (fNegative || fOverflow || target == 0) {
        return std::nullopt;
    }
    
    if (target > UintToArith256(pow_limit)) {
        target = UintToArith256(pow_limit);
    }
    
    return target;
}

bool PermittedDifficultyTransition(const Consensus::Params& params, int64_t height, uint32_t old_nbits, uint32_t new_nbits) {
    // Basic difficulty transition validation logic (modify as per your algorithm)
    if (new_nbits > old_nbits) return false; // Difficulty cannot increase
    return true;  // Allow the transition
}
