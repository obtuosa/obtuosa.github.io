![Ubuntu](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/jxewzt84mv6k1b6zuwom.png)

Essa semana eu estava tentando instalar World of Warcraft na minha distro do Linux para jogar, no entanto, por questão automática acabei dando um **sudo apt upgrade** de maneira direta sem pestanejar, e nesse processo algo ocorreu e fez com que o sistema tivesse um tipo de pane ao reinicializar, com a seguinte mensagem:
![Linux](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ccwuikwl6c0qitd93ie3.jpeg)
#### Oh não! Alguma coisa está errada. Ocorreu um problema e o sistema não pôde ser recuperado. Por favor, entre em contato com um administrador de sistemas.
E aí o desespero bateu legal, porque veio o receio do sistema ter corrompido, algo ter sido afetado e que não pudesse ser revertido. Com tudo isso, seria muito chato ter que formatar e reconfigurar toda a distro com as ferramentas que já utilizava. Entretanto, durante a busca pelos fóruns da vida consegui encontrar  um tópico que me ajudou muito no processo lá no[Diolinux](https://plus.diolinux.com.br/t/sistema-com-pane-para-inicializar-e-nao-inicializa-recuperar-sistema-ubuntu-22-04/62797/3]) e aqui seria mais uma forma de pensar nas possibilidades que poderiam ter causado esse problema e a resolução caso alguém acabe passando por isso, porque não capturei ou busquei os logs da situação devido ao desespero do momento, para que fosse possível ter uma melhor exatidão do que aconteceu.
## Linux
Antes de mais nada é importante revisarmos sobre a arquitetura do sistema Linux e basicamente como ele funciona.
De maneira direta e informação de amplo acesso, Linux é um SO (Sistema Operacional) de código aberto e é bastante utilizado para servidores e data centers, dispositivos pessoais, dispositivos IoT, etc. Nele existem alguns componentes principais que fazem parte do seu funcionamento e merecem ser mencionados.
* **Hardware**: A parte física que já tenhos conhecimento sobre, tal qual o processador, a memória RAM, disco rídigo, etc.
* **Kernel**:  É o coração do Linux, e é a partir desse núcleo que iremos pensar no que ocasionou esse pane no sistema ou apenas presumir uma possibilidade. Será mais aprofundado posteriormente.
* **Shell**:  A interface entre o usuário e o kernel, tanto sendo linha de comando (terminal) quanto interface gráfica (GUI).
* **Aplicativos e Utilitários**: Nesse caso são os programas utilizados pelo usuário, como editores de texto, navegadores, etc. e os utilitários são as  ferramentas do sistema como ls, grep, etc.
* **Bibliotecas do Sistema**: Para que os aplicativos funcionem é necessário de funções especiais para acessar os recursos do sistema e garantir a funcionalidade desses aplicativos e utilitários.
* **Daemons**:  São serviços que funcionam em segundo plano para tarefas. Esses processos não necessitam da interação com o usuário. 

## Kernel
Como foi dito de maneira breve mais acima, o kernel é o núcleo do SO Linux, com isso é o coração responsável por realizar o gerenciamento de recursos de hardware, processos, os sistemas de arquivos e também a comunicação entre software e hardware. Então de maneira geral, tudo vai acabar perpassando pelo núcleo, e essa falha que ocorreu na atualização ubuntu passa pelo kernel.
Por ser o pilar central, o kernel tem seu espaço privilegiado chamado kernel space, enquanto os aplicativos rodam em modo não-privilegiado (user space). O usuário inicia um aplicativo e faz com que esse aplicativo use o system calls (syscalls), que são as portas controladas pelo kernel para que seja possível acessar os recursos que são gerenciados por ele. Portanto, o app vai utilizar (normalmente) a biblioteca padrão C, para que possa converter os seus processos em operações syscalls. Se durante essa chamada ocorrer algum tipo de falha, seja algum problema nas biblioteca, permissões ou até mesmo problemas no sistema, isso pode desencadear eventos críticos que vão desde uma falha mais simples até o sistema crashar. 
![Fluxo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/qz5766m0rmudaq1b0qmz.png)
### Glibc corrompida ou incompatível
Aqui seria mais achismo do que tudo, justamente porque não foi possível conseguir o acesso aos logs da data específica, pois quando lembrei dessa possibilidade já tinha se passado alguns dias e já não tinha mais informações no **/var/log**, apenas os mais recentes. 
Nesse caso, talvez poderia ter sido a glibc (biblioteca padrão C) que acabou ficando incompatível ou corrompida com a atualização da distro Ubuntu e ocasionou essa falha no sistema, já que é importante para o funcionamento do ecossistema Linux e acabou entrando em colapso por não ser compatível com a atualização mais recente e gerando incompatibilidade quando tudo foi atualizado.

![Fluxo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1bt9bozk980bdwhp6qlu.png)

O glibc incompatível ou corrompido geraria uma falha na tradução que acaba sendo rejeitada pelo kernel e o sistema "crasha".
## Resolução do problema
O primeiro ponto ao aparecer a mensagem de Oh não! Alguma coisa está errada, é reiniciar e dar ctrl + fn (em caso de não estar ativado) + alt + f3 no modo recuperação nas opções avançadas da distro e ter acesso as versões antigas, já que é onde teria acesso a feramenta para reparar o sistema no modo recuperação e usar essas teclas dá acesso a um terminal e possibilidade de executar alguns comandos.
#### Gerenciador de boot e ir para opções avançadas
![GNU Linux](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ijxqbt6pzit2ekkbmjz1.jpeg)
#### Seguir na opção de recovery mode

![recovery mode](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/gvgv3f0i5goxeixl29mn.jpeg)
#### Atalho para abrir um terminal 

![Atalho](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/hhbk1m9goisrdr0kgo0x.jpeg)
#### Comandos
```
1. sudo apt update && sudo apt dist-upgrade
2. sudo dpkg --configure -a
3. sudo apt --fix-broken install
4. sudo apt update && sudo apt dist-upgrade
5. sudo apt clean && sudo apt autoremove
6. sudo reboot now
```
Sem especificar cada passo, essa sequência assim que o terminal aparecer e for realizado o login vai justamente atualizar, reparar as dependências, limpar o sistema e por fim reiniciar, assim conseguindo resolver os problemas causados pós atualização. Com enfase principalmente no **sudo apt --fix-broken install**, que realiza essa correção dos pacotes que foram corrompidos ou tiveram algum tipo de problema quanto a isso e seguindo a lógica de atualizar tudo pós realização desses reparos.
## Conclusão
O princípio é apenas de buscar uma possível solução, mas sem ser uma verdade absoluta, justamente por serem diversas variáveis nesse processo que culminaram nesse crash do sistema. Porém, o fluxo de ideias é usar essas pequenas situações para compreender alguns entendimentos e buscar conhecimento sobre o que está sendo feito, não só apenas de realizar os comandos no automático e quem sabe ajudar alguém que acabe passando por essa situação.
Agradecimentos principalmente ao fórum do **Diolinux** que me ajudou muito e  em compreender que não é legal atualizar o sistema assim diretamente para uma versão que não está estável ;).
Em caso de erros, dúvidas, questionamentos, etc., sempre estarei aberta a ouvir e debater sobre, porque o importante é aprender.

### Referências bibliográficas
**DIOLINUX.** Sistema com pane para inicializar e não inicializa – recuperar sistema Ubuntu 22.04. **Diolinux Plus**, 2023. Disponível em: [https://plus.diolinux.com.br/t/sistema-com-pane-para-inicializar-e-nao-inicializa-recuperar-sistema-ubuntu-22-04/62797](https://plus.diolinux.com.br/t/sistema-com-pane-para-inicializar-e-nao-inicializa-recuperar-sistema-ubuntu-22-04/62797).

**DYER, Bill.** Linux Daemons: Understanding and Managing These Background Processes. **It's FOSS**, [2023]. Disponível em: [https://itsfoss.com/linux-daemons/](https://itsfoss.com/linux-daemons/).

**LINUX MAN-PAGES.** syscalls(2) - Linux manual page. **man7.org**, [2025]. Disponível em: [https://www.man7.org/linux/man-pages/man2/syscalls.2.html](https://www.man7.org/linux/man-pages/man2/syscalls.2.html).

**WIKIPEDIA.** User space and kernel space. **Wikipedia**, [2025]. Disponível em: [https://en.wikipedia.org/wiki/User_space_and_kernel_space](https://en.wikipedia.org/wiki/User_space_and_kernel_space).