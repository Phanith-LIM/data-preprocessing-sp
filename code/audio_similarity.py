from pydub import AudioSegment
import numpy as np

# Load the audio files
audio_file_1 = AudioSegment.from_file("../sample/1.mp3")
audio_file_2 = AudioSegment.from_file("../sample/2.mp3")

# Convert audio to mono and get raw data
audio_data_1 = np.array(audio_file_1.set_channels(1).get_array_of_samples())
audio_data_2 = np.array(audio_file_2.set_channels(1).get_array_of_samples())

# Ensure both audio files have the same length
min_length = min(len(audio_data_1), len(audio_data_2))
audio_data_1 = audio_data_1[:min_length]
audio_data_2 = audio_data_2[:min_length]

# Compute similarity score (e.g., correlation coefficient)
similarity_score = np.corrcoef(audio_data_1, audio_data_2)[0, 1]
print(f'Similarity score: {similarity_score}')