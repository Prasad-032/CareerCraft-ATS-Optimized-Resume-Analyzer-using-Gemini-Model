import os
from openai import OpenAI

client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv("NVIDIA_API_KEY")
)

INPUT_PROMPT = """
As an experienced ATS (Applicant Tracking System), proficient in the technical domain encompassing
Software Engineering, Data Science, Data Analysis, Big Data Engineering, Web Developer, Mobile App Developer,
DevOps Engineer, Machine Learning Engineer, Cybersecurity Analyst, Cloud Solutions Architect, Database Administrator,
Network Engineer, AI Engineer, Systems Analyst, Full Stack Developer, UI/UX Designer, IT Project Manager,
and additional specialized areas, your objective is to meticulously assess resumes against provided job descriptions.
In a fiercely competitive job market, your expertise is crucial in offering top-notch guidance for resume enhancement.
Assign precise matching percentages based on the JD (Job Description) and meticulously identify any missing keywords
with utmost accuracy.

resume: {text}
description: {jd}

I want the response in the following structure:
The first line indicates the percentage match with the job description (JD).
The second line presents a list of missing keywords.
The third section provides a profile summary.
Mention the title for all the three sections.
While generating the response put some space to separate all the three sections.
"""

def analyze_resume(resume_text, jd):
    prompt = INPUT_PROMPT.format(text=resume_text, jd=jd)
    completion = client.chat.completions.create(
        model="google/gemma-2-27b-it",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        top_p=0.7,
        max_tokens=1024,
        stream=True
    )
    result = ""
    for chunk in completion:
        if chunk.choices and chunk.choices[0].delta.content is not None:
            result += chunk.choices[0].delta.content
    return result
