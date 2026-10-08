@echo off
echo ========================================================
echo  Starting Agentic Legal Assistant Dashboard (HNX26EPS01)
echo ========================================================
echo.
python -m pip install -r requirements.txt
echo.
echo Launching Streamlit in browser...
streamlit run app.py
pause
