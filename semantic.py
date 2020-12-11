from anytree import Node
import anytree

class Semantic():
    def __init__(self, **kwargs):
        self.symbolTable = []
        self.attrVars = []
        self.variables = []
        self.attr = []
        self.arrayErrors = []
        self.scope = "global"
        self.indice = False
        self.found_node = None
        self.success = True
        self.errors = {
           "has_principal": False,
           "principal_has_return": False,
           "wrong_function_call": []
        }
        self.operations = ['+', '-', '*', '/', ':=', ':']
        self.listPruneNodes = [
            'acao', 'expressao', 'expressao_logica', 'expressao_simples', 'expressao_aditiva', 
            'expressao_multiplicativa', 'expressao_unaria', 'operador_relacional', 
            'operador_logico', 'operador_negacao', 'fator', 'lista_variaveis'
        ]


    # Funções utilizadas para fazer a poda da árvore
    def prune_especial(self, tree):
        aux = []

        if(tree.parent.name in ["operador_soma", "operador_multiplicacao"]):
            self.prune_one_node(tree.parent)

        dad = tree.parent
        aux = [dad.children[0], dad.children[2]] 
        tree.children = aux
        dad.children = [tree]
        
    def prune_one_node(self, tree):
        aux = []
        dad = tree.parent

        for i in range(len(dad.children)):
            if (dad.children[i].name == tree.name):
                aux += tree.children
            else:
                aux.append(dad.children[i])

        dad.children = aux

    def prune(self, tree):
        for node in tree.children:
            self.prune(node)

        if(tree.name in self.operations):
            self.prune_especial(tree)

        if(tree.name in self.listPruneNodes):
            self.prune_one_node(tree)
        
        if(tree.name in ['corpo', 'lista_declaracoes', 'lista_parametros', 'lista_argumentos'] and tree.parent.name == tree.name):
            self.prune_one_node(tree)

    def get_node(self, node, name):
        global found_node
        for n in node.children:
            if (n.name == name):
                found_node = n.children
            
            else:
                self.get_node(n, name)
        
        return found_node

    def find_scope(self, node):
        if(node.parent.name != "programa"):
            if(node.parent.name == "cabecalho"):
                self.scope = node.parent.children[0].name
            else:
                self.find_scope(node.parent)

    def get_func(self, func):
        for symbol in self.symbolTable:
            if(symbol["symbol_type"] == "function" and symbol["name"] == func):
                return symbol
        
        return None

    def get_attr(self, node):
        for n in node.children:
            if (n.name == "indice"):
                self.indice = True
            if (n.name == "var" and len(n.children) == 1):
                for s in self.symbolTable:
                    if (n.children[0].name == s["name"] and s["symbol_type"] == "variable"):
                        self.attrVars.append(s["value_type"])
            elif (n.name == "numero"):
                if (n.children[0].name.isdigit()):
                    self.attrVars.append("inteiro")
                else:
                    self.attrVars.append("flutuante")
            self.get_attr(n)

    # Função utilizada para gerar a tabela de símbolos
    def generate_symbol_table(self, tree):
        for node in tree.children:
            symbol = {
                "symbol_type": None,
                "name": None,
                "value_type": None,
                "scope": None,
                "parameters": [],
                "return": [],
                "dimensions": [],
                "declared": True,
                "inicialized": False,
                "used": False
            }

            if(node.name == "declaracao_funcao"):
                symbol["symbol_type"] = "function"
                symbol["value_type"] = self.get_node(node, "tipo")[0].name
                symbol["name"] = self.get_node(node, "cabecalho")[0].name

                retorno = self.get_node(node, "retorna")[2]

                if(retorno.name == "numero"):
                    ret_type = "inteiro"
                    if(not retorno.children[0].name.isdigit()):
                        ret_type = "flutuante"

                    symbol["return"].append({
                        "is_variable": False,
                        "ret_type": ret_type,
                        "ret_value": retorno.children[0].name
                    })

                elif(retorno.name == "var"):
                    ret_type = "inteiro"
                    
                    for s in self.symbolTable:
                        if(s["name"] == retorno.children[0].name and s["symbol_type"] == "variable"):
                            ret_type = s["value_type"]

                    symbol["return"].append({
                        "is_variable": True,
                        "ret_type": ret_type,
                        "ret_value": retorno.children[0].name
                    })

                for param in (self.get_node(node, "lista_parametros")):
                    if(param.name == "parametro"):
                        symbol["parameters"].append({
                            "par_type": self.get_node(param, "tipo")[0].name,
                            "par_name": self.get_node(param, ":")[1].name
                        })

                        self.symbolTable.append({
                            "symbol_type": "variable",
                            "name": self.get_node(param, ":")[1].name,
                            "value_type": self.get_node(param, "tipo")[0].name,
                            "scope": node.children[0].children[0].name,
                            "parameters": [],
                            "declared": True,
                            "inicialized": False,
                            "used": False
                        })
                self.symbolTable.append(symbol)

            elif(node.name == "declaracao_variaveis"):
                symbol["symbol_type"] = "variable"
                symbol["value_type"] = self.get_node(node, "tipo")[0].name
                symbol["name"] = self.get_node(node, "var")[0].name

                if(node.parent.name == "corpo"):
                    symbol["scope"] = node.parent.parent.children[0].name
                
                else:
                    symbol["scope"] = "global"

                
                if(len(node.children[0].children[1].children) > 1):
                    indice = node.children[0].children[1].children[1]

                    if(len(indice.children) == 3):
                        symbol["dimensions"].append(indice.children[1].children[0].name)
                    
                    elif(len(indice.children) >  3):
                        symbol["dimensions"].append(indice.children[0].children[1].children[0].name)
                        symbol["dimensions"].append(indice.children[2].children[0].name)
                self.symbolTable.append(symbol)

            self.generate_symbol_table(node)

    # Funções para fazer a checagem de erros
    def check_recursive_call(self, node):
        for n in node.children:
            if(n.name == "chamada_funcao" and n.children[0].name == "principal"):
                print("AVISO: Chamada recursiva para principal.")
            self.check_recursive_call(n)

    def check_main_function(self, tree):
        for node in tree.children:
            if(node.name == "cabecalho" and node.children[0].name == "principal"):
                self.check_recursive_call(node)
                self.errors["has_principal"] = True

                if(node.children[-1].children[-1].name == "retorna"):
                    self.errors["principal_has_return"] = True
                
            
            self.check_main_function(node)

    def check_func_call(self, tree):
        for node in tree.children:
            if(node.name == "chamada_funcao"):
                func = self.get_func(node.children[0].name)

                if(func == None):
                    self.success = False
                    print("ERRO: Chamada à função \'", func["name"], "\' que não foi declarada.")

                else:
                    func["used"] = True

                    if(node.children[0].name == "principal" and  node.parent.name == "corpo" and node.parent.parent.children[0].name != "principal"):
                        self.success = False
                        print("ERRO: Chamada para a função principal não permitida.")

                    else:
                        if(len(func["parameters"]) == 1):
                            if (len(func["parameters"]) != len(node.children[2].children)):
                                self.errors["wrong_function_call"].append(func["name"])
                        elif(len(func["parameters"]) > 1):
                            if (len(func["parameters"]) != len(node.children[2].children)-1):
                                self.errors["wrong_function_call"].append(func["name"])


            self.check_func_call(node)

    def check_not_used_functions(self):
        for symbol in self.symbolTable:
            if(symbol["symbol_type"] == "function" and not symbol["used"] and symbol["name"] != "principal"):
                print("AVISO: Função \'", symbol["name"], "\' declarada, mas não utilizada.")

    def check_var_errors(self):
        for symbol in self.symbolTable:
            if(symbol["symbol_type"] == "variable"):
                declared = symbol["declared"]
                inicialized = symbol["inicialized"]
                used = symbol["used"]

                if(declared and not inicialized or not used):
                    print("AVISO: Variável \'", symbol["name"], "\' declarada e não utilizada")

    def check_var_inicialization(self, tree):
        for node in tree.children:
            if (node.name in [":=", "leia", "escreva", "repita", "se", "lista_argumentos"]):
                for n in node.children:
                    if(n.name == "var"):
                        if (n.children[0].name not in self.variables):
                            self.variables.append(n.children[0].name)

                for symbol in self.symbolTable:
                    if(symbol["symbol_type"] == "variable" and symbol["name"] in self.variables):
                        self.find_scope(node)
                        if(symbol["scope"] == "global" or symbol["scope"] == self.scope):
                            symbol["used"] = True

                            if (node.name in [":=", "leia"]):
                                symbol["inicialized"] = True

            self.check_var_inicialization(node)

    def check_attrib(self, tree):
        value_type = ""
        for node in tree.children:
            if(node.name == ":="):
                self.indice = False
                self.attrVars = []
                self.get_attr(node)

                if(not self.indice):
                    for s in self.symbolTable:
                        if(s["symbol_type"] == "variable"):
                            if(s["name"] == node.children[0].children[0].name):
                                value_type = s["value_type"]
                    
                    if(value_type == "inteiro" and "flutuante" in self.attrVars):
                        print("AVISO: Atribuição de tipos distintos \'", node.children[0].children[0].name, "\' inteiro e expressão flutuante.")
                    
                    elif(value_type == "flutuante" and "inteiro" in self.attrVars):
                        print("AVISO: Atribuição de tipos distintos \'", node.children[0].children[0].name, "\' flutuante e expressão inteiro.")
            
            self.check_attrib(node)

    def check_array(self, node):
        indice = None
        aux = 1
        err = False
        for n in node.children:
            if(n.name == ":" and len(n.children[1].children) > 1):
                indice = n.children[1].children[1]
            
            elif(n.name == ":=" and len(n.children[0].children) > 1):
                indice = n.children[0].children[1]
                aux = 0

            if(indice != None):
                if(n.children[aux].children[0].name not in self.arrayErrors):
                    if(len(indice.children) == 3):
                        if(indice.children[1].name == "numero"):
                            if (not indice.children[1].children[0].name.isdigit()):
                                self.success = False
                                print("ERRO: Índice de array \'", n.children[aux].children[0].name ,"\' não inteiro.")
                                err = True
                        else:
                            var = indice.children[1].children[0].name
                            for s in self.symbolTable:
                                if(var == s["name"] and s["symbol_type"] == "variable" and s["value_type"] == "flutuante"):
                                    self.success = False
                                    print("ERRO: Índice de array \'", n.children[aux].children[0].name ,"\' não inteiro.")
                                    err = True
                    
                    else:
                        if(indice.children[0].children[1].name == "numero"):
                            if (not indice.children[0].children[1].children[0].name.isdigit()):
                                self.success = False
                                print("ERRO: Índice de array \'", n.children[aux].children[0].name ,"\' não inteiro.")
                                err = True
                        else:
                            var = indice.children[0].children[1].children[0].name
                            for s in self.symbolTable:
                                if(var == s["name"] and s["symbol_type"] == "variable" and s["value_type"] == "flutuante"):
                                    self.success = False
                                    print("ERRO: Índice de array \'", n.children[aux].children[0].name ,"\' não inteiro.")
                                    err = True

                        if(not err):
                            if(indice.children[2].name == "numero"):
                                if (not indice.children[2].children[0].name.isdigit()):
                                    self.success = False
                                    print("ERRO: Índice de array \'", n.children[aux].children[0].name ,"\' não inteiro.")
                                    err = True
                            else:
                                var = indice.children[2].children[0].name
                                for s in self.symbolTable:
                                    if(var == s["name"] and s["symbol_type"] == "variable" and s["value_type"] == "flutuante"):
                                        self.success = False
                                        print("ERRO: Índice de array \'", n.children[aux].children[0].name ,"\' não inteiro.")
                                        err = True

                if (err):
                    self.arrayErrors.append(n.children[aux].children[0].name)

            self.check_array(n)

    def check_index(self, node):
        indices = []
        for n in node.children:
            if(n.name == ":="):
                if(len(n.children[0].children) > 1):
                    indice = n.children[0].children[1]

                    if(len(indice.children) == 3):
                        if(indice.children[1].name == "numero"):
                            numero = indice.children[1].children[0].name

                            for s in self.symbolTable:
                                if(n.children[0].children[0].name == s["name"] and s["symbol_type"] == "variable"):
                                    if(numero >= s["dimensions"]):
                                        self.success = False
                                        print("ERRO: índice de array ", s["name"] ," fora do intervalo (out of range)")
                    
                    else:
                        if(indice.children[0].children[1].name == "numero"):
                            indices.append(indice.children[0].children[1].children[0].name)
                        
                        if(indice.children[2].name == "numero"):
                            indices.append(indice.children[2].children[0].name)

                        for s in self.symbolTable:
                                if(n.children[0].children[0].name == s["name"] and s["symbol_type"] == "variable"):
                                    if(len(s["dimensions"]) > 0):
                                        for i in range(len(s["dimensions"])):

                                            if(int(indices[i]) >= int(s["dimensions"][i])):
                                                self.success = False
                                                print("ERRO: índice de array ", s["name"] ," fora do intervalo (out of range)")
                                                break




            self.check_index(n)

    def semantics(self, tree):

        # Faz a podagem da árvore de acordo com várias funções
        self.prune(tree)

        # Gera uma tabela com informações de tipo, nome, escopo, dentre outros
        self.generate_symbol_table(tree)

        # Checa se o código possuí uma função principal
        self.check_main_function(tree)

        if(not self.errors["has_principal"]):
            self.success = False
            print("ERRO: Função principal não declarada.")
        
        elif(not self.errors["principal_has_return"]):
            self.success = False
            print("ERRO: Função principal deveria retornar inteiro, mas retorna vazio.")
        
        # Verificação de chamadas de função 
        self.check_func_call(tree)
        self.check_not_used_functions()

        if(len(self.errors["wrong_function_call"]) > 0):
            for err in self.errors["wrong_function_call"]:
                self.success = False
                print("ERRO: Chamada à função \'", err , "\' com número de parâmetros diferente que o declarado.")

        # Faz a checagem da inicialização de variáveis
        self.check_var_inicialization(tree)

        for symbol in self.symbolTable:
            if (symbol["name"] in self.variables):
                self.variables.remove(symbol["name"])

            if(symbol["symbol_type"] == "variable"):
                if (not symbol["inicialized"] and not symbol["used"]):
                    print("AVISO: Variável \'", symbol["name"] , "\' declarada e não utilizada.")
                
                elif(not symbol["inicialized"] and symbol["used"]):
                    print("AVISO: Variável \'", symbol["name"] , "\' declarada e não inicializada.")
        
        if(len(self.variables) > 0):
            for var in self.variables:
                self.success = False
                print("ERRO: Variável \'", var ,"\'  não declarada.")

        count = 0

        for s in self.symbolTable:
            for t in self.symbolTable:
                if (s["name"] == t["name"] and s["scope"] == t["scope"]):
                    count += 1
            
            if(count > 1):
                print("AVISO: Variável \'", t["name"] ,"\' já declarada anteriormente")

            count = 0
        
        # Checa tipos dos atributos, como inteiro e ponto flutuante por exemplo
        self.check_attrib(tree)

        # Checa os arrays, como se está sendo feito o acesso aos indíces corretos
        self.check_array(tree)
        self.check_index(tree)

        return tree, self.symbolTable, self.success