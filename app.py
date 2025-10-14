import os
from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)
API_KEY = os.environ.get('AIzaSyADZwhyN67hO5Otuqc3MCfrxZ5-N7jIF0k')  # pegar a chave da variável ambiente

HTML_PAGE = '''
<!doctype html>
<title>Verificador de Fake News</title>
<h1>Verifique sua notícia</h1>
<form method=post>
  <textarea name=text rows=4 cols=50 placeholder="Digite sua notícia aqui...">{{ request.form.text }}</textarea><br><br>
  <input type=submit value=Verificar>
</form>

{% if results %}
  <h2>Resultados:</h2>
  {% for r in results %}
    <div style="margin-bottom:20px; padding:10px; border:1px solid #ccc;">
      <strong>🔎 Notícia:</strong> {{ r['text'] }}<br>
      <strong>📰 Fonte:</strong> {{ r['publisher'] }}<br>
      <strong>✅ Veredito:</strong> {{ r['claimReview'] }}<br>
      <a href="{{ r['url'] }}" target="_blank">🔗 Link</a>
    </div>
  {% endfor %}
{% elif results is not none %}
  <p>Nenhum resultado encontrado.</p>
{% endif %}
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
    results = None
    if request.method == 'POST':
        query = request.form['text']
        results = search_fact_check(query)
    return render_template_string(HTML_PAGE, results=results)

if __name__ == '__main__':
    app.run(debug=True)
