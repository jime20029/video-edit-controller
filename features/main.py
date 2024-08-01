from mock_data import original_video_segments, fake_original_video_segments, clipped_video_segments
from create_allowed_deletion_list import create_allowed_segment_combinations_list
from sign import sign_original_video_segments, generate_key_pair
from verify import verify

# 動画作成者のセットアップ
def setup(original_video_segments):
    # 削除許可リスト作成
    allowed_segment_combinations_list = create_allowed_segment_combinations_list(original_video_segments)

    private_key, public_key = generate_key_pair()

    signature = sign_original_video_segments(private_key, original_video_segments, allowed_segment_combinations_list)

    return public_key, signature, allowed_segment_combinations_list


def main():
    print('original_video_segments =', original_video_segments)
    print('fake_original_video_segments =', fake_original_video_segments)

    public_key, signature, allowed_segment_combinations_list = setup(original_video_segments)

    print('allowed_segment_combinations_list =', allowed_segment_combinations_list)
    print('clipped_video_segments =', clipped_video_segments)

    verify_result = verify(original_video_segments, clipped_video_segments, allowed_segment_combinations_list, signature, public_key)
    
    print('Verified result is', verify_result)

if __name__ == "__main__":
    main()
