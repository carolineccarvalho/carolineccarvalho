def escrever_coordenada(lista_por_tamanho, ferramenta, drill_file):
    for numero_do_item, item in enumerate(lista_por_tamanho):
        if numero_do_item == 0:
            dado = f"{item}{ferramenta}\n"
        else:
            dado = f"{item}\n"
        drill_file.write(dado)



with open("nails.asc","r") as nails_files:
     lista_nails = nails_files.readlines()
     

nails_dict = {"BOT": {"mils_100": [], "mils_75" : [], "mils_50" : [], "mils_39": []},
            "TOP": {"mils_100": [], "mils_75" : [], "mils_50" : [], "mils_39": []}}


cabecalho = """M48
INCH,DZ
T01C0.067
T02C0.055
T03C0.035
T04C0.028
T05C0.000
M95\n"""


for linha in lista_nails:
    linha_valida = False
    if "(B)" in linha:
        linha_quebrada = linha.split() 
        tamanho_da_agulha = linha_quebrada[3]
        linha_valida = True
        lado = 'BOT'

    elif "(T)" in linha:
        linha_quebrada = linha.split() 
        tamanho_da_agulha = linha_quebrada[3]
        linha_valida = True
        lado = 'TOP'


    if linha_valida == True:
        if tamanho_da_agulha == '1':
            nails_dict[lado]["mils_100"].append("x{}y{}".format(linha_quebrada[1],linha_quebrada[2]))

        elif tamanho_da_agulha == '2':
            nails_dict[lado]["mils_75"].append("x{}y{}".format(linha_quebrada[1],linha_quebrada[2]))

        elif tamanho_da_agulha == '3':
            nails_dict[lado]["mils_50"].append("x{}y{}".format(linha_quebrada[1],linha_quebrada[2]))  

        elif tamanho_da_agulha == '4':
            nails_dict[lado]["mils_39"].append("x{}y{}".format(linha_quebrada[1],linha_quebrada[2]))



with open(f"drill_top.ex","w") as drill_top:
    with open(f"drill_bottom.ex","w") as drill_bot:
        drill_bot.write(cabecalho)
        drill_top.write(cabecalho)

        for b_t in nails_dict:
            dict_por_tamanho = nails_dict[b_t]
            if b_t == 'BOT':
                drill_file = drill_bot
            elif b_t == 'TOP':
                drill_file = drill_top

            
            for ferr_numero, chave_da_lista in enumerate(dict_por_tamanho, start=1):
                ferramenta = f"T0{ferr_numero}"
                lista_por_tamanho = dict_por_tamanho[chave_da_lista]
                escrever_coordenada(lista_por_tamanho, ferramenta, drill_file)


            drill_top.write("""T00\nM00""")
            drill_bot.write("""T00\nM00""")
