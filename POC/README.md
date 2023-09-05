# Proof of Concept (POC) - Readme

## Inleiding

Dit is een Proof of Concept (POC) project met instructies om de scrapers uit te voeren.

## Vooraf te downloaden en installerens

Voordat je aan de slag gaat, zorg ervoor dat je de volgende tools hebt geïnstalleerd:

- [VirtualBox](https://virtualbox.org/)
- [Vagrant](https://vagrantup.com/)
- [Git & Git bash](https://git-scm.com/).
- Ansible (only on Mac/Linux)
- [Python](https://www.python.org/)
- [Pip](https://pypi.org/project/pip/)

## Setup

1. Voer de Proof of Concept-setup uit door het `SETUP_POC.bat` script als beheerder uit te voeren.
   - Zorg ervoor dat je met beheerdersrechten bent aangemeld op je computer.
   - Navigeer naar de locatie van het script en klik met de rechtermuisknop op `SETUP_POC.bat`.
   - Kies 'Uitvoeren als administrator'.
   - Note: bij het krijgen van een vagrant init error probeer het script uit te voeren in powershell. Moest u nog steeds problemen hebben verplaats de
     vagrant file uit de folder, open een cmd en voer uit "vagrant init almalinux/9". Hierna sleept u de vagrant file terug en overschrijft u de nieuwgemaakte en start u de SETUP_POC.bat opnieuw.

## Scrapers Uitvoeren

1. Ga naar de map `scripts/scrapers` in het project.

2. Voer het `runScrapers.bat` script uit om de scrapers uit te voeren.

   - Navigeer naar de map `scripts/scrapers`.
   - Dubbelklik op `runScrapers.bat` om het script uit te voeren.

   **Opmerking:** Zorg ervoor dat je de scrapers alleen uitvoert nadat je de Proof of Concept-setup hebt voltooid.

## Aanvullende Opmerkingen

- Bij het uitvoeren van SETUP_POC.bat zal eerst de provision falen, dit is normaal. Dit komt omdat de grub pas geupdate wordt na het heropstarten van de VM.
  Daarnaa voert het nogmaals een provision uit dat deze keer niet meer zal falen.
