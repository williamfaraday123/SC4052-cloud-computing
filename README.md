# Instructions to run project
## to run backend
```
cd Project\backend
python -m venv venv
venv\Scripts\activate
pip install -r app/requirements.txt
uvicorn app.main:app --reload
deactivate //when done
```
## to run frontend
```
cd Project\frontend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run ui.py
deactivate
```
# System architecture
![image](https://github.com/user-attachments/assets/06733d71-007e-49cc-94f2-3e643b5c734f)
