# Carrega pacotes necessários
import pandas as pd
import numpy as np
import pickle
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder, MinMaxScaler
from sklearn.calibration import calibration_curve
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Funções 


# Função para contagem de observações em cada categoria

def conta_categorias(variavel, df):
    # variavel = string
    # df = pandas dataframe

    # contagem absoluta
    versao1 = pd.DataFrame(df[variavel].value_counts()).reset_index().sort_values(by=variavel)
    
    # contagem relativa
    versao2 = pd.DataFrame(df[variavel].value_counts()/df.shape[0]*100).reset_index().sort_values(by=variavel)
    
    return(versao1, versao2)


# Função para categorização de variáveis numéricas

def Categorizacao(dataframe, pontos_corte, variavel):
    # dataframe é um pandas dataframe
    # pontos_corte é a quantidade de categorias
    # variavel é o nome da coluna da variável numérica a ser categorizada -- string
    
    # nome_coluna = variavel + '_Cat'
    # dataframe[nome_coluna] = pd.qcut(dataframe[variavel], q = pontos_corte)
    categorias, bins = pd.qcut(dataframe[variavel], q = pontos_corte, retbins=True)

    return(categorias, bins)


# Função que retorna uma lista de variáveis correlacionadas

def Vars_Correl(dataframe, list_vars_num, limiar = 0.7, metodo = 'spearman'):
    # dataframe é um pandas dataframe
    # list_vars_num é uma lista das colunas do dataframe que são numéricas
    # limiar é o valor mínimo para o qual consideraremos a correlação. Valores superiores ao limiar serão considerados altamente correlacionados
    # metodo é o critério de correlação dos dados. Pode ser spearman ou pearson
    
    aux1 = dataframe[list_vars_num]
    matriz_correl = aux1.corr(method = metodo)
    
    linha = []
    coluna = []
    valor = []
    
    for i in matriz_correl.index:
        for j in matriz_correl.columns:
            if ((i != j) & (np.abs(matriz_correl[i][j]) >= limiar)):
                linha.append(i)
                coluna.append(j)
                valor.append(matriz_correl[i][j])
    
    Var1 = pd.DataFrame({'Var1': linha})
    Var2 = pd.DataFrame({'Var2': coluna})
    Valores = pd.DataFrame({'Valores': valor})
    Resultado_correl = pd.concat([Var1, Var2, Valores], axis = 1)
    Resultado_correl = Resultado_correl.drop_duplicates(subset=['Valores']).reset_index(drop = 'True')

    return(Resultado_correl)

# Função que retorna o IV em cada categoria e IV total da variável

def IV(dataframe, variavel, target):
    # dataframe é um pandas dataframe
    # variavel é o nome da variável para calcularmos o IV -- string (nesse caso a variável deve ser categórica)
    # target é o nome da variável target -- string
    
    # eventos de interesse / bads
    qtd_bads = dataframe[dataframe[target] == 1].shape[0]
    df_bads = pd.DataFrame(dataframe[variavel][dataframe[target] == 1].value_counts()/qtd_bads).reset_index().sort_values(by=variavel)
    df_bads.columns = [variavel, 'Perc_bads']
    # df_bads
    
    # eventos de não interesse / bons
    qtd_bons = dataframe[dataframe[target] == 0].shape[0]
    df_bons = pd.DataFrame(dataframe[variavel][dataframe[target] == 0].value_counts()/qtd_bons).reset_index().sort_values(by=variavel)
    df_bons.columns = [variavel, 'Perc_bons']
    # df_bons
    
    df_result = df_bads.merge(df_bons, on = variavel, how = 'left')
    df_result['Odds'] = df_result['Perc_bons']/df_result['Perc_bads']
    df_result['Woe'] = np.log(df_result['Odds'])
    df_result['IV_parcial'] = (df_result['Perc_bons']-df_result['Perc_bads'])*df_result['Woe']
    df_result['IV'] = sum(df_result['IV_parcial'])

    return(df_result)


# Função que retorna uma lista de IVs das variáveis

