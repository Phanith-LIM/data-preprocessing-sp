import os
import shutil
import random
base_dir = '/Users/PhanithLIM/Documents/04.Projects/create_ml/data'
male_dir = os.path.join(base_dir, 'males')
female_dir = os.path.join(base_dir, 'females')

train_dir = os.path.join(base_dir, 'train')
test_dir = os.path.join(base_dir, 'test')

# Create train and test folders
os.makedirs(os.path.join(train_dir, 'male'), exist_ok=True)
os.makedirs(os.path.join(test_dir, 'male'), exist_ok=True)
os.makedirs(os.path.join(train_dir, 'female'), exist_ok=True)
os.makedirs(os.path.join(test_dir, 'female'), exist_ok=True)

# Function to split data
def split_data(source_dir, train_dir, test_dir, test_ratio=0.2):
    files = os.listdir(source_dir)
    random.shuffle(files)
    
    test_size = int(len(files) * test_ratio)
    test_files = files[:test_size]
    train_files = files[test_size:]
    
    for file in train_files:
        shutil.copy(os.path.join(source_dir, file), os.path.join(train_dir, file))
    
    for file in test_files:
        shutil.copy(os.path.join(source_dir, file), os.path.join(test_dir, file))

# Split male and female folders
split_data(male_dir, os.path.join(train_dir, 'male'), os.path.join(test_dir, 'male'))
split_data(female_dir, os.path.join(train_dir, 'female'), os.path.join(test_dir, 'female'))

print("Data splitting complete!")
