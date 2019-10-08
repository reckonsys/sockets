FROM node:10.16.3-alpine

WORKDIR /code

COPY package*.json /code/
RUN apk --update add --virtual build-dependencies build-base python \
    && npm install \
    && apk del build-dependencies

COPY . /code/

EXPOSE 8008

CMD ["node", "index.js"]
