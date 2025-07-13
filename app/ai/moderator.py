import re
import json
import logging
import requests
import os
from app.ai.dto import ScreenCommentResult, CommentModerationResult, AIModel
from .load_models import get_translation_model

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://dcc_ollama:11434")

def generate(prompt: str, model: str):
    """
    Call Ollama REST API to generate a response from the specified model.
    Host is read from OLLAMA_HOST environment variable.
    Handles and logs error responses from Ollama.
    """
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "temperature": 0, # So it will format JSON strictly
                "stream": False
            },
            timeout=30
        )
        try:
            data = response.json()
        except Exception:
            data = {}
        if response.status_code == 200:
            return data.get("response", "No response from LLM.")
        else:
            error_msg = data.get("error", response.text)
            logging.error(f"Ollama LLM error: {error_msg}")
            return f"Ollama error: {error_msg}"
    except Exception as e:
        logging.error(f"Ollama LLM call failed: {e}")
        return f"Error: LLM moderation failed. Exception: {e}"


def moderate_comment_with_llm(comment_id: int, screening_result: ScreenCommentResult, flag_reason):
    """
    Use an LLM to moderate a comment flagged as spam or toxic.
    Accepts a ScreenCommentResult and a reason, extracts text/context.
    Calls Ollama llama3 model via REST API.
    """

    translated_subject = translate_text(screening_result.subject) if screening_result.subject is not None else None
    translated_context = translate_text(screening_result.context) if screening_result.context is not None else None
    translated_comment = get_translated_comment(screening_result)

    prompt = f"""
        You are a strict but fair content moderator.

        Your task is to evaluate whether a user-submitted comment is correctly flagged as either "toxic" or "spam", based on the given subject and context.

        Important guidelines:
        - **Toxicity does NOT include legitimate criticism**.
        - A comment is only toxic if it includes **personal attacks**, **hostile intent**, **hateful or dehumanizing language**, or **wishes of harm**, or **racism**.
        - Negative opinions, disagreements, or strong language directed at **ideas or actions** are allowed, as long as they do not become personal or abusive.

        You **must** return a **valid JSON object only**, and **nothing else**. No explanations, no preambles, no markdown.

        If you output anything outside the JSON block, your response will be **discarded and considered invalid**.

        ---

        Given the following:
        - subject: can be an article or product title
        - context: either the article's first paragraph or a previous comment
        - comment: the user-submitted comment
        - flag_reason: either "toxic" or "spam", depending on the system's classification

        Please analyze the comment based on the given context and reason. Return your response in **strict JSON format** with the following fields:

        - "confidence": A float between 0 and 1 indicating how confident you are that the flag is appropriate
        - "reasoning": A clear, concise explanation of *why* the comment was classified this way
        - "action": What action should be taken? Options: "allow", "warn", "delete", or "escalate"

        Here are the inputs you need to analyze:
        subject: {translated_subject}
        context: {translated_context}
        comment: {translated_comment}
        flag_reason: {flag_reason}

        Respond with **exactly** this JSON structure:
        {{
            \"confidence\": float,
            \"reasoning\": "...\",
            \"action\": \"...\"
        }}
    """

    model = "llama3"
    logging.info(f"Moderating comment {comment_id} with {model}")
    llm_output = generate(prompt, model)
    logging.info(f"LLM output: {llm_output}")

    try:
        llm_output_json = extract_json(llm_output)
        return CommentModerationResult(
            comment_id=comment_id,
            model=AIModel(type="LLM", name=model),
            prompt=prompt,
            classifier_flagged_as=flag_reason,
            llm_output_json=llm_output_json,
            moderation_decision=llm_output_json.get('action', 'No action provided'),
            reasoning=llm_output_json.get('reasoning', 'No reasoning provided'),
            confidence=llm_output_json.get('confidence', 0)
        )
    except Exception as e:
        logging.error(f"LLM did not return valid JSON: {e}")
        # Let it crash
        raise e

def get_translated_comment(result: ScreenCommentResult):
    for job in result.jobs:
        if job.type == "translation":
            return job.output.get("translation")
    return None

def translate_text(text):
    translator = get_translation_model()
    translation = translator(text)[0]['translation_text']
    return translation

def extract_json(text):
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return json.loads(match.group(0))
    raise ValueError("No valid JSON found")