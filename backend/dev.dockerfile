FROM python:3.8-slim

ARG username=app
ARG uid=1000
ARG extras=""

# Add a non-root user as docker best practice
RUN useradd --create-home --shell /bin/bash --uid ${uid} ${username}
USER ${username}
# Add local user paths so that installed command line tools work.
ENV PATH="/home/${username}/.local/bin:${PATH}"

# create a dedicated code directory so we don't install our code in the same directory that we install conda
# and all of it's packages (installed in the home directory below).
RUN mkdir ~/code
WORKDIR /home/${username}/code

COPY  --chown=app:app requirements.txt .
RUN pip install --user -r requirements.txt

COPY --chown=app:app . .
RUN pip install -e ".$extras"

CMD ["/bin/bash"]