FROM node:14-alpine

FROM node:18-alpine

WORKDIR '/app'

COPY ../frontend .

RUN rm -rf node_modules package-lock.json

RUN npm install

RUN npm i typescript

RUN npm i typescript ts-node


RUN npm i #--save-dev @types/node

RUN chmod +x ./node_modules/.bin/tsc

EXPOSE 3000

CMD ["npm", "run", "dev"]