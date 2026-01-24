# Déploiement { #deployment }

Le déploiement d'une application **FastAPI** est relativement simple.

## Que signifie le déploiement { #what-does-deployment-mean }

**Déployer** une application signifie effectuer les étapes nécessaires pour la rendre **disponible pour les utilisateurs**.

Pour une **API Web**, cela implique normalement de la placer sur une **machine distante**, avec un **programme serveur** qui offre de bonnes performances, une bonne stabilité, etc, afin que vos **utilisateurs** puissent **accéder** à l'application efficacement et sans interruption ni problème.

Ceci contraste avec les étapes de **développement**, où vous êtes constamment en train de modifier le code, de le casser et de le réparer, d'arrêter et de redémarrer le serveur de développement, etc.

## Stratégies de déploiement { #deployment-strategies }

Il existe plusieurs façons de procéder, en fonction de votre cas d'utilisation spécifique et des outils que vous utilisez.

Vous pouvez **déployer un serveur** vous-même en utilisant une combinaison d'outils, vous pouvez utiliser un **service cloud** qui fait une partie du travail pour vous, ou encore d'autres options possibles.

Par exemple, nous, l'équipe derrière FastAPI, avons créé <a href="https://fastapicloud.com" class="external-link" target="_blank">**FastAPI Cloud**</a>, afin de rendre le déploiement d'apps FastAPI sur le cloud aussi rationalisé que possible, avec la même expérience développeur que celle du travail avec FastAPI.

Je vais vous montrer certains des principaux concepts que vous devriez probablement avoir à l'esprit lors du déploiement d'une application **FastAPI** (bien que la plupart de ces concepts s'appliquent à tout autre type d'application web).

Vous verrez plus de détails à avoir en tête et certaines des techniques pour le faire dans les sections suivantes. ✨
