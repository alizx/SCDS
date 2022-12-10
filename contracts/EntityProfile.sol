// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.12;
import {DataContract} from "./DataContract.sol";

contract EntityProfile {
    string public identifier;
    string public publicKey;
    DataContract[] private dataContracts;

    constructor(string memory _identifier, string memory _publicKey) {
        require(
            bytes(_identifier).length > 0,
            "Identifier cannot be emptu string."
        );
        require(
            bytes(_publicKey).length > 0,
            "PublicKey cannot be of length zero."
        );
        identifier = _identifier;
        publicKey = _publicKey;
    }

    function createDataContract(
        string calldata _identifier
    ) public returns (DataContract) {
        return new DataContract(_identifier, this);
    }
}
