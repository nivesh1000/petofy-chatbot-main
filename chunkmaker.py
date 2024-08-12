def read_chunks(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        while True:
            chunk = file.read(2048)
            if not chunk:
                break
            yield chunk

