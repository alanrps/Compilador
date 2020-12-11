from llvmlite import ir
from llvmlite import binding as llvm
import itertools

class CodeGenerate():
    def __init__(self, **kwargs):
        self.info = {"global_variables": [] }
        self.local_vars = []
        self.aux = []
        self.functions = []
        self.module = ir.module.Module()

        llvm.initialize()
        llvm.initialize_all_targets()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()

        module = ir.Module('module.bc')
        module.triple = llvm.get_default_triple()
        target = llvm.Target.from_triple(module.triple)
        target_machine = target.create_target_machine()
        module.data_layout = target_machine.target_data

        self.escrevaInteiro = ir.Function(module,ir.FunctionType(ir.VoidType(), [ir.IntType(32)]),name="escrevaInteiro")
        self.escrevaFlutuante = ir.Function(module,ir.FunctionType(ir.VoidType(),[ir.FloatType()]),name="escrevaFlutuante")
        self.leiaInteiro = ir.Function(module,ir.FunctionType(ir.IntType(32),[]),name="leiaInteiro")
        self.leiaFlutuante = ir.Function(module,ir.FunctionType(ir.FloatType(),[]),name="leiaFlutuante")


    def find_var(self, name, local_vars, function):
        for var in self.info["global_variables"] + local_vars:
            if(var.name == name):
                return var, "var"
        
        for arg in function["function"].args:
            if(arg.name == name):
                return arg, "arg"


    def solve_expression(self, n, local_vars, function):
        param_1 = 0
        param_2 = 0

        if(n.children[0].name == "numero"):
            param_1 = ir.Constant(ir.IntType(32), int(n.children[0].children[0].name))
        elif(n.children[0].name == "var"):
            ret, what = self.find_var(n.children[0].children[0].name, local_vars, function)

            if(what == "var"):
                param_1 = function["builder"].load(ret)
            
            else:
                param_1 = ret
        
        if(n.children[1].name == "numero"):
            param_2 = ir.Constant(ir.IntType(32), int(n.children[1].children[0].name))
        elif(n.children[1].name == "var"):
            ret, what = self.find_var(n.children[1].children[0].name, local_vars, function)
            
            if(what == "var"):
                param_2 = function["builder"].load(ret)
            
            else:
                param_2 = ret
            
        if(n.name == "+"): return function["builder"].add(param_1, param_2, name='summ')
        elif(n.name == "-"): return function["builder"].sub(param_1, param_2, name='sub')
        elif(n.name == "*"): return function["builder"].mul(param_1, param_2, name='mult')
        elif(n.name == "/"): return function["builder"].sdiv(param_1, param_2, name='div')


    def solve_func_call(self, n, builder, local_vars, function):
        params = []

        for f in self.functions:
            if(f["function"].name == n.children[0].name):
                if(len(n.children[2].children) > 0):
                    for arg in n.children[2].children:
                        if(arg.name == "var"):
                            ret, what = self.find_var(arg.children[0].name, local_vars, f)
                            params.append(
                                function["builder"].load(ret)
                            )
                        elif(arg.name == "numero"):
                            params.append(
                                ir.Constant(ir.IntType(32), int(arg.children[0].name))
                            )
                    return builder.call(f["function"], params)

                else:
                    return builder.call(f["function"], [])

    def fill_function(self, corpo, function):
        for node in corpo.children:
            if(node not in self.aux):
                self.aux.append(node)
                if(node.name == "declaracao_variaveis"):
                    if(node.children[0].children[0].children[0].name == "inteiro"):
                        var = function["builder"].alloca(ir.IntType(32), name=node.children[0].children[1].children[0].name)

                    elif(node.children[0].children[0].children[0].name == "flutuante"):
                        var = function["builder"].alloca(ir.FloatType(), name=node.children[0].children[1].children[0].name)

                    var.align = 4
                    self.local_vars.append(var)
                
                elif(node.name == "atribuicao"):
                    # Atribuição de um único número ou uma única variável.

                    if(node.children[0].children[1].name == "numero" or node.children[0].children[1].name == "var"):
                        var = 0
                        
                        for local in self.local_vars + self.info["global_variables"]:
                            if(local.name == node.children[0].children[0].children[0].name):
                                var = local

                        if(node.children[0].children[1].name == "var"):
                            self.aux = self.local_vars + self.info["global_variables"]

                            for a in self.aux:
                                if(node.children[0].children[1].children[0].name == a.name):
                                    temp = function["builder"].load(a,"")
                                    function["builder"].store(temp, var)
                        
                        else:
                            if(str(var.type) == "i32*"):
                                function["builder"].store(ir.Constant(ir.IntType(32),  int(node.children[0].children[1].children[0].name)) , var)
                            
                            elif(str(var.type) == "float*"):
                                function["builder"].store(ir.Constant(ir.FloatType(),  float(node.children[0].children[1].children[0].name)) , var)

                    elif(node.children[0].children[1].name in ["+", "-", "*", "/"]):
                        op = self.solve_expression(node.children[0].children[1] ,self.local_vars, function)
                        ret, what = self.find_var(node.children[0].children[0].children[0].name,self.local_vars, function)
                        function["builder"].store(op, ret)

                    elif(node.children[0].children[1].name == "chamada_funcao"):
                        f = self.solve_func_call(node.children[0].children[1], function["builder"], self.local_vars, function)
                        ret, what = self.find_var(node.children[0].children[0].children[0].name ,self.local_vars, function)
                        function["builder"].store(f, ret)

                elif(node.name == "repita" and len(node.children) > 0):
                    repita = function["builder"].append_basic_block('repita')
                    ate = function["builder"].append_basic_block('ate')
                    repita_fim = function["builder"].append_basic_block('repita_fim')

                    function["builder"].branch(repita)
                    function["builder"].position_at_end(repita)
                    self.fill_function(node.children[1], function)
                    function["builder"].branch(ate)

                    function["builder"].position_at_end(ate)
                    
                    aux_1 = None
                    if (node.children[3].name == "var"):
                        for var in self.local_vars + self.info["global_variables"]:
                            if (var.name == node.children[3].children[0].name):
                                aux_1 = function["builder"].load(var, 'aux_1', align=4)
                    
                    elif (node.children[3].name == "numero"):
                        aux_1 = ir.Constant(ir.IntType(32), int(node.children[3].children[0].name))

                    aux_2 = None
                    if (node.children[5].name == "var"):
                        for var in self.local_vars + self.info["global_variables"]:
                            if (var.name == node.children[5].children[0].name):
                                aux_2 = function["builder"].load(var, 'aux_1', align=4)
                    
                    elif (node.children[5].name == "numero"):
                        aux_2 = ir.Constant(ir.IntType(32), int(node.children[5].children[0].name))

                    comp = function["builder"].icmp_signed("==", aux_1, aux_2, name='comp')
                    function["builder"].cbranch(comp, repita_fim, repita)

                    function["builder"].position_at_end(repita_fim)

                elif(node.name == "condicional"):
                    has_else = False

                    for n in node.children:
                        if (n.name == "senão"):
                            has_else = True

                    iftrue_1 = function["builder"].append_basic_block('iftrue_1')
                    iffalse_1 = function["builder"].append_basic_block('iffalse_1')
                    ifend_1 = function["builder"].append_basic_block('ifend_1')

                    aux_1 = None
                    if (node.children[1].name == "var"):
                        for var in self.local_vars + self.info["global_variables"]:
                            if (var.name == node.children[1].children[0].name):
                                aux_1 = function["builder"].load(var, 'aux_1', align=4)

                    
                    elif (node.children[1].name == "numero"):
                        aux_1 = ir.Constant(ir.IntType(32), int(node.children[1].children[0].name))

                    aux_2 = None
                    if (node.children[3].name == "var"):
                        for var in self.local_vars + self.info["global_variables"]:
                            if (var.name == node.children[3].children[0].name):
                                aux_2 = function["builder"].load(var, 'aux_1', align=4)
                    
                    elif (node.children[3].name == "numero"):
                        aux_2 = ir.Constant(ir.IntType(32), int(node.children[3].children[0].name))
                    
                    If_1 = function["builder"].icmp_signed(node.children[2].name, aux_1, aux_2, name='if_test_1')
                    function["builder"].cbranch(If_1, iftrue_1, iffalse_1)

                    then_body = node.children[5]

                    function["builder"].position_at_end(iftrue_1)
                    self.fill_function(then_body, function)
                    function["builder"].branch(ifend_1)

                    if(has_else):
                        else_body = node.children[7]
                        function["builder"].position_at_end(iffalse_1)
                        self.fill_function(else_body, function)
                        function["builder"].branch(ifend_1)
                    else:
                        function["builder"].position_at_end(iffalse_1)
                        function["builder"].branch(ifend_1)

                    function["builder"].position_at_end(ifend_1)

                elif(node.name == "leia" and len(node.children) > 0):
                    if(node.children[2].name == "var"):
                        for v in self.local_vars + self.info["global_variables"]:
                            if (v.name == node.children[2].children[0].name):
                                if(str(v.type) == "i32*"):
                                    ret = function["builder"].call(self.leiaInteiro, [])
                                    function["builder"].store(ret, v)

                                elif(str(v.type) == "float*"):
                                    ret = function["builder"].call(self.leiaFlutuante, [])
                                    function["builder"].store(ret, v)
                
                elif(node.name == "escreva" and len(node.children) > 0):
                    if(node.children[2].name == "var"):
                        for v in self.local_vars + self.info["global_variables"]:
                            if (v.name == node.children[2].children[0].name):
                                if(str(v.type) == "i32*"):
                                    var = function["builder"].load(v, name='write_var', align=4)
                                    function["builder"].call(self.escrevaInteiro, [var])
                                elif(str(v.type) == "float*"):
                                    var = function["builder"].load(v, name='write_var', align=4)
                                    function["builder"].call(self.escrevaFlutuante, [var])
                    elif(node.children[2].name == "numero"):
                        if(node.children[2].children[0].name.isdigit()):
                            var = ir.Constant(ir.IntType(32), int(node.children[2].children[0].name))
                            
                            function["builder"].call(self.escrevaInteiro, [var])

                        elif(not node.children[2].children[0].name.isdigit()):
                            var = ir.Constant(ir.FloatType(), float(node.children[2].children[0].name))
                            function["builder"].call(self.escrevaFlutuante, [var]) 

                elif(node.name == "retorna" and len(node.children) > 0):
                    r = 0
                    if(node.children[2].name == "numero"):
                        r = ir.Constant(ir.IntType(32), int(node.children[2].children[0].name))
                    
                    elif(node.children[2].name == "var"):
                        for var in self.local_vars+self.info["global_variables"]:
                            if(var.name == node.children[2].children[0].name):
                                r = function["builder"].load(var, name='ret_temp', align=4)
                    
                    elif(node.children[2].name in ["+", "-", "*", "/"]):
                        r = function["builder"].alloca(ir.IntType(32), name='ret_temp')
                        op = self.solve_expression(node.children[2], self.local_vars, function)
                        function["builder"].store(op, r)

                    function["builder"].ret(r)
            
            self.fill_function(node, function)


    def go_through_tree(self, tree, functions):
        for node in tree.children:

            for f in functions:
                if((f["function"].name == node.name or (f["function"].name == "main" and node.name == "principal")) and node.parent.name == "cabecalho"):
                    self.local_vars = []
                    self.fill_function(node.parent.children[-1], f)

            self.go_through_tree(node, functions)
        
    def code_generate(self, tree, symbol_table, sema_success):

        for symbol in symbol_table:
            if (symbol["symbol_type"] == "variable" and symbol["scope"] == "global"):
                var_type = symbol["value_type"]

                if(var_type == "inteiro"):
                    if(len(symbol["dimensions"]) == 0):
                        g = ir.GlobalVariable(self.module, ir.IntType(32), symbol["name"])

                    if(len(symbol["dimensions"]) == 1):
                        g_type = ir.ArrayType(ir.IntType(32), int(symbol["dimensions"][0]))
                        g = ir.GlobalVariable(self.module, g_type, symbol["name"])
                        self.info["global_variables"].append(g)
                
                elif(var_type == "flutuante"):

                    if(len(symbol["dimensions"]) == 0):
                        g = ir.GlobalVariable(self.module, ir.FloatType(), symbol["name"])

                    if(len(symbol["dimensions"]) == 1):
                        g_type = ir.ArrayType(ir.FloatType(), int(symbol["dimensions"][0]))
                        g = ir.GlobalVariable(self.module, g_type, symbol["name"])
                
                g.linkage = "common"
                g.align = 4
                self.info["global_variables"].append(g)

            elif (symbol["symbol_type"] == "function"):
                if(symbol["name"] == "principal"):
                    symbol["name"] = "main"
                
                arguments_list = []

                if (len(symbol["parameters"]) > 0):
                    for a in symbol["parameters"]:
                        if(a["par_type"] == "inteiro"):
                            arguments_list.append(ir.IntType(32))
                        else:
                            arguments_list.append(ir.FloatType())


                if(len(symbol["return"]) > 0):
                    if(symbol["return"][0]["ret_type"] == "inteiro"):
                        f_ret = ir.IntType(32)
                    else:
                        f_ret = ir.FloatType()
                
                    f_func = ir.FunctionType(f_ret, arguments_list)
                    f = ir.Function(self.module, f_func, name=symbol["name"])
                    entryBlock = f.append_basic_block('entry')
                    builder = ir.IRBuilder(entryBlock)
                    
                else:
                    f_func = ir.FunctionType(ir.VoidType(), arguments_list)
                    f = ir.Function(self.module, f_func, name=symbol["name"])
                    entryBlock = f.append_basic_block('entry')
                    builder = ir.IRBuilder(entryBlock)
                
                for i in range(len(f.args)):
                    f.args[i].name = symbol["parameters"][i]["par_name"]


                self.functions.append({"function": f, "builder": builder, "arguments": f.args})

        self.go_through_tree(tree, self.functions)

        file = open('module.ll', 'w')
        file.write(str(self.module))
        file.close()
        print(self.module)