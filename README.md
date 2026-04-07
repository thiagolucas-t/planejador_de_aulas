# Sistema de Geração de Planos de Aula com IA

## Descrição

Este projeto consiste em um sistema inteligente para geração automática de planos de aula utilizando modelos de linguagem (LLMs).

O sistema recebe informações do usuário e gera um plano completo, incluindo conteúdo pedagógico e elementos de gamificação, além de permitir refinamento iterativo.

---

## Funcionalidades

* Geração automática de planos de aula
* Aplicação de gamificação educacional
* Pipeline modular com múltiplas etapas
* Refinamento iterativo com base em feedback
* Persistência dos dados com histórico completo
* Interface web interativa com Streamlit

---

## Arquitetura do Pipeline

O sistema segue um pipeline com 3 etapas principais:

1. **Análise de Input**

   * Validação e normalização dos dados do usuário

2. **Geração de Conteúdo (LLM)**

   * Criação do plano de aula estruturado

3. **Formatação Gamificada**

   * Aplicação de mecânicas de jogo ao conteúdo

---

## Tecnologias Utilizadas

* Python
* Streamlit
* Ollama (LLM local)
* Requests (requisições HTTP)

---

## Dependências

### Instalar bibliotecas Python

```bash
pip install streamlit requests
```

---

### Instalar o Ollama

Baixe em:

https://ollama.com

---

### Rodar modelo local

```bash
ollama run llama3
```

---

## Como Executar

```bash
python -m streamlit run app.py
```

---

## Persistência de Dados

Os dados são armazenados em:

```text
data/aulas.json
```

O sistema salva:

* Tema
* Nível
* Objetivo
* Data de criação
* Histórico completo de refinamentos

---

## Refinamento Iterativo

O usuário pode fornecer feedback para:

* Ajustar conteúdo
* Adicionar exercícios
* Melhorar explicações

O sistema responde apenas com as modificações solicitadas.

---

## Uso de Prompt Engineering

O sistema utiliza:

* Role Prompting
* Instruções estruturadas
* Prompts modulares
* Instruções restritivas

Essas técnicas garantem maior controle sobre a saída da LLM.

---

## Diferenciais

* Separação clara de pipeline
* Controle fino da geração com IA
* Persistência com histórico completo
* Interface simples e funcional

---

## Autor

Projeto desenvolvido como atividade acadêmica na disciplina de Programação Avançada.
