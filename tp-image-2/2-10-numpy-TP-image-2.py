# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all,-hidden,-heading_collapsed,-run_control,-trusted
#     cell_metadata_json: true
#     notebook_metadata_filter: all, -jupytext.text_representation.jupytext_version,
#       -jupytext.text_representation.format_version, -language_info.version, -language_info.codemirror_mode.version,
#       -language_info.codemirror_mode, -language_info.file_extension, -language_info.mimetype,
#       -toc
#     text_representation:
#       extension: .py
#       format_name: percent
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
#   language_info:
#     name: python
#     nbconvert_exporter: python
#     pygments_lexer: ipython3
#   nbhosting:
#     title: suite du TP simple avec des images
# ---

# %% [markdown]
# Licence CC BY-NC-ND, Valérie Roy & Thierry Parmentelat

# %%
from IPython.display import HTML
HTML(url="https://raw.githubusercontent.com/ue12-p22/python-numerique/main/notebooks/_static/style.html")



# %% [markdown]
# # suite du TP simple avec des images
#
# merci à Wikipedia et à stackoverflow
#
# **le but de ce TP n'est pas d'apprendre le traitement d'image  
# on se sert d'images pour égayer des exercices avec `numpy`  
# (et parce que quand on se trompe ça se voit)**

# %%
import numpy as np
from matplotlib import pyplot as plt

# %% [markdown] {"tags": ["framed_cell"]}
# **notions intervenant dans ce TP**
#
# sur les tableaux `numpy.ndarray`
#
# * `reshape()`, tests, masques booléens, *ufunc*, agrégation, opérations linéaires sur les `numpy.ndarray`
# * les autres notions utilisées sont rappelées (très succinctement)
#
# pour la lecture, l'écriture et l'affichage d'images
#
# * utilisez `plt.imread`, `plt.imshow`
# * utilisez `plt.show()` entre deux `plt.imshow()` dans la même cellule
#
# **note**
#
# * nous utilisons les fonctions de base sur les images de `pyplot` par souci de simplicité
# * nous ne signifions pas là du tout que ce sont les meilleures  
# par exemple `matplotlib.pyplot.imsave` ne vous permet pas de donner la qualité de la compression  
# alors que la fonction `save` de `PIL` le permet
#
# * vous êtes libres d'utiliser une autre librairie comme `opencv`  
#   si vous la connaissez assez pour vous débrouiller (et l'installer), les images ne sont qu'un prétexte
#
# **n'oubliez pas d'utiliser le help en cas de problème.**

# %% [markdown]
# ## Création d'un patchwork

# %% [markdown]
# 1. Le fichier `rgb-codes.txt` contient une table de couleurs:
# ```
# AliceBlue 240 248 255
# AntiqueWhite 250 235 215
# Aqua 0 255 255
# .../...
# YellowGreen 154 205 50
# ```
# Le nom de la couleur est suivi des 3 valeurs de ses codes `R`, `G` et `B`  
# Lisez cette table en `Python` et rangez-la dans la structure qui vous semble adéquate.
# <br>
#
# 1. Affichez, à partir de votre structure, les valeurs rgb entières des couleurs suivantes  
# `'Red'`, `'Lime'`, `'Blue'`
# <br>
#
# 1. Faites une fonction `patchwork` qui  
#
#    * prend une liste de couleurs et la structure donnant le code des couleurs RGB
#    * et retourne un tableau `numpy` avec un patchwork de ces couleurs  
#    * (pas trop petits les patchs - on doit voir clairement les taches de couleurs  
#    si besoin de compléter l'image mettez du blanc  
#    (`numpy.indices` peut être utilisé)
# <br>
# <br>   
# 1. Tirez aléatoirement une liste de couleurs et appliquez votre fonction à ces couleurs.
# <br>
#
# 1. Sélectionnez toutes les couleurs à base de blanc et affichez leur patchwork  
# même chose pour des jaunes  
# <br>
#
# 1. Appliquez la fonction à toutes les couleurs du fichier  
# et sauver ce patchwork dans le fichier `patchwork.jpg` avec `plt.imsave`
# <br>
#
# 1. Relisez et affichez votre fichier  
#    attention si votre image vous semble floue c'est juste que l'affichage grossit vos pixels
#    
# vous devriez obtenir quelque chose comme ceci
# <img src="patchwork-all.jpg" width="200px">

