from os import PRIO_USER
import rsa
import string,random
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2


def key():
    with open("keys/privateKey.pem",'rb') as f:
        privateKey = rsa.PrivateKey.load_pkcs1(f.read(),format="PEM")
    
    with open("keys/publicKey.pem",'rb') as f:
        publicKey = rsa.PublicKey.load_pkcs1(f.read(),format="PEM")
    
    return privateKey,publicKey


private_key_2,public_key_2 =  key()

def decyrpt_payload(payload):
    payload = bytes.fromhex(payload)

    ## Decrypt Payload with RSA
    rsa_decrypted = rsa.decrypt(payload,priv_key=private_key_2)
    rsa_decrypted = rsa_decrypted.decode('utf-8')

    ## Decrypt RSA
    parsed = rsa_decrypted.split("|")

    aes_ciphertext_hex = parsed[0]
    aes_otp_key = parsed[1]
    aes_nonce = parsed[2]

    cipher = AES.new(key=aes_otp_key.encode('utf-8'),mode=AES.MODE_EAX,nonce=bytes.fromhex(aes_nonce))

    aes_decrypted = cipher.decrypt(bytes.fromhex(aes_ciphertext_hex))
    aes_decrypted = aes_decrypted.decode("utf-8")

    print(aes_decrypted)

    ## Verify Payload
    parsed_aes = aes_decrypted.split("|")
    payload = parsed_aes[0]
    signature_hex = parsed_aes[1]
    public_key_hex = parsed_aes[2]
    
    is_valid_data = rsa.verify(payload.encode("utf-8"),bytes.fromhex(signature_hex),rsa.PublicKey.load_pkcs1(bytes.fromhex(public_key_hex)))

    if not is_valid_data :
        return False
    decrypted = payload
    return decrypted



payload = "5413373147e301bcdbaa7d49281c4e8769719a61c26bfc7c70df222d9933a7269708f31b17f9a0f3888ab0f1f1f364cee49303a35902929a8456143a5e05809a2eecc7ebaa5a42666006694965b9dae02cf51c9ae6eb70011130d3da0f458fc2faa4a5b92dee8323bedbd41ddb412a33676fa61787c9acb7d60789b59f530d6ad9918e397d0151ec62aba7e11091ffcbf5f592330e09f7d95d350cb9503b2f299eeede998d611e1706640875c777e1781c3e410e8f2212726317992910910f04795eacb1915b99ceacd422d4e20ef5003870fd992723f8d30336ce7a79812161842bc2de43894f076c80df67b50c91184c8ff658e538f4409a1cd44808f0c246ef975be27319c220a02875a8561e628d1ef0f643a76f1cc4118a1f571b6eba82277f74ddb81ad92fc2bfe8d9993f10eda6e9b4a52337e556c5370aa4703b7fa33f78975aa9173fb92c1daca60a766cffe7c5fb9358bf9496620dbde8e2d640b180dcd229c2091af2c6b1297a14ea214475dc5374280c223605ee27f768dd31b9d85bd907a8dae13c18a2d5341ad660d9a6a0c4a116c430cd9a29a511190d1b3d56a6747fd31110b0de6b5a4446f6510dc028040c43a38109db95ad9868bbedc9f81b482065931f1a464aa8594fe94a841f10674a30b28add5963fe262b9db3f521ecb7c011f09ad43789c9ecd0938405037910e141435a6493aea9b54ee5005dd02b977c7026a49d13692ff3afc15304f3b763f8683009c8da9ac1b8c0dc4bd23265cea5fd1ea8ff2ea79c45854eb9d426b22608ef4615482924efa10884fda39eb896372c4109f0ada41e6b3a22c3af658ad0918e0cb1aafd1b2a3d84cf9cd3cd9b2f51aaa8554d681d98ef22586846a99f1a92bff1722c1f936c8adf4d09ff0798a5c67b82fc8308d7e14cb8bcb0c1959decab381ccac6c6760f90bd084f344f549ef5a0009ae420ae0b0163d90465d62f2263795bdfef32a01e4e862011a47fc347334bd73c64c674cc255377ab6fe95db34e67a0058ea6be52c3f26af51bf3c0a4da2fe2ff3bf7c54d2cbd2e0e5f1357abe7dbbc0bbbfd4d4159646d554de5446da50958b53fa30b347ca44854ffb31383a366594f31c573999361ea3a54bd03aca860ac316d5f9d22d0a37dd1cb34a0ac686f6e04e0b067664aa59167ee393d141e56edae067c1b3122e8cf8b51e70b68d7865762e68a23a51227f0b3abe4d445b8002edb172b3dcbceaeb859f084497b1656e1c46a189e5f6188b160db34a0ecbeea348eab908b57cb92f78f52f07aa9ccfadd2de3b971f15d0325e89f4912601d9e29df76291ddc70fa6f70b6906d7aeaabc8dd3ba65db3f65be93c05da95a692687e80853b0d06242948543afb08d515a56c6b24a5ad6a63d15df62d3b9e2ae74d1520b279ffb25a66367df0b27c89a6d815987bff66e97a068f795d"


print(decyrpt_payload(payload=payload))