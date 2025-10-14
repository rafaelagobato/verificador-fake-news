from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)
API_KEY = 'AIzaSyADZwhyN67hO5Otuqc3MCfrxZ5-N7jIF0k'

HTML = '''
<!DOCTYPE html>
<html>
<head><title>Verificador de Fake News</title></head>
<body>
    <h1>Verifique sua notícia</h1>
    <form method="POST">
        <input type="text" name="noticia" placeholder="Digite a notícia aqui" required style="width:300px;">
        <button type="submit">Verificar</button>
    </form>
    {% if resultados %}
        <h2>Resultados:</h2>
        {% for r in resultados %}
            <div style="border:1px solid #ccc; padding:10px; margin-top:10px;">
                <p><strong>Notícia:</strong> {{ r['text'] }}</p>
                <p><strong>Fonte:</strong> {{ r['publisher'] }}</p>
                <p><strong>Veredito:</strong> {{ r['claimReview'] }}</p>
                <p><a href="{{ r['url'] }}" target="_blank">Ver mais</a></p>
            </div>
        {% endfor %}
    {% elif resultados is not none %}
        <p><strong>Nenhum resultado encontrado.</strong></p>
    {% endif %}
</body>
</html>
'''

def search_fact_check(query):
    url = f"https://factchecktools.googleapis.com/v1alpha1/claims:search?key={API_KEY}&query={query}"
    resp = requests.get(url)
    if resp.status_code != 200:
        return None
    data = resp.json()
    results = []
    for claim in data.get('claims', []):
        text = claim.get('text', 'Sem texto')
        publisher = claim.get('claimReview', [{}])[0].get('publisher', {}).get('name', 'Sem fonte')
        claimReview = claim.get('claimReview', [{}])[0].get('textualRating', 'Sem veredito')
        url = claim.get('claimReview', [{}])[0].get('url', '#')
        results.append({'text': text, 'publisher': publisher, 'claimReview': claimReview, 'url': url})
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    resultados = None
    if request.method == 'POST':
        noticia = request.form.get('noticia')
        resultados = search_fact_check(noticia)
    return render_template_string(HTML, resultados=resultados)

if __name__ == '__main__':
    app.run(debug=True)
