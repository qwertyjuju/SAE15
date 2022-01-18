import os

def read_file(path):
    """
    Lecture d'un fichier.

    :param path: le chemin du fichier
    :return: liste des lignes du fichier
    """

    try:
        with open(path, encoding="utf8") as f:
            return f.read().splitlines()
    except:
        print("Le fichier n'existe pas %s", os.path.abspath(path))
        return None
i=0   
res=read_file("fichier_a_traiter.txt")
for line in res:
    if line.startswith("11:42"):
        i+=1
print(i)