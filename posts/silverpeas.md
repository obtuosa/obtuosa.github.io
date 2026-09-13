![CVE](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/f6qso2v1y0pcjn7pzvk8.png)

A princípio esse texto é um embrionário da minha apresentação realizada na reunião 0x04 do [Axé Sec](https://axesec.cc/events/2025-03-23-meeting/), uma comunidade de cibersegurança com uma baita iniciativa foda na Bahia e que nasceu a partir do [Raul Hacker Club](https://raulhc.cc/). Inclusive, vale muito a pena dar uma olhada nesse propósito para incentivar a cultura hacking! (Depois diga que não avisei hein). 

Além disso, também foi realizada uma apresentação dessa proposta alinhada ao OWASP Top 10 na [Donas Security](https://www.instagram.com/donasecurity/), um coletivo muitíssimo importante que traz um ambiente seguro de construção e contribuições muito significativas para as mulheres baianas de Salvador com foco não só em Cibersegurança (apesar de ser o princípio), mas com ideias e insights para levar para vida! Um grande abraço para Rebeca ;), Mayara, Gab, Gio, Marcela e a todas as meninas que fazem parte desse processo tão lindo que é a Donas Security s2!

A propósito essa apresentação nasceu de um CTF realizado em conjunto com o Well (um abraço meu véio!) e que foi levado para a reunião como forma de debate entre os membros do Axé Sec e também da Donas Security, que inclusive teve uma contribuição muito massa do Gildásio que será pontuada no decorrer da análise da vulnerabilidade.

## Introdução
Para falar sobre a vulnerabilidade em sí, se faz importante entender o que seria o [**Silverpeas**](https://www.silverpeas.org/), já que o processo se dá por ele, a depender de como está a atualização dos patchs de correção de quem usa a ferramenta para centralizar as informações da sua empresa.
O Silverpeas é um projeto open-source francês que basicamente permite unificar os usuários em um ambiente só, para que assim consigam trabalhar em conjunto, além de contribuir para o compartilhamento de seus respectivos conhecimentos e é nesse ponto que acaba sendo atrativo para uma empresa ou grupo por exemplo, que deseja concentrar o 
que está sendo compartilhado e construído entre os membros. Funciona basicamente como uma Intranet, podendo assim ter seu trabalho otimizado e traçando boas práticas e gerando melhorias no fluxo de trabalho.
No momento em que esse texto está sendo publicado o projeto está na versão 6.4.2, assim possuindo a última publicação e no caso patch de 2025-03-17.
O que é interessante é que plataformas desse tipo se tornam um item vantajoso para uma empresa, tendo em vista o controle e a possibilidade de alocar no próprio servidor.
A origem de analisar essa CVE foi desencadeada em um dia comum de CTF, porque a ideia era encontrar as flags da máquina [Silver Platter](https://tryhackme.com/room/silverplatter), que a propósito pode ser uma referência a uma empresa de banco de dados com referência em CD-ROMs, mas fica apenas a curiosidade caso tenha interesse em ler sobre. No entanto, acabou se tornando um local para praticar sobre essa CVE em questão numa perspectiva de "cenário real"e assim entendendo melhor a estrutura desse software.


## Análise do Ecossistema Silverpeas no Shodan e ZoomEye
![Shodan Report](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/fj5myz5jx55rpraojn5o.png)

![Shodan](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/nwn3ecgmy5zeucwd5jya.PNG)
O Shodan que inclusive foi algo que o  Well trouxe foi bacana para entender os ativos digitais que utilizam a plataforma.
Sendo o Silverpeas  um projeto francês, isso reflete a sua centralização na França e em Guiné Francesa. Isso é claro confirma que o país com maior exposição das instâncias é a França, mas não necessariamente é o único pais de uso.
Os sistemas expostos levam  a possibilidade de estarem vulneráveis ao bypass de autenticação.
![ZoomEye](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/k87iq8lfz141aszagid1.png)

## Visão Geral do Silverpeas
Com essa plataforma você basicamente consegue gerir os documentos elaborados entre os usuários ali presentes, além de funcionar como uma rede social interna, no qual  ocorre comunicações entre esses usuários, um controle de acesso que traria uma maior segurança e ferramentas de colaboração entre os mesmos.  Além disso, na página oficial do [Silverpeas](https://www.silverpeas.com/clients) é possível ter acesso aos diversos clientes, desde a área de saúde, cultura, etc. 

## Descrição da CVE 2024-36042
De acordo com o CVSS (Common Vulnerability Scoring System), a **CVE 2024-36042** possui severidade crítica 9.8/10, que afeta as versões 6.3.4 para baixo e que foi mitigada na versão 6.3.5. É um tipo de ataque com complexidade baixo, que não exige privilégios e nem interação com o usuário e afeta igualmente em um nível alto a tríade CIA: Confidencialidade, Integridade e Disponibilidade.
Basicamente permite bypassar a autenticação omitindo o campo de senha, pois no processo o mesmo valida como um tipo de login SSO (Single Sign-On), ou seja, um login único que permite logar em múltiplos serviços com apenas uma credencial. Um exemplo disso é a autenticação única com o próprio e-mail da Google, Microsoft, etc. Uma curiosidade é que é possível apenas excluir o campo de senha no HTML do navegador e assim tendo o mesmo efeito de omitir no repetidor do Burp suite! Que foi um teste feito pelo Gildásio!
O ponto mais interssante disso é que o Silverpeas por padrão possui um usuário padrão intitulado **SilverAdmin**, que é um user com um alto privilégio no sistema e por consequência de ser um usuário padrão, se utiliza o mesmo para realizar o bypass, podendo ter assim um acesso que não foi autenticado e com isso causar danos maiores, em quem utiliza no caso de uma não atualização com o patch 6.3.5.,  já que estamos falando de um usuário com grandes poderes na plataforma. 
Talvez ser um Admin padrão não seria tão interessante ou alguma forma de troca das informações desse possível usuário, assim como ter mais camadas de segurança nesse aspectos, para que seja evitável danos maiores.

![CVSS](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/kzorbmpajosxua16ia90.png)

## Demonstração Prática da Exploração
A vulnerabilidade se dá a partir de alguns pontos das linhas de código do Silverpeas quando o mesmo não verifica se o usuário que está tentando logar sem o campo de senha é de fato um SSO (Single-Sign-On) e com isso faz com que o mesmo tenha possibilidade de acessar o painel principal com qualquer usuário válido. Por se tratar de uma praticidade maior e poder maior, o usuário SilverAdmin por ser um administrador e ter todos os privilégios possíveis na aplicação acaba se tornando o foco maior, mas poderia ser pensado em uma possibilidade até de força bruta sem o campo de senha, apenas focado no username e com isso ter a resposta sobre os usuários válidos, no entanto seria algo mais trabalhoso e pensando no SilverAdmin como pilar dessa plataforma e todo o poder existente, você já teria acesso aos usuários válidos a partir dele.
![SilverAdmin](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/d19janisdfokgzswakgj.png)

No fluxo abaixo temos um pouco de como seria uma autenticação normal e a resposta que seria o ideal sem o bypass.  O corpo da requisição possui três itens e seus respectivos valores que são o login, que é o usuário, a senha e o domainId que é um identificador único que define o domínio dentro do Silverpeas onde estão organizados os usuários, grupos e também recursos, para assim ter o controle de acesso no domínio especificado. Nesse contexto apresentado no fluxo sem o bypass, a senha é totalmente aleatória e é claro que com isso a resposta que o servidor retorna é de erro.
![Antes do Bypass](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/d06qkzhv0ullp2ntlzk6.PNG)

No momento em que se retira o campo de senha do corpo da requisição e envia para o servidor, faz com que o servidor entenda como um login de credencial única, sem a necessidade de validação de senha e redireciona o usuário para a tela inicial do painel da plataforma.
![Bypass Silverpeas](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/5ajtarcrpzwnars7vba3.PNG)
###  Burp Suite
Peço desculpas, talvez a imagem fique um pouco sem qualidade porque usei uma ferramenta de melhoria na qualidade da imagem e não ficou tão fiel assim, porém os campos são os mesmos: Login, Password e DomainId.
![Repetidor sem o bypass](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/lchps0en3q3od6zk1mtq.png)

![Repetidor com Bypass](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/i233krckv5r8r50nuusz.png)
###  Navegador
Para realizar o procedimento pelo navegador é apenas necessário encontrar o campo Password no HTML e com isso removê-lo.
![HTML](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ufaoxic7nbr1vh7qhdnj.jpeg)
Assim que remover é só colocar o usuário SilverAdmin normalmente e logar sem colocar a senha.
![HTML](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/i37gih1x6yk8c8im33w7.jpeg)
### Resultado
Com isso é possível ter acesso ao painel quando interceptamos de maneira continuada no próprio burp ou removendo o campo Password no HTML.
![Bypass realizado](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/gjqmsmggjd9o6kb4prdc.png)
## Relação com o OWASP Top 10
![OWASP Top 10](https://owasp.org/Top10/assets/mapping.png)
Quando se pensa no Top 10 do OWASP é um ponto interessante de se debater sobre as possíveis vulnerabilidades ali presentes e não só isso, como também se completam. Nesse tópico é mais interessante pontuar em forma de listagem.
*  **A01  Broken Access Control** (Quebra de controle de acesso) -   Já que é um acesso não autorizado, pois um simples usuário comum consegue ir além, mas nesse caso nem deveria ter qualquer tipo de acesso, pois é uma plataforma com foco em empresas e grupos.
* **A04  Insecure Design** (Design Inseguro) e -  O fato do software ter sido planejado sem uma perspectiva maior sobre os riscos de segurança torna o projeto vulnerável desde o seu "nascimento", mas aqui seria um ponto interessante de se questionar: Será que toda aplicação não é no fim um Design Inseguro? Já que não existe algo realmente 100% seguro?
* **A05  Security Misconfiguration** (Configuração Incorreta de Segurança) - Em um design inseguro consequentemnte terá configurações incorretas de Segurança, já que em muitos contextos ou em boa parte das vezes, não se tem uma proteção apropriada. Só que ao mesmo tempo não é tudo 100% protegido, já que poderia ter até mesmo uma situação de zero-day ali, mas é claro que pensando na perspectiva dessa cve era algo evitável, já que existe uma conta padrão de admin, a falta de atualização, etc.
* **A06 Vulnerable and Outdated Components** (Componentes Vulneráveis e Desatualizados) - Esse não precisa especificar tanto, já que também se adequa a configurações incorretas de segurança e a necessidade de manter atualizações na medida do possível. No caso de ter uma versão abaixo da 6.3.5 já se torna algo crítico.
* **A07 Identification and Authentication Failures** (Falha de identificação e autenticação) - Por não validar da maneira correta se a retirada do campo Password é realmente uma autenticação remota (SSO), o mesmo acaba gerando o acesso a uma conta privilegiada sem a necessidade de senha ou qualquer autenticação multifator (MFA).
* **A08 Software and Data Integrity Failures** (Falhas de Software e Integridade de Dados) - Aqui é um contexto curioso onde ocorre a falta de integridade do código e principalmente dos dados, já que se perde a integridade das credenciais e a modificação dos dados de maneira não autorizada, pois o usuário que consegue esse acesso também podera fazer qualquer tipo de alteração no sistema.
## Mitigações
As mitigações foram realizadas no patch 6.3.5!
### AuthenticationCredential.java
![AuthenticationCredential.java](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/90wexihf3w6zdc10roem.png)Nessa primeira imagem é parte do código em java que armazena os dados de login do usuário e foi adicionado um novo campo chamado authenticated para assim verificar se o usuário já foi autenticado remotamente.

### AuthenticationService.java
![AuthenticationService.java](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/q26y9avfz01m24emesid.png) Nesse caso, se não possuía senha, o mesmo autenticava apenas com o login e o domínio. Com a atualização, o usuário só pula a verificação de senha se for confirmado o login remoto.

### AuthenticationServlet.java
![Image description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/11h6socvrsvdpotxuenp.png)O controle do processo de autenticação é feito através do AuthenticationServlet.java, porque não se tinha uma clareza quanto ao fator do usuário vir  de um login externo. Agora o sistema deixa claro se de fato o login é por meio de uma fonte externa.

Além disso, é interessante pensar na realização de atualizações, validações que necessitam ser mais "fortes" e também em como o sistema pode se comportar em alguma manipulação diferente até mesmo no DomainId. Outro ponto que seria válido é o bloqueio via WAF (Web Application Firewall) para a situações de requisições POST como essas no login.
## Conclusão
A vulnerabilidade CVE 2024-36042 se tornou um ponto interessante para pensar o quanto algumas vulnerabilidades podem de fato ser previsíveis e danosos, causando impactos muito maiores no sistema, principalmente na implementação da lógica por parte da autenticação remota.
A análise é justamente para compreender nesse processo de aprendizado em cibersegurança e unindo os conhecimentos que vão se complementando nessa jornada na construção de novos entendimentos e compreensões.
Isso significa que tudo foi resolvido com um patch? claro que não!, mas abre margem de pensar para além de só realizar um exploit e fim. Quando se pega desde o princípio e destrincha aos poucos, as coisas vão se tornando um pouco mais claras, desde o processo de reconhecimento, entendimento sobre como o servidor vai reagindo com o que é solicitado pelo cliente e em como acontecem as interações da camada de aplicação, já que no fim tudo termina em redes e uma limonada!
## Referências
-   GITHUB. GHSA-4w54-wwc9-x62c: Authentication Bypass in Silverpeas. Disponível em: https://github.com/advisories/GHSA-4w54-wwc9-x62c
* OWASP FOUNDATION. OWASP Top Ten: The Ten Most Critical Web Application Security Risks. [S. l.], 2021. Disponível em: <https://owasp.org/www-project-top-ten/>.
*  OWASP Foundation. OWASP Top 10: The Top Ten Most Critical Web Application Security Risks. [S.I], 2021. Seção "Metodologia". Disponível em: https://owasp.org/Top10/pt_BR/#methodology.
-   PRITCHARD, Chris. CVE-2024-36042: Silverpeas Authentication Bypass. Disponível em: https://gist.github.com/ChrisPritchard/4b6d5c70d9329ef116266a6c238dcb2d
-   SILVERPEAS. Silverpeas: the open-source collaborative  portal. [S. l.], [2024]. Disponível em: https://github.com/advisories/GHSA-4w54-wwc9-x62c
- TRYHACKME. _Silver Platter_. Disponível em: [https://tryhackme.com/room/silverplatter](https://tryhackme.com/room/silverplatter).