FROM mcr.microsoft.com/vscode/devcontainers/javascript-node:0-14-bullseye

RUN apt update

# for node-gyp (needed for sass compiler)
RUN apt install python -y 

# for webp generation
RUN apt install imagemagick -y
