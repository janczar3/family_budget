FROM node:16

WORKDIR /srv/app

COPY package*.json ./

RUN npm config delete registry
RUN npm config delete //registry.npmjs.org/:_authToken

RUN npm config set registry https://registry.npmjs.org/

RUN npm install

COPY . .

EXPOSE 3000

CMD ["npm", "start"]
