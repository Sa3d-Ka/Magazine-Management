import random
import csv


# Dictionnaires pour stocker les produits, clients, paniers et relations clients-produits
produit = {}
client = {}
pannier = {}

# Les fonctionnalités du gérant

def AjouterProduit():
    # Demande d'informations pour un nouveau produit et ajout au dictionnaire
    codeP = input("\nEntrer code produit: ")
    nom = input("Entrer nom de produit: ")
    prix = float(input("Entrer le prix de produit: "))
    quantite = int(input("Entrer la quantite de produit: "))
    
    produit[codeP] = {
        "Nom": nom,
        "Prix": prix,
        "Quantite": quantite,
    }
    print(f"\nProduit {nom} ajouté avec succès!")

def ModifierQuantiteProduit(codeP):
    # Modifie la quantité d'un produit en stock
    if codeP not in produit:
        print("Le produit n'existe pas.")
        return

    print("\n1. Ajouter quantité")
    print("2. Retirer quantité")
    choix = input("Entrez votre choix: ")

    if choix == '1':
        quantite = int(input("\nEntrez la quantité à ajouter: "))
        produit[codeP]['Quantite'] += quantite
        print(f"\nQuantité ajoutée avec succès! Nouvelle quantité: {produit[codeP]['Quantite']}")
    elif choix == '2':
        quantite = int(input("\nEntrez la quantité à retirer: "))
        if produit[codeP]['Quantite'] >= quantite:
            produit[codeP]['Quantite'] -= quantite
            print(f"\nQuantité retirée avec succès! Nouvelle quantité: {produit[codeP]['Quantite']}")
        else:
            print("\nErreur : La quantité à retirer dépasse la quantité disponible.")
    else:
        print("\nChoix invalide.")

def SupprimerProduit(codeP):
    # Supprime un produit du stock
    if codeP not in produit:
        print("Le produit n'existe pas.")
        return
    print(f"Produit {produit[codeP]['Nom']} supprimé avec succès!\n")
    del produit[codeP]

def AjouterClient(prenom):
    # Ajoute un nouveau client avec un identifiant unique généré
    numCl = input("Entrer le numéro de client: ")
    if numCl in client:
        print("Erreur : Ce numéro de client existe déjà.")
        return
    CAC = genererCAC(prenom)  
    client[numCl] = CAC
    print(f"Le Client {prenom} ajouté avec succès!")
    print(f"Numéro Client: {numCl}")
    print(f"CAC: {CAC}")

def SupprimerClient(numCl):
    # Supprime un client de la liste
    if numCl not in client:
        print("Le client n'existe pas.\n")
        return
    del client[numCl]
    print("Client supprimé avec succès!\n")

def AfficherQuantite(codeP):
    # Affiche la quantité disponible d'un produit
    if codeP not in produit:
        print("Le Produit n'existe pas.\n")
        return
    quantite = produit[codeP]['Quantite']
    print(f"La quantite du produit avec le codeP {codeP} est: {quantite}")



# Les fonctionnalités du client



def AfficherInformationProduit():
    # Affiche tous les produits disponibles
    print("\nProduits actuellement en stock:")
    if not produit:
        print("Aucun produit n'est disponible pour le moment.")
        return

    for codeP, details in produit.items():
        nom = details.get("Nom", "N/A")
        prix = details.get("Prix", "N/A")
        quantite = details.get("Quantite", "N/A")
        print(f"Code Produit: {codeP}, Nom: {nom}, Prix: {prix} MAD, Quantité: {quantite}")

def AjouterPannier(CAC):
    # Permet au client d'ajouter un produit à son panier
    codeP = input("Entrer le code produit: ")
    if codeP not in produit:
        print("Le produit n'existe pas.\n")
        return
    quantiteS = int(input("La quantité souhaitée: "))
    if produit[codeP]['Quantite'] < quantiteS:
        print("\nErreur : Quantité demandée dépasse le stock disponible.")
        return
    
    nom = produit[codeP]['Nom']
    prix = produit[codeP]['Prix']

    pannier[CAC] = {
        "Nom": nom,
        "Code produit": codeP,
        "Prix": prix,
        "QuantiteS": quantiteS,
    }
    print(f"\nProduit {nom} ajouté au pannier avec succès!")

    # Réduit la quantité de produit en stock après l'ajout au panier
    produit[codeP]['Quantite'] -= quantiteS

def RetirerPannier(CAC):
    # Permet au client de retirer un produit de son panier
    if CAC not in pannier:
        print("Erreur : Aucun achat trouvé pour ce CAC.")
        return

    codeP = pannier[CAC]['Code produit']
    quantiteR = int(input("\nEntrez la quantité à retirer: "))

    if pannier[CAC]['QuantiteS'] >= quantiteR:
        pannier[CAC]['QuantiteS'] -= quantiteR
        produit[codeP]['Quantite'] += quantiteR

        print(f"\nQuantité retirée avec succès! Nouvelle quantité dans le panier: {pannier[CAC]['QuantiteS']}")

        if pannier[CAC]['QuantiteS'] == 0:
            del pannier[CAC]
            print("\nProduit retiré du panier car la quantité est maintenant zéro.")
    else:
        print("\nErreur : La quantité à retirer dépasse la quantité dans le panier.")

def Achat(CAC):
    # Permet au client d'acheter les produits dans son panier
    if CAC not in pannier:
            print("Erreur : Aucun achat trouvé pour ce CAC.")
            return

    client_info = pannier[CAC]
    total = client_info["Prix"] * client_info["QuantiteS"]

    print("\n========== Reçu ==========")
    print(f"Nom du Produit: {client_info['Nom']}")
    print(f"Code Produit: {client_info['Code produit']}")
    print(f"Prix Unitaire: {client_info['Prix']:.2f} MAD")
    print(f"Quantité: {client_info['QuantiteS']}")
    print(f"Total: {total:.2f} MAD")
    print("==========================\n")

