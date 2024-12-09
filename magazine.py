import random
import csv
import json


# Dictionnaires pour stocker les produits, clients, et leurs paniers
produit = {}  # produit = {codeP: {"Nom": ..., "Prix": ..., "Quantite": ...}}
client = {}   # client = {CAC: {"N° Client": ..., "Panier": {codeP: {"Quantite": ...}}}}\
ventes = {}  # ventes = {codeP: quantiteVendu}

dernier_code_produit = 0  # Dernier code produit utilisé
dernier_num_client = 0    # Dernier numéro client incrémental


# Les fonctionnalités du gérant

def AjouterProduit():
    """Ajoute un nouveau produit."""
    global dernier_code_produit

    dernier_code_produit += 1
    codeP = dernier_code_produit

    nom = input("Entrez le nom du produit : ").strip()
    while True:
        try:
            prix = float(input("Entrez le prix du produit : "))
            quantite = int(input("Entrez la quantité du produit : "))
            break
        except ValueError:
            print("Veuillez entrer des valeurs numériques valides pour le prix et la quantité.")

    produit[codeP] = {"Nom": nom, "Prix": prix, "Quantite": quantite}
    print(f"\nProduit {nom} ajouté avec succès sous le code {codeP}.")

def ModifierQuantiteProduit(codeP):
    """Modifie la quantité d'un produit."""
    if codeP not in produit:
        print("Produit introuvable.")
        return

    print("\n1. Ajouter quantité")
    print("2. Retirer quantité")
    choix = input("Entrez votre choix : ")

    try:
        quantite = int(input("Entrez la quantité : "))
        if choix == '1':
            produit[codeP]['Quantite'] += quantite
            print(f"Quantité mise à jour : {produit[codeP]['Quantite']}.")
        elif choix == '2':
            if produit[codeP]['Quantite'] >= quantite:
                produit[codeP]['Quantite'] -= quantite
                print(f"Quantité mise à jour : {produit[codeP]['Quantite']}.")
            else:
                print("Erreur : Quantité insuffisante en stock.")
        else:
            print("Choix invalide.")
    except ValueError:
        print("Veuillez entrer une valeur numérique valide pour la quantité.")

def SupprimerProduit(codeP):
    """Supprime un produit."""
    if codeP not in produit:
        print("Produit introuvable.")
        return
    print(f"Produit {produit[codeP]['Nom']} supprimé avec succès.")
    del produit[codeP]

def AjouterClient(prenom):
    """Ajoute un nouveau client."""
    global dernier_num_client
    CAC = genererCAC(prenom)
    dernier_num_client += 1
    client[CAC] = {"N° Client": dernier_num_client, "Panier": {}}
    print(f"Client ajouté : {prenom}, CAC : {CAC}, N° Client : {dernier_num_client}.")

def SupprimerClient(CAC):
    """Supprime un client."""
    if CAC not in client:
        print("Client introuvable.")
        return
    print(f"Client {CAC} supprimé avec succès.")
    del client[CAC]

def AfficherQuantite(codeP):
    """Affiche la quantité d'un produit."""
    if codeP not in produit:
        print("Produit introuvable.")
        return
    print(f"Quantité du produit {produit[codeP]['Nom']} : {produit[codeP]['Quantite']}.")



# Les fonctionnalités du client



def AfficherInformationProduit():
    """Affiche la liste des produits."""
    print("\nProduits disponibles :")
    if not produit:
        print("Aucun produit en stock.")
    else:
        for codeP, details in produit.items():
            print(f"Code : {codeP}, Nom : {details['Nom']}, Prix : {details['Prix']} MAD, Quantité : {details['Quantite']}")

