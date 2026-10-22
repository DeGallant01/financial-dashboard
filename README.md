# Ireland Household Planner

Example Irish household calculator for pay, housing, pensions, cars, and investing. Open it, change the starter figures, and model a plan.

Public app: https://financial-dashboard-gallant.streamlit.app/

## Run on your computer

```text
py -3 -m pip install -r requirements.txt
py -3 -m streamlit run app.py
```

Open http://localhost:8501

Starter numbers are round examples (for example two people aged 30 on €50,000, €10,000 cash, one car, no children). They are not a real household file. Each visitor’s inputs stay in their own browser.

## Deploy your own copy

Streamlit Community Cloud rebuilds from the connected GitHub branch when you push. Sign in at https://share.streamlit.io, pick this repository, main file `app.py`, and deploy.
