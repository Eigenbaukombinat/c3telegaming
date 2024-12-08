FROM debian:bookworm

#build yate
RUN apt update && apt install -y -f \
  autoconf \
  build-essential \
  doxygen \
  gcc \
  git \
  grep \
  make \
  original-awk \
  sed \
  vim

#ADD deps/yate /yate
RUN git clone https://github.com/yatevoip/yate.git /yate
WORKDIR "/yate"
RUN ./autogen.sh
RUN ./configure
RUN make all
RUN make install

#yate-tcl
RUN apt update && apt install -y -f \
  ffmpeg \
  lame \
  libmp3lame0 \
  netcat-openbsd \
  python3-pip \
  python3-venv \
  tcl \
  tcl-tls \
  tcllib

#yate-tcl
COPY deps/yate-tcl /opt/yate-tcl
RUN mkdir /usr/local/share/tcltk && ln -s /opt/yate-tcl/ygi /usr/local/share/tcltk/ygi

#RUN pip3 install python-yate requests
RUN python3 -m venv /venv
RUN /venv/bin/pip install requests python-yate

#yate-config
COPY config /usr/local/etc/yate

COPY sounds /usr/local/share/yate/sounds/

COPY hotline /usr/local/share/yate/scripts/

ENTRYPOINT [ "yate", "upstream_broke_it" ]
