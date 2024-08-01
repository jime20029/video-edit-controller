from mock_data import allowed_segment_combinations_list

## 東北大学側システム（T）にオリジナル動画を渡してスコアを組み合わせごとに取得
## 取得データイメージ：{('a', 'b'): 0.2, ('a', 'b', 'e'): 0.6, ('a', 'e'): 0.9}

# # Tに問い合わせて塊ごとのスコア取得
# def get_segment_scores(original_video_segments):
#     # Tに問い合わせする処理を追加
#     return allowed_segment_combinations_list

# # Tの結果をもとに閾値を決定
# def decide_threshold(segment_and_scores):
#     # セグメントと組み合わせとスコアのセットから閾値を決定する処理を追加
#     return threshold

# 閾値とスコアから許可リストを作成
def create_allowed_segment_combinations_list(original_video_segments):
    ### Tに問い合わせ＝＞削除許可リスト作成
    ### セグメントと閾値から削除許可リストを作成する処理
    # segment_and_scores = get_segment_scores(original_video_segments)
    # threshold = decide_threshold(segment_and_scores)
    # allowed_list = {k: v for k, v in segment_and_scores.items() if v < threshold}
    # return allowed_list
    return allowed_segment_combinations_list
