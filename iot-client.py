import rsa
import string,random
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2

def key_generator(size=16, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# plaintext = "SENSOR BARU"
# key_bit_length = 2048*4
# (blob_pub_key,blob_private_key) = rsa.newkeys(8192)

# with open("keys/publicKey.pem",'wb')as f:
#     f.write(blob_pub_key.save_pkcs1("PEM"))


# with open("keys/privateKey.pem",'wb')as f:
#     f.write(blob_private_key.save_pkcs1("PEM"))

def key():
    with open("keys/privateKey.pem",'rb') as f:
        privateKey = rsa.PrivateKey.load_pkcs1(f.read(),format="PEM")
    
    with open("keys/publicKey.pem",'rb') as f:
        publicKey = rsa.PublicKey.load_pkcs1(f.read(),format="PEM")
    
    return privateKey,publicKey


def encrypt_plaintext(plaintext):
    
    ## Encode Plaintext
    plaintext = plaintext.encode("utf-8")

    ## Load RSA Key
    private_key_2,public_key_2 =  key()

    ## Generate RSA Key ( dalam bentuk blob / bytes)
    (blob_pub_key,blob_private_key) = rsa.newkeys(512)

    ## Generate Signature Use Generated RSA
    hash_signature = rsa.sign(plaintext,blob_private_key,hash_method="SHA-256").hex()
    public_key_hex = blob_pub_key.save_pkcs1("PEM").hex()


    ## Generate String Key
    otp =  key_generator(size=16)

    ## Encrypty hash_signature, plaintext, and public_key_hex
    rich_plaintext = [plaintext.decode('utf-8'),hash_signature,public_key_hex]
    rich_plaintext = "|".join(rich_plaintext)

    cipher = AES.new(key=otp.encode('utf-8'),mode=AES.MODE_EAX)

    ciphertext = cipher.encrypt(rich_plaintext.encode("utf-8")).hex()

    ## Create Payload 
    payload = [ciphertext,otp,cipher.nonce.hex()]
    payload = "|".join(payload)

    ## Encrypty Payload Using RSA
    enc_payload_hex = rsa.encrypt(payload.encode("utf-8"),pub_key=public_key_2).hex()
    # print(payload)
    return enc_payload_hex

print(encrypt_plaintext(plaintext="2929"))