def genererCAC(prenom):
    # Génère un code client unique à partir du prénom
    lettre = prenom[:2].upper()
    CAC = f"{lettre}{random.randint(10, 99)}"
    return CAC

def exporter_donnees():
    # Exporte les données des produits, clients et paniers vers des fichiers CSV
    with open('produit.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['CodeP', 'Nom', 'Prix', 'Quantite'])
        for codeP, details in produit.items():
            writer.writerow([codeP, details['Nom'], details['Prix'], details['Quantite']])
    print("Les données des produits ont été exportées avec succès.")
    
    with open('client.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Numéro Client', 'CAC'])
        for numCl, CAC in client.items():
            writer.writerow([numCl, CAC])
    print("Les données des clients ont été exportées avec succès.")

    with open('pannier.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['CAC', 'Nom', 'Code Produit', 'Prix', 'QuantiteS'])
        for CAC, details in pannier.items():
            writer.writerow([CAC, details['Nom'], details['Code produit'], details['Prix'], details['QuantiteS']])
    print("Les données du pannier ont été exportées avec succès.")

def charger_donnees():
    # Charge les données des produits à partir d'un fichier CSV
    try:
        with open('produit.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                produit[row['CodeP']] = {
                    "Nom": row['Nom'],
                    "Prix": float(row['Prix']),
                    "Quantite": int(row['Quantite']),
                }
        print("Les données des produits ont été chargées avec succès.")
    except FileNotFoundError:
        print("Fichier produit.csv introuvable. Les données des produits sont vides.")

    # Charge les données des clients à partir d'un fichier CSV
    try:
        with open('client.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                client[row['Numéro Client']] = row['CAC']
        print("Les données des clients ont été chargées avec succès.")
    except FileNotFoundError:
        print("Fichier client.csv introuvable. Les données des clients sont vides.")

    # Charge les données des paniers à partir d'un fichier CSV
    try:
        with open('pannier.csv', mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                pannier[row['CAC']] = {
                    "Nom": row['Nom'],
                    "Code produit": row['Code Produit'],
                    "Prix": float(row['Prix']),
                    "QuantiteS": int(row['QuantiteS']),
                }
        print("Les données des paniers ont été chargées avec succès.")
    except FileNotFoundError:
        print("Fichier pannier.csv introuvable. Les données des paniers sont vides.")

def menu_gerant():
    # Affiche le menu pour le gérant et permet de choisir une option
    while True:
        print(f"\n{'-' * 15} Menu Gerant {'-' * 15}")
        print("1.Ajouter le produit")
        print("2.Modifier la quantite de produit")
        print("3.Supprimer le produit")
        print("4.Ajouter client")
        print("5.Supprimer client")
        print("6.Afficher la quantite total")
        print("7.Exporter les données")
        print("8.Quitter")
        print('-' * 40)
        choix = input("Entrer votre choix: ")
        if choix == '1':
            AjouterProduit()
        elif choix == '2':
            codeP = input("\nEntrer le code produit: ")
            ModifierQuantiteProduit(codeP)
        elif choix == '3':
            codeP = input("\nEntrer le code produit: ")
            SupprimerProduit(codeP)
        elif choix == '4':
            prenom = input("\nEntrer le PRENOM: ").upper()
            AjouterClient(prenom)
        elif choix == '5':
            numCl = input("\nEntrer le numero de client: ")
            SupprimerClient(numCl)
        elif choix == '6':
            codeP = input("\nEntrer code produit: ")
            AfficherQuantite(codeP)
        elif choix == '7':
            exporter_donnees()
        elif choix == '8':
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

def menu_client():
    # Affiche le menu pour le client et permet de choisir une option
    while True:
        print(f"\n{'-' * 15} Menu Client {'-' * 15}")
        print("1.Afficher le menu des produits")
        print("2.Ajouter au pannier")
        print("3.Retirer du pannier")
        print("4.Achat")
        print("5.Quitter")
        print('-' * 40)
        choix = input("Entrer votre choix: ")

        if choix == '1':
            AfficherInformationProduit()
        elif choix == '2':
            CAC = input("\nEntrer le CAC: ")
            if CAC not in client.values(): 
                print("\nErreur : Le client n'existe pas.")
            else:
                AjouterPannier(CAC)

        elif choix == '3':
            CAC = input("\nEntrer le CAC: ")
            if CAC not in client.values(): 
                print("\nErreur : Le client n'existe pas.")
            else:
                RetirerPannier(CAC)
        elif choix == '4':
            CAC = input("\nEntrer le CAC: ")
            if CAC not in client.values(): 
                print("\nErreur : Le client n'existe pas.")
            else:
                Achat(CAC)
        elif choix == '5':
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

def program_principal():
    charger_donnees()
    # Affiche le menu principal et dirige l'utilisateur vers le gérant ou le client
    while True:
        print(f"\n{'-' * 15} Menu Principal {'-' * 15}")
        print("1.Gerant")
        print("2.Client")
        print("3.Quitter")
        print('-' * 40)
        type_utilisateur = input("Entrer votre choix: ")
        if type_utilisateur == '1':
            menu_gerant()
        elif type_utilisateur == '2':
            menu_client()
        elif type_utilisateur == '3':
            break
        else:
            print("Choix invalide. Veuillez réessayer.")

program_principal()