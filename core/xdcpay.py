from web3 import Web3

web3 = Web3(Web3.HTTPProvider("https://apothemxdcpayrpc.blocksscan.io/"))

connect = lambda:web3.isConnected()

def pay(from_acc,to_acc,pk,amt):
    context = {"msg":"","done":False,"error":"","hash":"","url":"https://xdc.blocksscan.io/"}
    try:
        if from_acc[:3] =='xdc' and to_acc[:3] == 'xdc':
            address1 = web3.toChecksumAddress("0x"+from_acc[3:])
            address2 = web3.toChecksumAddress("0x"+to_acc[3:])
            blance = web3.eth.get_balance(address1)
            print("Blance : "+str(web3.fromWei(blance, 'ether'))+ " ETH")
            if blance<=amt:
                context["error"] = "Not Enough Blance!"
            else:
                tx = {
                    'nonce':web3.eth.getTransactionCount(address1),
                    'to':address2,
                    'value':web3.toWei(amt, 'ether'),
                    'gas':200000,
                    'gasPrice':web3.toWei('50', 'gwei')
                }
                signd_tx = web3.eth.account.signTransaction(tx,private_key=pk)
                tx_trans = web3.eth.send_raw_transaction(signd_tx.rawTransaction)
                hash_ = web3.toHex(tx_trans)
                context["hash"] = hash_
                context['done'] = True
                context['url'] = f"https://explorer.apothem.network/txs/{hash_}"
                context['msg'] = "Transaction Successfull !!"

        else:
            context['error'] = "Not an XDC Address !!"
    except Exception as e:
        context['error'] = str(e)  
    return context

if __name__ == '__main__':
    c = pay("xdc2c9d3e542e1dc0946bdc9798b35de1cfbecf18e4", "xdc348c663b71c7f780bc6c00d520f9a2d27792584d", "69072e6ff5ee48eefd9b4fe524838ceb8a7b0d674d515f278742df14795b1bb6", 100)
    print(c)