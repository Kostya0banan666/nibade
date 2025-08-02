FROM public.ecr.aws/docker/library/python:3.12-slim-bookworm

# 📦 Metadata as per Open Container Initiative (OCI) standards
LABEL \
  org.opencontainers.image.authors="Andrii Savchenko <sava777@gmail.com>, Kotiantyn Savchenko <savchenko.kostya777@gmail.com>" \
  org.opencontainers.image.base.name="public.ecr.aws/docker/library/python:3.12-slim-bookworm" \
  org.opencontainers.image.created="2025-08-02" \
  org.opencontainers.image.description="TDB" \
  org.opencontainers.image.title="TBD" \
  org.opencontainers.image.url="https://github.com/Kostya0banan666/nibade" \
  org.opencontainers.image.vendor="Savchenko" \
  org.opencontainers.image.version="0.0.1"

# ✨ Define constants and basic user metadata
ARG APP_HOME=/app
ARG GROUP=workers
ARG USER=worker
ARG USER_GID=1001
ARG USER_UID=1001
ARG PORT=8000
ENV POETRY_VIRTUALENVS_CREATE=false

# 📂 Set working directory
WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install -y make

# 👤 Create a dedicated system user/group to run the app without root privileges
RUN groupadd --system -f -g ${USER_GID} ${GROUP} \
    && useradd --system -m -d ${APP_HOME} -s /bin/bash -g ${USER_GID} -u ${USER_UID} -m ${USER}

# 🧰 Install Poetry
RUN pip install --no-cache-dir poetry

# 📦 Copy dependency definitions
COPY poetry.lock pyproject.toml ./

# 🚀 Installing essential packages (no dev stuff here!)
RUN poetry config virtualenvs.create false \
    && poetry install --only main

# 📂 Copy the application code into the container
COPY app/ ./

# 🔐 Ensure the app files are owned by the non-root user
RUN chown -R ${USER}:${GROUP} ./

# 👤 Switch to non-root user for execution
USER ${USER}

# 📡 Expose the port on which the app will run
EXPOSE ${PORT}

# 🚀 Launch
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT}"]
