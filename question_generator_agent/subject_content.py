SLIDES_CONTENT = """
### Tema - 01 EAD - Fundamentos de GenAI
# Fundamentos de GenAI

## Introdução à GenAI

A Generative Artificial Intelligence (GenAI), ou Inteligência Artificial Generativa, refere-se a uma área da IA que tem como principal foco a criação de novos conteúdos. Esses conteúdos podem variar desde textos, imagens e músicas até simulações e arte digital. A principal característica da GenAI é sua capacidade de produzir resultados autênticos e criativos, que muitas vezes imitam a produção humana, oferecendo uma variedade de aplicações como geração de arte, escrita criativa, design gráfico e experimentações em ambientes virtuais.

## Modelos Discriminativos e Modelos Generativos

No campo da IA, é comum distinguir dois tipos principais de modelos: os discriminativos e os generativos, cada um com suas funções específicas. Os modelos discriminativos possuem como objetivo modelar diretamente as relações entre as variáveis de entrada, ou seja, eles aprendem a discernir ou classificar dados com base em classes ou rótulos predefinidos. Esses modelos são utilizados principalmente em tarefas de classificação ou regressão, não tendo a finalidade de aprender a distribuição completa do conjunto de dados. Exemplos de modelos discriminativos incluem regressão logística, Máquinas de Vetores de Suporte (SVM) e Redes Neurais Artificiais (RNA). Em termos mais técnicos, eles operam na forma de probabilidades condicionais p(y|x), onde y representa a classe e x as variáveis de entrada.

Por outro lado, os modelos generativos visam modelar a distribuição completa dos dados de entrada. Isso lhes permite gerar novas amostras que são semelhantes às originais, sendo capazes de criar textos, imagens ou preencher lacunas de dados ausentes. Além de gerar, esses modelos exploram a estrutura dos dados, capturando informações importantes sobre sua distribuição. Quando combinados com modelos discriminativos, podem melhorar significativamente o desempenho de tarefas específicas. Sua função principal é aprender a distribuição de probabilidade p(x|y), ou seja, a probabilidade dos dados de entrada dada uma determinada classe, ou de forma mais geral, a distribuição dos próprios dados, o que permite a geração de novidades desses conteúdos.

## Modelagem Generativa: Processo e Critérios de Avaliação

A modelagem generativa baseia-se em um processo sistemático que começa com a coleta de um conjunto de dados representativo, assumindo que esses dados foram gerados por alguma distribuição de probabilidade ainda desconhecida. O objetivo do modelo generativo é aprender essa distribuição, de modo que possa ser utilizado para gerar novas observações que aparentem ser provenientes da mesma fonte original. Para isso, o modelo tenta imitar a distribuição de probabilidades com precisão suficiente, produzindo exemplos que não apenas parecem originários da mesma distribuição, mas que também sejam suficientemente diversos para refletir a variedade existente nos dados originais. Isso garante que as gerações não sejam meramente cópias ou repetições, mas sim variações plausíveis.

A avaliação do desempenho de um modelo generativo considera dois aspectos principais: primeiramente, se ele consegue gerar exemplos que parecem verdadeiramente provenientes da distribuição de dados original (“parecem extraídos da distribuição”); e, em segundo lugar, se esses exemplos são suficientemente diversos, evitando a simples reprodução do que foi visto anteriormente. Assim, um bom modelo é aquele capaz de criar novas instâncias plausíveis e variadas, aumentando sua utilidade em aplicações reais.

## História e Evolução dos Modelos Iniciais de IA Generativa

Os modelos generativos têm uma história evolutiva marcada por diferentes abordagens e avanços tecnológicos. Antes do advento dos grandes modelos de linguagem (LLMs) e das modernas técnicas de difusão, diversas arquiteturas precedentes deram o suporte para o desenvolvimento da GenAI. Entre esses destacam-se os autoencoders, Variational Autoencoders (VAEs) e as Redes Adversariais Generativas (GANs).

Os autoencoders, desenvolvidos na década de 1980, são redes neurais capazes de aprender representações eficientes dos dados de entrada, chamadas de codificações. Essas representam os dados em uma forma comprimida, geralmente de menor dimensão, facilitando tarefas como redução de dimensionalidade, geração de novos dados e remoção de ruídos. A sua estrutura básica consiste na combinação de duas partes: um codificador que comprime os dados, e um decodificador que reconstrói a entrada a partir dessa representação.

Os Variational Autoencoders, introduzidos em 2013, representam uma evolução dos autoencoders tradicionais. Em vez de aprender uma única codificação, eles modelam a distribuição latente dos dados usando uma distribuição probabilística, frequentemente uma Gaussiana multivariada. Essa abordagem possibilita gerar novas amostras ao amostrar o espaço latente de forma controlada, permitindo criar dados realistas e diversos. A técnica envolve um procedimento de reparametrização que facilita o treinamento e aprimora a capacidade de gerar novidades.

Ainda em 2014, surgiram as Redes Adversariais Generativas (GANs), que representam um avanço importante no campo da modelagem generativa. Essas redes consistem na interação de duas redes neurais distintas: uma geradora, que recebe ruído aleatório e tenta criar amostras falsas próximas às reais, e uma discriminadora, que tenta distinguir entre amostras reais e falsas. O objetivo do treinamento é fazer com que a geradora produza amostras tão convincentes que enganem a discriminadora, que também aprende a identificar de forma cada vez mais precisa as diferenças. Assim, ambas as redes evoluem em um jogo de suma zero, resultando em modelos capazes de criar conteúdos visualmente realistas, como imagens de alta qualidade.

## Técnicas Modernas e o Futuro da GenAI

Atualmente, a evolução contínua de modelos como autoencoders, VAEs e GANs contribui para o avanço da GenAI, culminando na criação de grandes modelos de linguagem (LLMs) e nos modelos de difusão. Estes últimos utilizam técnicas de reversão de ruído e operações em espaço latente para gerar imagens e outros conteúdos com alta fidelidade. Essas inovações visam ampliar ainda mais o potencial criativo da IA, possibilitando aplicações cada vez mais sofisticadas na produção de arte, texto, som e outros tipos de mídia, além de contribuir para áreas como educação, saúde, entretenimento e negócios.

## Referências

FOSTER, David. *Generative Deep Learning: Teaching Machines to Paint, Write, Compose, and Play*. O'Reilly Media, 2019.

HANY, John; WALTERS, Greg. *Hands-On Generative Adversarial Networks with PyTorch*. Birmingham: Packt Publishing, 2020.
####################################################################################################################################################################################

### Tema - 02 EAD - Principais Arquiteturas - Transformer
# Arquiteturas e Modelos Generativos de Transformadores em NLP

## Introdução aos Modelos Generativos Pré-Treinados

Os modelos de linguagem pré-treinados baseados em arquiteturas de Transformer têm revolucionado o campo de processamento de linguagem natural (PLN) e Deep Learning desde sua proposta seminal, apresentada no artigo "Attention is All You Need" por Vaswani et al. (2017). Esses modelos são treinados em grandes corpora de texto, muitas vezes provenientes da internet, com o objetivo de aprender padrões da linguagem, regras gramaticais, fatos do mundo e, em alguma medida, raciocínio comum. A fase inicial de treinamento, conhecida como pré-treino, permite que esses modelos captem conhecimentos gerais de forma autônoma antes de serem ajustados para tarefas específicas, por meio de um processo chamado fine-tuning.

A arquitetura do Transformer, que substitui modelos sequenciais tradicionais como RNNs e LSTMs, é a base desses modelos. Os Transformers destacam-se por sua eficiência em lidar com contextos extensos, utilizando mecanismos de atenção para focar em partes relevantes do texto ao gerar saídas, além de possibilitar alta paralelização durante o treinamento.

## O Funcionamento e Estrutura do Transformer

### Elementos Fundamentais

No núcleo do Transformer estão os embeddings, que representam cada token (palavras ou subpalavras) em vetores numéricos, acompanhados do positional encoding, que informa a ordem dos tokens na sequência. O mecanismo de atenção, especialmente o self-attention, permite que cada token interaja com todos os outros de uma forma dinâmica, capturando relações contextuais mesmo quando os tokens estão distantes dentro do texto. A seguir, destacam-se duas variações principais de atenção: o scaled dot-product attention, que realiza cálculos usando consultas (queries), chaves (keys) e valores (values), e o multi-head attention, que emprega múltiplas cabeças para que diferentes relações possam ser capturadas simultaneamente.

A arquitetura também inclui camadas feed-forward, que aplicam redes totalmente conectadas a cada posição individualmente, enriquecendo assim as representações geradas. Para garantir uma maior estabilidade e eficiência no treinamento, utilizam-se técnicas de normalização e regularização, tais como conexões residuais, layer normalization e dropout.

### Arquitetura Encoder–Decoder

O Transformer pode ser implementado como um modelo encoder–decoder, onde o encoder processa toda a entrada de uma vez, gerando uma representação contextual, enquanto o decoder produz a saída token a token, utilizando atenção mascarada para evitar que futuros tokens influenciem a previsão presente. Essa estrutura é ideal para tarefas de tradução automática, resumo de textos, perguntas e respostas, e qualquer tarefa que envolva transformação de sequência em sequência.

### Arquitetura Encoder Only

Outra configuração comum é a do encoder único, que compõe modelos como BERT, RoBERTa, DistilBERT, e ModernBERT. Esses modelos são treinados para compreender o texto, produzindo embeddings mais ricos e contextuais, utilizados em tarefas discriminativas de entendimento, como classificação de sentimento, reconhecimento de entidades nomeadas, análise semântica, busca semântica e tarefas de recuperação de informação. A principal vantagem reside na sua eficiência para interpretar texto, sem foco na geração de novas frases.

### Arquitetura Decoder Only

A arquitetura decoder only é caracterizada pelo uso exclusivo de decoders em seus modelos. Esses modelos, exemplificados pela família GPT, operam de modo autoregressivo, prevendo o próximo token dado o contexto anterior, concebendo-se assim como soluções ideais para tarefas de geração de linguagem natural. Utilizam atenção causal (ou mascarada) para garantir que a previsão de um token só seja influenciada pelo passado, não pelo futuro. São utilizados em chatbots, assistentes virtuais, geração de textos, resumo e tradução automática, sendo a arquitetura preferencial para modelos de linguagem de grande escala, os Large Language Models (LLMs).

## Modelos Generativos Pré-Treinados e LLMs

Os modelos de linguagem de grande escala, ou Large Language Models (LLMs), representam uma evolução quantitativa e qualitativa na área. Estes modelos empregam principalmente a arquitetura decoder-only, com bilhões de parâmetros treinados em corpora massivos e diversos. A escala desses modelos é o que possibilita o aparecimento de comportamentos emergentes, como maior coerência, criatividade e capacidade de raciocínio, além de ampliar a gama de tarefas que podem ser realizadas com alta performance.

Ao aprenderem uma distribuição probabilística sobre sequências de tokens, esses modelos conseguem prever a próxima palavra ou sequência de palavras com base no histórico, o que os torna extremamente versáteis para uma vasta gama de aplicações. Exemplos de LLMs incluem GPT-4, Llama 3, Gemini, Claude e Mistral.

Apesar de o tamanho ser uma característica marcante, o diferencial dos LLMs reside na sua escala, capaz de alterar qualitativamente suas habilidades. Ou seja, ao aumentar significativamente a quantidade de dados de treinamento e o número de parâmetros, os modelos passam a realizar tarefas complexas de forma mais eficiente, mostrando comportamentos que os modelos tradicionais, menores, não apresentavam.

## Considerações Finais

A evolução das arquiteturas de Transformer, aliada ao desenvolvimento dos modelos pré-treinados e dos grandes modelos de linguagem, tem impulsionado avanços notáveis na pesquisa e na aplicação prática de PLN. Desde modelos especializados em compreensão de texto até sistemas de geração de conteúdo, esses avanços oferecem novas possibilidades e desafios, exigindo uma compreensão aprofundada de seus mecanismos internos e limitações.

## Referências

VASWANI, Ashish et al. Attention is all you need. In: *Advances in Neural Information Processing Systems*, 2017, p. 5998-6008.

Raschka, S. The big LLM architecture comparison: From DeepSeek-V3 to Kimi K2: A look at modern LLM architecture design. Ahead of AI, 2025. Disponível em: <link>.

Stollnitz, B. How GPT models work: Accessible to everyone. 2023. Disponível em: <link>.
####################################################################################################################################################################################

### Tema - 03 EAD - Principais Plataformas
# Plataformas de Inteligência Artificial Geral (GenAI) no Mercado

## Introdução às Principais Plataformas de GenAI

Nos últimos anos, o mercado de Inteligência Artificial Geral (GenAI) tem se consolidado por meio do desenvolvimento de plataformas que oferecem modelos cada vez mais avançados, multimodais e acessíveis. Essas plataformas representam o estado-da-arte na utilização de grandes modelos de linguagem (LLMs) e outras tecnologias que integram processamento de texto, imagem, vídeo e áudio em sistemas capazes de realizar tarefas complexas de forma autônoma e eficiente. A seguir, serão apresentadas as principais plataformas de GenAI atualmente disponíveis no mercado, destacando suas características, investimentos, aplicações e diferenciais.

## OpenAI — ChatGPT

Fundada em 2015 na cidade de São Francisco, nos Estados Unidos, a OpenAI é uma das pioneiras no desenvolvimento de modelos de inteligência artificial voltados para aplicações comerciais e acadêmicas. Sua plataforma mais conhecida é o ChatGPT, baseada em uma série de modelos que evoluíram ao longo do tempo, como GPT-3, GPT-4 e versões superiores, incluindo o GPT-4o — que foi o primeiro modelo multimodal da empresa. A OpenAI destaca-se pelo seu avançado raciocínio, capacidade de processamento de múltiplos tipos de dados simultaneamente, além de uma API amplamente adotada pelo mercado global.

Entre seus produtos, destacam-se o ChatGPT Plus, destinado a usuários individuais; o ChatGPT Teams para equipes corporativas e o ChatGPT Enterprise, voltado para grandes empresas. A parceria estratégica com a Microsoft também é relevante, tendo recebido um investimento de aproximadamente US$ 13 bilhões, o que possibilitou ampliações em infraestrutura e integração com produtos Microsoft, como o Azure. Em 2026, estima-se que a OpenAI atingirá uma avaliação de mercado de cerca de US$ 730 bilhões, refletindo a forte adesão do mercado aos seus modelos avançados. Atualmente, a OpenAI conta com mais de 200 milhões de usuários ativos, demonstrando sua liderança na área.

Um destaque importante é o GPT-5.3-Codex, um modelo que foi fundamental na construção de novas versões do GPT. Além disso, o GPT-4o foi o primeiro modelo capaz de processar dados multimodais, permitindo aplicações que envolvem diferentes tipos de mídia de forma integrada.

## Google — Gemini

O Google, por meio de sua divisão DeepMind, desenvolveu a plataforma Gemini, que vem ganhando destaque como uma das principais alternativas de modelos de linguagem. A versão mais recente, Gemini 2.0, incorpora avanços significativos, como a capacidade de lidar com um contexto de até 1 milhão de tokens — o que equivale a um volume de informações bastante elevado para tarefas de análise de textos longos. Um diferencial do Gemini é sua integração nativa com o ecossistema Google, incluindo Google Workspace, Search e Google Cloud, facilitando a aplicação em ambientes corporativos e de pesquisa.

A plataforma oferece versões gratuitas e de acesso aberto, incluindo o Gemini básico, além de disponibilizar código em ambientes como Google Colab e BigQuery, o que promove maior acessibilidade e experimentação por parte de desenvolvedores e pesquisadores. Com suporte multimodal, o Gemini permite o processamento de diversos tipos de mídia e dados de forma integrada, potencializando soluções em diversas áreas.

## Anthropic — Claude

Fundada por ex-pesquisadores da OpenAI, a Anthropic se diferencia por um foco intenso em segurança, alinhamento ético e confiabilidade de suas soluções de IA. Seu principal produto é a série Claude, incluindo modelos como Claude Opus 4.6, Sonnet 4.6 e Haiku 4.5. Destaca-se pelo uso de uma abordagem denominada "Constitutional AI", na qual a IA é guiada por princípios e regras claras para evitar respostas inadequadas ou sesgadas. Isso reforça seu foco em aplicações críticas, como empresas, educação e pesquisa de alta complexidade.

O modelo Claude oferece um contexto de até 200 mil tokens, permitindo análises detalhadas de grandes volumes de documentos. Desde sua fundação, em 2021, a Anthropic busca oferecer uma tecnologia de IA que seja não apenas poderosa, mas também segura e confiável, atendendo às demandas de ambientes corporativos sensíveis. A plataforma disponibiliza APIs e SDKs acessíveis via claude.ai e claude.ai, consolidando sua proposta de valor baseada em princípios éticos e de segurança.

## Meta — LLaMA (Open Source)

A Meta, antiga Facebook e Instagram, lançou a série LLaMA (Large Language Model Meta AI), que representa uma opção de código aberto para o desenvolvimento de modelos de linguagem. Models como LLaMA 3.3, 3.2 e Llama 4 Scout/Maverick oferecem uma alternativa para organizações que desejam implantar soluções de IA sem dependência de APIs comerciais com custos elevados.

A característica principal do LLaMA é sua licença open source, permitindo uso comercial, além de compatibilidade com deploys locais, na nuvem própria ou em provedores de terceiros. Essa liberdade de implementação é especialmente útil para organizações preocupadas com privacidade de dados e custo de operação. Com mais de 70 bilhões de parâmetros na sua maior versão, o LLaMA se destaca pelo seu potencial de execução offline, privacidade total e baixa barreira de entrada para desenvolvedores, já que seu uso é gratuito e acessível.

## Outras Plataformas Relevantes

Além das principais enlistadas, outras plataformas também têm se destacado no cenário de GenAI, especialmente por suas aplicações específicas ou por oferecerem modelos abertos. Entre estas, podemos citar:

- **Mistral AI**, que desenvolve modelos europeus de alta eficiência, como Mixtral e Mistral Large.
- **Perplexity AI**, focada em responder perguntas em tempo real com fontes citadas, aprimorando a confiabilidade das respostas.
- **xAI**, a plataforma de Elon Musk, integrada ao Twitter (agora X), oferecendo acessos em tempo real a informações e dados atuais.
- **Stability AI**, conhecida pela geração de imagens por meio do Stable Diffusion, seu framework open source.
- **Hugging Face**, um dos maiores hubs de modelos open source do mundo, com uma vasta comunidade de desenvolvedores e pesquisadores.
- **DeepSeek**, uma plataforma chinesa voltada a LLMs de código aberto.

## Tendências no Mercado de GenAI

O mercado de GenAI apresenta diversas tendências que indicam o futuro da tecnologia. Entre elas, destacam-se:

1. **Modelos Multimodais**: a integração de diferentes tipos de mídia — texto, imagem, vídeo e áudio — em um único sistema, ampliando a aplicabilidade das IA.
   
2. **Agentes Autônomos**: inteligência artificial capazes de planejar, executar tarefas complexas e utilizar ferramentas externas de forma autônoma, avançando na automação de processos.

3. **Edge AI**: o desenvolvimento de modelos que operam em dispositivos locais, sem depender de conexão com a nuvem, o que reforça a privacidade e a eficiência em ambientes com conectividade limitada.

4. **IA Corporativa**: a adoção crescente para automação de processos empresariais e melhoria de eficiência em diferentes setores.

5. **Regulamentação**: a implantação de normas globais que regem o uso responsável de IA, refletindo preocupações éticas e de segurança.

6. **Custo Decrescente**: a redução no custo de modelos de IA, promovendo maior acessibilidade para pequenas e médias empresas, democratizando o uso dessas tecnologias.

## Conclusão

O cenário de Plataformas de GenAI tem se consolidado com o surgimento de soluções diversas, desde modelos open source acessíveis a qualquer desenvolvedor até plataformas proprietárias altamente avançadas. A tendência aponta para uma maior integração multimodal, autonomia e democratização do acesso, acompanhada por uma crescente atenção às questões de segurança e regulação. Assim, espera-se que a evolução dessas plataformas continue a impulsionar a inovação em múltiplos setores, transformando a forma como humanos interagem com a inteligência artificial.

## Referências

- OpenAI. (2023). *OpenAI — ChatGPT*. Disponível em: https://openai.com  
- Google. (2023). *Gemini*. Disponível em: https://gemini.google.com  
- Anthropic. (2023). *Claude*. Disponível em: https://anthropic.com / claude.ai  
- Meta. (2023). *LLaMA*. Disponível em: https://llama.meta.com / huggingface.co  
- Outros materiais extraídos do conteúdo fornecido, com referências internas às fontes mencionadas ao longo do texto.
####################################################################################################################################################################################

### Tema - 02 EAD - Principais Arquiteturas - Modelos de Difusão
# Modelos Generativos Baseados em Ruído Progressivo e Difusão

## Introdução às Arquiteturas de Geração de Imagens
Nas últimas décadas, as soluções de inteligência artificial voltadas à geração de imagens passaram por uma evolução significativa. Entre as principais arquiteturas modernas, destacam-se os modelos generativos baseados em processos de ruído progressivo, que desempenham um papel central na atual geração de algoritmos de geração de imagens, especialmente na vasta área da GenAI (Inteligência Artificial Generativa). Esses modelos são considerados uma alternativa superior aos tradicionais Generative Adversarial Networks (GANs) em termos de diversidade de produções e controle sobre os resultados finais.

O funcionamento desses modelos se apoia no conceito de adicionar ruído de forma progressiva às imagens reais, até que elas se tornem completamente distorcidas por ruído puro. Posteriormente, o processo reverso consiste em ensinar uma rede neural a remover esse ruído passo a passo, reconstruindo a imagem original de forma sequencial. Assim, a ideia central é que a geração de uma nova imagem seja o efeito de um processo de "desruídificação" controlada, iniciando de um estado de ruído completo e gradualmente retornando uma imagem coerente.

## Modelos de Difusão: Definição e Processo
Os modelos de difusão representam uma classe de modelos probabilísticos que utilizam uma abordagem de adição e remoção de ruído para a geração de novos dados. Nesse método, uma imagem real de entrada passa por várias etapas de introdução de ruído gaussiano, até que seja completamente transformada em uma matriz de ruído puro após dezenas de passos. Este procedimento de degradação é conhecido como o processo de difusão.

O grande diferencial desses modelos está no processo reverso: a rede neural aprende a prever o ruído presente em cada um desses passos intermediários. Com essa capacidade, ela consegue reverter o processo de difusão passo a passo, reconstruindo a imagem original a partir do ruído. Dessa forma, ao gerar novas imagens, o modelo fornece um processo sequencial controlado que transforma ruído em uma imagem coerente. Essa técnica permite criar imagens de alta fidelidade visual, com maior estabilidade de treinamento e maior controle na geração dos resultados.

A arquitetura padrão utilizada nesses modelos é a U-Net, uma rede convolucional que foi originalmente desenvolvida para segmentação de imagens biomédicas. Ela é adaptada para o contexto de difusão, incorporando mecanismos de atenção e embeddings de tempo, essenciais para que o modelo entenda em que estágio do processo de difusão se encontra. Essas integrações contribuem para a produção de imagens de alta qualidade e coherence.

## Vantagens e Limitações dos Modelos de Difusão
Entre as vantagens dos modelos de difusão destacam-se a alta fidelidade visual das imagens geradas e a possibilidade de um treinamento mais consistente. Além disso, esses modelos oferecem um controle considerável sobre o processo de geração, permitindo ajustar aspectos específicos das imagens finais. Outra benefício importante é a estabilidade no treinamento, que geralmente é mais difícil de alcançar em modelos baseados em GANs.

No entanto, esses modelos também apresentam algumas limitações. Normalmente, a amostragem de imagens via difusão é lenta, uma vez que envolve múltiplos passos de processamento sequencial. Além disso, o treinamento demanda grande capacidade computacional, sendo bastante custoso em termos de recursos. Essas dificuldades justificam a busca constante por melhorias e evoluções na arquitetura de difusão.

## Evoluções Recentes na Geração de Imagens com Difusão
Para superar as limitações tradicionais, diversas inovações têm sido propostas. Uma delas é o Denoising Diffusion Implicit Models (DDIM), que consegue reduzir consideravelmente o número de passos necessários para a geração de uma imagem, tornando o processo de inferência mais rápido. Outra evolução importante é o ControlNet, uma arquitetura que permite um condicionamento avançado do processo de geração, controlando de maneira precisa e estruturada os aspectos finais das imagens produzidas.

Atualmente, essas tecnologias também estão sendo adaptadas para aplicações voltadas ao vídeo, ampliando o espectro de possibilidades de geração multimídia com maior flexibilidade e maior controle sobre o resultado final. Essas evoluções representam o esforço contínuo de tornar os modelos de difusão uma ferramenta mais eficiente e aplicável a diferentes contextos.

## Referências
HO, J.; JAIN, A.; ABBEEL, P. Denoising Diffusion Probabilistic Models. 2020. Disponível em: arXiv preprint arXiv:2006.11239.

RONNEBERGER, O.; FISCHER, P.; THOMAS, T. U-Net: Convolutional Networks for Biomedical Image Segmentation. arXiv:1505.04597 [cs.CV], 2015.

VADAT, A.; KREIS, K. Improving Diffusion Models as an Alternative to GANs, Part 2. NVIDIA Technical Blog, 26 abr. 2022.

[VERIFICAR: fontes específicas para as referências do conteúdo completo, incluindo links se disponíveis.]
####################################################################################################################################################################################
"""