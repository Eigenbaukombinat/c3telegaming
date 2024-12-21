# Multi-stage Dockerfile for building and running Yate

# Stage 1: Build
FROM debian:bookworm as build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    autoconf \
    build-essential \
    gcc \
    git \
    make \
    original-awk \
    sed \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Clone and build Yate
WORKDIR /yate
RUN git clone https://github.com/yatevoip/yate . \
    && ./autogen.sh \
    && ./configure --disable-doc \
    && make -j$(nproc) doc=no

# Stage 2: Runtime
FROM debian:bookworm-slim

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    make \
    python3-venv \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Copy only necessary binaries and libraries from the build stage
COPY --from=build /yate /yate

WORKDIR /yate
# Set up shared library cache
RUN make install-noapi && ldconfig

# Set up Python virtual environment
RUN python3 -m venv /python-venv \
    && /python-venv/bin/pip3 install --no-cache-dir \
        filelock \
        requests \
        python-yate

# Copy configuration, scripts, and sound files
COPY config /usr/local/etc/yate
COPY sounds /usr/local/share/yate/sounds/
COPY scripts /usr/local/share/yate/scripts/

# Set entrypoint
ENTRYPOINT ["yate"]
