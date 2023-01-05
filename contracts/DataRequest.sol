// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.12;
import {EntityProfile} from "./EntityProfile.sol";
import {DataContract} from "./DataContract.sol";

contract DataRequest {
    event OwnerChecked(address owner, address caller);
    event DataContractSigned();
    event DataContractRevoked();

    // string public identifier;
    EntityProfile public requester;
    DataContract public dataset;
    bool public isActive = false;
    string public encryptedKey;

    constructor(EntityProfile _requester, DataContract _dataset) {
        requester = _requester;
        dataset = _dataset;
    }

    modifier onlyDataContractOwner() {
        emit OwnerChecked(dataset.owner().ownerAddress(), msg.sender);
        require(dataset.owner().ownerAddress() == msg.sender);
        _;
    }

    function signDataContract(
        string calldata _encryptedKey
    ) public onlyDataContractOwner {
        encryptedKey = _encryptedKey;
        isActive = true;
        emit DataContractSigned();
    }

    function revokeDataContract() public onlyDataContractOwner {
        isActive = false;
        encryptedKey = "";
        emit DataContractRevoked();
    }
}
