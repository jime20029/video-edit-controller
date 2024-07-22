import itertools
import pickle
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

original_video = ('a', 'b', 'c', 'd', 'e')
edited_video = ('a', 'b', 'e')
scores_per_segment = {('a', 'b'): 0.2, ('a', 'b', 'e'): 0.6, ('a', 'e'): 0.9}
threshold = 0.7

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

# 関数f
def verify_edited_video(edited_video, allowed_list):
    # 許可された削除リストに含まれる編集か検証する処理
    return edited_video in allowed_list

# Tシステムに問い合わせて塊ごとのスコア取得
def get_segment_scores(original_video):
    # Tシステムに問い合わせする処理を追加
    return scores_per_segment

# Tシステムの結果をもとに閾値を決定
def decide_threshold(segment_and_scores):
    # セグメントと組み合わせとスコアのセットから閾値を決定する処理を追加
    return threshold

# 全ての長さの組み合わせを生成する関数
def all_combinations(s):
    return list(itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(1, len(s) + 1)))

# 閾値とスコアから許可リストを作成
def create_allowed_deletion_list(original_video):
    ### Tのシステムに問い合わせ＝＞削除許可リスト作成
    ### セグメントと閾値から削除許可リストを作成する処理
    segment_and_scores = get_segment_scores(original_video)
    threshold = decide_threshold(segment_and_scores)
    allowed_list = {k: v for k, v in segment_and_scores.items() if v < threshold}
    return allowed_list

# 動画作成者のセットアップ
def setup(original_video):
    ### Tのシステムに問い合わせ＝＞削除許可リスト作成
    allowed_deletion_list = create_allowed_deletion_list(original_video)
    #####################

    private_key, public_key = generate_key_pair()

    signature = sign_original_video(private_key, original_video, allowed_deletion_list)

    return public_key, signature, allowed_deletion_list

# 署名を検証
def verify_signature(original_video, edited_video, allowed_deletion_list, signature, public_key):

    # 編集が適切かどうかを判定
    is_proper_edited_video = verify_edited_video(edited_video, allowed_deletion_list)

    key = RSA.import_key(public_key)

    ordered_list = sorted(list(original_video))

    # リストを文字列に変換
    data_str = ''.join(ordered_list)

    # 文字列をバイト列に変換
    original_video_bytes = data_str.encode('utf-8')
    hash_for_original_video = SHA256.new(original_video_bytes).digest()

    allowed_deletion_list_bytes = pickle.dumps(allowed_deletion_list)
    hash_for_allowed_deletion_list = SHA256.new(allowed_deletion_list_bytes).digest()

    combined_hash = hash_for_original_video + hash_for_allowed_deletion_list

    h = SHA256.new(combined_hash)

    verifier = PKCS1_v1_5.new(key)

    # 署名が正当かつ編集が適切ならTrueを返す
    if verifier.verify(h, signature) and is_proper_edited_video:
        return True
    else:
        return False
    

def main():
    print('original_video =', original_video)

    public_key, signature, allowed_deletion_list = setup(original_video)

    print('allowed_deletion_list =', allowed_deletion_list)
    print('edited_video =', edited_video)

    verify_result = verify_signature(original_video, edited_video, allowed_deletion_list, signature, public_key)
    
    print('Verified result is', verify_result)

if __name__ == "__main__":
    main()
