"""
Automated Reporting page for PDF generation.
"""
import streamlit as st
from datetime import datetime, timedelta
from database.connection import get_session
from database.models import Event, Service, TestCase, Defect
from utils.auth import require_role
from reports.pdf_generator import generate_analytics_report, generate_uat_report
from pages.analytics import load_events_data, calculate_completion_rate, calculate_error_rate, calculate_avg_journey_time
from pages.uat_tracker import load_test_cases, load_defects
import pandas as pd
from utils.logger import logger


def show_reports_page():
    """Display reports generation page."""
    from utils.ui import render_page_header, STUDIO_COLORS
    render_page_header("Project Reports", "Generate and Export Summary Reports", icon="reports")

    # Report Type Selection
    report_type = st.radio(
        "Select Report Type",
        options=["Analytics Report", "UAT & Testing Report"],
        horizontal=True
    )

    st.markdown("---")

    if report_type == "Analytics Report":
        st.subheader("Analytics Report Configuration")

        # Date range selection
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Start Date",
                value=datetime.now() - timedelta(days=30),
                max_value=datetime.now()
            )
        with col2:
            end_date = st.date_input(
                "End Date",
                value=datetime.now(),
                max_value=datetime.now()
            )

        # Service filter
        with get_session() as session:
            services = session.query(Service).all()
            service_options = {0: "All Services"}
            service_options.update({s.id: s.name for s in services})

        selected_service_id = st.selectbox(
            "Service",
            options=list(service_options.keys()),
            format_func=lambda x: service_options[x],
            index=0
        )

        if st.button("Generate Analytics Report", type="primary", use_container_width=True):
            try:
                with st.spinner("Generating report..."):
                    # Load data
                    service_filter = None if selected_service_id == 0 else selected_service_id
                    start_datetime = datetime.combine(start_date, datetime.min.time())
                    end_datetime = datetime.combine(end_date, datetime.max.time())

                    events_df = load_events_data(service_filter, start_datetime, end_datetime)

                    if events_df.empty:
                        st.warning("⚠️ No data available for the selected filters. Please add data first or adjust your filters.")
                        st.info("💡 Tip: Use 'Generate Sample Data' in the sidebar to create sample data for testing.")
                    else:
                        # Calculate KPIs
                        kpi_data = {
                            "total_events": len(events_df),
                            "completion_rate": calculate_completion_rate(events_df),
                            "error_rate": calculate_error_rate(events_df),
                            "avg_journey_time": calculate_avg_journey_time(events_df)
                        }

                        # Service performance
                        service_perf = events_df.groupby("service").agg({
                            "status": lambda x: (x == "success").sum() / len(x) * 100,
                            "id": "count"
                        }).rename(columns={"status": "completion_rate", "id": "total_events"}).reset_index()

                        # Generate PDF
                        pdf_buffer = generate_analytics_report(kpi_data, events_df, service_perf)

                        # Download button
                        st.success("Report generated successfully!")
                        st.download_button(
                            label="📥 Download Analytics Report (PDF)",
                            data=pdf_buffer.getvalue(),
                            file_name=f"analytics_report_{start_date}_{end_date}.pdf",
                            mime="application/pdf"
                        )
            except Exception as e:
                st.error(f"Error generating report: {e}")
                logger.error(f"Error generating analytics report: {e}")

    else:  # UAT Report
        st.subheader("UAT & Testing Report Configuration")

        # Service filter
        with get_session() as session:
            services = session.query(Service).all()
            service_options = {0: "All Services"}
            service_options.update({s.id: s.name for s in services})

        selected_service_id = st.selectbox(
            "Service",
            options=list(service_options.keys()),
            format_func=lambda x: service_options[x],
            index=0,
            key="uat_service_filter"
        )

        if st.button("Generate UAT Report", type="primary", use_container_width=True):
            try:
                with st.spinner("Generating report..."):
                    # Load data
                    service_filter = None if selected_service_id == 0 else selected_service_id
                    test_cases_df = load_test_cases(service_filter)
                    defects_df = load_defects(service_filter)

                    if test_cases_df.empty and defects_df.empty:
                        st.warning("No data available for the selected filters.")
                    else:
                        # Generate PDF
                        pdf_buffer = generate_uat_report(test_cases_df, defects_df)

                        # Download button
                        st.success("Report generated successfully!")
                        st.download_button(
                            label="📥 Download UAT Report (PDF)",
                            data=pdf_buffer.getvalue(),
                            file_name=f"uat_report_{datetime.now().strftime('%Y%m%d')}.pdf",
                            mime="application/pdf"
                        )
            except Exception as e:
                st.error(f"Error generating report: {e}")
                logger.error(f"Error generating UAT report: {e}")


if __name__ == "__main__":
    show_reports_page()



