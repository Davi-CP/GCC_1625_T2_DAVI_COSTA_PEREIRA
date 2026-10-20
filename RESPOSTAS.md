# Trabalho de Inferência Estatística

> Execute os scripts com os arquivos do professor em `data/`. Os números abaixo
> são preenchidos/atualizados pelos JSON gerados na execução.

## Q1 - Um estilo diferente ajuda?

### (i) Normalidade das diferenças
As observações são pareadas por jogador. A diferença é definida como pontuação com
taco original menos pontuação com taco experimental, ou seja, $d=Original−Experimental$. 
A normalidade dessas diferenças é avaliada pelo teste de Shapiro-Wilk a 5%. A hipótese nula é que as diferenças vêm de uma distribuição normal. 
Consulte `resultados/q1_resultados.json`
para a estatística e o valor-p. Se o valor-p for maior que 0,05, não há evidências suficientes para rejeitar a hipótese de normalidade das diferenças. Caso contrário, há evidência contra essa suposição. Caso a normalidade das diferenças não seja rejeitada, a utilização do teste t pareado é considerada apropriada.

Diagnóstico: [diferenças](resultados/q1_diferencas.png).

### (ii) Teste t pareado
1. Hipóteses: $H_0: mu_d <= 0$ e $H_1: mu_d > 0$, em que $mu_d$ é $d=Original−Experimental$ (original menos experimental). Essa alternativa corresponde
   à alegação de que o novo taco reduz a pontuação.
2. $\alpha = 0,01$ foi adotado e teste t pareado foi utilizado para a média das diferenças, pois a variância populacional é desconhecida e as medições são dos mesmos jogadores.
3. A estatística, graus de liberdade e valor-p estão em `resultados/q1_resultados.json`.
4. Se o valor-p for inferior, rejeita-se $H_0$ e conclui-se  que existem evidências estatísticas de que os tacos experimentais produzem pontuações médias menores.

## Q2 - Transmissões automática versus manual

### (i) Exploração gráfica
O boxplot compara mediana, dispersão e possíveis valores extremos; os histogramas
mostram a forma e a sobreposição das distribuições de MPG.

![Boxplot](resultados/q2_boxplot.png)

![Histogramas](resultados/q2_histogramas.png)

### (ii) Normalidade
Para cada grupo apliquei Shapiro-Wilk e D'Agostino-Pearson, ambos a 5%. As
estatísticas e os valores-p estão em `resultados/q2_resultados.json`. Para cada
teste, valor-p acima de 0,05 não fornece evidência para rejeitar normalidade.

### (iii) Intervalo de confiança
Calculei o intervalo de 95% para `media_automatica - media_manual` usando o
intervalo t de Welch, que não pressupõe variâncias populacionais iguais. O
intervalo está em `welch_ci95`.

### (iv) Teste unilateral (quatro passos)
1. `H0: mu_automatic >= mu_manual`; `H1: mu_automatic < mu_manual`.
2. Usei alpha = 0,05 e o teste t unilateral de Welch.
3. A estatística, graus de liberdade e valor-p estão no JSON.
4. Rejeito `H0` se o valor-p for menor que 0,05. Nesse caso, concluo que há
   evidência de maior MPG médio nos carros manuais; caso contrário, a suspeita
   não é sustentada pelos dados.

## Q3 - ANOVA: categorias de carros

### (i) Condições
Os testes de Shapiro-Wilk verificam a normalidade aproximada de cada grupo e o
teste de Levene verifica homogeneidade das variâncias, todos a 5%. Seus
resultados estão em `resultados/q3_resultados.json`. Os gráficos estão em
![grupos](resultados/q3_grupos.png).

### (ii) ANOVA
1. `H0: mu_compactos = mu_medios = mu_grandes`; `H1`: pelo menos uma média difere.
2. Usei alpha = 0,05 e ANOVA de um fator.
3. A estatística F e o valor-p estão no JSON.
4. Rejeito `H0` se valor-p < 0,05. A conclusão informa se as categorias têm
   evidência de médias diferentes.

## Q4 - ANOVA: custos de materiais

### (i) Procedimento
Li `data/data9.xls`, agrupei as três colunas numéricas de custos por disciplina e
calculei suas médias. A visualização comparativa está em
![custos](resultados/q4_custos.png).

### (ii) Teste em quatro passos
1. `H0`: as três médias são iguais; `H1`: pelo menos uma média difere.
2. Usei ANOVA de um fator com alpha = 0,01.
3. A estatística F e o valor-p estão em `resultados/q4_resultados.json`.
4. Rejeito `H0` se valor-p < 0,01; isso indicaria evidência de diferença entre
   custos médios de disciplinas.

## Q5 - Qui-quadrado de independência

### (i) Tabela observada
O script constrói a tabela cruzando `treatment` e `improvement`. Ela e a tabela
esperada ficam registradas no JSON, e a visualização está em
![contingência](resultados/q5_contingencia.png).

### (ii)-(vi) Procedimento e conclusão
As hipóteses são `H0`: tratamento e melhora são independentes e `H1`: são
dependentes. Apliquei o qui-quadrado de Pearson com alpha = 0,05, sem correção
de continuidade. A estatística, graus de liberdade, valor-p e decisão estão em
`resultados/q5_resultados.json`. Se valor-p < 0,05, rejeito a independência e
concluo que há associação entre medicamento e melhora; caso contrário, não há
evidência suficiente de associação. Também verifico a menor frequência esperada
no JSON; a aproximação é adequada quando as frequências esperadas não são muito
pequenas.
