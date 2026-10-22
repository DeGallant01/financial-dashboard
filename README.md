# Personal Finance Dashboard

Generic Ireland-first household planner (Streamlit). No personal data is stored in the code. What you type stays in your browser session.

## Run locally

```text
py -3 -m pip install -r requirements.txt
py -3 -m streamlit run app.py
```

Open http://localhost:8501

## Share with friends or the public (Streamlit Community Cloud)

This is a calculator, not a login product. Anyone with the link can move sliders. Do not type real account numbers, PPS numbers, or passwords into it.

1. Put the project on a **GitHub** repository (`app.py`, `requirements.txt`, `.streamlit/config.toml`). Keep it free of `.env` and credentials.
2. Sign in at [share.streamlit.io](https://share.streamlit.io) with GitHub.
3. **New app** → pick the repo → main file `app.py` → Deploy.
4. You get a public URL such as `https://your-app-name.streamlit.app`. Send that to friends, or leave it public.

Each visitor gets their own session. They do not see each other’s numbers.

## What is in the defaults

Round Irish planning figures only (example salaries, a €25,000 cash start, catalogue car prices, typical bank rate bands). Nothing is a real person’s file.

Business and rental are **off** on the master graph until someone turns them on.
