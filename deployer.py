import requests
import json
from solders.keypair import Keypair
from solders.transaction import VersionedTransaction
from solders.keypair import Keypair
from solders.commitment_config import CommitmentLevel
from solders.rpc.requests import SendVersionedTransaction
from solders.rpc.config import RpcSendTransactionConfig

def send_local_create_tx():
    signer_keypair = Keypair.from_base58_string('REPLACE_KEYPAIR') #ask grok to replace this

    # Generate a random keypair for token
    mint_keypair = Keypair()

    # Define token metadata
    form_data = {
        'name': 'REPLACE_NAME',
        'symbol': 'REPLACE_SYMBOL',
        'description': 'REPLACE_DESCRIPTION',
        'twitter': 'https://x.com/deployedbyai/', #this should be manual, or leave it empty if you dont want socials
        'showName': 'true'
    }

    url = "REPLACE_IMG_URL"
    response = requests.get(url)
    if response.status_code == 200:
        file_content = response.content
    else:
        raise Exception(f"Failed to download file: {response.status_code}")

    # Create IPFS metadata storage
    metadata_response = requests.post("https://pump.fun/api/ipfs", data=form_data, files=file_content)
    metadata_response_json = metadata_response.json()

    # Token metadata
    token_metadata = {
        'name': form_data['name'],
        'symbol': form_data['symbol'],
        'uri': metadata_response_json['metadataUri']
    }

    # Generate the create transaction
    response = requests.post(
        "https://pumpportal.fun/api/trade-local",
        headers={'Content-Type': 'application/json'},
        data=json.dumps({
            'publicKey': str(signer_keypair.pubkey()),
            'action': 'create',
            'tokenMetadata': token_metadata,
            'mint': str(mint_keypair.pubkey()),
            'denominatedInSol': 'true',
            'amount': REPLACE_BUY_AMOUNT, # grok will replace this with an amount. Make sure its an integer
            'slippage': 10,
            'priorityFee': 0.0005,
            'pool': 'pump'
        })
    )

    tx = VersionedTransaction(VersionedTransaction.from_bytes(response.content).message, [mint_keypair, signer_keypair])

    commitment = CommitmentLevel.Confirmed
    config = RpcSendTransactionConfig(preflight_commitment=commitment)
    txPayload = SendVersionedTransaction(tx, config)

    response = requests.post(
        url="Your RPC endpoint - Eg: https://api.mainnet-beta.solana.com/",
        headers={"Content-Type": "application/json"},
        data=SendVersionedTransaction(tx, config).to_json()
    )
    txSignature = response.json()['result']
    print(f'https://solscan.io/tx/{txSignature}')
    print(f'https://pump.fun/coin/{response.json()['address']}')

send_local_create_tx()
