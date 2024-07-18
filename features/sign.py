from cryptography import x509
from cryptography.x509.oid import NameOID
import datetime
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.Cipher import PKCS1_OAEP

# RSA鍵の生成
key = RSA.generate(2048)

# 秘密鍵をPEMフォーマットで保存
private_key_pem = key.export_key()
with open("private_key.pem", "wb") as f:
    f.write(private_key_pem)

# 公開鍵をPEMフォーマットで保存
public_key_pem = key.publickey().export_key()
with open("public_key.pem", "wb") as f:
    f.write(public_key_pem)

print("Keys generated and saved.")

# 鍵ペアの生成
def generate_key_pair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

# 自己署名証明書の生成
def generate_self_signed_certificate(private_key):
    # 秘密鍵から公開鍵を取得
    public_key = private_key.public_key()

    # 証明書のsubjectとissuerを設定
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"JP"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"Osaka"),
        x509.NameAttribute(NameOID.LOCALITY_NAME, u"Osaka"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"xxxxx"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"xxxxx.com"),
    ])

    # 自己署名証明書を生成
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        public_key
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.utcnow()
    ).not_valid_after(
        # 証明書の有効期限を1年後に設定
        datetime.datetime.utcnow() + datetime.timedelta(days=365)
    ).add_extension(
        # Subject Alternative Nameを追加
        x509.SubjectAlternativeName([x509.DNSName(u"localhost")]),
        critical=False,
    ).sign(private_key, SHA256())

    return cert

# 動画に署名
def sign_original_video(private_key, original_video, allowed_deletion_list):
    key = RSA.import_key(private_key)

    hash_for_original_video = SHA256.new(original_video)
    hash_for_allowed_deletion_list = SHA256.new(allowed_deletion_list)

    combined_hash = SHA256.new(hash_for_original_video + hash_for_allowed_deletion_list)

    signer = PKCS1_v1_5.new(key)
    signature = signer.sign(combined_hash)

    return signature

# 関数f
def verify_edited_video(edited_video, allowed_list):
    # 許可された削除リストに含まれる編集か検証する処理
    return True

# 東北大学側システムに問い合わせて塊ごとのスコア取得
def get_segment_scores(original_video):
# 東北大学側システムに問い合わせする処理を追加
    return {'a': 0.2, 'b': 0.6, 'c': 0.9}

# 東北大学側システムの結果をもとに閾値を決定
def decide_threshold(segment_and_scores):
    # 閾値を決定する処理を追加
    return 0.7

# 閾値とスコアから許可リストを作成
def create_allowed_deletion_segment_list(segment_and_scores, threshold):
    # セグメントと閾値から削除許可リストを作成する処理
    return [{'a', 'b'}]

# 動画作成者のセットアップ
def setup(original_video):
    ### 東北大学側のシステムに問い合わせ＝＞削除許可リスト作成
    segment_and_scores = get_segment_scores(original_video)
    threshold = decide_threshold(segment_and_scores)
    allowed_deletion_list = create_allowed_deletion_segment_list(segment_and_scores, threshold)
    #####################

    ### 

# 署名を検証
def verify_signature(original_video, edited_video, allowed_deletion_list, signature, public_key):

    is_proper_edited_video = verify_edited_video(edited_video)

    key = RSA.import_key(public_key)

    hash_for_original_video = SHA256.new(original_video)
    hash_for_allowed_deletion_list = SHA256.new(allowed_deletion_list)

    combined_hash = SHA256.new(hash_for_original_video + hash_for_allowed_deletion_list)

    h = SHA256.new(combined_hash)

    verifier = PKCS1_v1_5.new(key)
    if verifier.verify(h, signature) and is_proper_edited_video:
        return True
    else:
        return False
    

def main():
    print('main')

if __name__ == "__main__":
    main()
