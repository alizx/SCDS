// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.12;
import {EntityProfile} from "./EntityProfile.sol";
import {DataContract} from "./DataContract.sol";

contract DataRequest {
    // string public identifier;
    EntityProfile requester;
    DataContract dataset;
    bool isActive = false;
    string encryptedKey;

    constructor(EntityProfile _requester, DataContract _dataset) {
        requester = _requester;
        dataset = _dataset;
    }

    modifier onlyDataContractOwner() {
        require(dataset.owner.address == msg.sender);
        _;
    }

    function signDataContract(string calldata _encryptedKey) public onlyDataContractOwner {
        encryptedKey = _encryptedKey;
        isActive = true;
    }

    function revokeDataContract() public onlyDataContractOwner {
         isActive = false;
    }
}
