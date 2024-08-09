def read_chunks(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        chunk = ''
        for line in file:
            # print(line)
            # print("----------------------------------------------------------")
            
            if len(chunk) + len(line) <= 2048:
                chunk += line
            else:
                yield chunk.strip()
                chunk = line  # Start a new chunk with the current line
        
        # Yield the last chunk if it's not empty
        if chunk:
            yield chunk.strip()
