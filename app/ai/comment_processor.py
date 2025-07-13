from .load_models import get_spam_detection_model, get_toxicity_detection_model, get_translation_model
from app.ai.dto import ScreenCommentResult, ScreenCommentJob

def screen_comment(text: str, context: str = None, subject: str = None, subject_id: str = None):
    spam_detector = get_spam_detection_model()
    toxicity_detector = get_toxicity_detection_model()
    translation = translate_text(text)

    spam_result = spam_detector(translation)[0]
    toxicity_result = toxicity_detector(translation)[0]

    jobs = [
        ScreenCommentJob(
            type="translation",
            model={"type": "translation", "name": "Helsinki-NLP/opus-mt-nl-en"},
            output={"translation_text": translation}
        ),
        ScreenCommentJob(
            type="spam_classification",
            model={"type": "text-classification", "name": "valurank/distilroberta-spam-comments-detection"},
            output={"label": spam_result['label'], "score": spam_result['score']}
        ),
        ScreenCommentJob(
            type="toxicity_classification",
            model={"type": "text-classification", "name": "unitary/toxic-bert"},
            output=toxicity_result
        )
    ]
    return ScreenCommentResult(
        subject_id=subject_id,
        subject=subject,
        context=context,
        text=text,
        jobs=jobs,
        
    )

def translate_text(str):
    translator = get_translation_model()
    translation = translator(str)[0]['translation_text']
    return translation
