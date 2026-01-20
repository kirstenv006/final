# De Persona Generator

De Persona Generator is een webtool voor CMD-studenten waarmee zij hun doelgroep kunnen omzetten in een persona. Persona’s zijn fictieve personages die een doelgroep representeren en worden gebruikt om ontwerpen en concepten te testen binnen projecten. De website functioneert als een generator: de gebruiker voert doelgroep kenmerken in, zoals leeftijd, doelen, frustraties en karaktereigenschappen. Op basis van deze input genereert de website een persona. De ingevoerde data worden opgeslagen in een database, zodat persona’s later opnieuw gebruikt, aangepast of verder ontwikkeld kunnen worden. Dit maakt het understand- en ideate-proces sneller en efficiënter.


# Hoe werkt de Persona Generator? In stappen:

    1. Inlogpagina
    
    De gebruiker opent de website en komt terecht op een inlogpagina, hier kan hij/zij inloggen om eerder gemaakte persona's te bekijken of een account aanmaken om te beginnen met het makenn van persona's.


    2. Dashboard/Home

    Zodra de gebruiker is ingelogd zijn er 3 knoppen en een schermpje te zien. Dit zijn de acties die de gebruiker op de website kan uitvoeren. Zo kan de gebruiker een nieuwe persona maken, eerder gemaakte persona's bekijken of weer uitloggen. Verder is er een schermpje/overzicht waar de gebruiker zijn/haar laatst gemaakte persona inclusief gekozen stijl kan bekijken.
    

    3. Nieuw persona

        3.1 Stap 1
        De eerste stap is een algemeen profiel creëren wat voor doelgroep is de persona, hoe heet de persona? hou oud is de persona? en welk geslacht is de persona? 

        3.2 Stap 2
        In stap 2 wordt het leven van de persona ingericht. Wat doet die? Studeert hij/zij nog of zit ze nog maar net op de basisschool. Wie weet is de persona al lang afgestudeerd en werkt hij/zij al fulltime. Dit beeld wordt in stap 2 geschetst. 

        3.3 Stap 3
        Wat voor persoon is de persona eigenlijk? Wat zijn de doelen/drijfveren en waar loopt de persona tegen aan? Dit wordt gevisualiseerd in stap 3. Naast de doelen worden ook de karaktereigenschappen vormgegeven. Zo weet de gebruiker wie de doelgroep is en waar hij/zij een project voor kan gaan maken.


    4. Resultaat/genereren 
    
    Zodra de persona tot leven is gekomen wordt de data van de persona opgeslagen en gevisualiseerd. Alle ingevulde velden komen tot leven en worden samengevoegd tot een afbeelding. Is de persona nog niet helemaal de doelgroep? Geen probleem, de gebruiker kan zijn/haar persona in dit overzicht nog aanpassen, opslaan of niet opslaan en een nieuwe persona maken. Is de persona wel naar wens? Dan kan de gebruiker zijn/haar persona een vormgevingsstijl opgeven en opslaan in de database. 


    5. Mijn persona's
    
    De gebruiker kan op deze pagina visueel alle gemaakte persona's zien, moet de gebruiker een persona van een eerder project gebruiken? Geen probleem ze staan allemaal hier overzichtelijk op een rijtje. Ook hier kan de gebruiker verschillende acties doen met de persona. Zo kan de persona in het groot bekeken worden (alle ingevulde data zien), de persona toch nog aanpassen of als de persona niet goed is of niet meer relevant kan hij/zij deze verwijderen. 


    6. Uitloggen
    
    Klaar met werken aan de persona's? De gebruiker kan uitloggen en later weer terug inloggen om later nieuwe persona's te maken of eerdere persona's opnieuw bekijken.



# Technische opzet

Frontend
De frontend van de Persona Generator bestaat uit HTML-templates met Jinja2 en CSS voor de vormgeving.
De applicatie maakt gebruik van een basislayout (base.html) die wordt uitgebreid door andere pagina’s, zoals het dashboard, de persona-stappen en het persona-overzicht.

De interface is opgezet als een stap-voor-stap generator, waarbij de gebruiker via meerdere formulieren geleidelijk een persona opbouwt. Visuele feedback, zoals de stappen-indicator en persona-kaarten, helpt de gebruiker overzicht te houden tijdens het proces.

Backend
De backend is ontwikkeld in Python met het Flask-framework.
Deze laag is verantwoordelijk voor:

- Route-afhandeling
- Gebruikersauthenticatie (login, registratie, sessies)
- Verwerking van formulierdata
- Opslaan, ophalen en bewerken van persona’s

Tijdens het aanmaken van een persona wordt gebruikersinvoer tijdelijk opgeslagen in sessions, zodat de data behouden blijft tussen de verschillende stappen. Na afronding wordt de persona definitief opgeslagen in de database.

Data-opslag
De applicatie gebruikt een SQLite-database in combinatie met SQLAlchemy als ORM.
Er zijn twee hoofdmodellen: de User (voor gebruikersaccounts) en de  Persona (voor de aangemaakte persona’s). Elke persona is gekoppeld aan één gebruiker via een foreign key (user_id). Hierdoor kan iedere gebruiker alleen zijn of haar eigen persona’s bekijken en beheren. De database wordt automatisch aangemaakt bij het starten van de applicatie.

Architectuur
De applicatie is modulair opgebouwd:
- app.py bevat de applicatielogica en routes
- models.py definieert de database-structuur
- extensions.py initialiseert de database
- templates/ bevat de HTML-templates
- static/ bevat CSS en afbeeldingen
Deze structuur zorgt voor een duidelijke scheiding tussen logica, data en presentatie, waardoor de applicatie eenvoudig uitbreidbaar en onderhoudbaar blijft.

Beheer & beveiliging
Om de applicatie veilig en overzichtelijk te houden zijn verschillende maatregelen toegepast:
- Alleen ingelogde gebruikers hebben toegang tot persona-functionaliteiten
- Sessies worden gebruikt om gebruikers te identificeren
- Persona’s zijn alleen zichtbaar en bewerkbaar door de eigenaar
- Basisvalidatie voorkomt fouten bij invoer
- Gebruikers kunnen persona’s aanpassen of verwijderen via beschermde routes


# Gebruikte technieken

- Python 3
- Flask
- Flask-SQLAlchemy
- SQLite
- HTML / Jinja2
- CSS
- Sessions

# Installatie

Het onderstaande stappenplan zorgt ervoor dat de applicatie lokaal kan worden uitgevoerd.

Vereisten

    Python 3.10 of hoger

    pip (standaard bij Python-installatie)

    Installatie (met virtual environment – aanbevolen)

# Clone deze repository:

    1. git clone <repository-url>
        cd final


    2. Maak een virtual environment aan:
        python -m venv venv


    3. Activeer de virtual environment:
        Windows
            .venv\Scripts\activate

        macOS / Linux
            source .venv/bin/activate

    4. Installeer de benodigde dependencies:
        pip install -r requirements.txt


Start de applicatie: python app.py of via flask run


De applicatie draait nu op: http://127.0.0.1:5000


# Bekende beperkingen
- De gemaakte persona's kunnen niet tot pdf geexporteerd worden
- De gebruiker kan niet zelf onderwerpen toevoegen
- De gebruiker kan zelf geen afbeelding invoeren

# Toekomstige verbeteringen
- Een export functie tot pdf
- De gebruiker kan zelf afbeeldingen toevoegen
- Meer stijlen 