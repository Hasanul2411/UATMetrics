"""
Digital Journey Analytics page with KPIs and filters.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from database.connection import get_session
from database.models import Event, Service
from utils.auth import require_role
from utils.validators import validate_date_range
from utils.logger import logger


def calculate_completion_rate(df: pd.DataFrame) -> float:
    """Calculate completion rate (success events / total events)."""
    try:
        if df.empty or len(df) == 0:
            return 0.0
        if "status" not in df.columns:
            return 0.0
        success_count = len(df[df["status"] == "success"])
        return (success_count / len(df)) * 100 if len(df) > 0 else 0.0
    except Exception:
        return 0.0


def calculate_error_rate(df: pd.DataFrame) -> float:
    """Calculate error rate (error events / total events)."""
    try:
        if df.empty or len(df) == 0:
            return 0.0
        if "status" not in df.columns:
            return 0.0
        error_count = len(df[df["status"] == "error"])
        return (error_count / len(df)) * 100 if len(df) > 0 else 0.0
    except Exception:
        return 0.0


def calculate_avg_journey_time(df: pd.DataFrame) -> float:
    """Calculate average journey time in seconds."""
    try:
        if df.empty or len(df) == 0:
            return 0.0
        if "journey_time" not in df.columns:
            return 0.0
        journey_times = df["journey_time"].dropna()
        if len(journey_times) == 0:
            return 0.0
        return float(journey_times.mean())
    except Exception:
        return 0.0


def load_events_data(service_id: int = None, start_date: datetime = None, end_date: datetime = None) -> pd.DataFrame:
    """Load events data from database with optional filters."""
    try:
        with get_session() as session:
            query = session.query(Event, Service).join(Service)

            if service_id:
                query = query.filter(Event.service_id == service_id)
            if start_date:
                query = query.filter(Event.timestamp >= start_date)
            if end_date:
                # Add one day to include the entire end date
                end_date_inclusive = end_date + timedelta(days=1)
                query = query.filter(Event.timestamp < end_date_inclusive)

            results = query.all()
            data = []
            for event, service in results:
                data.append({
                    "id": event.id,
                    "service": service.name,
                    "channel": service.channel,
                    "action": event.action,
                    "status": event.status,
                    "timestamp": event.timestamp,
                    "journey_time": event.journey_time,
                    "error_message": event.error_message
                })
            return pd.DataFrame(data)
    except Exception as e:
        logger.error(f"Error loading events data: {e}")
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()


def show_analytics_page():
    """Display analytics dashboard."""
    require_role(["Analyst", "Tester", "Viewer"])
    
    st.title("📊 Digital Journey Analytics")

    # Load services for filter
    with get_session() as session:
        services = session.query(Service).all()
        service_options = {0: "All Services"}
        service_options.update({s.id: s.name for s in services})

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        selected_service_id = st.selectbox(
            "Service",
            options=list(service_options.keys()),
            format_func=lambda x: service_options[x],
            index=0
        )

    with col2:
        start_date = st.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=30),
            max_value=datetime.now()
        )

    with col3:
        end_date = st.date_input(
            "End Date",
            value=datetime.now(),
            max_value=datetime.now()
        )

    # Validate date range
    is_valid, error_msg = validate_date_range(start_date, end_date)
    if not is_valid:
        st.error(error_msg)
        return

    # Convert dates to datetime
    start_datetime = datetime.combine(start_date, datetime.min.time())
    end_datetime = datetime.combine(end_date, datetime.max.time())

    # Load data
    service_filter = None if selected_service_id == 0 else selected_service_id
    df = load_events_data(service_filter, start_datetime, end_datetime)

    if df.empty:
        st.info("📊 No data available for the selected filters.")
        st.markdown("""
        **To add data:**
        - Use the "Generate Sample Data" button in the sidebar (Analyst role)
        - Or manually add events through your application integration
        - See the **Data Entry Guide** for more information
        """)
        return

    # KPI Metrics
    st.markdown("---")
    st.subheader("📈 Key Performance Indicators")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        total_events = len(df)
        st.metric("Total Events", f"{total_events:,}")

    with col2:
        completion_rate = calculate_completion_rate(df)
        st.metric("Completion Rate", f"{completion_rate:.2f}%")

    with col3:
        error_rate = calculate_error_rate(df)
        st.metric("Error Rate", f"{error_rate:.2f}%")

    with col4:
        avg_journey_time = calculate_avg_journey_time(df)
        st.metric("Avg Journey Time", f"{avg_journey_time:.2f}s")

    # Charts Section
    st.markdown("---")
    st.subheader("📉 Visualizations")

    # Event Status Distribution
    col1, col2 = st.columns(2)

    with col1:
        try:
            if "status" in df.columns and not df["status"].empty:
                status_counts = df["status"].value_counts()
                if len(status_counts) > 0:
                    fig_status = px.pie(
                        values=status_counts.values,
                        names=status_counts.index,
                        title="Event Status Distribution",
                        color_discrete_map={"success": "#2ecc71", "error": "#e74c3c", "pending": "#f39c12"}
                    )
                    fig_status.update_layout(showlegend=True)
                    st.plotly_chart(fig_status, use_container_width=True)
                else:
                    st.info("No status data available for chart")
            else:
                st.info("No status data available for chart")
        except Exception as e:
            st.warning(f"Could not generate status chart: {e}")

    with col2:
        # Events Over Time
        df_time = df.copy()
        df_time["date"] = pd.to_datetime(df_time["timestamp"]).dt.date
        daily_counts = df_time.groupby(["date", "status"]).size().reset_index(name="count")
        fig_timeline = px.line(
            daily_counts,
            x="date",
            y="count",
            color="status",
            title="Events Over Time",
            labels={"date": "Date", "count": "Event Count", "status": "Status"}
        )
        fig_timeline.update_layout(showlegend=True)
        st.plotly_chart(fig_timeline, use_container_width=True)

    # Service Performance
    st.markdown("#### Service Performance")
    service_perf = df.groupby("service").agg({
        "status": lambda x: (x == "success").sum() / len(x) * 100,
        "id": "count"
    }).rename(columns={"status": "completion_rate", "id": "total_events"})
    service_perf = service_perf.reset_index()

    fig_service = px.bar(
        service_perf,
        x="service",
        y="completion_rate",
        title="Completion Rate by Service",
        labels={"service": "Service", "completion_rate": "Completion Rate (%)"},
        color="completion_rate",
        color_continuous_scale="Viridis"
    )
    fig_service.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig_service, use_container_width=True)

    # Detailed Data Table
    st.markdown("---")
    st.subheader("📋 Event Details")

    # Format timestamp for display
    df_display = df.copy()
    df_display["timestamp"] = pd.to_datetime(df_display["timestamp"]).dt.strftime("%Y-%m-%d %H:%M:%S")
    df_display = df_display.rename(columns={
        "id": "ID",
        "service": "Service",
        "channel": "Channel",
        "action": "Action",
        "status": "Status",
        "timestamp": "Timestamp",
        "journey_time": "Journey Time (s)",
        "error_message": "Error Message"
    })

    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        height=400
    )

    # Export option
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download Data as CSV",
        data=csv,
        file_name=f"events_{start_date}_{end_date}.csv",
        mime="text/csv"
    )


if __name__ == "__main__":
    show_analytics_page()