def AjouterPanier(CAC):
    """Ajoute un produit au panier du client."""
    codeP = int(input("Entrez le code du produit à ajouter : "))
    if codeP not in produit:
        print("Produit introuvable.")
        return

    try:
        quantite = int(input("Entrez la quantité à ajouter : "))
        if produit[codeP]['Quantite'] < quantite:
            print("Quantité insuffisante en stock.")
            return

        panier = client[CAC]['Panier']
        if codeP in panier:
            panier[codeP]['Quantite'] += quantite
        else:
            panier[codeP] = {"Quantite": quantite}
        produit[codeP]['Quantite'] -= quantite

        print(f"{quantite} unité(s) du produit {produit[codeP]['Nom']} ajoutée(s) au panier.")
    except ValueError:
        print("Veuillez entrer une quantité valide.")


def RetirerPanier(CAC):
    """Retire un produit du panier du client."""
    codeP = int(input("Entrez le code du produit à retirer : "))
    panier = client[CAC]['Panier']

    if codeP not in panier:
        print("Produit introuvable dans le panier.")
        return

    try:
        quantite = int(input("Entrez la quantité à retirer : "))
        if panier[codeP]['Quantite'] <= quantite:
            produit[codeP]['Quantite'] += panier[codeP]['Quantite']
            del panier[codeP]
            print("Produit retiré du panier.")
        else:
            panier[codeP]['Quantite'] -= quantite
            produit[codeP]['Quantite'] += quantite
            print("Quantité mise à jour dans le panier.")
    except ValueError:
        print("Veuillez entrer une quantité valide.")


def Achat(CAC):
    """Génère et affiche un reçu pour les achats effectués par un client."""
    panier = client[CAC]['Panier']
    print(f"\nReçu d'achat pour le client {CAC} :")

    if not panier:
        print("Le panier est vide. Aucun achat à traiter.")
    else:
        total = 0
        print("\n========== Reçu ==========")
        for codeP, details in panier.items():
            quantite = details['Quantite']  # Extraire la quantité du produit
            prix_unitaire = produit[codeP]['Prix']
            sous_total = prix_unitaire * quantite
            total += sous_total
            print(f"Produit : {produit[codeP]['Nom']}")
            print(f"  Quantité : {quantite}")
            print(f"  Prix Unitaire : {prix_unitaire:.2f} MAD")
            print(f"  Sous-total : {sous_total:.2f} MAD\n")

            # Mise à jour de la quantité vendue pour le produit dans le dictionnaire ventes
            if codeP in ventes:
                ventes[codeP] += quantite
            else:
                ventes[codeP] = quantite

        print(f"Montant total : {total:.2f} MAD")
        print("==========================")
        
        # Enregistrer les données dans le fichier JSON
        EcrireFichierCSV()

        # Vider le panier après l'achat
        client[CAC]['Panier'] = {}
        print("\nMerci pour votre achat ! Le panier a été vidé.")



def genererCAC(prenom):
    return prenom[:2].upper() + str(random.randint(10, 99))

def generer_num_client_incremental():
    global dernier_num_client
    dernier_num_client += 1
    return str(dernier_num_client).zfill(8)  # Retourne un numéro de 8 chiffres

