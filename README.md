## Instagram clone in FastAPI

___

* Git clone project
* A virtual environment is created
* Installing requirements.txt

        pip install -r requirements.txtv
* Alembic init

        alembic init migrations
* env.py files database url is given
* Alembic migrations

        alembic revision --autogenerate -m "Create tables"
* Alembic upgrade

        alembic upgrade head
* Let's launch the project

         uvicorn main:app --reload



### Thank you all [Temirovuz](https://github.com/temirovuz) was with you 🙂
___

![image](https://github.com/temirovuz/news_FastAPI/assets/100820263/ad07393e-59de-4374-83af-3fd6987a7b27)
