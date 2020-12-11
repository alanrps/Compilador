# Bibliotecas utilizadas
import sys

# Utilizado para exportar gráficos
from anytree.exporter import UniqueDotExporter

# Módulos compilador
from lex import Lexer
from parser import Parser
from semantic import Semantic
from codeGenerate import CodeGenerate

# Lê todo o arquivo
codeFile = open(sys.argv[1], 'r', encoding = 'utf-8').read()

# Quantidade de linhas do arquivo
numberOfLines = sum(1 for line in open(sys.argv[1], 'r', encoding = 'utf-8'))

# Instãncia lexer para teste
# tppLexer = Lexer()
# tppLexer.lex(codeFile)

# Análisador sintático
parse = Parser()
resultTree, resultParser = parse.syntactic(codeFile, numberOfLines)

if(resultParser):
    # Cria gráfico com árvore sem podas
    UniqueDotExporter(resultTree).to_picture("tree.png")

    # Lista as funcoes e variáveis do programa 
    semantic = Semantic()
    tree, symbolTable, resultSemantics = semantic.semantics(resultTree)

    # Gráfico após as podas
    UniqueDotExporter(tree).to_picture("prunedTree.png")

    if(resultSemantics):
        codeGenerate = CodeGenerate()
        codeGenerate.code_generate(tree, symbolTable, resultSemantics)