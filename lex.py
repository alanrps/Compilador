# -*- coding: UTF-8 -*-
import ply.lex as lex

class Lexer(object):
    # Tupla, estática e pode ser heterogênea
    tokens = (
        'MAIS',
        'MENOS',
        'MULTIPLICACAO',
        'DIVISAO',
        'DOIS_PONTOS',
        'VIRGULA',
        'MENOR',
        'MAIOR',
        'IGUAL',
        'DIFERENTE',
        'MENOR_IGUAL',
        'MAIOR_IGUAL',
        'E_LOGICO',
        'OU_LOGICO',
        'NEGACAO',
        'ABRE_PARENTESE',
        'FECHA_PARENTESE',
        'ABRE_COLCHETE',
        'FECHA_COLCHETE',
        'ATRIBUICAO',
        'NUM_INTEIRO',
        'NUM_PONTO_FLUTUANTE',
        'NUM_NOTACAO_CIENTIFICA',
        'ID',
    )
    
    reserved = {
        'se':'SE',
        'senão':'SENAO',
        'então':'ENTAO',
        'fim':'FIM',
        'repita':'REPITA',
        'até':'ATE',
        'leia':'LEIA',
        'escreva':'ESCREVA',
        'retorna':'RETORNA',
        'inteiro':'INTEIRO',
        'flutuante':'FLUTUANTE',
    } 

    tokens = list(tokens) + list(reserved.values())

    # Regras de expressões Regulares
    t_ATRIBUICAO = r':='
    t_MAIS = r'\+'
    t_MENOS = r'-'
    t_MULTIPLICACAO = r'\*'
    t_DIVISAO = r'/'
    t_DOIS_PONTOS = r':'
    t_VIRGULA = r','
    t_MENOR = r'<'
    t_MAIOR = r'>'
    t_IGUAL = r'='
    t_DIFERENTE = r'<>'
    t_MENOR_IGUAL = r'<='
    t_MAIOR_IGUAL = r'>='
    t_E_LOGICO = r'&&'
    t_OU_LOGICO = r'\|\|'
    t_NEGACAO = r'!'
    t_ABRE_PARENTESE = r'\('
    t_FECHA_PARENTESE = r'\)'
    t_ABRE_COLCHETE = r'\['
    t_FECHA_COLCHETE = r'\]'

    # Expressão regular para números em notação cientifica
    def t_NUM_NOTACAO_CIENTIFICA(self,t):
        r'(([0-9]+\.[0-9]*)|((-|\+)?[0-9]+))(e|E)(-|\+)?[0-9]+' 
        t.value = float(t.value)

        return t
    
    # Expressão regular para números em ponto flutuante
    def t_NUM_PONTO_FLUTUANTE(self,t):
        r'[0-9]+\.[0-9]*'
        t.value = float(t.value)

        return t

    # Expressão regular para números inteiros
    def t_NUM_INTEIRO(self,t):
        r'[0-9]+'
        t.value = int(t.value)
        
        return t
    
    # Expressão regular para identificador
    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Zà-úÀ-Ú_0-9]*'
        t.type = self.reserved.get(t.value,'ID')    # verifica a correspondência com as palavras reservadas
        
        return t

    # Expressão regular para palavras reservadas
    def t_palavra_reservada(self,t):
        r'senão|se|então|fim|repita|até|leia|escreva|retorna|inteiro|flutuante'
        t.type = self.reserved.get(t.value,'PR')

        return t

    # Expressão regular para comentários
    def t_COMMENT(self,t):
        r'(\{(.|\n)*?\})|(\{(.|\n)*?)$'
        t.lexer.lineno += len(t.value.split('\n')) - 1

        pass

    # Expressão regular para espaços em branco, tabulação e carriage return
    def t_ESPACO_EM_BRANCO(self,t):
        '[ \r\t]+'
        pass

    # Expressão regular para quebra de linha
    def t_newline(self,t):
         r'\n+'
         t.lexer.lineno += len(t.value) # Faz a contagem da quantidade de linhas
    
    # # Calcula a coluna do token para caso ocorra algum erro
    # def find_column(self, t):
    #     line_start = codeFile.rfind('\n', 0, t.lexpos) + 1

    #     return (t.lexpos - line_start) + 1

    # Error 
    def t_error(self,t):
        # colunaToken = self.find_column(t)
        print("Caractere Ilegal:%s, linha:%d" % (t.value[0],t.lexer.lineno))
        t.lexer.skip(1) 
    
    def f_column(self, t):
        input = t.lexer.lexdata
        line_start = input.rfind('\n', 0, t.lexpos) + 1
        return (t.lexpos - line_start) + 1
        
    
    def printToken(self, tok):
        print('[',tok.value,']',' -> ','[',tok.type,']')

    # Build the lexer
    def __init__(self, **kwargs):
         self.lexer = lex.lex(module=self, debug=False, **kwargs)

    # Test it output
    def lex(self, data):
         self.lexer.input(data)
         while True:
              tok = self.lexer.token()
              if not tok: 
                  break
              self.printToken(tok)

# Instância o objeto Mylexer
l = lex.Lexer()

# Passa o texto do arquivo lido como argumento para fazer a coleta dos tokens
# l.lex(codeFile)