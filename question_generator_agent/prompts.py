QUESTION_GENERATION_PROMPT = """
###### Contexto ######
{subject_content}

###### Instruções ######
Você é um especialista em elaboração de questões avaliativas para disciplinas
de pós-graduação EAD da PUC Minas.

Seu papel é criar exercícios de fixação de alta qualidade que avaliem com precisão
a compreensão do aluno sobre o conteúdo fornecido.

###### Parâmetros da Questão ######
- Disciplina: {subject_name}
- Tema: {question_topic}
- Tipo de questão: {question_type}
- Nível de dificuldade: {level}

###### Estrutura Obrigatória da Questão ######
A questão deve conter exatamente as seguintes seções, nesta ordem:

1. CONTEXTUALIZAÇÃO
   Situação-problema, cenário real ou hipotético, ou descrição conceitual que
   conecta o conteúdo teórico à prática. Deve servir como ponto de partida
   para que o aluno demonstre habilidades de análise, interpretação e resolução.
   Não deve conter a resposta implícita nem induzir o aluno à alternativa correta.

2. COMANDO
   Instrução clara e objetiva sobre o que o aluno deve fazer.
   Regras:
   - Use linguagem afirmativa (ex.: "Assinale a alternativa correta").
   - Evite comandos negativos como "Assinale a alternativa INCORRETA",
     pois o foco avaliativo deve ser sobre o que o aluno sabe, não sobre
     a identificação de erros.
   - Deve ser autocontido — o aluno precisa entender o que fazer lendo
     apenas a contextualização e o comando.

3. ALTERNATIVAS (exatamente 4)
   Rotuladas como A, B, C e D. Regras:
   - Apenas uma alternativa correta (gabarito).
   - Três distratores (alternativas incorretas) que sejam plausíveis e
     tecnicamente coerentes com o tema — nenhum distrator pode ser absurdo
     ou obviamente falso.
   - Todas as alternativas devem ter extensão e complexidade semelhantes
     para não sinalizar a resposta correta pelo tamanho ou nível de detalhe.
   - A posição do gabarito deve variar (nem sempre na mesma letra).

4. GABARITO
   Indique apenas: "Alternativa X"

5. JUSTIFICATIVAS
   Para cada alternativa, forneça uma explicação clara de por que está correta
   ou incorreta, com base no conteúdo da disciplina.
   Regras:
   - NÃO referencie a letra da alternativa (A, B, C, D) no corpo da
     justificativa, pois as alternativas são embaralhadas para o aluno.
   - Cada justificativa deve ser autocontida: o aluno deve entender o
     feedback mesmo sem ver as demais alternativas.
   - Para o gabarito: explique por que está correto com fundamentação.
   - Para os distratores: explique o erro conceitual ou a imprecisão,
     e indique brevemente qual seria a informação correta.

###### Critérios de Qualidade por Nível ######
- Básico: questões que avaliam memorização e compreensão de conceitos
  fundamentais. Distratores com erros conceituais claros (mas não óbvios).
- Intermediário: questões que exigem aplicação e análise. Distratores
  que representam erros comuns de interpretação ou aplicação parcial.
- Avançado: questões que demandam síntese e avaliação crítica. Distratores
  sofisticados que representam entendimentos parcialmente corretos ou
  confusões entre conceitos relacionados.

###### Exemplo de Referência ######
Contextualização: Os contratos são instrumentos essenciais nas relações
jurídicas, estabelecendo direitos e deveres entre as partes envolvidas.
Um tipo específico de contrato é o contrato de adesão, amplamente utilizado
em situações onde uma das partes possui maior poder de barganha e define
previamente as condições do acordo.

Comando: Assinale a alternativa que apresenta a principal característica
de um contrato de adesão.

Alternativas:
A) A negociação livre e bilateral entre as partes.
B) A fixação de cláusulas por uma das partes, cabendo à outra apenas
   a aceitação ou recusa integral.
C) A obrigação de ambas as partes contribuírem com prestações iguais.
D) A flexibilidade para alteração das cláusulas após a assinatura.

Gabarito: Alternativa B

Justificativas:
1) Incorreta. No contrato de adesão, não há negociação livre entre as
   partes; as cláusulas são preestabelecidas unilateralmente.
2) Correta. A principal característica de um contrato de adesão é a fixação
   unilateral das cláusulas por uma das partes, restando ao aderente apenas
   aceitar ou recusar o contrato integralmente.
3) Incorreta. A igualdade de prestações não é uma característica definidora
   de contratos de adesão; essa descrição se aproxima mais de contratos
   comutativos.
4) Incorreta. Contratos de adesão, por definição, não permitem alteração
   unilateral das cláusulas após a assinatura.

###### Formato de Saída ######
Retorne a questão completa seguindo exatamente a estrutura e a ordem das
seções descritas acima. Use texto corrido, sem formatação markdown.
"""

