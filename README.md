# SimpleScrape

## Table of Contents
1. [Beschreibung des Projekts](#Beschreibung des Projekts)
2. [Installation](#Installation)
3. [Libraries und Frameworks](#Libraries und Frameworks)
4. [Deployment](#deployment)
5. [Collaboration](#collaboration)
6. [FAQs](#faqs)

## Beschreibung des Projekts
Mit SimpleScrape ermöglichen wir unseren Usern, Webseiten nach Daten zu scrapen. Hierbei können sie über eine URL nach der Verfügbarkeit von Produkten suchen. Jeder User ist in der Lage, ein Benutzerkonto mit seiner E-Mail Adresse zu erstellen. Im Benutzerkonto wird automatisch der Verlauf der Webseiten gespeichert und für erneutes Durchsuchen bereitgestellt. Sollte ein Produkt zunächst nicht verfügbar sein, wird der User benachrichtigt, sobald das gewünschte Produkt wieder verfügbar ist.


## Installation
Installation von Libraries:

```bash
pip install -r requirements.txt
```


Folgende libraries installieren:
- Flask
- Flask-Login
- Flask-SQLAlchemy
- SQLAlchemy
- Jinja2


## Libraries und Frameworks
- Flask
- Jinja2
- BeautifulSoup4
- Requests
- SQLAlchemy

## Deployment
```bash
ssh <A-Kennung>@ssh.informatik.haw-hamburg.de

ssh scraper@141.22.10.182

<VM password>

git clone https://git.haw-hamburg.de/acx810/simplescrape.git

sudo service nginx restart

sudo pkill -f gunicorn3

cd simplescrape/

gunicorn3 --workers=3 app:app --daemon
```


## Collaboration
Der main-Branch ist protected. Bei jeder Änderung, die in das Projekt hinzugefügt werden soll, muss der Entwickler zunächst einen Branch erstellen und die Änderung dort pushen. Später wird ein Merge-Request erstellt mit dem erstellten Branch.

## FAQs





