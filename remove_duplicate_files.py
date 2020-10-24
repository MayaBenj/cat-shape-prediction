import hashlib
import os
from collections import defaultdict

path = "cats_standing_up"

def md5(fname):
    hash_md5 = hashlib.md5()
    with open("%s/%s" % (path, fname), 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

count = 0
md5_dict = defaultdict(list)
for root, dirs, files in os.walk(path):
    for filename in files:
        filepath = os.path.join(root, filename)
        file_md5 = md5(filename)
        md5_dict[file_md5].append(filepath)
for key in md5_dict:
    file_list = md5_dict[key]
    while len(file_list) > 1:
        item = file_list.pop()
        os.remove(item)
        count +=1

print("Removed total of %d duplicate images" % count)