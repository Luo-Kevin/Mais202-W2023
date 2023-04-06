# -*- coding: utf-8 -*-
"""model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/github/Luo-Kevin/MAIS202/blob/main/code/model.ipynb
"""

! pip install -q transformers
! apt-get install git-lfs
! pip install datasets

from datasets import load_dataset
from transformers import RobertaTokenizer
from transformers import pipeline
import tensorflow as tf
from transformers import TFRobertaModel
import pandas as pd

# Defining some key variables that will be used later on in the training
MAX_LEN = 62
TRAIN_BATCH_SIZE = 32
VALID_BATCH_SIZE = 4
# EPOCHS = 1
LEARNING_RATE = 1e-05

gpus = tf.config.list_physical_devices('GPU')
if gpus:
  try:
    # Currently, memory growth needs to be the same across GPUs
    for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)
    logical_gpus = tf.config.list_logical_devices('GPU')
    print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
  except RuntimeError as e:
    # Memory growth must be set before GPUs have been initialized
    print(e)

#getting the dataset from huggingface
data = load_dataset('SetFit/sst2')

data_train = data["train"]
data_valid = data['validation']
data_test = data['test']

#to pandas to view
data_train_pd = pd.DataFrame(data_train)
data_valid_pd = pd.DataFrame(data_valid)
data_train_pd.dropna()
data_valid_pd.dropna()

#see label distribution

data_train_pd['label'].value_counts().plot(kind='bar')
print(data_train_pd['label'].value_counts())

y_train = data_train['label']
y_valid = data_valid['label']
y_test = data_test['label']

task='sentiment'
MODEL = f"cardiffnlp/twitter-roberta-base-{task}"
tokenizer = RobertaTokenizer.from_pretrained(MODEL)

#Preprocess function

def preprocess(data):
  return tokenizer(data['text'], truncation=True, padding=True, max_length=MAX_LEN, return_tensors='tf')



preprocess_train = preprocess(data_train)
preprocess_valid = preprocess(data_valid)
preprocess_test = preprocess(data_test)
preprocess_train

#Reformating input to this structure
def map_features(input_ids, input_mask,label):
    return ({"input_ids":input_ids, 'attention_mask': input_mask}, label) #(input, output) reformat

train_ds =  tf.data.Dataset.from_tensor_slices((preprocess_train['input_ids'], preprocess_train['attention_mask'], y_train)).map(map_features)
valid_ds =  tf.data.Dataset.from_tensor_slices((preprocess_valid['input_ids'], preprocess_valid['attention_mask'], y_valid)).map(map_features)
test_ds =  tf.data.Dataset.from_tensor_slices((preprocess_test['input_ids'], preprocess_test['attention_mask'], y_test)).map(map_features)
train_ds

#input pipeline
train_ds = train_ds.cache().batch(TRAIN_BATCH_SIZE).prefetch(buffer_size=10)
valid_ds = valid_ds.cache().batch(TRAIN_BATCH_SIZE).prefetch(buffer_size=10)
test_ds = test_ds.cache().batch(TRAIN_BATCH_SIZE).prefetch(buffer_size=10)
train_ds

"""# Transfer Learning

"""

base_model = TFRobertaModel.from_pretrained(MODEL) # bringing in pretrained model
base_model.trainable = False # Don't want to change the weights of pre-defined model -> only want to train the new layers

input_ids = tf.keras.layers.Input(shape=(MAX_LEN,), dtype=tf.int32, name='input_ids')
attention_mask = tf.keras.layers.Input(shape=(MAX_LEN,), dtype=tf.int32, name='attention_mask')

# Inference mode: just want the model to output and make predictions, and not train
# Transformer
x = base_model(input_ids, attention_mask=attention_mask, training=False)[1] # Don't want to change the weights of pre-defined model

# Classifier head
x = tf.keras.layers.Dense(128, activation='relu')(x)
x = tf.keras.layers.Dropout(0.5)(x)
y = tf.keras.layers.Dense(1, activation='sigmoid', name='classifier')(x)

model = tf.keras.Model(inputs=[input_ids, attention_mask], outputs=y)
model.summary()

model.compile(
    optimizer= tf.keras.optimizers.Adam(),
    loss= tf.keras.losses.BinaryCrossentropy(from_logits=True),
    metrics = [tf.keras.metrics.BinaryAccuracy()],
)

epoch = 10
model.fit(train_ds, epochs=epoch, validation_data=valid_ds)

from google.colab import drive
drive.mount('/content/drive')

model.save_weights('./myCheckpoint/my_checkpoint')

base_model.trainable = True
model.summary()

model.compile(
    optimizer= tf.keras.optimizers.Adam(LEARNING_RATE),
    loss= tf.keras.losses.BinaryCrossentropy(from_logits=True),
    metrics = [tf.keras.metrics.BinaryAccuracy()],
)

epoch = 3
model.fit(train_ds, epochs=epoch, validation_data=valid_ds)

model.save('models')

model.save_weights('./weight/weight')

predictions = model.predict(test_ds)

predictions

print(model.evaluate(x=test_ds))
