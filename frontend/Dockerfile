FROM node:18-alpine

# Устанавливаем рабочую директорию
WORKDIR /frontend

# Копируем package.json и package-lock.json для установки зависимостей
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем остальные файлы приложения
COPY . .

# Устанавливаем дополнительные пакеты
RUN npm install --save-dev typescript ts-node

# Устанавливаем права на выполнение для tsc
RUN chmod +x ./node_modules/.bin/tsc

# Открываем порт
EXPOSE 5173

# Запускаем приложение
CMD ["npm", "run", "dev"]