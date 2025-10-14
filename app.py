from flask import Flask, request, render_template_string
from verificador import verificar_noticia

app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Verificador de Fake News</title>
</head>
<body>
    <h1>Verificador de Fake News</h1>
    <form method="POST">
        <input type="text" name="noticia" placeholder="Digite a notícia aqui" style="width:300px;" required>
        <button type="submit">Verificar</button>
    </form>

    {% if resultados %}
        <h2>Resultados:</h2>
        {% for r in resultados %}
            <div style="border:1px solid #ccc; padding:10px; margin-top:10px;">
                <p><strong>Notícia:</strong> {{ r['title'] }}</p>
                <p><strong>Fonte:</strong> {{ r['source'] }}</p>
                <p><strong>Veredito:</strong> {{ r['veredito'] }}</p>
                <p><a href="{{ r['link'] }}" target="_blank">Ver mais</a></p>
            </div>
        {% endfor %}
    {% elif request.method == 'POST' %}
        <p><strong>Nenhum resultado encontrado.</strong></p>
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    resultados = []
    if request.method == 'POST':
        noticia = request.form.get('noticia')
        if noticia:
            resultados = verificar_noticia(noticia)
    return render_template_string(HTML, resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)
