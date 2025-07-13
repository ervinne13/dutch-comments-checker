FROM ollama/ollama:latest

RUN apt-get update && apt-get install -y curl

COPY shell/ollama_entrypoint.sh /ollama_entrypoint.sh
RUN chmod +x /ollama_entrypoint.sh

ENTRYPOINT ["/bin/bash", "/ollama_entrypoint.sh"]