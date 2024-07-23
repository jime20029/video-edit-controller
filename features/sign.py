import pickle
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

# 鍵ペアの生成
def generate_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# 動画に署名
def sign_original_video(private_key, original_video, allowed_deletion_list):
    key = RSA.import_key(private_key)

    # リストを文字列に変換
    data_str = ''.join(original_video)

    # 文字列をバイト列に変換
    original_video_bytes = data_str.encode('utf-8')
    hash_for_original_video = SHA256.new(original_video_bytes).digest()

    allowed_deletion_list_bytes = pickle.dumps(allowed_deletion_list)
    hash_for_allowed_deletion_list = SHA256.new(allowed_deletion_list_bytes).digest()

    combined_hash = SHA256.new(hash_for_original_video + hash_for_allowed_deletion_list)

    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(combined_hash)
    return signature
