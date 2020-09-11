from modules import childesr_wrapper

test_tokens = childesr_wrapper.get_tokens(token = "dog%", corpus = ["providence","manchester"], age = [2, 40])
print(test_tokens)