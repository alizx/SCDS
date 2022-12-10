// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.12;
import {EntityProfile} from "./EntityProfile.sol";
import {DataContract} from "./DataContract.sol";

contract DataRequest {
    // string public identifier;
    EntityProfile requester;
    DataContract dataset;
    bool isActive = false;
    string dataUrl;
    string signedKey;

    constructor(EntityProfile _requester, DataContract _dataset) {
        requester = _requester;
        dataset = _dataset;
    }

    function signDataContract() public {

    }

    function revokeDataContract() public {
        
    }
}
