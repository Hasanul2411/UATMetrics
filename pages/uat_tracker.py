"""
UAT & Regression Testing Tracker page.
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from database.connection import get_session
from database.models import TestCase, Defect, Service
from utils.auth import require_role, check_role_access
from utils.validators import validate_required_field, validate_severity, validate_status
from utils.logger import logger


def load_test_cases(service_id: int = None) -> pd.DataFrame:
    """Load test cases from database."""
    try:
        with get_session() as session:
            query = session.query(TestCase, Service).join(Service)
            if service_id:
                query = query.filter(TestCase.service_id == service_id)
            results = query.all()
            data = []
            for test_case, service in results:
                data.append({
                    "id": test_case.id,
                    "service": service.name,
                    "title": test_case.title,
                    "description": test_case.description,
                    "expected_result": test_case.expected_result,
                    "status": test_case.status,
                    "created_at": test_case.created_at
                })
            return pd.DataFrame(data)
    except Exception as e:
        logger.error(f"Error loading test cases: {e}")
        return pd.DataFrame()


def load_defects(service_id: int = None) -> pd.DataFrame:
    """Load defects from database."""
    try:
        with get_session() as session:
            query = session.query(Defect, Service).join(Service)
            if service_id:
                query = query.filter(Defect.service_id == service_id)
            results = query.all()
            data = []
            for defect, service in results:
                data.append({
                    "id": defect.id,
                    "service": service.name,
                    "title": defect.title,
                    "severity": defect.severity,
                    "status": defect.status,
                    "created_at": defect.created_at,
                    "test_case_id": defect.test_case_id
                })
            return pd.DataFrame(data)
    except Exception as e:
        logger.error(f"Error loading defects: {e}")
        return pd.DataFrame()


def show_uat_tracker_page():
    """Display UAT tracker page."""
    require_role(["Analyst", "Tester", "Viewer"])
    from utils.ui import render_page_header, STUDIO_COLORS
    render_page_header("UAT & Regression Testing", "Add and Manage User Acceptance Test Events", icon="tracker")

    # Load services
    with get_session() as session:
        services = session.query(Service).all()
        service_dict = {s.id: s.name for s in services}

    # Tabs for Test Cases and Defects
    tab1, tab2 = st.tabs(["Test Cases", "Defects"])

    # ========== TEST CASES TAB ==========
    with tab1:
        st.subheader("Test Cases Management")

        # Filter by service
        service_filter = st.selectbox(
            "Filter by Service",
            options=[0] + list(service_dict.keys()),
            format_func=lambda x: "All Services" if x == 0 else service_dict[x],
            key="test_case_filter"
        )

        # Load and display test cases
        with st.spinner("Loading test cases..."):
            test_cases_df = load_test_cases(service_filter if service_filter != 0 else None)

        if not test_cases_df.empty:
            st.markdown(f"**Total Test Cases: {len(test_cases_df)}**")

            # Test case status summary
            if "status" in test_cases_df.columns:
                status_counts = test_cases_df["status"].value_counts()
                cols = st.columns(len(status_counts))
                for idx, (status, count) in enumerate(status_counts.items()):
                    with cols[idx]:
                        st.metric(status, count)

            # Display test cases with editing capabilities
            if check_role_access(["Analyst", "Tester"]):
                st.info("💡 You can edit 'Status' directly in the table below. Select rows to Delete.")
                
                # Add a selection column for deletion
                test_cases_df["Delete"] = False
                
                edited_df = st.data_editor(
                    test_cases_df,
                    column_config={
                        "Delete": st.column_config.CheckboxColumn(
                            "Delete",
                            help="Select to delete",
                            default=False,
                        ),
                        "status": st.column_config.SelectboxColumn(
                            "Status",
                            options=["Not Started", "Passed", "Failed", "Blocked"],
                            required=True
                        ),
                        "id": st.column_config.NumberColumn("ID", disabled=True),
                        "service": st.column_config.TextColumn("Service", disabled=True),
                        "title": st.column_config.TextColumn("Title", disabled=True),
                        "created_at": st.column_config.DatetimeColumn("Created At", disabled=True),
                    },
                    use_container_width=True,
                    hide_index=True,
                    key="tc_editor"
                )
                
                if st.button("Save Changes", key="save_tc"):
                    try:
                        with get_session() as session:
                            changes_count = 0
                            
                            # Process checks for deletion
                            rows_to_delete = edited_df[edited_df["Delete"] == True]
                            for _, row in rows_to_delete.iterrows():
                                tc_to_delete = session.query(TestCase).get(row["id"])
                                if tc_to_delete:
                                    session.delete(tc_to_delete)
                                    changes_count += 1
                            
                            # Process updates (scan for status changes)
                            # Since we don't have the original df easily accessible to compare diffs row-by-row efficiently without iterating,
                            # and N is small, we can just update status for all non-deleted rows if they differ.
                            # Optimization: Just look at touched rows if possible? 
                            # Simpler: Iterate edited_df, skip deleted.
                            
                            # Actually, st.data_editor returns the final state.
                            # We can just iterate and update.
                            
                            for _, row in edited_df.iterrows():
                                if not row["Delete"]:
                                    tc = session.query(TestCase).get(row["id"])
                                    if tc and tc.status != row["status"]:
                                        tc.status = row["status"]
                                        changes_count += 1
                                        
                            session.commit()
                            if changes_count > 0:
                                st.success(f"Successfully saved {changes_count} changes.")
                                st.rerun()
                            else:
                                st.info("No changes detected.")
                                
                    except Exception as e:
                        st.error(f"Error saving changes: {e}")
            else:
                 # Read-only view for viewers
                 st.dataframe(
                    test_cases_df[["id", "service", "title", "status", "created_at"]],
                    use_container_width=True,
                    hide_index=True
                )

        # Create/Edit Test Case (only for Analyst and Tester)
        if check_role_access(["Analyst", "Tester"]):
            st.markdown("---")
            with st.expander("➕ Create New Test Case"):
                with st.form("create_test_case"):
                    new_service_id = st.selectbox(
                        "Service",
                        options=list(service_dict.keys()),
                        format_func=lambda x: service_dict[x]
                    )
                    new_title = st.text_input("Title *")
                    new_description = st.text_area("Description")
                    new_expected_result = st.text_area("Expected Result *")
                    new_test_steps = st.text_area("Test Steps")
                    new_status = st.selectbox(
                        "Status",
                        options=["Not Started", "Passed", "Failed", "Blocked"]
                    )

                    if st.form_submit_button("Create Test Case"):
                        is_valid, error = validate_required_field(new_title, "Title")
                        if not is_valid:
                            st.error(error)
                        else:
                            is_valid, error = validate_required_field(new_expected_result, "Expected Result")
                            if not is_valid:
                                st.error(error)
                            else:
                                try:
                                    with get_session() as session:
                                        new_test_case = TestCase(
                                            service_id=new_service_id,
                                            title=new_title,
                                            description=new_description,
                                            expected_result=new_expected_result,
                                            test_steps=new_test_steps,
                                            status=new_status
                                        )
                                        session.add(new_test_case)
                                        session.commit()
                                        st.success("Test case created successfully!")
                                        logger.info(f"Test case created: {new_title}")
                                        st.rerun()
                                except Exception as e:
                                    st.error(f"Error creating test case: {e}")
                                    logger.error(f"Error creating test case: {e}")

    # ========== DEFECTS TAB ==========
    with tab2:
        st.subheader("Defects Management")

        # Filter by service
        defect_service_filter = st.selectbox(
            "Filter by Service",
            options=[0] + list(service_dict.keys()),
            format_func=lambda x: "All Services" if x == 0 else service_dict[x],
            key="defect_filter"
        )

        # Load and display defects
        with st.spinner("Loading defects..."):
            defects_df = load_defects(defect_service_filter if defect_service_filter != 0 else None)

        if not defects_df.empty:
            st.markdown(f"**Total Defects: {len(defects_df)}**")

            # Defect summary by severity and status
            col1, col2 = st.columns(2)

            with col1:
                if "severity" in defects_df.columns:
                    severity_counts = defects_df["severity"].value_counts()
                    st.markdown("**By Severity:**")
                    for severity, count in severity_counts.items():
                        st.write(f"- {severity}: {count}")

            with col2:
                if "status" in defects_df.columns:
                    status_counts = defects_df["status"].value_counts()
                    st.markdown("**By Status:**")
                    for status, count in status_counts.items():
                        st.write(f"- {status}: {count}")

            # Display defects with editing capabilities
            if check_role_access(["Analyst", "Tester"]):
                st.info("💡 You can edit 'Status' and 'Severity' directly. Select rows to Delete.")
                
                defects_df["Delete"] = False
                
                edited_defects_df = st.data_editor(
                    defects_df,
                    column_config={
                        "Delete": st.column_config.CheckboxColumn(
                            "Delete",
                            help="Select to delete",
                            default=False,
                        ),
                        "status": st.column_config.SelectboxColumn(
                            "Status",
                            options=["Open", "In Progress", "Resolved", "Closed"],
                            required=True
                        ),
                         "severity": st.column_config.SelectboxColumn(
                            "Severity",
                            options=["Critical", "High", "Medium", "Low"],
                            required=True
                        ),
                        "id": st.column_config.NumberColumn("ID", disabled=True),
                        "service": st.column_config.TextColumn("Service", disabled=True),
                        "title": st.column_config.TextColumn("Title", disabled=True),
                        "created_at": st.column_config.DatetimeColumn("Created At", disabled=True),
                    },
                    use_container_width=True,
                    hide_index=True,
                    key="defect_editor"
                )
                
                if st.button("Save Changes", key="save_defects"):
                    try:
                        with get_session() as session:
                            changes_count = 0
                            
                            # Process deletions
                            rows_to_delete = edited_defects_df[edited_defects_df["Delete"] == True]
                            for _, row in rows_to_delete.iterrows():
                                defect_to_delete = session.query(Defect).get(row["id"])
                                if defect_to_delete:
                                    session.delete(defect_to_delete)
                                    changes_count += 1
                                    
                            # Process updates
                            for _, row in edited_defects_df.iterrows():
                                if not row["Delete"]:
                                    defect = session.query(Defect).get(row["id"])
                                    if defect:
                                        if defect.status != row["status"] or defect.severity != row["severity"]:
                                            defect.status = row["status"]
                                            defect.severity = row["severity"]
                                            changes_count += 1
                            
                            session.commit()
                            if changes_count > 0:
                                st.success(f"Successfully saved {changes_count} changes.")
                                st.rerun()
                            else:
                                st.info("No changes detected.")

                    except Exception as e:
                        st.error(f"Error saving changes: {e}")

            else:
                 # Read-only view
                st.dataframe(
                    defects_df[["id", "service", "title", "severity", "status", "created_at"]],
                    use_container_width=True,
                    hide_index=True
                )

        # Create/Edit Defect (only for Analyst and Tester)
        if check_role_access(["Analyst", "Tester"]):
            st.markdown("---")
            with st.expander("🐛 Create New Defect"):
                with st.form("create_defect"):
                    defect_service_id = st.selectbox(
                        "Service *",
                        options=list(service_dict.keys()),
                        format_func=lambda x: service_dict[x],
                        key="defect_service"
                    )
                    defect_title = st.text_input("Title *", key="defect_title")
                    defect_description = st.text_area("Description *", key="defect_description")
                    defect_severity = st.selectbox(
                        "Severity *",
                        options=["Critical", "High", "Medium", "Low"],
                        key="defect_severity"
                    )
                    defect_status = st.selectbox(
                        "Status",
                        options=["Open", "In Progress", "Resolved", "Closed"],
                        index=0,
                        key="defect_status"
                    )
                    defect_steps = st.text_area("Steps to Reproduce", key="defect_steps")
                    defect_expected = st.text_area("Expected Behavior", key="defect_expected")
                    defect_actual = st.text_area("Actual Behavior", key="defect_actual")

                    if st.form_submit_button("Create Defect"):
                        is_valid, error = validate_required_field(defect_title, "Title")
                        if not is_valid:
                            st.error(error)
                        else:
                            is_valid, error = validate_required_field(defect_description, "Description")
                            if not is_valid:
                                st.error(error)
                            else:
                                try:
                                    with get_session() as session:
                                        new_defect = Defect(
                                            service_id=defect_service_id,
                                            title=defect_title,
                                            description=defect_description,
                                            severity=defect_severity,
                                            status=defect_status,
                                            steps_to_reproduce=defect_steps,
                                            expected_behavior=defect_expected,
                                            actual_behavior=defect_actual
                                        )
                                        session.add(new_defect)
                                        session.commit()
                                        st.success("Defect created successfully!")
                                        logger.info(f"Defect created: {defect_title}")
                                        st.rerun()
                                except Exception as e:
                                    st.error(f"Error creating defect: {e}")
                                    logger.error(f"Error creating defect: {e}")


if __name__ == "__main__":
    show_uat_tracker_page()



