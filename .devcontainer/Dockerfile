# Simple devcontainer based on the official Python development image
FROM mcr.microsoft.com/devcontainers/python:0-3.11

# Avoid running as root in interactive sessions
ARG VARIANT="3.11"
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
  && apt-get install -y --no-install-recommends git curl build-essential \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

COPY --chown=vscode:vscode . /workspace
WORKDIR /workspace

USER vscode
