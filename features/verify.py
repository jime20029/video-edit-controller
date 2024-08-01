import pickle
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256

# 削除が適切かどうか判定する関数
def verify_clipped_video_segments(clipped_video_segments, allowed_list):
    # 許可された削除リストに含まれる編集か検証する処理
    return clipped_video_segments in allowed_list

# 検証関数（編集と署名の正当性の検証を行う）
def verify(original_video_segments_segments, clipped_video_segments, allowed_segment_combinations_list, signature, public_key):

    # 編集が適切かどうかを判定
    is_proper_clipped_video_segments = verify_clipped_video_segments(clipped_video_segments, allowed_segment_combinations_list)

    key = RSA.import_key(public_key)

    ordered_list = sorted(list(original_video_segments_segments))

    # リストを文字列に変換
    data_str = ''.join(ordered_list)

    # 文字列をバイト列に変換
    original_video_segments_segments_bytes = data_str.encode('utf-8')
    hash_for_original_video_segments_segments = SHA256.new(original_video_segments_segments_bytes).digest()

    allowed_segment_combinations_list_bytes = pickle.dumps(allowed_segment_combinations_list)
    hash_for_allowed_segment_combinations_list = SHA256.new(allowed_segment_combinations_list_bytes).digest()

    combined_hash = hash_for_original_video_segments_segments + hash_for_allowed_segment_combinations_list

    h = SHA256.new(combined_hash)

    verifier = PKCS1_v1_5.new(key)

    # 署名が正当かつ編集が適切ならTrueを返す
    if verifier.verify(h, signature) and is_proper_clipped_video_segments:
        return True
    else:
        return False
