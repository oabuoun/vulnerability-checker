FROM python:3
COPY Account-Generator /Account-Generator 
COPY requirements.txt /
RUN pip install -r requirements.txt
EXPOSE 5000/tcp
CMD ["python", "Account-Generator/main.py"]
