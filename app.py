from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

app = Flask(__name__)

client = genai.Client(
    api_key=os.getenv("poner api aquí")
)

@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/transcribir", methods=["POST"])
def transcribir():

    if "audio" not in request.files:
        return jsonify({
            "error": "No se recibió audio"
        }), 400

    archivo = request.files["audio"]

    ruta = os.path.join("audios", archivo.filename)

    archivo.save(ruta)

    myfile = client.files.upload(file=ruta)

    respuesta = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=[
            myfile,
            "Transcribe exactamente este audio en español."
        ]
    )

    return jsonify({
        "transcripcion": respuesta.text
    })


@app.route("/transcribir-web", methods=["POST"])
def transcribir_web():

    archivo = request.files["audio"]

    ruta = os.path.join("audios", archivo.filename)

    archivo.save(ruta)

    myfile = client.files.upload(file=ruta)

    respuesta = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=[
            myfile,
            "Transcribe exactamente este audio en español."
        ]
    )

    return f"""
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Resultado</title>

<style>

body {{
    font-family: Arial, sans-serif;
    background: linear-gradient(135deg,#2563eb,#7c3aed);
    min-height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
}}

.card {{
    background:white;
    max-width:800px;
    padding:30px;
    border-radius:20px;
    box-shadow:0 10px 25px rgba(0,0,0,0.2);
}}

h1 {{
    color:#2563eb;
}}

p {{
    font-size:18px;
    line-height:1.6;
}}

a {{
    text-decoration:none;
    background:#2563eb;
    color:white;
    padding:10px 15px;
    border-radius:8px;
}}

</style>

</head>
<body>

<div class="card">

<h1>✅ Transcripción completada</h1>

<p>{respuesta.text}</p>

<br><br>

/⬅ Volver</a>

</div>

</body>
</html>
"""

if __name__ == "__main__":
    app.run(debug=True)