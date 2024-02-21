import openai




async def get_classification(pergunta, model="gpt-3.5-turbo"):
    
    prompt = f"""Estou enviando uma pergunta enviada por um aluno, delimitada por ###.
                Você deve retornar somente a matérias que está mais relacionada à pergunta, dentre as matérias abaixo, responda com um ponto final imediatamente após a resposta.
                Matérias: (Matemática, Física, Química, Biologia, História, Geografia, Filosofia, Sociologia, Inglês, Espanhol, Português, História da Arte, Literatura, Redação, Orientação de Estudos, Ensino Religioso)

                ###
                {pergunta}
                ###

                Matéria relacionada à pergunta:"""

    openai.api_key = 'INSIRA CHAVE AQUI'
    messages = [{"role": "user", "content": prompt}]

    respose = openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
        max_tokens=1000, # the maximum number of tokens the model can ouptut 
    )
    text_response = respose.choices[0].message.content
    return text_response

def is_classification_valid(classification, response):
    return classification == response

async def evaluate_classification():
    evaluate_counter = 0
    duvidas_dict = {
        'Química.': [
            'Como são formadas as cavernas?',
            'E as estalactites e estalagmites?'
        ],
        'Biologia.': [
            'Qual a diferença entre a gordura animal e a gordura vegetal hidrogenada?',
            'Qual a relação das mitocôndrias com a síntese proteica?'
        ],
        'Matemática.': [
            'Como funciona a relação do ângulo externo do triângulo com os outros dois ângulos internos do triângulo?',
            'Sejam dois conjuntos não vazios...',
            'Quanto vale 18 rad?',
            'Se {-1; 2x+y; 2; 3; 1} = {2; 4; x-y; 1; 3}, então...'
        ],
        'História.': [
            'Entre as consequências da Expansão Marítima, não encontramos...'
        ],
        'Literatura.': [
            'Ainda não entendi o que significa eu lírico, pode me explicar?'
        ],
        'Física.': [
            'Todos os conceitos de potencial (potencial gravitacional, potencial elétrico, etc) utilizam noções de trabalho? Por quê?'
        ]
    }
    total_duvidas = sum(len(duvidas) for duvidas in duvidas_dict.values())
    for materia, perguntas in duvidas_dict.items():
        for pergunta in perguntas:
            classification = await get_classification(pergunta)
            if is_classification_valid(classification, materia):
                evaluate_counter += 1
                
    evaluate_counter = (evaluate_counter / total_duvidas) * 100
    return evaluate_counter


