import requests
import streamlit as st
import json
import uuid
import os
from datetime import datetime

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
## ✅ Gabarito

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

# 3 - Gamificação do Conteúdo

def apply_gamification(content, data):

    if not content:
        return "Erro: conteúdo vazio"

    prompt = f"""

A resposta deve ser OBRIGATORIAMENTE em português (pt-br)
Você é especialista em gamificação educacional.
Seja criativo, evite respostas curtas para preencher as seções e indique plataformas de gamificação que podem ser usadas para implementar a dinâmica.

-----------------------------------
{content}
-----------------------------------

Para cada seção:

🎮 Sistema de Pontuação
Explique como funciona a pontuação

🏆 Níveis
Defina níveis com critérios claros

🎯 Desafio Final
Crie um desafio coerente com o tema: {data['tema']}

-----------------------------------

Retorne o plano COMPLETO atualizado.
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
            return response.json().get("response", content)
        else:
            return content

    except Exception as e:
        return content + f"\n\nErro: {e}"

# Pipeline

def pipeline(data):
    step1 = analyze_input(data)

    if "erro" in step1:
        return {
            "erro": True,
            "mensagens": step1["mensagens"]
        }

    step2 = generate_content(step1)
    step3 = apply_gamification(step2, step1)

    resultado_final = step2 + "\n\n---\n\n" + step3

    return {
        "erro": False,
        "resultado": resultado_final
    }

# Sistema de Arquivos

def save_or_update_history(data, historico):

    os.makedirs("data", exist_ok=True)
    file_path = "data/aulas.json"

    registros = []

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            try:
                registros = json.load(f)
            except:
                registros = []

    atualizado = False

    for r in registros:
        if r["id"] == data["id"]:
            r["historico"] = historico
            atualizado = True
            break

    if not atualizado:
        registros.append({
            "id": data["id"],
            "tema": data["tema"],
            "nivel": data["nivel"],
            "objetivo": data["objetivo"],
            "criado_em": datetime.now().isoformat(),
            "historico": historico
        })

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(registros, f, ensure_ascii=False, indent=2)


# Interface Web

st.set_page_config(page_title="Plano de Aula com IA", layout="centered")

st.title("Plano de Aula com IA 🎓")
st.write("Preencha os dados e gere automaticamente uma aula completa.")

tema = st.text_input("Tema da aula")
nivel = st.selectbox("Nível", ["Iniciante", "Intermediário", "Avançado"])
objetivo = st.text_area("Objetivo de aprendizagem")

if st.button("Gerar Aula"):

    data = {
        "tema": tema,
        "nivel": nivel,
        "objetivo": objetivo,
        "id": str(uuid.uuid4())
    }

    with st.spinner("Gerando aula com IA..."):

        response = pipeline(data)

        if response["erro"]:
            for msg in response["mensagens"]:
                st.warning(msg)
        else:
            st.session_state["historico"] = [response["resultado"]]
            save_or_update_history(data, st.session_state["historico"])
            st.session_state["data"] = data

def refine_content(original_content, feedback, data):
    prompt = f"""
Você é um professor especialista em didática.

Sua tarefa é RESPONDER APENAS com o ajuste solicitado pelo usuário.

-----------------------------------
REGRAS (OBRIGATÓRIAS):

- NÃO reescreva o plano de aula
- NÃO repita conteúdos anteriores
- NÃO recrie títulos já existentes
- NÃO explique o que você fez
- NÃO diga "aqui está o plano atualizado"

✔ Retorne SOMENTE o conteúdo novo solicitado

-----------------------------------

CONTEXTO:

Tema: {data['tema']}

-----------------------------------

PLANO ORIGINAL (APENAS PARA REFERÊNCIA):
{original_content}

-----------------------------------

FEEDBACK DO USUÁRIO:
{feedback}


"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 400
                }
            }
        )

        if response.status_code == 200:
            data_json = response.json()

            if "response" in data_json and data_json["response"].strip():
                print(response.json())
                return data_json["response"]
            else:
                print(response.json())
                return original_content + "\n\n⚠️ Refinamento não gerou resposta válida."

        else:
            print(response.json())
            return original_content + f"\n\nErro na API: {response.status_code}"

    except Exception as e:
        return original_content + f"\n\nErro no refinamento: {e}"


#  FEEDBACK ITERATIVO
if "historico" in st.session_state:

    st.success("Aula gerada com sucesso!")

    for i, versao in enumerate(st.session_state["historico"]):
        if i == 0:
            st.markdown("### Plano de Aula Inicial")
        else:
            st.markdown(f"### 🔄 Ajustes")

        st.markdown(versao)
        st.markdown("---")

    st.markdown("### 💬 Feedback")
    st.write(
        "O plano de aula está de acordo com o esperado?"
    )

    feedback = st.text_area(
        "Ajuste seu plano de aula:",
        key="feedback_input",
        value="",
        placeholder="Pergunte alguma coisa"
    )

    col1, col2 = st.columns(2)

    # Botão Feedback (loop)
    with col1:
        if st.button("🔄 Ajustar Aula"):
            if feedback:
                with st.spinner("Refinando aula com base no feedback..."):

                    ultimo = st.session_state["historico"][-1]

                    novo_resultado = refine_content(
                        ultimo,
                        feedback,
                        st.session_state["data"]
                    )
                    st.session_state["historico"].append(novo_resultado)
                    save_or_update_history(st.session_state["data"], st.session_state["historico"])

                    st.success("Aula refinada com sucesso!")

                    st.rerun()

            else:
                st.warning("Digite um feedback!.")

    # BOTÃO RESETAR
    with col2:
        if st.button("♻️ Gerar Nova Aula"):
            st.session_state.clear()
            st.rerun()