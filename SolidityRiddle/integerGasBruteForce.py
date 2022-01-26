#Rune.game riddle
#https://bscscan.com/address/0xc9d4ed4bac9c9ff3c96f3e60c59d6a9a99185f3d

import sys
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account.messages import encode_defunct
from eth_account import Account
import json
from hexbytes import HexBytes

riddleAddress = Web3.toChecksumAddress('0xc9d4ed4bac9c9ff3c96f3e60c59d6a9a99185f3d')
#https://rune.game/sign?message=123
def main(_key):
    w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org:443'))

    _account = w3.eth.account.privateKeyToAccount(_key)
    print('Running the brute force with the account:')    
    myAddress = _account.address
    print(myAddress)
    print('Make sure other requirements of the contract are met, ie. RXS spending and sufficient balance')    

    with open("./ABI/runeRiddleABI.json", "r") as read_file:
        riddleAbi = json.load(read_file)
    riddleContract = w3.eth.contract(address=riddleAddress, abi=riddleAbi)
    _gasEstimates = []
    for i in range(0,100):
        message = encode_defunct(text= str(i))
        signed_message = w3.eth.account.sign_message(message, private_key=_key)


        nonce = w3.eth.get_transaction_count(myAddress) 
        riddle_txn = riddleContract.functions.attemptGate03(signed_message.signature).buildTransaction({
            'from': myAddress,
            'gas': 529186,
            'gasPrice': w3.eth.gas_price,
            'nonce': nonce,
            
        })
        gas_estimate = w3.eth.estimateGas(riddle_txn)
        _gasEstimates.append(gas_estimate)
        print(str(i) + " : " + str(gas_estimate))
    
    max_gas = max(_gasEstimates)
    max_gas_integer= _gasEstimates.index(max_gas)
    print(str(max_gas_integer) + " : Integer with highest gas estimate from the contrast" )

    



if __name__ == '__main__':
    print("---Rune.game Solidity riddle tool---")    
    print("Try to recover correct integer using gas estimate")    
    print("")    
    print("!!!WARNING!!!")    
    print('Use this tool with your "burner" account only')
    print('Never supply this tool with the private of your main wallet, it will steal all your funds')    
    print('')    
    if (len(sys.argv)>1):
        main(sys.argv[1])
    else:
        print("Specify the private key of the address that you'd like to use")
        print("ie. 'python3 integerGasBruteForce.py '")