import requests

API_KEY = 'AIzaSyADZwhyN67hO5Otuqc3MCfrxZ5-N7jIF0k'  

def verificar_noticia(texto):
    url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    params = {
        "query": texto,
        "key": API_KEY
    }

    resposta = requests.get(url, params=params)
    dados = resposta.json()

    if "claims" in dados:
        for claim in dados["claims"]:
            texto = claim.get("text", "Sem texto")
            fonte = claim["claimReview"][0]["publisher"]["name"]
            veredito = claim["claimReview"][0]["textualRating"]
            link = claim["claimReview"][0]["url"]

            print("🔎 Notícia:", texto)
            print("📰 Fonte:", fonte)
            print("✅ Veredito:", veredito)
            print("🔗 Link:", link)
            print("="*50)
    else:
        print("❌ Nenhum resultado encontrado.")

entrada = input("Digite a notícia para verificar: ")
verificar_noticia(entrada)
