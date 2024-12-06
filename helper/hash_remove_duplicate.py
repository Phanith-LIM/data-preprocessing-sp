import os
import hashlib

def get_file_hash(file_path, hash_algo='sha256'):
    hash_func = hashlib.new(hash_algo)
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192): 
            hash_func.update(chunk)
    return hash_func.hexdigest()

def remove_duplicate_audio_files(directory):
    seen_hashes = set()  
    files_to_remove = []

    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            file_hash = get_file_hash(file_path)

            if file_hash in seen_hashes:
                files_to_remove.append(file_path)
            else:
                seen_hashes.add(file_hash)
    for file_path in files_to_remove:
        print(f'Removing duplicate file: {file_path}')
        os.remove(file_path)

# Example usage:
directory = 'sample' 
remove_duplicate_audio_files(directory)
