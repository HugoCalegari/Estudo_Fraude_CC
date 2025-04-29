# Objetivo

Identificar as relações entre as variáveis explicativas e resposta, usando diferentes modelos. No mundo real, a detecção de fraude precisa ser feita rapidamente de modo que haja equilíbrio entre os falsos positivos e falsos negativos.

Avaliação de alguns testes:

1. Modelo aplicado na base completa (desbalanceado);

2. Modelo aplicado em folds balanceados (undersampling e oversampling) e validados em folds originais (desbalanceados).

OBS: será usado uma amostra para esse estudo.


# Descrição dos notebooks de modelagem

Modelos considerando a base completa e desbalanceada: 

- 1.Modelos_PT1: aplicação de modelos somente com as variáveis originais, aplicados os filtros de correlação e de IV;

- 2.Modelos_PT2: aplicação de modelos em variáveis criadas e originais, aplicados os filtros de correlação e de IV;