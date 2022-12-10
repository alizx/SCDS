// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.12;
import {EntityProfile} from "./EntityProfile.sol";
import {DataRequest} from "./DataRequest.sol";

contract DataContract {
    string public identifier;
    EntityProfile public owner;
    uint256 public lastChunkIndex;
    DataRequest[] public dataRequests;

    constructor(string memory _identifier, EntityProfile _owner) {
        require(
            bytes(_identifier).length > 0,
            "Identifier cannot be emptu string."
        );
        identifier = _identifier;
        owner = _owner;
    }

    function createDataRequest(
        EntityProfile _requester
    ) external returns (DataRequest) {
        DataRequest dataRequest = new DataRequest(_requester, this);
        dataRequests.push(dataRequest);
        return dataRequest;
    }
}
