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
mostram a forma e a sobreposição das distribuições de $mpg$.

![Boxplot](resultados/q2_boxplot.png)

![Histogramas](resultados/q2_histogramas.png)

O boxplot sugere que a mediana do $mpg$ dos veículos com transmissão manual é superior à observada nos veículos com transmissão automática. Além disso, os histogramas indicam uma maior concentração de carros manuais em faixas mais elevadas de $mpg$. Em conjunto, essas evidências visuais sugerem que os veículos com transmissão manual podem apresentar maior eficiência de combustível, hipótese que será avaliada formalmente pelos procedimentos inferenciais subsequentes.

### (ii) Normalidade
Para cada grupo foi aplicado Shapiro-Wilk e D'Agostino-Pearson, ambos a 5%. As
estatísticas e os valores-p estão em `resultados/q2_resultados.json`, os resultados servem para avaliar se a suposição de normalidade é razoável para os testes subsequentes. Para cada
teste, valor-p acima de 0,05 indica que não há evidências suficientes para rejeitar a hipótese de normalidade.

### (iii) Intervalo de confiança
Calculei o intervalo de 95% para `media_automatica - media_manual` usando o
intervalo t de Welch, que não pressupõe variâncias populacionais iguais. O
intervalo está em `welch_ci95`. Como o intervalo de confiança de 95% para $\mu_{automática}-\mu_{manual}​$ é inteiramente negativo, os dados fornecem evidências de que o MPG médio dos veículos com transmissão manual é superior ao dos veículos com transmissão automática. Além disso, o intervalo sugere que essa diferença média não é pequena, situando-se entre aproximadamente 3,2 e 11,3 MPG.

### (iv) Teste unilateral (quatro passos)
1. $H0: \mu_{automatic} >= \mu_{manual}$ - Representa que automáticos são mais eficientes em média de combustível; $H1: \mu_{automatic} < \mu_{manual}$ - Representa a suspeita de que carros manuais são mais eficientes em média de combustível .
2. Usei $\alpha = 0,05$ e o teste t unilateral de Welch.
3. A estatística, graus de liberdade e valor-p estão no JSON.
4. Rejeito $H0$ se o valor-p for menor que 0,05. Nesse caso, há
   evidências estatísticas para concluir que
    de maior MPG médio nos carros manuais; caso contrário, a suspeita
   não é sustentada pelos dados.

## Q3 - ANOVA: categorias de carros

### (i) Condições
Os testes de Shapiro-Wilk foram utilizados para verificar se a hipótese de normalidade é plausível para os valores de MPG em cada categoria de veículo. Além disso, apliquei o teste de Levene para avaliar a homogeneidade das variâncias entre os grupos. Essas verificações são importantes porque constituem as condições clássicas de aplicabilidade da ANOVA. Para todos os testes foi adotado nível de significância de 5%. Os resultados estão em `resultados/q3_resultados.json`. Os gráficos estão em
![grupos](resultados/q3_grupos.png).

### (ii) ANOVA
1. $H0: \mu_{compactos} = \mu_{medios} = \mu_{grandes}$; $H1$: pelo menos uma média difere.
2. Usei alpha = 0,05 e ANOVA de um fator.
3. A estatística F e o valor-p estão no JSON.
4. Se o valor-p for inferior a 0.05, rejeita-se $H_0$​ e conclue-se que existem evidências estatísticas de que nem todas as categorias de veículos possuem o mesmo MPG médio. Caso contrário, não há evidências suficientes para afirmar que as médias diferem.

## Q4 - ANOVA: custos de materiais

### (i) Procedimento
Li os dados de `data/data9.xls`, organizei os custos em três grupos correspondentes às disciplinas e calculei estatísticas descritivas, incluindo o tamanho das amostras e as médias de cada grupo. Também produzi um boxplot para comparar visualmente a distribuição dos custos entre as disciplinas, permitindo observar diferenças de tendência central, dispersão e possíveis valores extremos.. A visualização comparativa está em
![custos](resultados/q4_custos.png).

### (ii) Teste em quatro passos
1. Hipóteses
   - $H_0: os custos médios das três disciplinas são iguais$
   - $H_1: pelo menos uma das médias populacionais difere das demais$
2. Utilizei ANOVA de um fator com nível de significância $\alpha=0,01$, conforme solicitado no enunciado. Esse teste permite comparar simultaneamente as médias de três grupos independentes.
3. A estatística $F$ e o valor-p foram registrados em `resultados/q4_resultados.json`.
4. Rejeito $H_0$​ quando o valor-p é inferior a 0,01. Nesse caso, concluo que existem evidências estatísticas de que os custos médios não são iguais entre as três disciplinas. Caso contrário, não há evidências suficientes para afirmar que os custos médios diferem ao nível de significância adotado.

## Q5 - Qui-quadrado de independência

### (i) Tabela observada
O script constrói uma tabela de contingência cruzando as variáveis treatment e improvement, permitindo observar as frequências de pacientes em cada combinação de tratamento e resultado. 
Ela e a tabela esperada ficam registradas no JSON, e a visualização está em
![contingência](resultados/q5_contingencia.png).

### (ii)-(vi) Procedimento e conclusão
As hipóteses são $H0$: não existe associação entre receber o tratamento e apresentar melhora e $H1$: são
dependentes. Apliquei o qui-quadrado de Pearson com alpha = 0,05, sem correção
de continuidade. A estatística, graus de liberdade, valor-p e decisão estão em
`resultados/q5_resultados.json`. Se o valor-p for inferior a 0,05, rejeito a hipótese de independência e concluo que existem evidências estatísticas de associação entre o uso do medicamento e a melhora dos pacientes. Caso contrário, não há evidências suficientes para afirmar que essas variáveis são dependentes.
