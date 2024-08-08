from transformers import pipeline

# Load the zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Define possible labels for sentiment analysis
candidate_labels = ["positive", "negative", "neutral"]

# Define a function to classify the sentiment
def sen_class(review):
    result = classifier(review, candidate_labels)
    r=result['labels'][0]  # The label with the highest score
    if(r=="positive"):
        return 1
    elif(r=="negative"):
        return -1
    else:
        return 0
    
comp=["complete","incomplete"]
def completeness(review):
    result = classifier(review, comp)
    r=result['labels'][0]  # The label with the highest score
    if(r=="complete"):
        return 1
    else:
        return -1