def charger_clients():
    global dernier_num_client
    try:
        with open('client.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Ignore l'en-tête
            for row in reader:
                numCl = int(row[0])  # Premier champ : numéro de client
                dernier_num_client = max(dernier_num_client, numCl)
    except FileNotFoundError:
        print("Aucun fichier client.csv trouvé, création d'un nouveau fichier...")
    except Exception as e:
        print(f"Erreur lors du chargement des clients : {e}")


def charger_produits():
    """Charge les produits depuis un fichier CSV et met à jour le dernier code produit."""
    global dernier_code_produit
    try:
        with open('produit.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Ignore la ligne d'en-tête
            for row in reader:
                codeP, nom, prix, quantite = row
                produit[int(codeP)] = {
                    "Nom": nom,
                    "Prix": float(prix),
                    "Quantite": int(quantite)
                }
                dernier_code_produit = max(dernier_code_produit, int(codeP))
        print("Produits chargés avec succès.")
    except FileNotFoundError:
        print("Fichier produit.csv introuvable. Démarrage avec une liste vide.")

def exporter_donnees():
    """Exporte les données des produits et des clients dans des fichiers CSV."""
    try:
        # Export des produits
        with open("produits.csv", mode="w", newline="", encoding="utf-8") as fichier_produits:
            writer = csv.writer(fichier_produits)
            # Écrire les en-têtes
            writer.writerow(["Code Produit", "Nom", "Prix (MAD)", "Quantité"])
            # Écrire les données des produits
            for codeP, details in produit.items():
                writer.writerow([codeP, details["Nom"], details["Prix"], details["Quantite"]])
        print("Données des produits exportées avec succès dans 'produits.csv'.")

        # Export des clients (sans panier)
        with open("clients.csv", mode="w", newline="", encoding="utf-8") as fichier_clients:
            writer = csv.writer(fichier_clients)
            # Écrire les en-têtes
            writer.writerow(["CAC", "N° Client"])
            # Écrire les données des clients
            for CAC, details in client.items():
                writer.writerow([CAC, details["N° Client"]])
        print("Données des clients exportées avec succès dans 'clients.csv'.")

    except Exception as e:
        print(f"Erreur lors de l'exportation des données : {e}")


def charger_donnees():
    """Charge les données des produits et des clients à partir de fichiers CSV, sans panier."""
    try:
        # Chargement des produits depuis le fichier CSV
        with open('produits.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Ignorer l'en-tête
            for row in reader:
                codeP, nom, prix, quantite = row
                produit[int(codeP)] = {
                    "Nom": nom,
                    "Prix": float(prix),
                    "Quantite": int(quantite)
                }
        print("Les produits ont été chargés avec succès depuis 'produits.csv'.")
    except FileNotFoundError:
        print("Fichier 'produits.csv' introuvable. Démarrage avec une liste vide de produits.")
    except Exception as e:
        print(f"Erreur lors du chargement des produits : {e}")
    
    try:
        # Chargement des clients depuis le fichier CSV
        with open('clients.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Ignorer l'en-tête
            for row in reader:
                CAC, numCl = row
                client[CAC] = {
                    "N° Client": numCl,
                    "Panier": {}  # Initialiser un panier vide pour chaque client
                }
        print("Les clients ont été chargés avec succès depuis 'clients.csv'.")
    except FileNotFoundError:
        print("Fichier 'clients.csv' introuvable. Démarrage avec une liste vide de clients.")
    except Exception as e:
        print(f"Erreur lors du chargement des clients : {e}")



def EcrireFichierCSV():
    """Enregistre les données des ventes dans un fichier CSV."""
    with open('ventes.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write header row if file is empty
        writer.writerow(['Code Produit', 'Nom Produit', 'Quantité Vendu'])

        for codeP, quantite in ventes.items():
            # Getting product name from produit dictionary
            nom_produit = produit[codeP]['Nom']
            # Write product data
            writer.writerow([codeP, nom_produit, quantite])

    print("Les données des ventes ont été enregistrées dans 'ventes.csv'.")



def charger_FichierCSV():
    """Charge les données des ventes depuis un fichier CSV."""
    try:
        with open('ventes.csv', mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            
            # Skip the header
            next(reader)

            # Clear the existing ventes data before loading new data
            ventes.clear()

            # Read and load the data into the ventes dictionary
            for row in reader:
                codeP, nom_produit, quantite = row
                quantite = int(quantite)  # Convert quantity to integer
                ventes[codeP] = quantite

        print("Les données des ventes ont été chargées depuis 'ventes.csv'.")
    except FileNotFoundError:
        print("Le fichier 'ventes.csv' n'a pas été trouvé.")
    except Exception as e:
        print(f"Une erreur est survenue lors du chargement du fichier CSV : {e}")



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
            if CAC not in client: 
                print("\nErreur : Le client n'existe pas.")
            else:
                AjouterPanier(CAC)

        elif choix == '3':
            CAC = input("\nEntrer le CAC: ")
            if CAC not in client: 
                print("\nErreur : Le client n'existe pas.")
            else:
                RetirerPanier(CAC)
        elif choix == '4':
            CAC = input("\nEntrer le CAC: ")
            if CAC not in client: 
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

charger_donnees()
charger_FichierCSV()
program_principal()
