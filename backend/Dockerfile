FROM python:3.10.5-buster

COPY dist/*.whl /tmp/
RUN pip install /tmp/*.whl
CMD rm -rf /tmp/*.whl

ENTRYPOINT ["python", "-m", "koala"]

