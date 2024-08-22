from src.dashboards.st_dashboard import Dashboard
import sys
from streamlit.web import cli as stcli

if __name__ == "__main__":
    Dashboard.run_streamlit_app(cls=Dashboard)
    sys.argv = ["streamlit", "run", "src/main.py"]
    sys.exit(stcli.main())
