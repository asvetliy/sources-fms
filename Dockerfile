FROM python:3.7-slim

RUN groupadd pygroup && useradd -m -g pygroup -s /bin/bash pyuser
RUN mkdir -p /home/pyuser/sources-fms

COPY . /home/pyuser/sources-fms
WORKDIR /home/pyuser/sources-fms

RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r /home/pyuser/sources-fms/requirements/prod.txt
RUN chown -R pyuser:pygroup /home/pyuser

USER pyuser

CMD ["python", "/home/pyuser/sources-fms/app/cmd/main.py"]
