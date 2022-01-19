
import sys
import json
from eth_account.messages import encode_defunct
from eth_account import Account
from web3 import Web3

#https://bscscan.com/tx/0xd3b232081665b74dd780a8c2633c454c2d682e05be2a8f2e999e81b97fe96438

def main(_tx):
    w3 = Web3(Web3.HTTPProvider('https://bsc-dataseed1.binance.org:443'))
    try:
        tx = w3.eth.get_transaction(_tx)
    except Exception as x:
        print(x)

    riddleAddress = Web3.toChecksumAddress('0x50D1B6D61b57581AaB00D248F81a1E8170a7f3aE')
    with open("./ABI/runeRiddleABI.json", "r") as read_file:
        riddleAbi = json.load(read_file)
    riddleContract = w3.eth.contract(address=riddleAddress, abi=riddleAbi)

    func_obj, func_params = riddleContract.decode_function_input(tx.input)

    signature = func_params['signature']
    address = Web3.toChecksumAddress(func_obj.address)
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