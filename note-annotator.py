import os

def read_file(file_name: str):
    print(f'Reading {file_name}...')
    with open(file_name, 'r') as f:
        # read line by line
        content = f.readlines()
    start_record = False
    notes = {}
    for line in content:
        if line == "# 註解\n":
            start_record = True
            continue
        if start_record:
            try: 
                number, note = line.split('：', 1)
                number = number.split('.')[1].strip()   # '1. 行便' -> '行便'
                notes[number] = note.strip()
            except:
                print(f'note extraction error: {line}')
    # transform the content from list to string
    content = ''.join(content)
    return content, notes

def generate_md(file_name: str, content: str, notes: dict, save_folder: None):
    file_name = file_name.split('/')[-1]
    for i, (key, value) in enumerate(notes.items()):
        # print(f'{key}[{i+1}]：{value}')
        cite = f'{key}[{i+1}]'
        # print(f'{cite}：{value}')
        # replace the original content with the annotated content
        content = content.replace(cite, f'[[{key}]]', 1)
        
        # create a new file with the cited content
        if not save_folder:
            os.makedirs('src')
            save_folder = 'src'
        with open(f'{save_folder}/{key}.md', 'w') as f:
            f.write(f"---\n")
            f.write(f"性質: \n")
            f.write(f"tags: \n")
            f.write(f"aliases: \n")
            f.write(f"---\n")
            f.write(f"# 補充說明\n")
            f.write(f"{value}\n")

    # create a new file with the annotated content
    with open(f'{save_folder}/{file_name}', 'w') as f:
        f.write(content)
        
    

if __name__ == '__main__':
    # debug
    # file_name = '1933/1933-09-04.md'
    # content, notes = read_file(file_name)
    # new_file_name = file_name.replace('.md', '_annotated.md')
    # generate_md(new_file_name, content, notes)

    dir = '1935'
    # create a new folder to store the annotated notes
    os.makedirs(f'{dir}/{dir}_annotated', exist_ok=True)

    for file_name in os.listdir(dir):
        if file_name.endswith('.md'):
            file_name = os.path.join(dir, file_name)
            content, notes = read_file(file_name)
            generate_md(file_name, content, notes, save_folder=f'{dir}/{dir}_annotated')
            print(f'Finish annotating {file_name}.')
