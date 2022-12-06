FROM python:3.8

RUN pip install explainerdashboard
RUN pip install pandas
RUN pip install lightgbm

COPY dashboard.py ./
COPY df_model.csv ./
COPY model_lgbm.pkl ./


EXPOSE 9050
CMD ["python", "./dashboard.py"]