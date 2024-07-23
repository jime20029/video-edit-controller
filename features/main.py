from mock_data import original_video, fake_original_video, edited_video
from create_allowed_deletion_list import create_allowed_deletion_list
from sign import sign_original_video, generate_key_pair
from verify import verify

# 動画作成者のセットアップ
def setup(original_video):
    # 削除許可リスト作成
    allowed_deletion_list = create_allowed_deletion_list(original_video)

    private_key, public_key = generate_key_pair()

    signature = sign_original_video(private_key, original_video, allowed_deletion_list)

    return public_key, signature, allowed_deletion_list


def main():
    print('original_video =', original_video)

    public_key, signature, allowed_deletion_list = setup(original_video)

    print('allowed_deletion_list =', allowed_deletion_list)
    print('edited_video =', edited_video)

    verify_result = verify(original_video, edited_video, allowed_deletion_list, signature, public_key)
    
    print('')
    print('Verified result is', verify_result)
    print('')

if __name__ == "__main__":
    main()
