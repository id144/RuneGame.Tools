
import sys
import json
from eth_account.messages import encode_defunct
from eth_account import Account
from web3 import Web3
from web3.middleware import geth_poa_middleware
#https://bscscan.com/tx/0xd3b232081665b74dd780a8c2633c454c2d682e05be2a8f2e999e81b97fe96438

def main(_tx):
    w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org:443'))
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)    
    try:
        tx = w3.eth.get_transaction(_tx)
    except Exception as x:
        print(x)

    riddleAddress = Web3.toChecksumAddress('0xc9d4ed4bac9c9ff3c96f3e60c59d6a9a99185f3d')
    with open("./ABI/runeRiddleABI.json", "r") as read_file:
        riddleAbi = json.load(read_file)
    riddleContract = w3.eth.contract(address=riddleAddress, abi=riddleAbi)

    func_obj, func_params = riddleContract.decode_function_input(tx.input)

    signature = func_params['signature']
    address = Web3.toChecksumAddress(tx['from'])
    for i in range(0,1000000000):
        message = encode_defunct(text= str(i))
        _acc = Account.recover_message(message,signature=signature)
        if (address == _acc):
            print(str(i) + " : " + address)
            return

if __name__ == '__main__':
    print("---Rune.game Solidity riddle tool---")    
    print("Try to recover integer from the signature of known transaction")    

    if (len(sys.argv)>1):
        main(sys.argv[1])
    else:
        print("Specify the transaction that you would like the brute-force to run on.")
        print("ie. 'python3 messageSignatureBruteForce.py 0xd3b232081665b74dd780a8c2633c454c2d682e05be2a8f2e999e81b97fe96438'")