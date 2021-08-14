PAGE_POST_STATUSES = ['a', 'b', 'c', 'd']

post_info_elements = {f'elements_{status}': [] for status in PAGE_POST_STATUSES}
post_info_num_elements = {f'num_elements_{status}': 0 for status in PAGE_POST_STATUSES}
post_info = {**post_info_elements, **post_info_num_elements}

post_info['elements_a'] = ['p1', 'p2']
post_info['num_elements_a'] = 2

print(post_info)
