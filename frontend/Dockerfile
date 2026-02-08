FROM node:18-alpine

WORKDIR /app

# Copier package.json
COPY package*.json ./

# Installer les dépendances
RUN npm install

# Copier le code
COPY . .

# Exposer le port
EXPOSE 3000

# Commande par défaut
CMD ["npm", "start"]
