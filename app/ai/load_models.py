# My first iteration was using Ollama and relying only on prompt engineering (You are a spam detector blah blah blah ...).
# This time we'll try using huggingfaces' existing models for translation, spam detection, and toxicity detection.
# This way we can simulate production "cheap first - smart later" approach.
# The plan is to let these do the initial processing first, ideally 90% of the time,
# and only escalate to a more expensive model when necessary.

from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification, TextClassificationPipeline
import logging
from functools import lru_cache

@lru_cache(maxsize=1)
def get_translation_model():
    return pipeline("translation", model="Helsinki-NLP/opus-mt-nl-en")

@lru_cache(maxsize=1)
def get_spam_detection_model():
    return pipeline("text-classification", model="valurank/distilroberta-spam-comments-detection")

@lru_cache(maxsize=1)
def get_toxicity_detection_model():
    model_name = "unitary/toxic-bert"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    return TextClassificationPipeline(
        model=model,
        tokenizer=tokenizer,
        return_all_scores=True,
        top_k=None,  # Return everything, not just top-k
        function_to_apply="sigmoid",  # I think this defaults anyway, but let's be explicit about it
    )


def get_all_models(verbose=False):
    if verbose:
        logging.basicConfig(level=logging.INFO)
        log = logging.info
    else:
        log = lambda *args, **kwargs: None

    log("Downloading/loading translation model...")
    translator = get_translation_model()

    log("Downloading/loading spam detection model...")
    spam_detector = get_spam_detection_model()

    log("Downloading/loading toxicity detection model...")
    toxicity_detector = get_toxicity_detection_model()

    return translator, spam_detector, toxicity_detector

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting model download and cache...")
    get_all_models(verbose=True)
    logging.info("All models downloaded and cached.")

