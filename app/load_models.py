from transformers import pipeline
import logging
from functools import lru_cache

# My first iteration was using Ollama and relying only on prompt engineering (You are a spam detector blah blah blah ...).
# This time we'll try using huggingfaces' existing models for translation, spam detection, and toxicity detection.
# This way we can simulate production "cheap first - smart later" approach.
# The plan is to let these do the initial processing first, ideally 90% of the time,
# and only escalate to a more expensive model when necessary.
@lru_cache(maxsize=1)
def get_models(verbose=False):
    if verbose:
        logging.basicConfig(level=logging.INFO)
        log = logging.info
    else:
        log = lambda *args, **kwargs: None

    log("Downloading/loading translation model...")
    translator = pipeline("translation", model="Helsinki-NLP/opus-mt-nl-en")

    log("Downloading/loading spam detection model...")
    spam_detector = pipeline("text-classification", model="valurank/distilroberta-spam-comments-detection")

    log("Downloading/loading toxicity detection model...")
    toxicity_detector = pipeline("text-classification", model="unitary/toxic-bert")

    return translator, spam_detector, toxicity_detector

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting model download and cache...")
    get_models(verbose=True)
    logging.info("All models downloaded and cached.")

