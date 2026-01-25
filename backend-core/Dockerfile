FROM node:20-alpine

WORKDIR /app

# Copia package.json e package-lock.json
COPY package*.json ./

# Instala dependências
RUN npm ci --only=production

# Copia código fonte
COPY . .

# Expõe porta
EXPOSE 3000

# Comando para iniciar
CMD ["npm", "start"]
