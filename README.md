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


## Exploração inicial

Notebook para estudo univariado das variáveis explivativas e a relação destas com a variável resposta, com o uso da base de treino. Além disso, avalia-se a criação de novas features ou transformações das existentes.

As variáveis analisadas são:

- fraud (target): marcação de transações fraudulentas. Em média, 8.7% das transações são fraudulentas;

- repeat_retailer (explicativa): variável categórica dicotômica, para transações que ocorreram em lojas que já haviam sido visitadas anteriormente. Em média, 88% das transações ocorreram em lojas que já foram visitadas anteriormente;

- used_chip (explicativa): variável categórica dicotômica, para transações que ocorreram com o uso do chip do cartão de crédito. Em média, 35% das transações usaram o chip do cartão;

- used_pin_number (explicativa): variável categórica dicotômica, para transações que ocorreram com o uso do número do PIN. Em média, 10% das transações usaram o número PIN;

- online_order (explicativa): variável categórica dicotômica, para transações que ocorreram em pedidos online. Em média, 65% das transações foram online;

- distance_from_home, distance_from_last_transaction, ratio_to_median_purchase_price (explicativas numéricas): distância de casa, distância da última transação e a razão da transação pelo valor mediano de compra. Essas variáveis estão bastante concentradas em valores baixos. Como as variáveis são positivas, aplicou-se o logarítmo neperiano para reavaliar a distribuição. Com essa transformação, notou-se que essas variáveis ficaram mais próximas de uma distribuição gaussiana.

Não foi possível identificar relações entre as variáveis categóricas explicativas (foi usado tabelas de contingência) e identificou-se relações interessantes entre as transações online e fraude, uso de chip e fraude (também com o uso de tabelas de contingência). Nota-se diferenças consideráveis entre transações que são fraudulentas: que ocorreram online x não online e com uso de chip x sem uso de chip.

Identificou-se uma correlação mais forte entre repeat_retailer e log_distance_from_home (0.61) e entre a variável fraud e log_ratio_to_median_purchase_price (0.39).

Por fim, foi calculado o IV das variáveis, para identificar as variáveis com maiores potenciais preditivos para a target fraud. Destacam-se as seguintes variáveis: log_distance_from_home, used_pin_number e online_order, considerando o intervalo de iv entre 0.1 e 0.5 (poder preditivo de médio a forte).

Potenciais features novas:

- repeat_retailer * online_order = se a transação foi feita online E a transação ocorreu em lojas que já haviam sido visitadas anteriormente então será 1, caso contrário será zero;

- repeat_retailer * used_chip = se a transação foi feita online E a transação ocorreu com o uso do chip do cartão de crédito (provávelmente, em local física);

Observação importante: foi visto que transações acima do valor mediano das últimas transações tendem a ser mais fraudulentas do que as demais transações. Pode-se pensar que esta variável (ratio_to_median_purchase_price) defina se uma transação é fraudulenta ou não. Isso também pode implicar em um data leakage. O IV também direcionou um poder preditivo muito suspeito dessa variável (1.8).

## Pré-processamento dos dados

As variáveis categóricas já são dicotômicas, então as variáveis numéricas foram trabalhadas. Usou-se a variável numérica transformada pelo logarítmo e posteriormente aplicado a padronização nessa variável.

O pré-processamento foi aplicado em treino e depois replicado em validação.


## Modelagem

Etapa de construção de diferentes modelos, estudados tanto na base desbalanceada quanto na base balanceada.