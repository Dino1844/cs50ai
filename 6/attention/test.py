import tensorflow as tf 
from transformers.tokenization_utils_base import BatchEncoding
mask_token_index = 103
input_ids = [ 101,  103, 2003, 1037, 3231, 1012,  102]
inputs = BatchEncoding(
    {"input_ids": tf.constant([input_ids])},
)
print(inputs.data['input_ids'].numpy()[0][1])