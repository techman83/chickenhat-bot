FROM python:3.12 AS base
RUN useradd -ms /bin/bash chicken
ADD . /chicken-hat
WORKDIR /chicken-hat
RUN pip install pip --upgrade
RUN chown -R chicken:chicken /chicken-hat
USER chicken
RUN pip install --user . --no-warn-script-location

FROM python:3.12 AS production
COPY --from=base /home/chicken /home/chicken
RUN useradd -Ms /bin/bash chicken
RUN chown -R chicken:chicken /home/chicken
WORKDIR /home/chicken
USER chicken
ENV PATH "$PATH:/home/chicken/.local/bin"
ENTRYPOINT [".local/bin/chickenhat-bot"]

FROM production
