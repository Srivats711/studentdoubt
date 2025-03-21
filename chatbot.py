from flask import Flask, render_template, request, redirect, url_for
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
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.3-70b-versatile",  # Update model name if needed
            stream=False,
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        print(f"Error calling Groq API: {e}")
        return "Sorry, I couldn't process your request."

@app.route("/")
def home():
    return render_template("chatbot.html")

@app.route("/ask", methods=["GET", "POST"])
def ask():
    if request.method == "GET":
        # Redirect GET requests to the home page
        return redirect(url_for("home"))
    
    # Handle POST request from the form
    user_input = request.form.get("user_input", "").strip()
    response = call_groq_api(user_input)
    return render_template("chatbot.html", user_input=user_input, response=response)

if __name__ == "__main__":
    app.run(debug=True)
