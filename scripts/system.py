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

    with open('{}/file_{}.bin'.format(directory, index), 'wb') as f:
        f.write(token)





# # Use the public key to encrypt a sample string
# sample_string = "This is a sample string"
# encrypted_string = rsa.encrypt(sample_string.encode('ascii'), pubkey)

# # Use the private key to decrypt the encrypted string
# decrypted_string = rsa.decrypt(encrypted_string, privkey)



def main():
    data_owner = Entity("dataOwner", accounts[0])
    data_requester = Entity("dataRequester", accounts[1])

    data_owner_entity_instance = EntityProfile.deploy(data_owner.identifier, data_owner.public_key, {'from': data_owner.account})
    EntityProfile.deploy(data_requester.identifier, data_requester.public_key, {'from': data_requester.account})

    #create the data and corresponding data contract
    key = "12345678901234567890123456789000".encode('ascii')
    key = base64.urlsafe_b64encode(key)
    #Fernet.generate_key()


    data_dir = '../data/dataset_1'
    # Create the directory for dataset_1 files if it doesn't already exist
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # Create the 10 files and write the index of the file to each one
    for i in range(10):
        create_chunk(data_dir, i, key)

    DataContract.deploy(data_owner.identifier, data_owner_entity_instance , {'from': data_owner.account})


# if __name__ == "__main__":
#     # Run the main function
#     test()