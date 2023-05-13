// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.12;
import {EntityProfile} from "./EntityProfile.sol";
import {DataRequest} from "./DataRequest.sol";

contract DataContract {
    string public identifier;
    string public url;
    EntityProfile public owner;
    uint256 public lastChunkIndex;
    bytes32 public lastChunkHash;
    DataRequest[] public dataRequests;

    constructor(string memory _identifier, string memory _url,  EntityProfile _owner) {
        require(
            bytes(_identifier).length > 0,
            "Identifier cannot be emptu string."
        );
        identifier = _identifier;
        owner = _owner;
        url = _url;
    }

    function appendDataChunk(
        bytes32 _chunkHash
    ) external {
        require(msg.sender == owner.ownerAddress(), "Only the owner can register a new data chunk.");
        lastChunkHash = _chunkHash;
        lastChunkIndex += 1;
    }

    function createDataRequest(
        EntityProfile _requester
    ) external returns (DataRequest) {
        DataRequest dataRequest = new DataRequest(_requester, this);
        dataRequests.push(dataRequest);
        return dataRequest;
    }
}
