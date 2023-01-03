// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.12;
import {DataContract} from "./DataContract.sol";

contract EntityProfile {
    address public ownerAddress;
    string public identifier;
    string public publicKey;
    DataContract[] private dataContracts;

    modifier onlyOwner() {
        require(
            msg.sender == ownerAddress,
            "Only the contract owner can call this function."
        );
        _;
    }

    constructor(string memory _identifier, string memory _publicKey) {
        require(
            bytes(_identifier).length > 0,
            "Identifier cannot be emptu string."
        );
        require(
            bytes(_publicKey).length > 0,
            "PublicKey cannot be of length zero."
        );
        ownerAddress = msg.sender;
        identifier = _identifier;
        publicKey = _publicKey;
    }

    function createDataContract(
        string calldata _identifier,
        string calldata _url
    ) public onlyOwner returns (DataContract) {
        DataContract newContract = new DataContract(_identifier, _url, this);
        dataContracts.push(newContract);
        return newContract;
    }
}
