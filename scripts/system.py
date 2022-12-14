from brownie import *
import rsa
from cryptography.fernet import Fernet, MultiFernet
import base64
import os

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





# # Use the public key to encrypt a sample string
# sample_string = "This is a sample string"
# encrypted_string = rsa.encrypt(sample_string.encode('ascii'), pubkey)

# # Use the private key to decrypt the encrypted string
# decrypted_string = rsa.decrypt(encrypted_string, privkey)



def main():
    owner = Entity("dataOwner", accounts[0])
    requester = Entity("dataRequester", accounts[1])

    owner_entity = EntityProfile.deploy(owner.identifier, owner.public_key, {'from': owner.account})
    requester_entity = EntityProfile.deploy(requester.identifier, requester.public_key, {'from': requester.account})

    #create the data and corresponding data contract
    key = "12345678901234567890123456789000".encode('ascii')
    key = base64.urlsafe_b64encode(key)
    #Fernet.generate_key()


    data_dir = '../data/dataset_1'
    # Create the directory for dataset_1 files if it doesn't already exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Create the 10 files and write the index of the file to each one
    i = 0 # Chunk index
    file_path = create_chunk(data_dir, i, key)

    create_data_contract_transaction = owner_entity.createDataContract("Dataset_1", file_path, {'from': owner.account})
    data_contract = DataContract.at(create_data_contract_transaction.new_contracts[0])

    # now the data requester wants to create a dataRequest for the above data set
    create_data_request_transaction = data_contract.createDataRequest(requester_entity, {'from': requester.account})
    data_request = DataRequest.at(create_data_request_transaction.new_contracts[0])

    data_request.signDataContract("<encryptedKey>", {'from': owner.account})
    print(data_request)

    # data owner should sign the data request



# if __name__ == "__main__":
#     # Run the main function
#     test()