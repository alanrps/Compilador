import re

arq = open('/home/alan/Área de Trabalho/Compilador_Linguagem_Tpp/Exemplos/fat.tpp', 'r')
tokens = []

texto = arq.readlines()
# print(texto)

buffer = ''
for l in texto:
    for c in l:        
        if(re.search(r'\+',buffer)):
            tokens.append("MAIS")
            buffer = ''
        
        if(re.search(r'-',buffer)):
            tokens.append("MENOS")
            buffer = ''

        if(re.search(r'\*',buffer)):
            tokens.append("MULTIPLICACAO")
            buffer = ''

        if(re.search(r'/',buffer)):
            tokens.append("DIVISAO")
            buffer = ''

        if(re.search(r':',buffer)):
            tokens.append("DOIS_PONTOS")
            buffer = ''
        
        if(re.search(r',',buffer)):
            tokens.append("VIRGULA")
            buffer = ''
        
        if(re.search(r'<',buffer)):
            tokens.append("MENOR")
            buffer = ''
        
        if(re.search(r'>',buffer)):
            tokens.append("MAIOR")
            buffer = ''
        
        if(re.search(r'=',buffer)):
            tokens.append("IGUAL")
            buffer = ''
        
        if(re.search(r'<>',buffer)):
            tokens.append("DIFERENTE")
            buffer = ''
        
        if(re.search(r'<=',buffer)):
            tokens.append("MENOR_IGUAL")
            buffer = ''
        
        if(re.search(r'>=',buffer)):
            tokens.append("MAIOR_IGUAL")
            buffer = ''

        if(re.search(r'&&',buffer)):
            tokens.append("E_LOGICO")
            buffer = ''
        
        if(re.search(r'\|\|',buffer)):
            tokens.append("OU_LOGICO")
            buffer = ''
        
        if(re.search(r'!',buffer)):
            tokens.append("NEGACAO")
            buffer = ''

        if(re.search(r'\(',buffer)):
            tokens.append("ABRE_PARENTESE")
            buffer = ''

        if(re.search(r'\)',buffer)):
            tokens.append("FECHA_PARENTESE")
            buffer = ''
        
        if(re.search(r'\[',buffer)):
            tokens.append("ABRE_COLCHETE")
            buffer = ''

        if(re.search(r'\]',buffer)):
            tokens.append("FECHA_COLCHETE")
            buffer = ''
        
        if(re.search(r'se',buffer)):
            tokens.append("SE")
            buffer = ''
        
        if(re.search(r'então',buffer)):
            tokens.append("ENTAO")
            buffer = ''
        
        if(re.search(r'fim',buffer)):
            tokens.append("FIM")
            buffer = ''

        if(re.search(r'repita',buffer)):
            tokens.append("REPITA")
            buffer = ''

        if(re.search(r'até',buffer)):
            tokens.append("ATE")
            buffer = ''
        
        if(re.search(r':=',buffer)):
            tokens.append("ATRIBUICAO")
            buffer = ''
        
        if(re.search(r'leia',buffer)):
            tokens.append("LEIA")
            buffer = ''
        
        if(re.search(r'escreva',buffer)):
            tokens.append("ESCREVA")
            buffer = ''
        
        if(re.search(r'retorna',buffer)):
            tokens.append("RETORNA")
            buffer = ''
        
        if(re.search(r'inteiro',buffer)):
            tokens.append("INTEIRO")
            buffer = ''

        if(re.search(r'flutuante',buffer)):
            tokens.append("FLUTUANTE")
            buffer = ''
        
        if(re.search(r'inteiro',buffer)):
            tokens.append("INTEIRO")
            buffer = ''

        if(re.search(r'\d+',buffer)):
            tokens.append("NUM_INTEIRO")
            buffer = ''

        if(re.search(r'inteiro',buffer)):
            tokens.append("INTEIRO")
            buffer = ''

        if(re.search(r'\d+\.?\d*',buffer)):
            tokens.append("NUM_PONTO_FLUTUANTE")
            buffer = ''
        
        # if(re.search(r'\d+\.?\d*e(+|-)?\d+',buffer)):
        #     tokens.append("NUM_NOTACAO_CIENTIFICA")
        #     buffer = ''

        buffer = buffer + c
    buffer = ''

print(tokens)
arq.close()