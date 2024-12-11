# Gestion de Magasin

## Description

Ce projet est un système de gestion de magasin développé en Python. Il permet de gérer les produits, les clients, les paniers et les ventes dans un environnement de magasin. Le programme inclut des fonctionnalités pour ajouter, modifier, supprimer des produits, gérer les paniers des clients et générer des reçus d'achats. De plus, il permet d'exporter et de charger les données des produits et des clients à partir de fichiers CSV.

## Fonctionnalités

### Gestion des Produits
- Ajouter un nouveau produit avec un code unique, un nom, un prix et une quantité.
- Modifier la quantité d'un produit existant.
- Supprimer un produit du stock.
- Afficher les produits disponibles en stock.

### Gestion des Clients
- Ajouter un nouveau client avec un identifiant unique.
- Supprimer un client du système.
- Afficher les informations des clients.

### Gestion des Paniers
- Ajouter des produits au panier d'un client.
- Retirer des produits du panier d'un client.
- Afficher le contenu du panier.

### Achat et Reçu
- Générer un reçu d'achat pour les produits dans le panier d'un client, incluant le prix unitaire, la quantité et le total.

### Export/Import des Données
- Exporter les données des produits, clients et ventes dans des fichiers CSV.
- Charger les données des produits et des clients à partir de fichiers CSV.

## Prérequis

- Python 3.x
- Bibliothèque `csv` pour la gestion des fichiers CSV
