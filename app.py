import requests



# 1 - Análise do Input

def analyze_input(data):
  
    erros = []

    tema = data.get("tema", "").strip()
    nivel = data.get("nivel", "").strip()
    objetivo = data.get("objetivo", "").strip()

    if not tema:
        erros.append("Tema não informado.")
    if not objetivo:
        erros.append("Objetivo não informado.")

    if erros:
        return {
            "erro": True,
            "mensagens": erros
        }

    return {
        "tema": tema,
        "nivel": nivel,
        "objetivo": objetivo
    }


# 2 - Gerar o Conteúdo

def generate_content(data):
    prompt = f"""
Você é um professor especialista em didática e design instrucional.

Crie um plano de aula COMPLETO.

Tema: {data['tema']}
Nível: {data['nivel']}
Objetivo: {data['objetivo']}

A resposta deve ser OBRIGATORIAMENTE em português (pt-br)
Estruture em Markdown com e IGNORE as seções Sistema de Pontuação, Níveis e Desafio Final, elas serão preenchidas pela próxima função:
Evite exercícios muito simples, tente gerar blocos de código e texto sempre que possível.

# 📘 Título da Aula
## 🎯 Objetivo
## 📖 Introdução
## 🧠 Conteúdo Teórico (passo a passo)
## ✏️ Exemplos Resolvidos
## 📝 Exercícios
## ✅ Gabarito Comentado
## 🎮 Sistema de Pontuação
- Gamificação
## 🏆 Níveis 
- Gamificação
## 🎯 Desafio Final 
- Gamificação



Seja claro, didático e organizado.
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        if response.status_code == 200:
            return response.json().get("response", "Erro: resposta vazia")
        else:
            return f"Erro na API: {response.status_code}"

    except Exception as e:
        return f"Erro ao conectar com Ollama: {e}"
