"""
Executive Dashboard page with high-level insights.
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from database.connection import get_session
from database.models import Event, Service, TestCase, Defect
from utils.auth import require_role
from utils.logger import logger


def load_dashboard_data():
    """Load all data needed for dashboard."""
    try:
        with get_session() as session:
            # Services count
            services_count = session.query(Service).count()

            # Events summary (last 30 days)
            thirty_days_ago = datetime.now() - timedelta(days=30)
            events = session.query(Event).filter(Event.timestamp >= thirty_days_ago).all()
            total_events = len(events)
            success_events = len([e for e in events if e.status == "success"])
            error_events = len([e for e in events if e.status == "error"])

            # Test cases summary
            test_cases = session.query(TestCase).all()
            total_test_cases = len(test_cases)
            passed_test_cases = len([tc for tc in test_cases if tc.status == "Passed"])
            failed_test_cases = len([tc for tc in test_cases if tc.status == "Failed"])

            # Defects summary
            defects = session.query(Defect).all()
            total_defects = len(defects)
            open_defects = len([d for d in defects if d.status == "Open"])
            critical_defects = len([d for d in defects if d.severity == "Critical"])

            # Service performance data
            service_perf = []
            for service in session.query(Service).all():
                service_events = [e for e in events if e.service_id == service.id]
                if service_events:
                    success_rate = len([e for e in service_events if e.status == "success"]) / len(service_events) * 100
                    service_perf.append({
                        "service": service.name,
                        "success_rate": success_rate,
                        "total_events": len(service_events)
                    })

            return {
                "services_count": services_count,
                "total_events": total_events,
                "success_events": success_events,
                "error_events": error_events,
                "total_test_cases": total_test_cases,
                "passed_test_cases": passed_test_cases,
                "failed_test_cases": failed_test_cases,
                "total_defects": total_defects,
                "open_defects": open_defects,
                "critical_defects": critical_defects,
                "service_perf": pd.DataFrame(service_perf) if service_perf else pd.DataFrame(),
                "defects_by_severity": pd.DataFrame([
                    {"severity": d.severity, "count": 1} for d in defects
                ]) if defects else pd.DataFrame()
            }
    except Exception as e:
        logger.error(f"Error loading dashboard data: {e}")
        st.error(f"Error loading dashboard data: {e}")
        return None


def show_dashboard_page():
    """Display executive dashboard."""
    require_role(["Analyst", "Tester", "Viewer"])
    
    st.title("📈 Executive Dashboard")
    st.markdown("### High-Level Performance Overview")

    data = load_dashboard_data()
    if data is None:
        st.error("Unable to load dashboard data. Please check your database connection.")
        return
    
    # Handle empty data gracefully
    if data["total_events"] == 0 and data["services_count"] == 0:
        st.info("👋 Welcome! Your dashboard is ready. Start by generating sample data or adding your first service.")
        st.markdown("""
        **Next Steps:**
        1. Click "Generate Sample Data" in the sidebar (Analyst role)
        2. Or manually add services, events, test cases, and defects
        3. See the **Data Entry Guide** for detailed instructions
        """)
        return

    # Key Metrics Row 1
    st.markdown("---")
    st.subheader("📊 Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Digital Services", data["services_count"])
    with col2:
        st.metric("Total Events (30d)", f"{data['total_events']:,}")
    with col3:
        try:
            completion_rate = (data["success_events"] / data["total_events"] * 100) if data["total_events"] > 0 else 0.0
            st.metric("Success Rate", f"{completion_rate:.1f}%")
        except (ZeroDivisionError, TypeError):
            st.metric("Success Rate", "0.0%")
    with col4:
        st.metric("Open Defects", data["open_defects"])

    # Key Metrics Row 2
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Test Cases", data["total_test_cases"])
    with col2:
        try:
            test_pass_rate = (data["passed_test_cases"] / data["total_test_cases"] * 100) if data["total_test_cases"] > 0 else 0.0
            st.metric("Test Pass Rate", f"{test_pass_rate:.1f}%")
        except (ZeroDivisionError, TypeError):
            st.metric("Test Pass Rate", "0.0%")
    with col3:
        st.metric("Critical Defects", data["critical_defects"], delta=f"-{data['critical_defects']}" if data["critical_defects"] > 0 else None)
    with col4:
        st.metric("Total Defects", data["total_defects"])

    # Visualizations
    st.markdown("---")
    st.subheader("📉 Visual Insights")

    col1, col2 = st.columns(2)

    with col1:
        # Service Performance
        if not data["service_perf"].empty:
            fig_service = px.bar(
                data["service_perf"],
                x="service",
                y="success_rate",
                title="Service Success Rate",
                labels={"service": "Service", "success_rate": "Success Rate (%)"},
                color="success_rate",
                color_continuous_scale="RdYlGn"
            )
            fig_service.update_layout(xaxis_tickangle=-45, showlegend=False)
            st.plotly_chart(fig_service, use_container_width=True)
        else:
            st.info("No service performance data available.")

    with col2:
        # Defects by Severity
        if not data["defects_by_severity"].empty:
            severity_counts = data["defects_by_severity"].groupby("severity").size().reset_index(name="count")
            severity_order = ["Critical", "High", "Medium", "Low"]
            severity_counts["severity"] = pd.Categorical(severity_counts["severity"], categories=severity_order, ordered=True)
            severity_counts = severity_counts.sort_values("severity")

            fig_severity = px.bar(
                severity_counts,
                x="severity",
                y="count",
                title="Defects by Severity",
                labels={"severity": "Severity", "count": "Count"},
                color="severity",
                color_discrete_map={
                    "Critical": "#e74c3c",
                    "High": "#e67e22",
                    "Medium": "#f39c12",
                    "Low": "#3498db"
                }
            )
            st.plotly_chart(fig_severity, use_container_width=True)
        else:
            st.info("No defects data available.")

    # Executive Summary
    st.markdown("---")
    st.subheader("📋 Executive Summary")

    summary_text = f"""
    **Platform Overview:**
    - The platform is monitoring **{data['services_count']}** digital service(s)
    - Over the last 30 days, **{data['total_events']:,}** events were processed
    - Overall success rate: **{completion_rate:.1f}%**

    **Testing Status:**
    - **{data['total_test_cases']}** test cases defined
    - Test pass rate: **{test_pass_rate:.1f}%**
    - **{data['failed_test_cases']}** test cases currently failing

    **Quality Metrics:**
    - **{data['total_defects']}** total defects tracked
    - **{data['open_defects']}** defects currently open
    - **{data['critical_defects']}** critical defects requiring immediate attention

    **Recommendations:**
    """
    if data["critical_defects"] > 0:
        summary_text += f"\n- ⚠️ **Urgent:** Address {data['critical_defects']} critical defect(s) immediately"
    if completion_rate < 95:
        summary_text += f"\n- 📉 **Action Required:** Success rate below 95% - investigate error patterns"
    if test_pass_rate < 90:
        summary_text += f"\n- 🧪 **Testing:** Test pass rate below 90% - review failing test cases"
    if data["open_defects"] > 10:
        summary_text += f"\n- 🐛 **Backlog:** High number of open defects ({data['open_defects']}) - prioritize resolution"

    st.markdown(summary_text)


if __name__ == "__main__":
    show_dashboard_page()



