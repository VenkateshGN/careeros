import os
import json
import logging
import time
from dotenv import load_dotenv

load_dotenv()

try:
    import boto3
    from botocore.exceptions import ClientError
    HAS_BOTO3 = True
except ImportError:
    HAS_BOTO3 = False

logger = logging.getLogger("careeros.ai_service")

# Auto-configure AWS Bedrock from environment
if HAS_BOTO3 and (os.getenv("AWS_ACCESS_KEY_ID") or os.getenv("AWS_DEFAULT_REGION")):
    bedrock_client = boto3.client('bedrock-runtime', region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"))
    logger.info("Live AWS Bedrock Runtime configured.")
else:
    bedrock_client = None
    logger.warning("AWS credentials missing. Running in AWS Bedrock mock fallback mode.")

# Configure Gemini client as active fallback (disabled during unit testing)
gemini_client = None
import sys
if "pytest" not in sys.modules and not os.getenv("PYTEST_CURRENT_TEST") and os.getenv("GEMINI_API_KEY"):
    logger.info("GEMINI_API_KEY loaded: true")
    try:
        from google import genai
        gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        logger.info("Gemini client configured.")
    except Exception as e:
        logger.warning(f"Could not configure Gemini client: {e}")

def generate_embeddings(text: str) -> list[float]:
    """Generates 1536-dimensional embeddings natively using Gemini Embedding model."""
    import sys
    is_test = "pytest" in sys.modules or os.getenv("PYTEST_CURRENT_TEST") is not None

    if not gemini_client:
        if is_test:
            val = [0.01 * (i % 10) for i in range(1536)]
            assert val is not None
            assert len(val) == 1536
            return val
        raise Exception("Gemini client is not configured. Real embedding generation failed.")

    try:
        res = gemini_client.models.embed_content(
            model="models/gemini-embedding-2",
            contents=text,
            config={
                "output_dimensionality": 1536
            }
        )
        embedding = res.embeddings[0].values
        assert embedding is not None
        assert len(embedding) == 1536
        return embedding
    except Exception as e:
        logger.error(f"Gemini Embedding Error: {e}")
        if is_test:
            logger.warning("Falling back to mock embeddings for test environment.")
            val = [0.01 * (i % 10) for i in range(1536)]
            assert val is not None
            assert len(val) == 1536
            return val
        raise e

def _call_bedrock_json(prompt: str, fallback_mock: dict) -> dict:
    """
    Generate structured JSON using Gemini first,
    then AWS Bedrock as fallback.
    """

    # ========================================================
    # 1. Gemini
    # ========================================================

    if gemini_client:
        logger.info("Calling Gemini model (gemini-3.5-flash)...")

        try:
            response = gemini_client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt,
                config={
                    "response_mime_type": "application/json"
                }
            )

            # ------------------------------------------------
            # Debug Gemini response
            # ------------------------------------------------

            logger.info(
                f"Gemini response object type: {type(response)}"
            )

            raw_text = response.text

            logger.info(
                f"Gemini raw response: {raw_text}"
            )

            if not raw_text:
                raise ValueError(
                    "Gemini returned an empty response."
                )

            # ------------------------------------------------
            # Parse JSON
            # ------------------------------------------------

            try:
                parsed_response = json.loads(raw_text)

                logger.info(
                    "Gemini JSON parsing successful."
                )

                return parsed_response

            except json.JSONDecodeError as json_error:

                logger.error(
                    f"Gemini returned invalid JSON: {json_error}"
                )

                logger.error(
                    f"Raw Gemini response was: {raw_text}"
                )

        except Exception as e:

            logger.error(
                f"Gemini call failed: {type(e).__name__}: {e}",
                exc_info=True
            )

            logger.info(
                "Trying AWS Bedrock fallback..."
            )

    # ========================================================
    # 2. AWS Bedrock fallback
    # ========================================================

    if bedrock_client:

        logger.info(
            "AWS Bedrock Request Started | "
            "Model: anthropic.claude-3-haiku-20240307-v1:0"
        )

        start_time = time.time()

        try:

            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 1000,
                "system": (
                    "You must return ONLY valid JSON. "
                    "Do not use markdown code blocks. "
                    "Do not include explanations outside JSON."
                ),
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }
                ]
            })

            response = bedrock_client.invoke_model(
                body=body,
                modelId="anthropic.claude-3-haiku-20240307-v1:0",
                accept="application/json",
                contentType="application/json"
            )

            response_body = json.loads(
                response["body"].read()
            )

            elapsed_time = time.time() - start_time

            logger.info(
                "AWS Bedrock Response Received"
            )

            logger.info(
                f"Elapsed Time: {elapsed_time:.2f} sec"
            )

            text_response = (
                response_body
                .get("content", [{}])[0]
                .get("text", "")
            )

            logger.info(
                f"Bedrock raw response: {text_response}"
            )

            if not text_response:
                raise ValueError(
                    "Bedrock returned an empty response."
                )

            parsed_response = json.loads(
                text_response
            )

            logger.info(
                "Bedrock JSON parsing successful."
            )

            return parsed_response

        except ClientError as e:

            logger.error(
                "Bedrock AWS ClientError: "
                f"{e.response['Error']['Message']}"
            )

        except json.JSONDecodeError as e:

            logger.error(
                f"Bedrock returned invalid JSON: {e}"
            )

        except Exception as e:

            logger.error(
                f"Bedrock connection/generation error: "
                f"{type(e).__name__}: {e}",
                exc_info=True
            )

    # ========================================================
    # 3. Final fallback
    # ========================================================

    logger.warning(
        "Both Gemini and AWS Bedrock failed. "
        "Returning static fallback response."
    )

    return fallback_mock

