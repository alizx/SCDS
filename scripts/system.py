from brownie import *

def main():
    a=2
    EntityProfile.deploy("Test Token", "TEST", 18, 1e23, {'from': accounts[0]})

 

# if __name__ == "__main__":
#     # Run the main function
#     test()