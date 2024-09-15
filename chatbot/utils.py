from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from torch.nn.functional import softmax
import torch

# Load pre-trained sentiment analysis model and tokenizer
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased-finetuned-sst-2-english')

def analyze_sentiment(text):
    # Tokenize the input text
    inputs = tokenizer(text, return_tensors='pt')
    
    # Get model outputs
    with torch.no_grad():  # Disable gradient calculations
        outputs = model(**inputs)
    
    # Apply softmax to get probabilities
    scores = softmax(outputs.logits, dim=1).detach().numpy()[0]
    
    # Print scores for debugging
    print("Scores:", scores)
    
    # Assuming the labels are [0: NEGATIVE, 1: POSITIVE] for the SST-2 model
    sentiment_labels = ['NEGATIVE', 'POSITIVE']
    sentiment = sentiment_labels[scores.argmax()]
    
    return sentiment, scores.max()

# Example usage:
print(analyze_sentiment("I am very happy today!"))  # Should return POSITIVE
print(analyze_sentiment("I am very sad today."))    # Should return NEGATIVE
print(analyze_sentiment("It is an average day."))   # Should return NEUTRAL or POSITIVE