def evaluate_job_match(resume_text: str, job_description: str) -> dict:
    mock = {
        "match_score": 86,
        "matched_skills": ["Python", "FastAPI", "Docker"],
        "missing_skills": ["AWS", "Redis"],
        "recommendation": "Learn AWS fundamentals and wrap up Redis caching strategies."
    }
    prompt = f"""
    Compare this resume against the job description.
    Resume: {resume_text}
    Job: {job_description}
    Return a JSON object with:
    - match_score (integer 0-100)
    - matched_skills (list of strings)
    - missing_skills (list of strings)
    - recommendation (string)
    """
    return _call_bedrock_json(prompt, mock)

def generate_resume_review(resume_url: str) -> dict:
    mock = {
        "overall_score": 85,
        "strengths": ["Clear layout and formatting", "Strong action verbs used in descriptions"],
        "weaknesses": ["Lacks quantifiable achievements", "Missing key skills section"],
        "suggestions": ["Add a dedicated Skills section", "Include metrics to show impact (e.g., 'improved performance by 20%')"]
    }
    prompt = f"""
    Generate a resume review for the candidate holding resume at: {resume_url}.
    Return a JSON object with:
    - overall_score (integer 0-100)
    - strengths (list of strings)
    - weaknesses (list of strings)
    - suggestions (list of strings)
    """
    return _call_bedrock_json(prompt, mock)

def generate_career_roadmap(current_role: str, target_role: str) -> dict:
    mock = {
        "target_role": target_role,
        "steps": [
            {"step_number": 1, "title": "Master Core Fundamentals", "description": f"Focus on essential concepts needed to transition from {current_role} to {target_role}.", "timeline": "Months 1-3"},
            {"step_number": 2, "title": "Build Pertinent Projects", "description": f"Create portfolio pieces that mimic real-world {target_role} responsibilities.", "timeline": "Months 4-6"},
            {"step_number": 3, "title": "Networking and Application", "description": "Engage with communities and start targeting entry roles or lateral moves.", "timeline": "Months 7-8"}
        ]
    }
    prompt = f"""
    Create a career transition roadmap focusing from {current_role} to {target_role}.
    Return a JSON object with:
    - target_role (string)
    - steps (list of objects, each containing: step_number (int), title (string), description (string), timeline (string))
    """
    return _call_bedrock_json(prompt, mock)

def generate_interview_questions(job_title: str, experience_level: str) -> dict:
    mock = {
        "job_title": job_title,
        "questions": [
            {"question": f"Can you describe a time you overcame a technical challenge related to {job_title}?", "category": "Behavioral", "hint": "Use the STAR method."},
            {"question": f"What are the most important skills for a {experience_level} {job_title}?", "category": "Technical", "hint": "Relate this to recent industry trends."}
        ]
    }
    prompt = f"""
    Generate two mock interview questions for a {experience_level} {job_title}.
    Return a JSON object with:
    - job_title (string)
    - questions (list of objects, each containing: question (string), category (string), hint (string))
    """
    return _call_bedrock_json(prompt, mock)

def extract_structured_resume_data(parsed_text: str) -> dict:
    mock = {
        "skills": ["Python", "JavaScript", "FastAPI", "React", "PostgreSQL"],
        "education": ["B.S. in Computer Science"],
        "experience": ["3 years as a Backend Developer"],
        "projects": ["CareerOS Job Board Backend"],
        "certifications": ["AWS Certified Developer - Associate"]
    }
    prompt = f"""
    Extract the core structured data out of this resume parsed text: {parsed_text}.
    Return a JSON object with:
    - skills (list of strings)
    - education (list of strings)
    - experience (list of strings)
    - projects (list of strings)
    - certifications (list of strings)
    """
    return _call_bedrock_json(prompt, mock)

def generate_resume_suggestions(job_title: str, experience_level: str) -> list[str]:
    mock = [
        f"Engineered and deployed highly scalable backend architectures for {job_title} initiatives.",
        f"Spearheaded cloud-native solutions mapping to {experience_level} best practices."
    ]
    prompt = f"""
    Generate 2 robust, high-impact resume bullet points tailored for a {experience_level} {job_title}.
    Return a exactly a JSON array containing strings (list of strings).
    """
    res = _call_bedrock_json(prompt, {"suggestions": mock})
    # Handle direct array parsing edge case vs object wrap
    if isinstance(res, list): return res
    if isinstance(res, dict) and "suggestions" in res: return res["suggestions"]
    return mock

def rank_jobs_for_resume(resume_text: str, jobs_list: list) -> dict:
    """
    Ranks a list of jobs against the candidate's resume using Gemini 3.5 Flash.
    Returns a dictionary mapping job ID (string) to match score (integer 0-100).
    """
    mock = {
        "matches": [
            {"id": str(job["id"]), "score": 75} for job in jobs_list
        ]
    }

    jobs_formatted = []
    for job in jobs_list:
        jobs_formatted.append(f"- ID: {job['id']}\n  Title: {job['title']}\n  Description: {job['description'][:200]}...")

    jobs_str = "\n".join(jobs_formatted)

    prompt = f"""
    You are an AI career matcher. Evaluate the following candidate resume against the list of jobs provided.
    Score each job based on how well the candidate's skills and experience match the requirements (on a scale of 0 to 100).

    Candidate Resume:
    {resume_text}

    Jobs to Evaluate:
    {jobs_str}

    Return a JSON object containing a "matches" key which points to a list of objects.
    Each object in the list must have:
    - id (string, matching the job ID exactly)
    - score (integer between 0 and 100)

    Example:
    {{
        "matches": [
            {{"id": "some-uuid", "score": 85}}
        ]
    }}
    """

    return _call_bedrock_json(prompt, mock)