def IV_lista_variaveis(dados, var_target, lista_variaveis = ['object', 'category']):
    # lista_variaveis = ['object', 'category']
    # var_target = ['Attrition_Flag']
    
    # var_target é o nome da coluna da variável target -- string
    # dados é um pandas dataframe
    
    aux1 = dados.select_dtypes(include=lista_variaveis)
    aux2 = dados[var_target]
    
    aux = pd.concat([aux1, aux2], axis = 1)
    
    del [aux1, aux2]
    
    lista_for = aux.columns
    resp_IVS = []
    
    for i in range(0,len(lista_for)-1):
        # print(lista_for[i])
        # resp_IVS.append(IV(aux, lista_for[i], lista_for[4])['IV'][0])
        resp_IVS.append(IV(aux, lista_for[i], lista_for[len(lista_for)-1])['IV'][0])
    
    aux1 = pd.DataFrame({'Variaveis': lista_for})
    # aux1 = aux1.drop(index = 4)
    aux1 = aux1.drop(index = max(aux1.index))
    aux2 = pd.DataFrame({'IV': resp_IVS})
    
    output = pd.concat([aux1, aux2], axis = 1)
    
    del [aux1, aux2, lista_for, resp_IVS]
    
    output = output.sort_values(by = 'IV', ascending = False)

    return(output)


# Função que retorna os dados numéricos padronizados ou normalizados e o caminho onde o padronizador foi saldo em formato pickle

def Padronizacao(dataframe, lista_variaveis_numericas, tipo = 'padro', path = os.getcwd(), nome_sclr = 'scaler.pkl'):
    # dataframe é um pandas dataframe
    # lista_variaveis_numericas é uma lista de variáveis numéricas
    # tipo é uma string com o tipo de padronizador selecionado, pode ser a padronização ou narmalização dos dados
    # nome_sclr é o nome com o qual o padronizador será salvo

    if tipo == 'padro':
        SC = StandardScaler()
        SC.fit(dataframe[lista_variaveis_numericas])
        dados_new = pd.DataFrame(SC.transform(dataframe[lista_variaveis_numericas]), columns=dataframe[lista_variaveis_numericas].columns)

        # Salva o StandardScaler para aplicação em dados futuros
        # path = os.getcwd()

        path = path + '/' + nome_sclr
        print('O StandardScaler será salvo no caminho:', path)
        
        with open(path,'wb') as f:
            pickle.dump(SC, f)

    elif tipo == 'norm':
        MMS = MinMaxScaler()
        MMS.fit(dataframe[lista_variaveis_numericas])
        dados_new = pd.DataFrame(MMS.transform(dataframe[lista_variaveis_numericas]), columns=dataframe[lista_variaveis_numericas].columns)

        # Salva o StandardScaler para aplicação em dados futuros
        # path = os.getcwd()

        path = path + '/' + nome_sclr
        print('O MinMaxScaler será salvo no caminho:', path)
        
        with open(path,'wb') as f:
            pickle.dump(MMS, f)
        
    return([dados_new, path])


# Função que retorna os dados categóricos "dummificados" e o caminho onde foi salvo 

def Aplica_Encoder(dataframe, lista_categoricas, drop = None, tipo = 'default', path = os.getcwd(), nome_Enc = 'OHE.pkl'):
    # dataframe é um pandas dataframe 
    # lista_categoricas é uma lista de variáveis categóricas para aplicar o OHE
    # drop especifica se retiramos uma das categorias (opções estão listadas aqui: https://scikit-learn.org/1.5/modules/generated/sklearn.preprocessing.OneHotEncoder.html)
    # tipo define se será usado o OHE ou pela criação de dummies ou pela criação de variáveis inteiras  
    # path é o caminho onde será salvo o OneHotEncoder
    # nome_Enc é o nome dado para o Encoder utilizado
    
    if tipo == 'default':
        OHE = OneHotEncoder(handle_unknown = 'error', dtype = np.int32, drop=drop)
        OHE.fit(dataframe[lista_categoricas])
        dados_cat = pd.DataFrame(OHE.transform(dataframe[lista_categoricas]).toarray(), columns = OHE.get_feature_names_out())
        
        # Salva o OneHotEncoder para aplicação em dados futuros
        # path = os.getcwd()
        path = path + '/' + nome_Enc
        print('O OneHotEncoder será salvo no caminho:', path)
        
        with open(path,'wb') as f:
            pickle.dump(OHE, f)
        
    elif(tipo == 'ordinal'):
        OHE_ordinal = OrdinalEncoder(handle_unknown='error')
        OHE_ordinal.fit(dataframe[lista_categoricas])
        dados_cat = pd.DataFrame(OHE_ordinal.transform(dataframe[lista_categoricas]), columns=OHE_ordinal.get_feature_names_out())

        # Salva o OneHotEncoder para aplicação em dados futuros
        # path = os.getcwd()
        path = path + '/' + nome_Enc
        print('O OneHotEncoderOrdinal será salvo no caminho:', path)
        
        with open(path,'wb') as f:
            pickle.dump(OHE_ordinal, f)
    
    return([dados_cat, path])


# Função que faz o gráfico da importância das variáveis

