# -*- coding: utf-8 -*-
class __Chiffrer:
    def __init__(self, version: int = 2):
        self.__version = version
        self.__toutes_les_versions = [1, 2]
        if self.__version not in self.__toutes_les_versions:
            raise Exception("La version {} n'est pas une version valide. Voici la liste des versions : {}".format(
                self.__version, self.__toutes_les_versions))

    def Chiffrer_chaine_caracteres(self, __chaine_caracteres: str, __hash :str = None):
        if self.__version == 1:
            __chaine = ''
            __clef = random.randint(0, 1000)
            for __caractere in __chaine_caracteres:
                __chaine += chr(ord(__caractere)+__clef)
            return __chaine
        elif self.__version == 2:
            __chaine = ""
            __indice_hash = 0
            for __indice in range(len(__chaine_caracteres)):
                __indice_hash = __indice % 128
                __chaine += self.Chiffrer_caractere(__chaine_caracteres[__indice], __hash[__indice_hash])
            return __chaine


    def Chiffrer_caractere(self, __caractere: str, __hash: str):
        if self.__version == 2:
            __dict_hex = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10,
                          'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}
            return chr(ord(__caractere)+__dict_hex[__hash])


class __Dechiffrer:
    def __init__(self, version: int = 2):
        self.__version = version
        self.__toutes_les_versions = [1, 2]
        if self.__version not in self.__toutes_les_versions:
            raise Exception("La version {} n'est pas une version valide. Voici la liste des versions : {}".format(
                self.__version, self.__toutes_les_versions))
        if self.__version == 1:
            self.__desincrementation = 0
            self.__clef = 0

    def Dechiffrer_chaine_caracteres(self, __chaine_caracteres: str, __hash: str = None):
        if self.__version == 1:
            __chaine = ' '
            __clef = 0
            try:
                while __chaine[0] != '{':
                    __clef += 1
                    __chaine = ''
                    for index in range(len(__chaine_caracteres)):
                        __chaine += chr(ord(__chaine_caracteres[index])-__clef)
            except ValueError:
                print("Erreur: Soit le fichier est corompu ou soit vous avez saisie la mauvaise version de chiffrement.")
                input("Appuyer sur Entrée pour continuer.")
                exit(-1)
            return __chaine
        elif self.__version == 2:
            __chaine = ""
            __indice_hash = 0
            for __indice in range(len(__chaine_caracteres)):
                __indice_hash = __indice % 128
                __chaine += self.Dechiffrer_caractere(__chaine_caracteres[__indice], __hash[__indice_hash])
            return __chaine

    def Dechiffrer_caractere(self, __caractere: str, __hash: str):
        if self.__version == 2:
            __dict_hex = {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'a': 10,
                          'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}
            return chr(ord(__caractere)-__dict_hex[__hash])

def __clear(_ = None):
    import os
    import platform
    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Linux":
        os.system("clear")

def __afficher_tout():
    __clear()
    print("- données global : " + str(__donnee_global_database) + "\n")
    print("- donnees : " + str(__donnees) + "\n")
    print("- utilisateurs : " + str(list(__donnees.keys())) + "\n")
    print("- utilisateur actuel : " + __utilisateur_actuel + "\n")
    print("- donnée utilisateur actuel : " + str(__donnees[__utilisateur_actuel]) + "\n")
    __clear(input("Appuyer sur Entrée pour continuer."))

def __enregistrer_database():
    __donnee_global_database["data"] = __donnees
    if __version_chiffrement == 1:
        open(__chemin_fichier, 'w', encoding='utf-8').write(__Chiffrer(1).Chiffrer_chaine_caracteres(__generer_caracteres_aleatoire(100)+str(__donnee_global_database)))
    elif __version_chiffrement == 2:
        open(__chemin_fichier, 'w', encoding='utf-8').write(__Chiffrer(2).Chiffrer_chaine_caracteres(str(__donnee_global_database), __hash_mdp))

def __generer_caracteres_aleatoire(nombre):
    __caracteres = '0123456789abcdef'
    __caracteres_aleatoires = ""
    for _ in range(nombre):
        __caracteres_aleatoires += __caracteres[random.randint(0, len(__caracteres)-1)]
    return __caracteres_aleatoires

def __ajouter_utilisateur():
    while 1:
        __clear()
        __nom = input("Veuillez entrez un nom/pseudo valide pour le nouvel utilisateur (Entrée avec aucune valeur pour quitter): ")
        __hash_mot_de_passe = hashlib.sha256(input("Veuillez entrez le mot de passe du nouvel utilisateur : ").encode('utf-8')).hexdigest()
        if __nom in __donnees.keys():
            print("L'utilisateur "+__nom+" existe déjà.")
        elif __nom == '':
            break
        else:
            __donnees[__nom] = {"___password___": __hash_mot_de_passe}
            print("L'utilisateur a bien été ajouté.")
            break
    __clear(input("Appuyer sur Entrée pour continuer."))

def __connecter_utilisateur():
    global __utilisateur_actuel
    __clear()
    __nom = input("Veuillez sasir un nom d'utilisateur valide : ")
    if __nom not in __donnees.keys():
        print("Cet utilisateur n'existe pas.")
    elif __nom == 'default':
        __utilisateur_actuel = 'default'
    else:
        __hash_mot_de_passe = hashlib.sha256(input("Veuillez entrez le mot de passe de l'utilisateur : ").encode('utf-8')).hexdigest()
        if __hash_mot_de_passe != __donnees[__nom]['___password___']:
            print("Vous avez saisie un mauvais mot de passe.")
        else:
            __utilisateur_actuel = __nom
            print("Vous avez été connecter avec succès.")
    __clear(input("Appuyer sur Entrée pour continuer."))

def __changer_mot_de_passe_utilisateur():
    __clear()
    if __utilisateur_actuel == 'default':
        print("Vous ne pouvez pas changer le mot de passe du compte 'default'.")
    else:
        __hash_nouveau_mdp = hashlib.sha256(input("Veuillez entrez le nouveau mot de passe : ").encode('utf-8')).hexdigest()
        __donnees[__utilisateur_actuel]['___password___'] = __hash_nouveau_mdp
        print("Le nouveau mot de passe a été enregistrer.")
    __clear(input("Appuyer sur Entrée pour continuer."))

def __ajouter_nouveau_compte():
    __clear()
    __nom = input("Entrez le nom du compte a ajouté : ")
    if __nom in __comptes_interdit:
        print("Ce nom de compte est interdit.")
    elif __nom in __donnees[__utilisateur_actuel].keys():
        print("Le compte existe déjà.")
    else:
        __login = input("Entrez le pseudo du compte : ")
        __mdp = input("Entrez le mot de passe du compte : ")
        __donnees[__utilisateur_actuel][__nom] = {"login": __login, "password": __mdp}
        print("Compte ajouté avec succès.")
    __clear(input("Appuyer sur Entrée pour continuer."))

def __modifier_compte():
    __clear()
    __nom = input("Entrez le nom du compte a modifier : ")
    if __nom not in __donnees[__utilisateur_actuel].keys():
        print("Veuillez saisir un nom de compte valide.")
        __clear(input("Appuyer sur Entrée pour continuer."))
        return
    elif __nom in __comptes_interdit:
        print("Vous ne pouvez pas modifier ce compte.")
        __clear(input("Appuyer sur Entrée pour continuer."))
        return
    while 1:
        print("Veuillez choisir ce que vous voulez faire :")
        print("1) Changer pseudo.")
        print("2) Changer mot de passe.")
        print("3) Changer pseudo et mot de passe.")
        print("4) Quitter.")
        try:
            __reponse = int(input())
            if __reponse not in (1, 2, 3, 4):
                print("Veuillez entrez un nombre valide.")
            elif __reponse == 1:
                __donnees[__utilisateur_actuel][__nom]["login"] = input("Veuillez entrez le nouveau pseudo : ")
            elif __reponse == 2:
                __donnees[__utilisateur_actuel][__nom]["password"] = input("Veuillez entrez le nouveau mot de passe : ")
            elif __reponse == 3:
                __donnees[__utilisateur_actuel][__nom]["login"] = input("Veuillez entrez le nouveau pseudo : ")
                __donnees[__utilisateur_actuel][__nom]["password"] = input("Veuillez entrez le nouveau mot de passe : ")
            elif __reponse == 4:
                break
        except ValueError:
            print("Veuillez entrez un nombre valide.")
    __clear(input("Appuyer sur Entrée pour continuer."))

def __supprimer_compte():
    __clear()
    __nom = input("Veuillez entrez le nom du compte à supprimer : ")
    if __nom not in __donnees[__utilisateur_actuel].keys():
        print("Il n'existe aucun compte au nom de '"+__nom+"' pour l'utilisateur actuel.")
    elif __nom in __comptes_interdit:
        print("Vous ne pouvez pas supprimer ce compte.")
    else:
        __donnees[__utilisateur_actuel].pop(__nom)
    __clear(input("Appuyer sur Entrée pour continuer."))

def __recuperer_login_compte():
    __clear()
    __nom = input("Sasir nom du compte : ")
    if __nom not in __donnees[__utilisateur_actuel].keys():
        print("Il n'existe aucun compte au nom de '" + __nom + "' pour l'utilisateur actuel.")
    else:
        print("Pseudo/login : " + __donnees[__utilisateur_actuel][__nom]["login"])
        print("Mot de passe : " + __donnees[__utilisateur_actuel][__nom]["password"])
    __clear(input("Appuyer sur Entrée pour continuer."))

def __modifier_mdp_maitre():
    if __utilisateur_actuel != 'default':
        __hash_mdp_utilisateur = hashlib.sha256(input("Veuillez entrez le mot de passe de l'utilisateur connecter : ").encode('utf-8')).hexdigest()
        if __hash_mdp_utilisateur != __donnees[__utilisateur_actuel]["___password___"]:
            print("Vous avez entrez le mauvais mot de passe.")
            __clear(input("Appuyer sur Entrée pour continuer."))
            return
    __hash_nouveau_mdp = hashlib.sha512(input("Veuillez entrez le nouveau mot de passe maitre : ").encode('utf-8')).hexdigest()
    __donnee_global_database["password"] = __hash_nouveau_mdp
    print("Le mot de passe maitre a bien été changé.")
    __clear(input("Appuyer sur Entrée pour continuer."))

def __supprimer_utilisateur():
    global __utilisateur_actuel
    __clear()
    __nom = input("Veuillez sasir un nom d'utilisateur valide a supprimer : ")
    if __nom not in __donnees.keys():
        print("Cet utilisateur n'existe pas.")
    elif __nom == 'default':
        print("Vous ne pouvez pas supprimer l'utilisateur 'default'.")
    else:
        __hash_mot_de_passe = hashlib.sha256(input("Veuillez entrée le mot de passe de l'utilisateur '"+__nom+"' : ").encode('utf-8')).hexdigest()
        if __hash_mot_de_passe != __donnees[__nom]["___password___"]:
            print("Vous avez entrez le mauvais mot de passe.")
        else:
            __donnees.pop(__nom)
            print("L'utilisateur '"+__nom+"' a été supprimer.")
            if __nom == __utilisateur_actuel:
                __utilisateur_actuel = 'default'
                print("Vous avez supprimer l'utilisateur actuellement connecter et donc vous avez connecter sur l'utilisateur 'default'.")
    __clear(input("Appuyer sur Entrée pour continuer."))

def __modifier_utilisateur():
    __clear()
    __nom = input("Veuillez sasir un nom d'utilisateur valide a modifier : ")
    if __nom not in __donnees.keys():
        print("Cet utilisateur n'existe pas.")
    elif __nom == 'default':
        print("Vous ne pouvez pas modifier l'utilisateur 'default'.")
    else:
        while 1:
            try:
                print("Que voulez-vous modifier ?")
                __choix_modifier = int(input("1) Modifiez nom d'utilisateur.\n2) Modifiez mot de passe.\n"))
                if __choix_modifier not in [1, 2]:
                    print("La valeur saisie n'est pas valide.")
                elif __choix_modifier == 1:
                    __modifier_nom_utilisateur(__nom)
                    break
                elif __choix_modifier == 2:
                    __modifier_mdp_utilisateur(__nom)
                    break
            except ValueError:
                print("La valeur saisie n'est pas valide.")
    __clear(input("Appuyer sur Entrée pour continuer."))

def __modifier_nom_utilisateur(__nom :str):
    while 1:
        __hash_mot_de_passse =  hashlib.sha256(input("Entrez mot de passe de l'utilisateur (Apuyer sur Entrée sans valeur pour annuler): ").encode('utf-8')).hexdigest()
        if __hash_mot_de_passse == '':
            break
        elif __hash_mot_de_passse != __donnees[__nom]["___password___"]:
            print("Mauvais mot de passe.")
        else:
            break
    while 1:
        __nouveau_nom = input("Entrez nouveau nom d'utilisateur : ")
        if __nouveau_nom in __donnees.keys():
            print("L'utilisateur '"+__nouveau_nom+"' existe déjà.")
        else:
            __donnees[__nouveau_nom] = __donnees[__nom]
            __donnees.pop(__nom)
            print("Le nom de l'utilisateur a bien été changé en '"+__nouveau_nom+"'.")
            break

def __modifier_mdp_utilisateur(__nom: str):
    while 1:
        __hash_mot_de_passse = hashlib.sha256(input("Entrez mot de passe actuel de l'utilisateur (Apuyer sur Entrée sans valeur pour annuler): ").encode('utf-8')).hexdigest()
        if __hash_mot_de_passse == '':
            break
        elif __hash_mot_de_passse != __donnees[__nom]["___password___"]:
            print("Mauvais mot de passe.")
        else:
            __nouveau_mdp = hashlib.sha256(input("Entrez nouveau mot de passe : ").encode('utf-8')).hexdigest()
            __donnees[__nom]["___password___"] = __nouveau_mdp
            print("Le mot de passe de l'utilisateur '"+__nom+"' a bien été changé.")
            break

import random
import ast
import hashlib
import getpass
import os
__chemin_fichier_par_default = "KMPS_database.db"
__comptes_interdit = ["___password___"]
__utilisateur_actuel = 'default'
__version_chiffrement = 2
__hash_mdp = ''
while 1 :
    print("Entrez le nom/chemin du fichier de la base de donnée ou appuyer sur Entrée pour utiliser le nom/chemin par défault ("+__chemin_fichier_par_default+"). Tapez 'nouvelle' pour créer une nouvelle table.")
    __chemin_fichier = input()
    if __chemin_fichier.lower() == 'nouvelle':
        __nouveau_chemin_bdd = input("Veuillez entrez le chemin/nom du fichier de la nouvelle base de donnée : ")
        while os.path.exists(__nouveau_chemin_bdd):
            print("Erreur : Le chemin existe déjà.")
            __nouveau_chemin_bdd = input("Veuillez entrez le chemin de la nouvelle base de donnée : ")
        __chemin_fichier = __nouveau_chemin_bdd
        print("Veuillez entrez un mot de passe maitre (sert a dévérouillez la base de données) :")
        __hash_nouveau_mdp_maitre = hashlib.sha512(getpass.getpass('', None).encode('utf-8')).hexdigest()
        __hash_mdp = __hash_nouveau_mdp_maitre
        __format_nouvelle_bdd = {'password': __hash_nouveau_mdp_maitre, 'data': {'default': {'___password___': None}}}
        while 1:
            print("Quel version de chiffrement est a utilisé ? (Versions : 1 et 2) (2 par défault car plus sécuriser et plus rapide) :")
            __version_chiffrement_nouvelle_bdd = int(input())
            if __version_chiffrement_nouvelle_bdd == 1:
                open(__nouveau_chemin_bdd, 'w', encoding='utf-8').write(__Chiffrer(1).Chiffrer_chaine_caracteres(__generer_caracteres_aleatoire(100) + str(__format_nouvelle_bdd)))
                break
            elif __version_chiffrement_nouvelle_bdd == 2:
                open(__nouveau_chemin_bdd, 'w', encoding='utf-8').write(__Chiffrer(2).Chiffrer_chaine_caracteres(str(__format_nouvelle_bdd), __hash_nouveau_mdp_maitre))
                break
            else:
                print("Veuillez choisir entre version 1 ou 2.")
        __version_chiffrement = __version_chiffrement_nouvelle_bdd
        print("La base de donnée a bie été crée. Appuyer sur Entrée pour vous connectez.")
        input()
    elif __chemin_fichier == '':
        __chemin_fichier = __chemin_fichier_par_default
    try:
        __donnee_global_database = open(__chemin_fichier, 'r', encoding='utf-8').read()
        __version_chiffrement = int(input("Veuillez entrez la version du chiffrement de la base de données (Versions : 1 ou 2 mais 2 par défault car plus sécuriser et plus rapide: "))
        while __version_chiffrement not in(1, 2):
            print("Veuillez choisir entre version 1 ou 2.")
            __version_chiffrement = int(input("Veuillez entrez la version du chiffrement de la base de données (Versions : 1 ou 2 mais 2 par défault car plus sécuriser et plus rapide: "))
        if len(__donnee_global_database) > 100:
            if __version_chiffrement == 1:
                __donnee_global_database = ast.literal_eval(__Dechiffrer(1).Dechiffrer_chaine_caracteres(__donnee_global_database[100:]))
                __donnees = __donnee_global_database['data']
                while __hash_mdp != __donnee_global_database['password']:
                    print("Veuillez saisir votre mot de passe maitre :")
                    __hash_mdp = hashlib.sha512(getpass.getpass('', None).encode('utf-8')).hexdigest()
                    if __hash_mdp != __donnee_global_database['password']:
                        print("Mauvais mot de passe.")
            elif __version_chiffrement == 2:
                while 1:
                    print("Veuillez saisir votre mot de passe maitre :")
                    __hash_mdp = hashlib.sha512(getpass.getpass('', None).encode('utf-8')).hexdigest()
                    try:
                        __donnee_global_database = ast.literal_eval(__Dechiffrer(2).Dechiffrer_chaine_caracteres(__donnee_global_database, __hash_mdp))
                        __donnees = __donnee_global_database['data']
                        break
                    except ValueError:
                        print("Mauvais mot de passe ou fichier corompu ou vous avez sélectionnez la mauvaise version de chiffrement.")
                    except SyntaxError:
                        print("Mauvais mot de passe ou fichier corompu ou vous avez sélectionnez la mauvaise version de chiffrement.")
            break
        else:
            print("Le fichier " + __chemin_fichier + " n'est pas un fichier de base de donnée valide.")
    except FileExistsError:
        print("Le fichier " + __chemin_fichier + " n'existe pas ou n'a pas été trouvé.")
    except FileNotFoundError:
        print("Le fichier " + __chemin_fichier + " n'existe pas ou n'a pas été trouvé.")
__clear()
while 1:
    print("Vous êtes connecter en tant que l'utilisateur '" + __utilisateur_actuel + "'.")
    print("Que voulez-vous faire ? (choisir le numéro voulu)")
    # print("-1) Afficher tout.")
    print("1) Modifier mot de passe maitre.")
    print("2) Se connecter à un autre utilisateur.")
    print("3) Changer le mot de passe de l'utilisateur actuel.")
    print("4) Ajouter un nouveau compte.")
    print("5) Modifier un compte.")
    print("6) Supprimer un compte.")
    print("7) Récupérer le login et le mot de passe d'un compte.")
    print("8) Ajouter un nouvel utilisateur.")
    print("9) Supprimer un utilisateur.")
    print("10) Modifier un utilisateur.")
    print("11) Quitter")
    try:
        __choix = int(input())
        """if __choix == -1:
            __afficher_tout()"""
        if __choix not in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11):
            print("Mauvais choix veuillez sasir un des nombres.")
            __clear(input("Appuyer sur Entrée pour continuer."))
        elif __choix == 1:
            __modifier_mdp_maitre()
        elif __choix == 2:
            __connecter_utilisateur()
        elif __choix == 3:
            __changer_mot_de_passe_utilisateur()
        elif __choix == 4:
            __ajouter_nouveau_compte()
        elif __choix == 5:
            __modifier_compte()
        elif __choix == 6:
            __supprimer_compte()
        elif __choix == 7:
            __recuperer_login_compte()
        elif __choix == 8:
            __ajouter_utilisateur()
        elif __choix == 9:
            __supprimer_utilisateur()
        elif __choix == 10:
            __modifier_utilisateur()
        elif __choix == 11:
            __enregistrer_database()
            print("Sortie du programme ...")
            break
    except ValueError:
        print("Mauvais choix veuillez sasir un des nombres.")
        __clear(input("Appuyer sur Entrée pour continuer."))
