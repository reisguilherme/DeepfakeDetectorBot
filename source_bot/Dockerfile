# Use the official Node.js image as the base image
FROM node:22

# Install dependencies 
RUN apt-get update \
    && apt-get install -y libnss3 libdbus-1-3 libatk1.0-0 libatk-bridge2.0-0 \
    && apt-get install -y libcups2 libdrm2 libxkbcommon0 libxcomposite1 libxdamage1 \
    && apt-get install -y libxfixes3 libxrandr2 libgbm1 libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Create and set the working directory
WORKDIR /app

# Copy the entire source_bot folder to the working directory
COPY source_bot/ .

# Install application dependencies
RUN npm install

# Install Chromium using puppeteer
RUN npx puppeteer browsers install chrome

# Expose the port the app runs on 
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
