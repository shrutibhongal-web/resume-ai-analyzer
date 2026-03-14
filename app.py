from flask import Flask, render_template, request
import pdfplumber
import requests

app = Flask(__name__)

API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"

headers={
    "Authorization": "YOUR_HF_TOKEN"
}


import tempfile

def extract_text_from_pdf(file):

    text = ""

    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            file.save(temp.name)

            with pdfplumber.open(temp.name) as pdf:
                for page in pdf.pages:
                    t = page.extract_text()
                    if t:
                        text += t.lower()

    except Exception as e:
        print("PDF Error:", e)
        text = ""

    return text


def ai_resume_analysis(text):

    prompt=f"""
    Analyze this resume and give:

    Resume score out of 100
    Skill gaps
    Suggestions

    Resume:
    {text}
    """

    payload={
        "inputs":prompt
    }

    try:

        response=requests.post(
            API_URL,
            headers=headers,
            json=payload,
            timeout=5
        )

        data=response.json()

        if isinstance(data,list):
            return data[0]["generated_text"]

        else:
            return fallback_analysis(text)

    except:
        return fallback_analysis(text)


def fallback_analysis(text):

    score=60

    gaps=[]
    tips=[]

    if "project" not in text:
        gaps.append("Projects not mentioned")
        tips.append("Add academic or personal projects")

    if "skill" not in text:
        gaps.append("Skills section missing")
        tips.append("Include technical and soft skills")

    if "experience" not in text:
        gaps.append("Work experience missing")
        tips.append("Add internship or practical experience")

    result=f"""
Resume Score: {score}/100

Skill Gaps:
{chr(10).join(gaps)}

Suggestions:
{chr(10).join(tips)}
"""

    return result


@app.route("/",methods=["GET","POST"])
def index():

    ai_result=None

    if request.method=="POST":

        file=request.files.get("resume")

        text=""

        if file and file.filename!="":
            text=extract_text_from_pdf(file)

        if text!="":
            ai_result=ai_resume_analysis(text)

            print("\nAI OUTPUT:\n",ai_result)

    return render_template(
        "index.html",
        ai_result=ai_result
    )


if __name__=="__main__":
    app.run(debug=True)