FROM python:latest
COPY requirements.txt /tmp/
RUN apt-get -y update && apt-get install -y git && apt-get install -y pip && apt-get install -y vim
RUN pip install --no-cache-dir -r tmp/requirements.txt
RUN git clone --single-branch --branch master https://github.com/luizgdias/maestro.git 
RUN cd maestro/dfa-lib-python && python setup.py install
RUN apt-get install -y mafft && apt-get install -y clustalw && apt-get install -y muscle
RUN apt-get install -y readseq

RUN apt-get install -y mrbayes && apt-get install -y raxml
RUN ls

# CMD ["python", "maestro/main.py"]
WORKDIR /maestro/sources
RUN ls
CMD ["python", "wf.py"]
# RUN python maestro/sources/wf.py
