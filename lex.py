# -*- coding: UTF-8 -*-
import ply.lex as lex
import re

class MyLexer(object):
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

    # print(list(reserved.values()))
    tokens = list(tokens) + list(reserved.values())
    # print(tokens)

    DIGITO = r'[0-9]+'
    LETRA =  r'[a-zA-Z]+'

# Regras de expressões Regulares
    
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
    t_NUM_INTEIRO = r'\d+'
    t_NUM_PONTO_FLUTUANTE = r'\d+\.?\d*'
    t_NUM_NOTACAO_CIENTIFICA = r'\d+\.?\d*e(\+|-)?\d+' 
    # t_ignore  = ' \t\n\r'

    # Define a rule so we can track line numbers
    def t_newline(self,t):
         r'\n+'
         t.lexer.lineno += len(t.value)

    # def t_COMMENT(self,t):
    #     teste = t.math(r'\{.*\}',re.DOTALL)
    #     print(teste)
    #     pass
     # No return value. Token discarded

    def t_palavra_reservada(self,t):
        r'senão|se|então|fim|repita|até|leia|escreva|retorna|inteiro|flutuante'
        t.type = self.reserved.get(t.value,'PR')
        return t

    def t_COMMENT(self,t):
        r'\{.*?\}'

    def t_ESPACO_EM_BRANCO(self,t):
        '[ \n\r\t]+'
        pass

    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value,'ID')    # Check for reserved words
        return t

    # Error handling rule
    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1) 
 
     # Build the lexer
    def build(self,**kwargs):
         self.lexer = lex.lex(module=self, **kwargs)
     
    # EOF handling rule
    def t_eof(self,t):
     # Get more input (Example)
     more = raw_input('... ')
     if more:
         self.lexer.input(more)
         return self.lexer.token()
     return None

     # Test it output
    def test(self,data):
         self.lexer.input(data)
         while True:
              tok = self.lexer.token()
            #   print('*',tok,'*')
              if not tok: 
                  break
              print(tok)
 
 # Build the lexer and try it out
arq = open('fat.tpp', 'r', encoding='UTF-8' )
texto = arq.read()

m = MyLexer()
m.build()           # Build the lexer
# print(m.lexer.lineno) 
m.test(texto)     # Test it
print(m.lexer.lineno)