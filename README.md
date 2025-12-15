# goudot-immo
démo projet Immobilier

G1 : Promise, Patricia
G2 : Dylan, Jonathan, Steve
G3 : Cyril, Melody, Maximilien
G4 : Arnaud, Fabien

# Instalation
```bash
 python3 -m venv venv
 source venv/bin/activate
 pip install -r requirements.txt
```

# Appli Web
```bash
 source venv/bin/activate
 fastapi dev main.py
```


# VM
créer instance
ssh -L5000:localhost:5000 ubuntu@ec2-18-133-252-5.eu-west-2.compute.amazonaws.com
```bash
sudo passwd ubuntu # définir PWD
sudo nano /etc/ssh/sshd_config
Ajout:
PasswordAuthentication yes
ChallengeResponseAuthentication yes
UsePAM yes
PubkeyAuthentication yes  # (Laisse activé si tu veux aussi garder les clés SSH)

sudo systemctl restart ssh
# redirection port...
ssh -fN -L5000:localhost:5001 p4g3@datalab.myconnectech.fr

```
