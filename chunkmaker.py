def read_chunks(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        chunk = ''
        prevline=''
        for line in file:
            if line == prevline:
                continue
            prevline=line
            
            if len(chunk) + len(line) <= 2048:
                chunk += line
            else:
                yield chunk.strip()
                chunk = line
        if chunk:
            yield chunk.strip()
