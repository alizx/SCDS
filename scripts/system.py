from brownie import *
from brownie import EntityProfile, DataContract, DataRequest

import rsa
from cryptography.fernet import Fernet
import base64, os
from scripts.key_generator import PublisherState, keyder, unwind

class Entity:
    def __init__(self, identifier, account):
        self.identifier = identifier

        # Generate a public/private key pair
        (pubkey, privkey) = rsa.newkeys(2048)
        self.public_key = pubkey
        self.private_key = privkey
        self.account = account

def create_chunk(directory, index, key):
    f = Fernet(key)
    content = 'This is the content for chunk {}'.format(index)
    token = f.encrypt(content.encode('ascii'))
    # decrypted_secret = f.decrypt(token)
    # print(decrypted_secret)

    file_name = '{}/file_{}.bin'.format(directory, index)
    with open(file_name, 'wb') as f:
        f.write(token)
    # Return the URL path of the file
    return os.path.abspath(file_name)



def main():
    owner = Entity("dataOwner", accounts[0])
    requester_1 = Entity("dataRequester_1", accounts[1])

    owner_entity = EntityProfile.deploy(owner.identifier, owner.public_key, {'from': owner.account})
    requester_1_entity = EntityProfile.deploy(requester_1.identifier, requester_1.public_key, {'from': requester_1.account})

    # Create the data and corresponding data contract
    ## create a key to encrypt the data
    stp = PublisherState(5)
    (stp, stm1) = stp.wind()
    k1 = keyder(stm1).ljust(32, b'\x00')
    k1 = base64.urlsafe_b64encode(k1)

    data_dir = '../data/dataset_1'
    ## Create the directory for dataset_1 files if it doesn't already exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    ## Create a data chuck and use it's index as content
    i = 0 # Chunk index
    file_1_path = create_chunk(data_dir, i, k1)

    tx = owner_entity.createDataContract("Dataset_1", file_1_path, {'from': owner.account})
    data_contract = DataContract.at(tx.new_contracts[0])

    # now the data requester 1 wants to create a dataRequest for the above data set
    tx = data_contract.createDataRequest(requester_1_entity, {'from': requester_1.account})
    data_request = DataRequest.at(tx.new_contracts[0])

    # data owner signs the request for data requester 1
    encrypted_key = rsa.encrypt(k1, requester_1.public_key)
    ## Encode the encrypted key as a base64 string
    encrypted_key_str = base64.b64encode(encrypted_key).decode('utf-8')
    tx = data_request.signDataContract(encrypted_key_str, {'from': owner.account})
    print(tx.events)



    # Verify if requester can access data 
    ## Get the encrypted data key from the DataRequest contract
    encrypted_key_str = data_request.encryptedKey()
    encrypted_key = base64.b64decode(encrypted_key_str)


    ## Decrypt the encrypted key using the data owner's private key
    decrypted_key = rsa.decrypt(encrypted_key, requester_1.private_key)

    ## Use the decrypted key to decrypt the data chunk
    with open(file_1_path, 'rb') as f:
        encrypted_chunk = f.read()
    fernet = Fernet(decrypted_key)
    decrypted_chunk = fernet.decrypt(encrypted_chunk)

    expected_content = "This is the content for chunk 0".encode('ascii')
    assert decrypted_chunk == expected_content, "Decrypted data does not match expected content"


    # Another entity joins 
    ## Create a new entity
    requester_2 = Entity("dataRequester_2", accounts[2])
    ## Deploy an EntityProfile contract for the new entity
    entity_2_entity = EntityProfile.deploy(requester_2.identifier, requester_2.public_key, {'from': requester_2.account})



    # Entity 2 asks for permission to access the data
    ## Create a data request for the new entity to access the data
    tx = data_contract.createDataRequest(entity_2_entity, {'from': requester_2.account})
    data_request_2 = DataRequest.at(tx.new_contracts[0])


    # Data owener signs the data request 2 
    ## Encrypt the data key with the data owner's public key
    encrypted_key = rsa.encrypt(k1, requester_2.public_key)

    ## Encode the encrypted key as a base64 string
    encrypted_key_str = base64.b64encode(encrypted_key).decode('utf-8')
    ## Sign the data request for the new entity
    tx = data_request_2.signDataContract(encrypted_key_str, {'from': owner.account})


    # Verify if entity 2 has access to data 
    ## Get the encrypted data key from the DataRequest contract
    encrypted_key_str = data_request_2.encryptedKey()
    encrypted_key = base64.b64decode(encrypted_key_str)

    ## Decrypt the encrypted key using the new entity's private key
    decrypted_key = rsa.decrypt(encrypted_key, requester_2.private_key)

    ## Use the decrypted key to decrypt the data chunk
    with open(file_1_path, 'rb') as f:
        encrypted_chunk = f.read()
    fernet = Fernet(decrypted_key)
    decrypted_chunk = fernet.decrypt(encrypted_chunk)

    ## Assert that the decrypted data chunk is equal to the original content of the file
    expected_content = "This is the content for chunk 0".encode('ascii')
    assert decrypted_chunk == expected_content, "Decrypted data does not match expected content"



    # now we want to revoke enity 2's access
    ## Revoke the new entity's access to the data
    tx = data_request_2.revokeDataContract({'from': owner.account})

    ## Verify that the DataContractRevoked event was emitted
    assert 'DataContractRevoked' in tx.events, "DataRequestRevoked event not emitted"


    # Create a new data chunk and encrypt it with the k2 key
    ## generate the k2
    (stp, stm2) = stp.wind()
    k2 = keyder(stm2).ljust(32, b'\x00')
    k2 = base64.urlsafe_b64encode(k2)

    new_data_dir = '../data/dataset_1'
    i =+ 1
    file_2_path = create_chunk(new_data_dir, i, k2)

    # User 1 receives the stm2
    # Verify user 1 can obtain the k2 from stm2 and decrypt the new data chunk
    # It should also be able to derive stm1 and subsequntly k1

    k2 = keyder(stm2).ljust(32, b'\x00')
    k2 = base64.urlsafe_b64encode(k2)
    with open(file_2_path, 'rb') as f:
        encrypted_chunk = f.read()
    fernet = Fernet(k2)
    decrypted_chunk = fernet.decrypt(encrypted_chunk)
    ## Assert that the decrypted data chunk is equal to the original content of the file
    expected_content = "This is the content for chunk 1".encode('ascii')
    assert decrypted_chunk == expected_content, "Decrypted data does not match expected content"

    stm1 = unwind(stm2)
    k1 = keyder(stm1).ljust(32, b'\x00')
    k1 = base64.urlsafe_b64encode(k1)
    with open(file_1_path, 'rb') as f:
        encrypted_chunk = f.read()
    fernet = Fernet(k1)
    decrypted_chunk = fernet.decrypt(encrypted_chunk)
    ## Assert that the decrypted data chunk is equal to the original content of the file
    expected_content = "This is the content for chunk 0".encode('ascii')
    assert decrypted_chunk == expected_content, "Decrypted data does not match expected content"


# if __name__ == "__main__":
#     # Run the main function
#     test()