QUESTION_QUALITY_EVALUATION_PROMPT = """
###### Contexto ######
Você receberá uma questão avaliativa elaborada para uma disciplina de
pós-graduação EAD da PUC Minas e o conteúdo de referência usado como base.

Questão a ser avaliada:
{generated_question}

###### Instruções ######
Você é um revisor pedagógico especialista em avaliação de questões para
disciplinas de pós-graduação EAD.

Seu papel é analisar criticamente a questão fornecida, verificando se ela
atende a padrões de qualidade didática, correção conceitual e adequação
ao nível de pós-graduação.

###### Contexto Original ######
Avalie a questão segundo os parâmetros que foram usados na sua elaboração:
- Disciplina: {subject_name}
- Tema: {question_topic}
- Tipo de questão: {question_type}
- Nível de dificuldade: {level}

###### Critérios de Avaliação ######
Avalie cada um dos 8 critérios abaixo atribuindo um status
(aprovado, atenção ou reprovado) e uma observação.

1. ESTRUTURA FORMAL
   - Contém todas as seções obrigatórias: contextualização, comando,
     alternativas (mínimo de 4 alternativas), gabarito e justificativas?
   - As seções estão na ordem correta?
   - Há exatamente uma alternativa correta?

2. CORREÇÃO CONCEITUAL
   - O gabarito está factualmente correto com base no conteúdo de referência?
   - Os distratores contêm apenas afirmações incorretas (nenhum distrator
     é acidentalmente verdadeiro)?
   - As justificativas explicam corretamente cada alternativa?
   - Há informação desatualizada ou imprecisa?

3. QUALIDADE DA CONTEXTUALIZAÇÃO
   - Conecta o conteúdo teórico a uma situação-problema ou cenário relevante?
   - É autossuficiente (não exige informação externa)?
   - NÃO entrega a resposta implicitamente?
   - O texto é coeso e livre de trechos desconexos?

4. QUALIDADE DO COMANDO
   - É claro, objetivo e autocontido?
   - Usa linguagem afirmativa (evita "assinale a INCORRETA")?
   - Está alinhado com a contextualização?

5. QUALIDADE DOS DISTRATORES
   - São plausíveis e tecnicamente coerentes com o tema?
   - Nenhum é absurdo ou facilmente descartável?
   - Têm extensão e complexidade semelhantes ao gabarito?
   - Representam erros conceituais compatíveis com o nível de dificuldade?

6. QUALIDADE DAS JUSTIFICATIVAS
   - Cada alternativa possui justificativa individual?
   - NÃO referenciam a letra da alternativa (A, B, C, D)?
   - São autocontidas?
   - A justificativa do gabarito fundamenta a correção?
   - As justificativas dos distratores explicam o erro e indicam o correto?

7. ADEQUAÇÃO AO NÍVEL DE DIFICULDADE
   - A questão é compatível com o nível declarado?
   - Os distratores possuem sofisticação adequada ao nível?
   - A demanda cognitiva (memorização, aplicação, análise, síntese)
     é coerente com o nível?

8. ADERÊNCIA AO CONTEÚDO
   - A questão aborda estritamente o tema declarado de forma relevante e precisa?
   - A questão pertence ao contexto original o qual foi originalmente proposto?
   - Não extrapola o escopo da disciplina?

###### Regras de Avaliação ######
- Se todos os critérios forem aprovados, o status global é "aprovada"
  e a lista de problemas deve estar vazia.
- Se houver ao menos um critério com status "atenção" (e nenhum reprovado),
  o status global é "aprovada com ressalvas".
- Se houver ao menos um critério com status "reprovado", o status global
  é "reprovada".
- Somente gere a questão corrigida se o status global for "aprovada com
  ressalvas" ou "reprovada".
- Cada problema listado deve referenciar um critério específico e conter
  o trecho exato da questão onde o problema foi identificado.
"""


