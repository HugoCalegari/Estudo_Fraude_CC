# Estudo_Fraude_CC

Estudo de fraude de transação de cartão de crédito.

# Links para as bases

- https://www.kaggle.com/datasets/dhanushnarayananr/credit-card-fraud


# Contexto

O uso cada vez mais frequente de recursos digitais, como diferentes comércios eletrônicos, e a adesão de uso de cartão de crédito como forma de pagamento se tornaram ótimos aliados. O progresso da tecnologia tem permitido movimentações cada vez mais seguras e isto também faz com que cyber criminosos testem novas formas engenhosas de burlar a lei.

Será considerado fraude toda movimentação no cartão de crédito sem consentimento de um determinado indivíduo. É válido considerar também outros casos como: engenharia social, páginas de web que são espelhos das páginas verdadeiras e usadas para obter os dados financeiros dos indivíduos (houve consentimento em um contexto falso), perda de cartão de crédito em ambiente público e outras pessoas de má-fé se aproveitarem, entre outros.

De acordo com o site Stride (https://stripe.com/br/resources/more/credit-card-fraud-detection-and-prevention), é comentado sobre um relatório de 2021 da Nilson que destaca que as fraudes de cartão de crédito totalizaram 28,65 bilhões de dólares. No mesmo link, a LexisNexis relata que a cada 1 dólar em fraude, as empresas de varejo e e-commerce dos EUA incorrem em um custo de 3,75 dólares. 

No mundo real, a necessidade de diagnosticar fraude é imediata a transação. Dessa forma, será dada a prioridade em classificar as transações como fraudulentas ou não. É necessário balancear os erros: classificar como fraudulento quando não é (atrito com o cliente, dado que a transação foi barrada) x classificar como não fraudulento quando é (perda financeira para a instituição financeira).


# Etapas das análises

1.Base_de_dados: download e leitura da base de dados, usando a API do Kaggle.

2.Exploracao_variaveis: estudo univariado e bivariado das variáveis; identificação de potenciais transformações e criação de variáveis; correlação entre as variáveis e avaliação do potencial preditivo de algumas delas.

3.Pre_processamento: há muitas variáveis categóricas dicotômicas e algumas variáveis numéricas. A priori, foi aplicado somente a transformação logarítma nos dados numéricos.

4.Modelagem: fase de avaliação de modelos e estratégias de modelagem para os dados.