def plot_feature_importance(importance, names, model_type):
    # importance é a variável dos valores de importância: MODELO.feature_importances_
    # names é a variável com os nomes para os respectivos valores de importância: MODELO.feature_names_in_
    # model_type é a variável string com o nome do modelo

    feature_importance = np.array(importance)
    feature_names = np.array(names)

    # Cria dicionário com nomes das variáveis e com os valores de importância
    data={'feature_names':feature_names,'feature_importance':feature_importance}
    fi_df = pd.DataFrame(data)

    # Ordena de forma decrescente a importância das variáveis
    fi_df.sort_values(by=['feature_importance'], ascending=False, inplace=True)

    # Define o tamanho da imagem
    plt.figure(figsize=(10,8))

    # Gráfico 
    sns.barplot(x=fi_df['feature_importance'], y=fi_df['feature_names'])
    
    # Rótulos
    plt.title(model_type + ' FEATURE IMPORTANCE')
    plt.xlabel('FEATURE IMPORTANCE')
    plt.ylabel('FEATURE NAMES')


# Função que faz o gráfico de calibração

def grafico_calibracao(y_verdadeiro, predicao, nbins = 10, strategy = 'quantile'):
    # y_verdadeiro é um array com os valores verdadeiros de y
    # predicao é um array com os valores estimados de probabilidade
    # nbins é a quantidade de quebras que vamos ter nos valores preditos, por default está como 10 decis
    # strategy é a quantidade de bins, que pode ser uniform ou quantile (https://scikit-learn.org/1.5/modules/generated/sklearn.calibration.calibration_curve.html)
    x, y = calibration_curve(y_verdadeiro, predicao, n_bins = nbins, strategy = strategy)
     
    # Gráfico do modelo idealmente calibrado
    plt.plot([0, 1], [0, 1], linestyle = '--', label = 'Idealmente Calibrado')
     
    # Gráfico da curva de calibração do modelo
    plt.plot(y, x, marker = '.', label = 'Modelo')
     
    leg = plt.legend(loc = 'upper left')
    plt.xlabel('Probabilidade predita média em cada bin')
    plt.ylabel('Proporção da variável target')
    plt.show()


# Função que faz o gráfico da variável numérica escolhida

def plot_histograma(variavel, df, label=None, bins=10):
    # variavel é uma string
    # df é um pandas dataframe
    # label é uma string com a informação de rótulo (variável target)
    # plotando um histograma básico

    if label == None:

        plt.hist(df[variavel], color='skyblue', edgecolor='black', label=label, bins=bins)
                    
        # Adicionando legenda e títulos
        plt.xlabel('Valores')
        plt.ylabel('Frequência')
        plt.title('Histograma')

        # Display do plot
        plt.show()

    elif label == 'fraud': 

        plt.hist(df[df['fraud'] == 0][variavel],  
                 alpha = 0.5,
                 label=['Not_fraud'],
                 bins=bins)
        
        plt.hist(df[df['fraud'] == 1][variavel],  
                 alpha = 0.5,
                 label=['Fraud'],
                 bins=bins) 
        
        # Adicionando legenda e títulos
        plt.xlabel('Valores')
        plt.ylabel('Frequência')
        plt.title('Histograma')
        plt.legend()

        # Display do plot
        plt.show()
    
    elif label != None or label != 'fraud':
        print("Nome de rótulo inválido")


# Função que calcula o PSI de cada variável

def PSI(dataframe_treino, dataframe_teste, variavel):
    # dataframe_treino é um pandas dataframe da base de treino
    # dataframe_teste é um pandas dataframe da base de teste
    # variavel é o nome da variável para calcularmos o PSI -- string (nesse caso a variável deve ser categórica)
    
    # quantidade de observações em treino
    qtd_treino = dataframe_treino.shape[0]
    treino = pd.DataFrame(dataframe_treino[variavel].value_counts()/qtd_treino).sort_values(by=variavel).reset_index()
    treino.columns = [variavel, 'count_treino']
    
    # quantidade de observações em teste
    qtd_teste = dataframe_teste.shape[0]
    teste = pd.DataFrame(dataframe_teste[variavel].value_counts()/qtd_teste).sort_values(by=variavel).reset_index()
    teste.columns = [variavel, 'count_teste']
    
    df_result = treino.merge(teste, on = variavel, how = 'left')
    df_result['Dif'] = df_result['count_treino'] - df_result['count_teste']
    df_result['Log'] = np.log(df_result['count_treino']/df_result['count_teste'])
    df_result['PSI_parcial'] = (df_result['Dif'])*df_result['Log']
    df_result['PSI'] = sum(df_result['PSI_parcial'])

    return(df_result)