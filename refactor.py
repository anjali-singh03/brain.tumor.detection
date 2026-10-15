
# Read the original app
with open('braintumorapp.py', 'r', encoding='utf-8') as f:
    code = f.read()

data_start = code.find('DATA = {')
cases_start = code.find('CASES = {')
cases_end = code.find('@st.cache_resource')

data_content = code[data_start:cases_end].strip()

content_py = f'''# content.py
# Contains all medical data and patient cases

{data_content}
'''

with open('src/content.py', 'w', encoding='utf-8') as f:
    f.write(content_py)

print("Created src/content.py")
