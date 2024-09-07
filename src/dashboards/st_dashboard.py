import logging.config
from typing import List, Dict, Any

import streamlit as st
import pandas as pd
import plotly.express as px
from PIL import Image

from src.config.log_config import LOGGING
from src.utils.connection_db import get_top_inviters


logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)


class Dashboard:
    """Streamlit dashboards for the Discord invite leaderboard."""

    @staticmethod
    def run_streamlit_app(cls) -> None:
        logger.info("Starting Streamlit app")

        discord_logo = Image.open("src/images/Foxian.webp")
        st.image(discord_logo, use_column_width=True)

        st.sidebar.title("Discord Invite Leaderboard")
        top_n = st.sidebar.slider("Number of top inviters to display", 5, 50, 10)

        st.markdown(
            """
            <style>
            .stApp > div > div > div > img {
                margin-top: auto;
                margin-bottom: auto;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        dashboard = cls()
        dashboard.display_leaderboard(top_n)

    def display_leaderboard(self, top_n: int) -> None:
        """Display the leaderboard."""
        logger.info(f"Displaying leaderboard for top {top_n} inviters")
        try:
            top_inviters = self._get_top_inviters(top_n)
            if not top_inviters:
                logger.warning("No data available for the leaderboard")
                st.warning("No data available for the leaderboard.")
                return

            df = self._prepare_dataframe(top_inviters)
            self._display_table(df)
            self._display_chart(df)

            if st.button("Refresh Leaderboard"):
                logger.info("Refreshing leaderboard")
                self.display_leaderboard(top_n)
        except Exception as e:
            logger.error(f"An error occurred while displaying the leaderboard: {str(e)}", exc_info=True)
            st.error(f"An error occurred: {str(e)}")

    @staticmethod
    def _get_top_inviters(top_n: int) -> List[Dict[str, Any]]:
        logger.debug(f"Fetching top {top_n} inviters from database")
        try:
            return get_top_inviters(top_n)
        except Exception as e:
            logger.error(f"Error fetching top inviters: {str(e)}", exc_info=True)
            raise

    @staticmethod
    def _prepare_dataframe(top_inviters: List[Dict[str, Any]]) -> pd.DataFrame:
        """Prepare the DataFrame for display."""
        logger.debug("Preparing DataFrame for display")
        df = pd.DataFrame(top_inviters, columns=['Discord ID', 'Invite Count'])
        df['Rank'] = df['Invite Count'].rank(method='min', ascending=False)
        return df.sort_values('Rank')

    @staticmethod
    def _display_table(df: pd.DataFrame) -> None:
        """Display the leaderboard table."""
        logger.debug("Displaying leaderboard table")
        st.subheader("Top Inviters")
        st.table(df)

    @staticmethod
    def _display_chart(df: pd.DataFrame) -> None:
        """Display the leaderboard chart."""
        logger.debug("Displaying leaderboard chart")
        fig = px.bar(df,
                     x='Discord ID',
                     y='Invite Count',
                     title='Top Inviters',
                     labels={'Discord ID': 'User', 'Invite Count': 'Number of Invites'},
                     color='Invite Count',
                     color_continuous_scale='Viridis'
                     )
        st.plotly_chart(fig, use_container_width=True)
