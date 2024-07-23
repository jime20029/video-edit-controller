original_video = ('a', 'b', 'c', 'd', 'e')
fake_original_video = ('b', 'c', 'd', 'e', 'f', 'g', 'h')
edited_video = ('a', 'b', 'e')
scores_per_segment = {('a', 'b'): 0.2, ('a', 'b', 'e'): 0.6, ('a', 'e'): 0.9}
threshold = 0.5
