# Bibliotecas utilizadas
import sys
from anytree.exporter import UniqueDotExporter

# Módulos do compilador
from parser import Parser
from lex import Lexer

# Lê todo o arquivo
codeFile = open(sys.argv[1], 'r', encoding = 'utf-8').read()
# Quantidade de linhas do arquivo
numberOfLines = sum(1 for line in open(sys.argv[1], 'r', encoding = 'utf-8'))

# Instãncia para teste do lexer
tppLexer = Lexer()
tppLexer.lex(codeFile)

# Análisador sintático
parse = Parser()
resultTree, result = parse.input(codeFile, numberOfLines)

if(result):
    UniqueDotExporter(resultTree).to_picture("tree.png")