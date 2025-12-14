# Używamy najnowszego Ubuntu
FROM ubuntu:latest

# Ustawiamy katalog roboczy
WORKDIR /app

# 1. Instalacja narzędzi, kompilatora C i Pythona
RUN apt-get update && apt-get install -y \
    build-essential \
    wget \
    python3 \
    python3-pip \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Instalacja NetworkX (wymuszamy instalację systemową - w Dockerze to bezpieczne)
RUN pip3 install networkx --break-system-packages

# 3. Pobranie i kompilacja Nauty (geng, genrang)
RUN wget http://users.cecs.anu.edu.au/~bdm/nauty/nauty27r3.tar.gz \
    && tar -xvzf nauty27r3.tar.gz \
    && cd nauty27r3 \
    && ./configure \
    && make \
    # Kopiujemy geng i genrang do folderu systemowego
    && cp geng genrang /usr/local/bin/ \
    && cd .. \
    && rm -rf nauty27r3 nauty27r3.tar.gz

# Domyślna komenda (bash)
CMD ["/bin/bash"]