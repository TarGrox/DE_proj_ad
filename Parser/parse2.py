import json
import os


cur_path = os.path.dirname(__file__)
dir_resourse_path = 'utils/resourse'
new_path = os.path.join(cur_path, "..", dir_resourse_path, 'inf_from_js.txt')
print(new_path)

# почти вся нужная информация о странице хранится в одном из скриптов JS-овских
# причем, нужная информация хранится почти в виде dict питоновских.
# В виде прототипа решил вырезать этот кусок кода (работая с ним, как с текстом), после уже трансформируя в dict
with open(new_path, 'r') as f:
    st = f.read()
    mark_product = st.find('"product":{')
    mark_comments_data = st.find('"comments_data":{')
    inf_prod = st[mark_product+len('"product":{')-1:mark_comments_data-1]

sts = json.loads(inf_prod)

1+1