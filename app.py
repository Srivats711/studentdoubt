from flask import Flask, render_template, request
from groq import Groq

app = Flask(__name__)

# Set your Groq API key (for testing; in production, use environment variables)
GROQ_API_KEY = "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"

def call_groq_api(prompt):
    """
    Calls the Groq API using the groq library.
    Sends the prompt to the model and returns the generated answer.
    """
    client = Groq(api_key=GROQ_API_KEY)
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="llama-3.3-70b-versatile",  # Update model name if needed
            stream=False,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return "Sorry, I couldn't process your request."

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", subject="ocr", question="", answer="", leaderboard=[])

@app.route("/<subject>", methods=["GET"])
def subject_page(subject):
    valid_subjects = ["math", "physics", "chemistry", "ocr"]
    if subject not in valid_subjects:
        return "Invalid subject", 404

    return render_template("index.html", subject=subject, question="", answer="", leaderboard=[])

@app.route("/ask/ocr", methods=["POST"])
def ask_ocr():
    question = request.form.get("question", "").strip()
    if not question:
        answer = "No question provided."
    else:
        answer = call_groq_api(question)
    return render_template("index.html", subject="ocr", question=question, answer=answer, leaderboard=[])

@app.route("/ask/<subject>", methods=["POST"])
def ask_subject(subject):
    question = request.form.get("question", "").strip()
    answer = ""

    print(f"Received question: '{question}' for subject: '{subject}'")  # Debugging line

    math_keywords = [
        "add", "subtract", "multiply", "divide", "equation", "geometry", "algebra",
        "calculus", "fraction", "derivative", "integral", "function", "limit",
        "theorem", "inequality", "graph", "sequence", "series", "combinatorics",
        "set theory", "matrix", "vector", "statistics", "probability", "trigonometry",
        "numerical methods", "hypothesis testing", "data analysis", "real analysis",
        "complex numbers", "linear algebra", "discrete mathematics", "mathematical modeling"
    ]

    physics_keywords = [
        "force", "energy", "mass", "velocity", "acceleration", "momentum", "gravity",
        "kinematics", "newton", "work", "power", "friction", "pressure", "torque",
        "angular momentum", "electric field", "magnetic field", "waves", "optics",
        "thermodynamics", "quantum mechanics", "relativity", "nuclear physics",
        "plasma", "superconductivity", "oscillation", "resonance", "dark matter",
        "black holes", "astrophysics", "fluid dynamics", "particle physics"
    ]

    chemistry_keywords = [
        "atom", "molecule", "reaction", "compound", "element", "periodic", "solution",
        "acid", "base", "catalyst", "stoichiometry", "concentration", "pH",
        "oxidation", "reduction", "equilibrium", "kinetics", "thermochemistry",
        "organic chemistry", "chemical bonds", "molecular geometry", "spectroscopy",
        "chromatography", "biochemistry", "environmental chemistry", "physical chemistry",
        "ionic compounds", "covalent bonds", "salts", "electrochemistry",
        "chemical equations", "reaction mechanisms", "synthesis", "thermodynamic properties"
    ]

    # Ensure the question is relevant to the subject
    if subject == "math":
        if any(keyword in question.lower() for keyword in math_keywords):
            answer = call_groq_api(question)
        else:
            answer = "This question is not relevant to Mathematics."

    elif subject == "physics":
        if any(keyword in question.lower() for keyword in physics_keywords):
            answer = call_groq_api(question)
        else:
            answer = "This question is not relevant to Physics."

    elif subject == "chemistry":
        if any(keyword in question.lower() for keyword in chemistry_keywords):
            answer = call_groq_api(question)
        else:
            answer = "This question is not relevant to Chemistry."

    else:
        return "Invalid subject", 400

    print(f"Answer: '{answer}'")  # Debugging line
    return render_template("index.html", subject=subject, question=question, answer=answer, leaderboard=[])

@app.route("/leaderboard", methods=["GET"])
def leaderboard_page():
    leaderboard_data = [
        {"rank": 1, "name": "Emma Johnson", "level": "Advanced", "math": "3/3", "physics": "3/3", "chemistry": "2/3", "total": "8/9"},
        {"rank": 2, "name": "Michael Chen", "level": "Intermediate", "math": "3/3", "physics": "2/3", "chemistry": "2/3", "total": "7/9"},
        {"rank": 3, "name": "Sophia Rodriguez", "level": "Advanced", "math": "2/3", "physics": "3/3", "chemistry": "2/3", "total": "7/9"},
        {"rank": 4, "name": "Aiden Patel", "level": "Beginner", "math": "3/3", "physics": "2/3", "chemistry": "1/3", "total": "6/9"},
        {"rank": 5, "name": "Olivia Kim", "level": "Intermediate", "math": "2/3", "physics": "1/3", "chemistry": "3/3", "total": "6/9"},
    ]
    return render_template("leaderboard.html", leaderboard=leaderboard_data)

if __name__ == "__main__":
    # Run on 0.0.0.0 to allow external access, on port 8080
    app.run(host="0.0.0.0", port=8080, debug=True)

