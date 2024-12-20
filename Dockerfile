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
  telnet \
  sed \
  vim

RUN git clone https://github.com/yatevoip/yate /yate
WORKDIR "/yate"
RUN ./autogen.sh
RUN ./configure
RUN make -j 8 all
RUN make install

RUN apt update && apt install -y -f \
#  espeak-ng \
#  ffmpeg \
#  lame \
#  libmp3lame0 \
  python3-pip \
  python3-venv 
#  tcl \
#  tcl-tls \
#  tcllib

#yate-tcl
#COPY deps/yate-tcl /opt/yate-tcl
#RUN mkdir /usr/local/share/tcltk && ln -s /opt/yate-tcl/ygi /usr/local/share/tcltk/ygi

#pyttsx3
#COPY deps/yate_tts.py /opt/

#RUN pip3 install python-yate requests
RUN python3 -m venv /python-venv/
RUN /python-venv/bin/pip3 install \
  aiohttp \
  filelock \
  requests \
  python-yate \
  pyttsx3

#yate-config
COPY config /usr/local/etc/yate

COPY sounds /usr/local/share/yate/sounds/

COPY scripts /usr/local/share/yate/scripts/

ENTRYPOINT [ "yate", "upstream_broke_it" ]
