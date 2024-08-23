def read_chunks(file_path, chunk_size=1024, overlap=200):
    with open(file_path, 'r', encoding='utf-8') as file:
        while True:
            start_pos = file.tell()  # Store the current position

            # Read the chunk
            chunk = file.read(chunk_size)
            
            # If we don't have enough characters to fill the chunk size, stop the loop
            if not chunk:
                break

            # Yield the current chunk
            yield chunk

            # If we're at the end of the file, don't try to seek back
            if len(chunk) < chunk_size:
                break

            # Move the file pointer back by 'overlap' characters
            file.seek(start_pos + chunk_size - overlap)


# print(next(read_chunks("staticdata/crawled_data.txt", chunk_size=1024, overlap=100)))
# for i,chunk in enumerate(read_chunks("staticdata/crawled_data.txt")):
#     print(chunk)
#     print("------------------------------------------------------------")
#     if(i==4):
#         break



