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
    print(type(payload))

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



# payload = "821db2d26b351fbcb5ea89f5bef0f88d50fff8b9ed0f6237e57f95ac3f54403c28ad213284ddf2315a010bc2b1e31ab455e954e194b7cc0f798f722baee5edbc4f575d5f7ac244f4aefad121afd4390f947185a6de90e26a9ab7f8cce8aaeb5674d6d70b93d1fddce6e5ff91bea0eaddd81bb062d6284f6f4a4c1767a2f15ec086cdb0098d6894a51c171b953dcdeea24b1e1a513a2ce5cee8fe04e496c31c16c77c8279218e571ccc6c1ace1dd226dc6620fd1d0cee0aa5eaa87de72b241f9fa0095dd9a99416de60a9f8e679d85b9ad9a1769b99401c95cd4f38c6620f2cfd0096d3ebb37847258616a4c9d91488db733c42614c7a91be77b195f7c46581da16a9628828fccb0a20331fd230c4828614b1d18ebc0ccf1efcc9d984134af3f093fc1d262e0fdd1173ae6ab28c1c14ebc044f04845c9b4a0fb59ffa7d88be403e17dc3317daabcb18e187e99caa91eb0db4a8b6e3baf70786c00a81aba473fa791fac006a44fa740d4e5dee13087ef6c726abbbd4f820d84c076f6c3c9d0e09c6462d37b524160f37eff8bf75f5cf31b56c2b64052f49fbf70b82a5e2b1779a6f12b1179479127448da91e56360954748edd4332548ad7e69bad4201b7431b6118b7d3c8b77f369335bb8674195e77fa1b051db7171d3dfec1750c0351af03ec559644fb2b4d1e35c936467cf4e5bb1eeb3380aca0a2363468a33e6693b0a9b3f00990fe5cf5f9b047676703d3ffb66b1f6ccce799e1360dbe6b11dc7b17ee2dd671390cad2280cb79e92bc83ed881a48c9ea0210a9922a64d5ce08d8a4d0e86581e32a9c2aa0bfc079baf7b57f7d1b6b2ef5717423cda11b8adcc8436f302f97519d4a55e430f0c0c46a4f2a28dd4169578fa0035f7e17cbff1f25d326b45c05bffbce1e6889babf4dd16f1a944a92a798cbc23433c0cc8d7ab54d0bf9aace5bfd60a64075375a5368214ca126608a017db874d63d9e62f3f69a8704df5a1f07f2e743f6959fbc3738ab54fbca18f7908f17e1ce66fc2410dcf923461f267c6b562e5f215d49d53d2e69d06e416ed1dcb233cac60f0c4554ac9468f9bd8d55b2f50120049c94a11983aa40040cbf175a0d3496f63e050b5c9e12f4a9acf725f94e25ae07ebbf2e784154334ef65c4fc3cce42a0f93ce3a6cbb82f46a2de6a2a9ce115a48343fa444a6b7069233c4081261595c731f1fa090825a9d560376b4d4286e1ae3c993eafbb151a2946df35e0b64407eac11331be092e7fc0abeadb36850428756a0a5c9f283072eafbba5723eee418e7ac5e3c1f1cc5f88abe21983605fb601949cda0a168afd600fe7626acc90a22fd97d6f181511b0b7c5dffc30bf7e7b7cf357fa1db5d1400b64a0ac24295bf902a69a7c29cb048b551d59e270af72ec05a91a261083b869e0f6f4781e6821b031053e343312a5312f54b4ec72c"


# print(decyrpt_payload(payload=payload))