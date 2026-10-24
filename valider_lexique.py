import re
import polib

def analyser_glossaire_pulaar(fichier_po):
    try:
        # Charger le fichier de traduction (.po)
        po = polib.pofile(fichier_po)
    except Exception as e:
        print(f"❌ Erreur lors du chargement du fichier : {e}")
        return

    mots_emprunts_detectes = 0
    total_traduit = 0
    
    # Base de données des classes nominales pulaar corrigée selon vos critères
    classes_nominales = {
        'o / oo': [],   # Personnes, rôles, fonctions (ex: neɗɗo oo, piyoowo, deenoowo)
        'ngo / ngoo': [], # Objets, actions (ex: duulo ngoo)
        'ngal': [],     # Classe ngal : -ngal, -gal
        'ka': [],       # Classe ka : -ka, -haa
        'ɗam': [],      # Classe ɗam : -ɗam, -dam
        'ɗi': [],       # Pluriels non-humains : -ɗi, -li
        'ɗe': [],       # Pluriels non-humains : -ɗe, -je
        'ko': [],       # Classe ko : -ko, -ho
        'ki': [],       # Classe ki : -ki, -hi
        'nde': [],      # Classe nde : -nde, -re
        'ndu': [],      # Classe ndu : -ndu, -ru
        'Incertain': []
    }

    print("=" * 60)
    print(f"📊 ANALYSE DU GLOSSAIRE PULAAR : {fichier_po}")
    print("=" * 60)

    for entry in po:
        if not entry.msgstr or entry.msgstr.strip() == "":
            continue
        
        total_traduit += 1
        traduction_pulaar = entry.msgstr.strip().lower()
        terme_anglais = entry.msgid.strip().lower()
        
        # Récupération du contexte français
        commentaire_fr = ""
        if entry.comment:
            match = re.search(r"french:\s*(.*)", entry.comment, re.IGNORECASE)
            if match:
                commentaire_fr = match.group(1).strip().lower()

        # 1. VÉRIFICATION DES EMPRUNTS ACCIDENTELS
        mots_anglais = set(re.findall(r'\b\w+\b', terme_anglais))
        mots_francais = set(re.findall(r'\b\w+\b', commentaire_fr)) if commentaire_fr else set()
        mots_pulaar = set(re.findall(r'\b\w+\b', traduction_pulaar))

        emprunts = (mots_pulaar.intersection(mots_anglais) | mots_pulaar.intersection(mots_francais))
        emprunts_filtres = {m for m in emprunts if len(m) > 2}

        if emprunts_filtres:
            mots_emprunts_detectes += 1
            print(f"⚠️ Alerte Emprunt sur ID '{entry.msgid}':")
            print(f"   - Pulaar: '{entry.msgstr}'")
            print(f"   - Mots suspects détectés: {list(emprunts_filtres)}")
            print("-" * 40)

        # 2. CLASSIFICATION GRAMMATICALE AVANCÉE
        dernier_mot = traduction_pulaar.split()[-1] if traduction_pulaar.split() else ""
        classe_trouvee = False
        
        # RÈGLE 1 : Classe Humaine (o / oo) -> Rôles, Fonctions, Suffixes d'agent
        # Capture les mots se terminant par oo, o (si c'est un article ou suffixe humain isolé), oowo, eejo, erjo
        if re.search(r'\b(oo|o)$', dernier_mot) or re.search(r'(oowo|eejo|erjo)$', dernier_mot):
            # Double vérification pour éviter que 'ngoo' ou 'go' soit capturé ici par erreur
            if not re.search(r'(ngoo|ngo|go)$', dernier_mot):
                classes_nominales['o / oo'].append(entry.msgstr)
                classe_trouvee = True
            
        # RÈGLE 2 : Classe des Objets & Actions (ngo / ngoo)
        if not classe_trouvee and re.search(r'(ngoo|ngo|go)$', dernier_mot):
            classes_nominales['ngo / ngoo'].append(entry.msgstr)
            classe_trouvee = True
            
        # RÈGLE 3 : Autres classes morphologiques standards
        if not classe_trouvee:
            règles_suffixes = {
                'ngal': r'(ngal|gal)$',
                'ka': r'(kaa|ka|ha)$',
                'ɗam': r'(ɗam|dam)$',
                'ɗi': r'(ɗi|li|di)$',
                'ɗe': r'(ɗe|je|de)$',
                'ko': r'(ko|ho)$',
                'ki': r'(ki|hi)$',
                'nde': r'(nde|re|de)$',
                'ndu': r'(ndu|ru|du)$'
            }
            
            for cl, pattern in règles_suffixes.items():
                if re.search(pattern, dernier_mot):
                    classes_nominales[cl].append(entry.msgstr)
                    classe_trouvee = True
                    break
                    
        if not classe_trouvee:
            classes_nominales['Incertain'].append(entry.msgstr)

    # AFFICHAGE DU RAPPORT FINAL
    print("\n" + "=" * 60)
    print("📈 RAPPORT DE CONFORMITÉ LINGUISTIQUE")
    print("=" * 60)
    print(f"✅ Total de termes traduits analysés : {total_traduit}")
    print(f"🚨 Total d'alertes " + ("ZÉRO ! Parfait." if mots_emprunts_detectes == 0 else f": {mots_emprunts_detectes} entrées à corriger."))
    
    print("\n📦 RÉPARTITION PAR CLASSES NOMINALES (PULAAR) :")
    for cl, termes in classes_nominales.items():
        if termes:
            print(f"  • {cl.upper()} ({len(termes)} termes) : {', '.join(termes[:5])}" + ("..." if len(termes) > 5 else ""))

if __name__ == "__main__":
    analyser_glossaire_pulaar("locales/ff/football_glossary.po")
