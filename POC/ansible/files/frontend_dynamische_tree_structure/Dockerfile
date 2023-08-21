FROM node:20-alpine

WORKDIR /app
EXPOSE 5000

COPY . .

RUN npm install
RUN npm run build

CMD ["npm", "start"]
