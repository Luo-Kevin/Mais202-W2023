from transformers import  RobertaTokenizer,TFRobertaModel
import tensorflow as tf

model = tf.keras.models.load_model("./model/final_model.h5", custom_objects={"TFRobertaModel": TFRobertaModel})

task='sentiment'
MODEL = f"cardiffnlp/twitter-roberta-base-{task}"
tokenizer = RobertaTokenizer.from_pretrained(MODEL)

def prep_data(text):
    tokens = tokenizer(text, max_length=62,
                                   truncation=True, padding='max_length',
                                   add_special_tokens=True, return_token_type_ids=False,
                                   return_tensors='tf')
    # tokenizer returns int32 tensors, we need to return float64, so we use tf.cast
    return (tf.cast(tokens['input_ids'], tf.float32),
            tf.cast(tokens['attention_mask'], tf.float32))
    

def extract_comments(comment_objects):
    comments = []
    
    for comment in comment_objects:
        user_comment = comment["snippet"]["topLevelComment"]["snippet"]
        plain_text_comment = user_comment["textOriginal"]
        comments.append(plain_text_comment)
            
    return comments

def evaluate_video(comments):
    total_score = 0
    for comment in comments:
        score = model.predict(prep_data(comment))[0]
        total_score += score
    print(len(comments))
    return total_score/len(comments)
        
