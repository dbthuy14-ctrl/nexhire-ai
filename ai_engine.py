import os
import json

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# Initialize the OpenAI Client
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key) if (OpenAI and api_key) else None

class NexHireAIEngine:
    """
    Core AI Engine for NexHire Platform.
    Falls back to highly realistic mock data if OPENAI_API_KEY is not defined.
    """
    
    @staticmethod
    def generate_job_post(role_prompt: str) -> dict:
        if not client:
            # Fallback mock for testing without API Key
            return {
                "title": f"{role_prompt.title()} (Generated)",
                "description": "We are seeking an extremely talented autonomous individual to join our fast-paced forward-thinking team. You will be responsible for architecting solutions, solving complex problems, and driving product innovation from day one.",
                "required_skills": ["Problem Solving", "System Design", "Communication", "Agile Methodologies"],
                "estimated_salary_range": "$120,000 - $180,000",
                "ai_disclaimer": "This is a simulated AI response. Please add OPENAI_API_KEY to see real capabilities."
            }
        
        system_prompt = "You are an expert tech recruiter. Given a short prompt, generate a highly attractive, bias-free job description."
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": role_prompt}
            ],
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content)

    @staticmethod
    def screen_and_score_cv(cv_text: str, role_requirements: str) -> dict:
        if not client:
            return {
                "match_score": 92,
                "skills_found": ["Python", "React", "Team Leadership", "Data Analysis"],
                "missing_skills": ["GraphQL", "Docker"],
                "logic_reasoning_est": 88,
                "summary": "Candidate shows strong senior-level architecture experience matching the primary requirements.",
                "ai_disclaimer": "This is a simulated AI response. Please add OPENAI_API_KEY to see real capabilities."
            }
        
        system_prompt = f"""
        Extract the core competencies from this CV text. Ignore formatting, names, or demographics.
        Score the candidate objectively out of 100 based strictly on these requirements: {role_requirements}.
        Output JSON: {{ "match_score": int, "skills_found": list, "missing_skills": list, "logic_reasoning_est": int, "summary": str }}
        """
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": cv_text}
            ],
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content)

    @staticmethod
    def generate_dynamic_test(role: str, candidate_skills: str) -> dict:
        if not client:
            return {
                "role": role,
                "questions": [
                    {
                        "type": "Logical Reasoning",
                        "question": "If a system can process 500 requests per second and spikes to 1000 requests per second for 1 minute every hour, what is the minimum buffer queue size required assuming the processing rate remains constant?",
                        "expected_answer_keywords": ["30000", "buffer", "queue", "bottleneck"]
                    },
                    {
                        "type": "Domain Skill",
                        "question": f"Explain how you would optimize a highly concurrent architecture heavily utilizing {candidate_skills.split(',')[0]} under extreme load.",
                        "expected_answer_keywords": ["caching", "load balancing", "horizontal scaling", "async"]
                    }
                ],
                "ai_disclaimer": "This is a simulated AI response. Please add OPENAI_API_KEY to see real capabilities."
            }
            
        system_prompt = f"Generate 2 technical screening questions (1 logic, 1 domain) for a {role} who claims to have skills in {candidate_skills}. Include expected answer keywords."
        
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt}
            ],
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content)
