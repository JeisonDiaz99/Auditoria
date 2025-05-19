from flask import Blueprint, render_template, request, redirect, flash, url_for
from src.utils.text_process import DocumentProcessorFactory
from src.settings import Settings
import requests

settings = Settings.get_config()


index_bp = Blueprint('index', __name__)


# MAIN SECTION
@index_bp.route("/", methods=["GET", "POST"])
def index():
    """
    Main page of the application.
    """
    if request.method == 'POST':
        pdf_file = request.files["pdf_file"]
        print(type(pdf_file))
        print(pdf_file.content_type)
        if not pdf_file:
            flash("No se ha cargado el archivo.")
            return redirect(url_for("index.index"))
            
        password = request.form.get("password")
        if not password:
            flash("No se ha ingresado la contraseña.")
            return redirect(url_for("index.index"))
            
        if password != settings.API_KEY:
            flash("Contraseña incorrecta.")
            return redirect(url_for("index.index"))
        
        try:
            processor = DocumentProcessorFactory.get_processor(pdf_file)
            processed_data = processor.process()
            text = processed_data["text"]
            print(f"Texto extraído: {text}")
            request_n8n = requests.post(
                url=settings.N8N_WEBHOOK_URL,
                json={
                    "text": text,
                    "file_type": processed_data["file_type"]
                },
                files={
                    "file": (pdf_file.filename, pdf_file.read(), pdf_file.content_type)
                }
            )
            # Process the text as needed
            # For example, you can save it to a database or perform further analysis
            print(f"Respuesta de n8n: {request_n8n.json()}")
            if request_n8n.status_code != 200:
                flash("Error al enviar el texto a n8n.")
                return redirect(url_for("index.index"))
            
            flash("Archivo procesado exitosamente.")
            return render_template("index.html")
        except Exception as e:
            flash(f"Error al procesar el archivo: {str(e)}")
            return redirect(url_for("index.index"))
    return render_template("index.html")