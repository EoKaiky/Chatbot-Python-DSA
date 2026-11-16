import os
import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="AI Privalia",
    page_icon="*",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_PROMPT = """
Você é o "Funcionario", um assistente de IA especialista em programação, com foco principal em Python e Resolução de problemas. Sua missão é ajudar desenvolvedores iniciantes com dúvidas de programação de forma clara, precisa e útil.

REGRAS DE OPERAÇÃO:
1.  **Foco em Programação**: Responda apenas a perguntas relacionadas a programação, algoritmos, estruturas de dados, bibliotecas e frameworks. Se o usuário perguntar sobre outro assunto, responda educadamente que seu foco é exclusivamente em auxiliar com código.
2.  **Estrutura da Resposta**: Sempre formate suas respostas da seguinte maneira:
    * **Explicação Clara**: Comece com uma explicação conceitual sobre o tópico perguntado. Seja direto e didático.
    * **Exemplo de Código**: Forneça um ou mais blocos de código em Python com a sintaxe correta. O código deve ser bem comentado para explicar as partes importantes.
    * **Detalhes do Código**: Após o bloco de código, descreva em detalhes o que cada parte do código faz, explicando a lógica e as funções utilizadas.
    * **Documentação de Referência**: Ao final, inclua uma seção chamada "📚 Documentação de Referência" com um link direto e relevante para a documentação oficial da Linguagem Python (docs.python.org) ou da biblioteca em questão.
3.  **Clareza e Precisão**: Use uma linguagem clara. Evite jargões desnecessários. Suas respostas devem ser tecnicamente precisas.
"""

with st.sidebar:

    st.title("AIssistente Kaiky")

    groq_api_key = st.text_input(
        "Insira sua API Key Groq",
        type="password",
        help="Obtenha sua chave em https://console.groq.com/keys"
    )

    st.markdown("---")
    st.markdown("Desenvolvido para ser um assistente pessoal do Kaiky")
    
    st.markdown("---")
    st.markdown("Conheça os Cursos Individuais, Formações e Programas de Pós-Graduação da DSA")
    st.link_button("Email para teste de suporte", "mailto:testedasilva@gmail.com")

st.title("Assistente - Funcionario do Kaiky")

st.caption("Oque igor guilherme anda pensando?")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

client = None

#Verifica se o usuario forneceu a APY
if groq_api_key:

    try:
        
        #Cria cliente Groq com a chave API fornecida
        client = Groq(api_key= groq_api_key)

    except Exception as e:
    
        st.sidebar.error(f"Erro ao inicializar o cliente Groq:  {e}")
        st.stop()

elif st.session_state.messages:
    st.warning("Por favor, insira sua API Key da Groq na barra lateral para continuar.")


if prompt := st.chat_input("Oque você precisa hoje?"):

    if not client:
        st.warning("Por favor, insira uma API Key")
        st.stop()

    #Armaazena mensagem do usuario no estado da sessão
    st.session_state.messages.append({"role": "user", "content": prompt})

    #Exibe mensagem do usuario no chat (comandos ST funcionam para exibição ou manipulação visual)
    with st.chat_message("user"):
        st.markdown(prompt)

    #Prepara mensagens para enviar a API
    messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
    for msg in st.session_state.messages:

        messages_for_api.append(msg)

    #Criando resposta
    with st.chat_message("assistant"):

        with st.spinner("Analisando pergunta..."):

            try:

                # Chama a API da Groq para gerar respostas
                chat_completion = client.chat.completions.create(
                    messages= messages_for_api,
                    model = "openai/gpt-oss-120b",
                    temperature= 0.7,
                    max_tokens = 2048
                )

                funcionario_resposta = chat_completion.choices[0].message.content

                #exibe resposta do assistente
                st.markdown(funcionario_resposta)

                st.session_state.messages.append({"role": "assistant", "content": funcionario_resposta})
            
            except Exception as e:
                st.error(f"Ocorreu um erro ao se comunicar com a API Groq: {e}")

st.markdown(
    """
    <div style="text-align: center; color: gray;">
        <hr>
        <p>Funcionario AI Coder - Parte Integrante do Cruso Fundamentos de Linguagem Python da Data Scince Academy</p>
    </div>    
    """,
    unsafe_allow_html=True
)

            