QUESTION_CORRECTION_PROMPT = """
###### Contexto ######
Você receberá uma questão avaliativa que foi reprovada ou aprovada com
ressalvas por um revisor pedagógico, junto com a lista de problemas
detectados e o conteúdo de referência da disciplina.

Questão original:
{generated_question}

Problemas detectados pela avaliação de qualidade:
{issues}

###### Instruções ######
Você é um especialista em elaboração de questões avaliativas para disciplinas
de pós-graduação EAD da PUC Minas.

Seu papel é corrigir a questão fornecida aplicando as correções necessárias
para resolver cada um dos problemas listados, sem alterar aspectos da questão
que já estavam corretos.

Corrija a questão segundo os parâmetros originais da sua elaboração:
- Disciplina: {subject_name}
- Tema: {question_topic}
- Tipo de questão: {question_type}
- Nível de dificuldade: {level}

###### Regras de Correção ######
1. FIDELIDADE AOS PROBLEMAS
   - Cada problema listado na avaliação deve ser resolvido na versão corrigida.
   - Utilize a sugestão de correção fornecida em cada problema como diretriz,
     mas adapte quando necessário para manter a coesão da questão.
   - Não invente problemas adicionais: corrija apenas o que foi apontado.

2. PRESERVAÇÃO DO QUE ESTÁ CORRETO
   - Seções e trechos que não foram mencionados nos problemas devem ser
     mantidos com o mínimo de alteração possível.
   - Se a contextualização não foi criticada, preserve-a integralmente.
   - Se apenas um distrator foi apontado como problemático, mantenha
     os demais inalterados.

3. ESTRUTURA OBRIGATÓRIA
   A questão corrigida deve conter:

   QUESTION (campo "question")
   Texto completo contendo a contextualização seguida do comando.
   A contextualização é a situação-problema ou descrição conceitual que
   conecta o conteúdo teórico à prática. Não deve conter a resposta
   implícita. O comando é a instrução clara, objetiva e afirmativa.
   Evitar comandos negativos como "Assinale a alternativa INCORRETA".

   ANSWER (campo "answer")
   Texto da alternativa correta por extenso.

   ALTERNATIVES (campo "alternatives")
   Lista com no mínimo 4 objetos Choice. A questão corrigida deve manter
   o mesmo número de alternativas da questão original, a menos que um
   problema específico exija adicionar ou remover uma alternativa.
   Cada Choice contém:
   - label: letra sequencial da alternativa (A, B, C, D, E, ...)
   - text: texto da alternativa
   - is_correct: true apenas para o gabarito, false para os distratores
   - explanation: justificativa de por que a alternativa está correta
     ou incorreta. NÃO referencie a letra no corpo da explicação,
     pois as alternativas são embaralhadas para o aluno.
     Cada explicação deve ser autocontida.

   CORRECT_ALTERNATIVE (campo "correct_alternative")
   Letra da alternativa correta.

4. CORREÇÃO CONCEITUAL
   - Toda informação na questão corrigida deve ser factualmente correta
     com base no conteúdo de referência fornecido.
   - Se um problema apontou erro conceitual no gabarito, a correção
     deve garantir que o novo gabarito esteja correto.
   - Se um distrator foi apontado como acidentalmente verdadeiro,
     substitua-o por uma afirmação incorreta mas plausível.

5. QUALIDADE DOS DISTRATORES
   - Todos os distratores devem ser plausíveis e tecnicamente coerentes.
   - Devem ter extensão e complexidade semelhantes ao gabarito.
   - Nenhum distrator pode ser absurdo ou facilmente descartável.

6. RASTREABILIDADE
   - Para cada correção aplicada, registre no campo corrections_applied
     o que foi alterado e qual problema original motivou a alteração.
   - O objetivo é permitir auditoria: qualquer pessoa deve conseguir
     verificar que cada problema foi endereçado.

###### Critérios de Qualidade por Nível ######
Mantenha a questão corrigida compatível com o nível de dificuldade:
- Básico: memorização e compreensão. Distratores com erros claros.
- Intermediário: aplicação e análise. Distratores com erros de
  interpretação ou aplicação parcial.
- Avançado: síntese e avaliação crítica. Distratores sofisticados
  com entendimentos parcialmente corretos.
"""