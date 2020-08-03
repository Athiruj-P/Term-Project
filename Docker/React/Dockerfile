FROM node:12.18.3

WORKDIR /usr/src/app

# Install app dependencies
# A wildcard is used to ensure both package.json AND package-lock.json are copied
COPY package*.json ./

RUN npm install
# Create app directory
COPY . .

EXPOSE 8080

CMD [ "npm", "start" ]