# %%
# votre code

colors = {}
with open("rgb-codes.txt") as file:
    for line in file:
        colorName, *rgb = line.split()
        colors[colorName] = list(map(int,rgb))
print(colors['Red'])
print(colors['Lime'])
print(colors['Blue'])


# %%
def patchwork(patchColors, globalColors):
    #Make a square fitted to show them all:
    nbColors = len(patchColors)
    h = int(np.sqrt(nbColors))
    if h**2 != nbColors:
        h += 1
    patchColors += ['White']*(h**2-nbColors) #we fill the rest of the square with wite
    
    patchColors = list(map(globalColors.get,patchColors))
    patch = np.array(patchColors, dtype=np.uint8)
    np.random.shuffle(patch)
    return patch.reshape((h,h,3))

res = patchwork('Red Lime Blue Brown DarkGray Beige'.split(),colors)
#plt.imshow(res);

#Select random colors without repetition:
availableColors = list(colors.keys())
size = len(availableColors)
selection = []
for i in range(50):
    colorIndex = np.random.randint(0,size)
    selection.append(availableColors[colorIndex])
    availableColors[colorIndex] = availableColors[-1]
    size -= 1

res = patchwork(selection,colors)
plt.axis('off') #thanks stackoverflow
plt.imshow(res);


# %%
#Selectionner les couleurs à base de blanc et de jaune
#je comprend pas ce que ça veut dire
def findColors(colorName):
    selection = []
    availableColors = list(colors.keys())
    for color in availableColors:
        if color.startswith(colorName):
            selection.append(color)
    return selection

plt.imshow(patchwork(findColors("Yellow"),colors));
plt.show()
plt.imshow(patchwork(findColors("White"),colors));

res = patchwork(list(colors.keys()),colors)
plt.imsave('patchwork.jpg', res)

# %%
img = plt.imread('patchwork.jpg')
plt.imshow(img);

# %% [markdown]
# ## Somme des valeurs RGB d'une image

# %% [markdown]
# 0. Lisez l'image `les-mines.jpg`
#
# 1. Créez un nouveau tableau `numpy.ndarray` en sommant **avec l'opérateur `+`** les valeurs RGB des pixels de votre image  
#
# 2. Affichez l'image (pas terrible), son maximum et son type
#
# 3. Créez un nouveau tableau `numpy.ndarray` en sommant **avec la fonction d'agrégation `np.sum`** les valeurs RGB des pixels de votre image
#
# 4. Affichez l'image, son maximum et son type
#
# 5. Pourquoi cette différence ? Utilisez le help `np.sum?`
#
# 6. Passez l'image en niveaux de gris de type entiers non-signés 8 bits  
# (de la manière que vous préférez)
#
# 7. Remplacez dans l'image en niveaux de gris,   
# les valeurs >= à 127 par 255 et celles inférieures par 0  
# Affichez l'image avec une carte des couleurs des niveaux de gris  
# vous pouvez utilisez la fonction `numpy.where`
#
# 8. avec la fonction `numpy.unique`  
# regardez les valeurs différentes que vous avez dans votre image en noir et blanc

# %%
# votre code
img = plt.imread('les-mines.jpg')

#img1 = np.ndarray(img.shape,dtype=np.uint8)
img1 = img[:,:,0] + img[:,:,1] + img[:,:,2]
plt.imshow(img1);
plt.show()
print(img1.max(), img1.dtype)

img2 = np.sum(img, axis=2)
plt.imshow(img2);
print(img2.max(), img2.dtype)
#Summing with + keeps the datatype of the original data which results in an overflow,
#np.sum uses by default the default integer type of the machine which is in general, as well as in my case, a uint32


