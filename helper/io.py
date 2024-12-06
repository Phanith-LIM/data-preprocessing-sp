def read_text_file(file_path):
    with open(file_path, 'r') as f:
        return f.read()

def write_text_file(file_path, content):
    with open(file_path, 'w') as f:
        f.write(content)


def get_first_line(path: str) -> str:
    with open(path, 'r') as f:
        return f.readline().strip()

def remove_first_line(path: str) -> None:
    with open(path, 'r') as f:
        lines = f.readlines()
    with open(path, 'w') as f:
        f.writelines(lines[1:])