Steps to run performance test: 

Install requirements :
pip install flask pyjwt requests

Initialize database: 
python db_init.py

Run flask app: 
python task.py

Install Locust: 
pip install locust

Run performance tests: 
locust --host=http://localhost:5000

Load user interface :
http://0.0.0.0:8089/

<img width="1566" alt="locust1" src="https://github.com/user-attachments/assets/4d7411bf-ee27-4ad9-bc52-8e0113946285" />