# %%
img3 = img2.astype(np.uint8)
img3[img3 >= 127] = 255
img3[img3 < 127] = 0
plt.imshow(img3, cmap='Greys');
np.unique(img3)


# %% [markdown]
# ## Image en sépia

# %% [markdown]
# Pour passer en sépia les valeurs R, G et B d'un pixel  
# (encodées ici sur un entier non-signé 8 bits)  
#
# 1. on transforme les valeurs $R$, $G$ et $B$ par la transformation  
# $0.393\, R + 0.769\, G + 0.189\, B$  
# $0.349\, R + 0.686\, G + 0.168\, B$  
# $0.272\, R + 0.534\, G + 0.131\, B$  
# (attention les calculs doivent se faire en flottants pas en uint8  
# pour ne pas avoir, par exemple, 256 devenant 0)  
# 1. puis on seuille les valeurs qui sont plus grandes que `255` à `255`
# 1. naturellement l'image doit être ensuite remise dans un format correct  
# (uint8 ou float entre 0 et 1)

# %% [markdown]
# **Exercice**
#
# 1. Faites une fonction qui prend en argument une image RGB et rend une image RGB sépia  
# la fonction `numpy.dot` doit être utilisée (si besoin, voir l'exemple ci-dessous) 
#
# 1. Passez votre patchwork de couleurs en sépia  
# Lisez le fichier `patchwork-all.jpg` si vous n'avez pas de fichier perso
# 2. Passez l'image `les-mines.jpg` en sépia   

# %%
# votre code
def sepia(img):
    coeffs = np.array([[0.393, 0.769, 0.189],[0.349, 0.686, 0.168],[0.272, 0.534, 0.131]])
    res = img.astype(float).dot(coeffs.T)
    res /= res.max()
    return res

res = sepia(img)
plt.imshow(res);
plt.show();
plt.imshow(sepia(plt.imread('patchwork.jpg')));

# %% {"scrolled": true}
# INDICE:

# exemple de produit de matrices avec `numpy.dot`
# le help(np.dot) dit: dot(A, B)[i,j,k,m] = sum(A[i,j,:] * B[k,:,m])

i, j, k, m, n = 2, 3, 4, 5, 6
A = np.arange(i*j*k).reshape(i, j, k)
B = np.arange(m*k*n).reshape(m, k, n)

C = A.dot(B)
# or C = np.dot(A, B)

A.shape, B.shape, C.shape

# %% [markdown]
# ## Exemple de qualité de compression

# %% [markdown]
# 1. Importez la librairie `Image`de `PIL` (pillow)   
# (vous devez peut être installer PIL dans votre environnement)
# 1. Quelle est la taille du fichier 'les-mines.jpg' sur disque ?
# 1. Lisez le fichier 'les-mines.jpg' avec `Image.open` et avec `plt.imread`  
#
# 3. Vérifiez que les valeurs contenues dans les deux objets sont proches
#
# 4. Sauvez (toujours avec de nouveaux noms de fichiers)  
# l'image lue par `imread` avec `plt.imsave`  
# l'image lue par `Image.open` avec `save` et une `quality=100`  
# (`save` s'applique à l'objet créé par `Image.open`)
#
# 5. Quelles sont les tailles de ces deux fichiers sur votre disque ?  
# Que constatez-vous ?
#
# 6. Relisez les deux fichiers créés et affichez avec `plt.imshow` leur différence  

# %%
# votre code
from PIL import Image
#les-mines.jpg: 726 ko
img1 = Image.open("les-mines.jpg")
img2 = plt.imread("les-mines.jpg")
plt.imsave('pltSave.jpg',img2) #134 ko
img1.save('pilSave.jpg', quality=100) #560 ko
plt.imshow(plt.imread('pltSave.jpg'));
plt.show()
plt.imshow(plt.imread('pilSave.jpg'));
#there is no detectable difference at least with my screen

# %%
