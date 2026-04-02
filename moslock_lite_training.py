import streamlit as st
from PIL import Image

st.set_page_config(page_title="MOSLock Lite – Training & Permit", page_icon="🔒", layout="wide")

st.title("MOSLock Lite – New Equipment Training & Isolation Permit")
st.markdown("**Demonstration for Underground Coal Operations**  \nThis Lite version shows the new equipment introduction workflow, the full HV isolation permit process, TVL observation, 12 step reference, equipment library and permit history.")

# Session state
if 'training_complete' not in st.session_state:
    st.session_state.training_complete = False
if 'rules' not in st.session_state:
    st.session_state.rules = []
if 'lock_photo' not in st.session_state:
    st.session_state.lock_photo = None
if 'show_permit_preview' not in st.session_state:
    st.session_state.show_permit_preview = None

# Horizontal tabs across the top
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Training Model",
    "High Voltage Access",
    "TVL Observation",
    "12 Step Isolation Reference",
    "Equipment Library",
    "Permit History"
])

with tab1:  # Training Model
    st.subheader("Step 1: New Equipment Introduction")
    st.image(Image.open("Substation.jpeg"), 
             caption="New Equipment – Mobile Substation (Clean Photo)", use_container_width=True)

    st.subheader("Step 2: Train Isolation Points, Compartments & Indicators")
    st.markdown("Select the **number** of each item to train the AI model on. (In the full app you can drag/drop each point directly onto the image.)")

    col1, col2, col3 = st.columns(3)
    with col1:
        num_iso = st.selectbox("Number of Isolation Points", [1, 2, 3, 4, 5], index=2, key="num_iso")
    with col2:
        num_comp = st.selectbox("Number of Compartments", [1, 2, 3, 4, 5], index=2, key="num_comp")
    with col3:
        num_ind = st.selectbox("Number of Indicators", [1, 2, 3], index=1, key="num_ind")

    st.subheader("Step 3: If This Then That Rules")
    st.markdown("**Define the logic the AI model will learn:**")

    if st.button("+ Add Another Logic Step", key="add_rule"):
        st.session_state.rules.append({"iso": 2, "cond": "Isolated", "comp": 2, "comp_status": "Isolated", "ind": 1, "ind_status": "Lit"})

    for i, rule in enumerate(st.session_state.rules):
        st.markdown(f"**Rule {i+1}**")
        c1, c2, c3 = st.columns([0.5, 0.5, 0.5])
        
        with c1:
            with st.container():
                st.markdown("**IF**") 
                rule["iso"] = st.selectbox("Isolation Point", [1, 2, 3], index=rule["iso"]-1, key=f"iso_{i}")
                rule["cond"] = st.selectbox("is", ["Isolated", "Not Isolated"], key=f"cond_{i}")
                
        with c2:
            st.markdown("**THEN**")
            rule["comp"] = st.selectbox("Compartment", [1, 2, 3], index=rule["comp"]-1, key=f"comp_{i}")
            rule["comp_status"] = st.selectbox("is", ["Isolated", "Energised"], key=f"comp_status_{i}")
            
        with c3:
            st.markdown("**AND Indicator**")
            rule["ind"] = st.selectbox("Indicator", [1, 2, 3], index=rule["ind"]-1, key=f"ind_{i}")
            rule["ind_status"] = st.selectbox("is", ["Lit", "Off"], key=f"ind_status_{i}")

    if st.button("Submit for Approval to AI Library", key="submit_ai_library"):
        st.success("✅ Equipment submitted for approval to AI Library. AI model will be trained once approved.")
        st.session_state.training_complete = True
        st.image(Image.open("Substation Trained.jpeg"), 
                 caption="Trained Equipment with Visual Annotations", use_container_width=True)

with tab2:  # High Voltage Access
    st.subheader("High Voltage Access Permit (Full STD0930 Flow)")
    if st.session_state.training_complete:
        with st.expander("Part 1 – Permit Details", expanded=False):
            st.text_input("Site", key="permit_site")
            st.text_input("Permit ID Number", key="permit_id")
            st.date_input("Start Date", key="start_date")
            st.date_input("End Date", key="end_date")
            st.text_input("Duration", key="duration")
            st.text_input("HV Permit Issuer", key="issuer")
            st.text_input("HV Permit Holder", key="holder")
            st.text_input("Lock Box Number", key="lock_box")
            st.text_area("Task Description", key="task_desc")
            st.checkbox("Post-work verification – dates and duration confirmed", key="post_work_verify")

        with st.expander("Part 2 – Permitted Work", expanded=False):
            st.caption("Description of work (Permit Issuer to complete)")
            st.text_area("Description of work", key="perm_work_desc")
            st.text_input("Work Authorisation reference (where applicable)", key="work_auth_ref")
            st.text_input("Company", key="company")

        with st.expander("Part 3 – Mains and Apparatus to be Accessed", expanded=False):
            st.text_input("Location", key="apparatus_location")
            st.text_input("System voltage", key="system_voltage")
            st.caption("List the areas and equipment to be accessed under this permit (pulled from trained library)")

        with st.expander("Part 4 – Attachments", expanded=False):
            st.file_uploader("Upload attachment(s)", type=["pdf", "docx", "jpg", "png"], key="attachments")

        with st.expander("Part 5 – Conditions and Requirements", expanded=False):
            st.caption("Permit conditions or requirements (Permit Issuer to complete)")
            for i in range(1, 11):
                st.text_area(f"Item {i}", key=f"cond_{i}")

        with st.expander("Part 6 – Permit Approval", expanded=False):
            st.write("**HV Permit Issuer Signature**")
            st.text_input("Name (printed) – Issuer", key="issuer_sig_name")
            if st.button("Submit for Approval – HV Permit Issuer", key="submit_issuer"):
                st.success("Approval request sent to HV Permit Issuer")
            st.write("**Electrical Engineer (or delegate) Signature**")
            st.text_input("Name (printed) – Engineer", key="engineer_sig_name")
            if st.button("Submit for Approval – Electrical Engineer", key="submit_engineer"):
                st.success("Approval request sent to Electrical Engineer")

        with st.expander("Part 7 – Pre-Isolation Tasks", expanded=False):
            st.caption("High Voltage Authorised Isolator to complete")
            st.checkbox("1. All required equipment is available for the job", key="pre_iso_1")
            st.checkbox("2. The high voltage test equipment has been checked", key="pre_iso_2")
            st.checkbox("3. Intention to isolate has been communicated", key="pre_iso_3")
            st.checkbox("4. Working earths are available and inspected", key="pre_iso_4")
            st.checkbox("5. Nearest live point(s) identified", key="pre_iso_5")
            st.checkbox("6. Latest HV Single Line Diagram attached", key="pre_iso_6")
            st.checkbox("7. High Voltage Isolation Verifier available", key="pre_iso_7")

        with st.expander("Part 8 – Switching Instructions (12 Step Process)", expanded=False):
            st.write("**Is an approved documented procedure available for this task?**")
            proc_available = st.radio("", ["Yes – attach copy and use in place of these instructions", "No – complete switching instructions below"], index=1, key="proc_radio")
            if proc_available == "No – complete switching instructions below":
                st.write("**Complete the 12 step switching instructions below**")
                st.table({
                    "Step": list(range(1,13)),
                    "Apparatus": [""]*12,
                    "Action": [""]*12,
                    "Permit Lock No.": [""]*12,
                    "Time": [""]*12,
                    "HV Isolator Initials": [""]*12,
                    "HV Isolation Verifier Initials": [""]*12
                })
                st.caption("Follows GCAA 12 step isolation process as required by Fatal Hazard Protocol 7")

        with st.expander("Isolation Verification", expanded=False):
            st.write("**Capture or upload verification photo (tablet ready)**")
            picture = st.camera_input("Take photo of isolation point", key="isolation_camera")
            if picture:
                st.success("Photo captured and saved to permit record")
                st.image(picture, use_container_width=True)
            uploaded = st.file_uploader("Or upload photo from device", type=["jpg", "png", "jpeg"], key="isolation_uploader")
            if uploaded:
                st.success("Photo uploaded and saved to permit record")
                st.image(uploaded, use_container_width=True)

        with st.expander("Part 9 – High Voltage Isolation (AR Verification by Isolator)", expanded=False):
            st.write("**Verification Photo – Lock Attached**")
            st.image(Image.open("Sub Locked Out.jpg"), 
                     caption="Verification Photo – Lock Attached (pre-loaded)", use_container_width=True)
            st.success("✅ AR Recognition: Lock detected at **Isolation Point 3**")
            st.image(Image.open("Substation Isolated LV.jpeg"), 
                     caption="Confirmed Isolation Status – Compartments Isolated / Energised", use_container_width=True)
            drawing = Image.open("Isolation drawing.jpg")
            drawing = drawing.resize((int(drawing.width * 0.5), int(drawing.height * 0.5)))
            st.image(drawing, caption="Isolation Drawing / Single Line Diagram – Additional AR Check", use_container_width=False)
            st.write("**HV Authorised Isolator Signature**")
            st.text_input("Name (printed) – Isolator", key="isolator_sig_name")
            st.text_input("Date / Time / Contact", key="isolator_sig_dt")
            st.write("**Isolation Verifier Signature**")
            st.text_input("Name (printed) – Verifier", key="verifier_sig_name")
            st.text_input("Date / Time / Contact", key="verifier_sig_dt")

        with st.expander("Part 10 – Permit Activation", expanded=False):
            st.caption("HV Permit Holder verifies isolation and attaches Permit Holder’s lock")
            st.text_input("Name (printed) – Permit Holder", key="activation_name")
            st.checkbox("I acknowledge isolation and verification are complete", key="activation_ack")

        with st.expander("Part 11 – Sign-on / Sign-off", expanded=False):
            st.caption("HV Permit Holder and Worker Sign-on / Sign-off / Handover")
            st.table({
                "Date": [""]*5,
                "Time": [""]*5,
                "Printed Name": [""]*5,
                "Signature": [""]*5,
                "Contact No": [""]*5
            })

        with st.expander("Part 12 – Working Earth Locations", expanded=False):
            st.caption("The location and details of working earths applied during the task")
            st.table({
                "Location and details": [""]*5,
                "Place by (printed name)": [""]*5,
                "HV Permit Holder initials": [""]*5,
                "Removed by (printed name)": [""]*5,
                "HV Permit Holder initials": [""]*5
            })

        with st.expander("Part 13 – Testing (Where applicable)", expanded=False):
            st.radio("Testing Procedure", ["Required", "Not Required"], key="testing_radio")
            st.caption("Testing to be directly supervised and each step initialled by the Permit Holder")
            st.checkbox("1. All personnel instructed to sign-off and remove personal locks", key="test_1")
            st.checkbox("2. High Voltage Authorised Isolator instructed to remove earths", key="test_2")
            st.checkbox("3. Permit Holder witnessed signature of isolator", key="test_3")
            st.table({
                "Testing Sign-on / Sign-off": [""]*3,
                "Date": [""]*3,
                "Time": [""]*3,
                "Signature": [""]*3
            })

        with st.expander("Part 14 – Task Monitoring and Inspection", expanded=False):
            st.caption("Includes supervisor, safety representatives, etc.")
            st.table({
                "Date": [""]*5,
                "Time": [""]*5,
                "Name (printed)": [""]*5,
                "Signature": [""]*5,
                "Comments": [""]*5
            })

        with st.expander("Part 15 – Permit Cancellation Pre-Restoration of Power", expanded=False):
            st.caption("The High Voltage Permit Holder is to complete the following checks")
            st.checkbox("1. Visual examination of area completed", key="pre_restore_1")
            st.checkbox("2. All tests completed and documented", key="pre_restore_2")
            st.checkbox("3. All earth bonds in place and secure", key="pre_restore_3")
            st.checkbox("4. All disconnected cables capped / insulated", key="pre_restore_4")
            st.checkbox("5. All identification labels and warning signs updated", key="pre_restore_5")
            st.checkbox("6. All barrier tape removed", key="pre_restore_6")
            st.checkbox("7. All personal locks removed and personnel signed off", key="pre_restore_7")
            st.checkbox("8. Work crews confirm equipment safe to operate", key="pre_restore_8")
            st.text_input("Name of person notified of intention to restore power", key="notified_person")
            st.text_input("Name (printed) – HV Permit Holder", key="pre_restore_holder")
            st.checkbox("I confirm all work completed or cancelled and equipment is safe", key="pre_restore_confirm")

        with st.expander("Part 16 – Restoration of Power", expanded=False):
            st.warning("⚠️ All energy source isolations are to include the 12 step process for isolation, as required by Glencore Fatal Hazard Protocol 7.")
            st.write("**Is an approved documented procedure available for this task?**")
            proc_restore = st.radio("", ["Yes – attach copy and use in place of these instructions", "No – complete switching instructions below"], index=1, key="proc_restore_radio")
            if proc_restore == "No – complete switching instructions below":
                st.write("**Complete the 12 step switching instructions below**")
                st.table({
                    "Step": list(range(1,13)),
                    "Apparatus": [""]*12,
                    "Action": [""]*12,
                    "Permit Lock No.": [""]*12,
                    "Time": [""]*12,
                    "HV Isolator Initials": [""]*12,
                    "HV Isolation Verifier Initials": [""]*12
                })
            st.caption("Restoration of power completed by HV Authorised Isolator")

        with st.expander("Part 17 – Permit Completion (HV Permit Holder to complete)", expanded=False):
            st.warning("⚠️ Only return plant or equipment to service when this permit is complete or cancelled and all signatures have been completed.")
            st.checkbox("Permit activities complete", key="part17_complete")
            st.checkbox("Permit activities incomplete (comments needed)", key="part17_incomplete")
            st.caption("The job / task activities authorised by this permit are complete, or are no longer needed. All applicable inspections have been completed. No further work is permitted under the authority of this permit.")
            st.text_area("Comments (Cancellation is to include all reasons)", key="part17_comments")
            st.write("**High Voltage Authorised Isolator (When authorised by the HV Permit Holder)**")
            st.caption("I have confirmed with the HV Permit Holder that the permit has been cancelled or completed. By signing as the High Voltage Authorised Isolator, I confirm that de-isolation has been completed and: - Power has been restored to the mains and apparatus covered by this permit following approved switching instructions. - I confirm that only the permit locks recorded on this permit have been removed.")
            st.table({
                "Date": [""]*3,
                "Time": [""]*3,
                "Contact details (phone / radio)": [""]*3,
                "Name (printed)": [""]*3,
                "Signature": [""]*3
            })

        with st.expander("Part 18 – Permit Review", expanded=False):
            st.caption("To be completed by an authorised Electrical Engineer or delegate")
            st.text_area("Comments (include any follow-up actions required)", key="review_comments")
            st.text_input("Name (printed) – Reviewer", key="reviewer_name")
            st.checkbox("This permit has been reviewed and complies with standards", key="review_confirm")

        if st.button("Finish Full Permit & Submit", key="finish_permit"):
            st.success("Full HV isolation permit completed and submitted to equipment library.")

    else:
        st.warning("Please complete the Training Model section first.")

with tab3:  # TVL Observation
    st.subheader("TVL – Targeted Visible Leadership Observation (FRM1277)")
    st.markdown("Complete the electrical safety and isolation observation checklist.")

    st.write("**Observation Details**")
    st.text_input("Date", key="tvl_date")
    st.text_input("Time", key="tvl_time")
    st.text_input("Location", key="tvl_location")
    st.selectbox("Shift", ["Day", "Afternoon", "Night"], key="tvl_shift")
    st.text_input("Observation Team Leader", key="tvl_leader")
    st.text_input("Description of Work being Performed", key="tvl_description")

    st.subheader("Linked Job / Permit")
    linked_job = st.selectbox("Select Linked Permit / Job", ["HV-2026-001 (Substation Isolation)", "HV-2026-002 (Conveyor Drive)"], key="linked_job")
    if linked_job and st.session_state.training_complete:
        st.image(Image.open("Sub Locked Out.jpg"), 
                 caption=f"Isolation Lock Photo from Linked Job: {linked_job}", use_container_width=True)
        st.success("✅ Linked isolation lock photo pulled from permit record")

    st.write("**Electrical Supervisor Credentials**")
    st.checkbox("1. Check of supervisor appointment", key="tvl_sup_1")
    st.checkbox("2. Check for presence of No Plan No Work booklet", key="tvl_sup_2")

    st.write("**Isolation & Personal Locks**")
    st.checkbox("1. Complete an audit on a work area to ensure compliance to isolation procedure", key="tvl_lock_1")
    st.checkbox("2. Challenge test a coal mine worker to ensure they have locks with them on the worksite", key="tvl_lock_2")

    st.write("**Electrical Area Signage**")
    st.checkbox("1. Are relevant and easily explainable", key="tvl_sign_1")
    st.checkbox("2. Encompasses the correct details and cover all entry points", key="tvl_sign_2")
    st.checkbox("3. Clearly define all details of qualifications", key="tvl_sign_3")
    st.checkbox("4. Clearly legible and are to Australian standards", key="tvl_sign_4")

    st.write("**New Starters – Electrical Workers**")
    st.checkbox("1. Verify Electrical Licence currency", key="tvl_new_1")
    st.checkbox("2. Verify EEHA currency", key="tvl_new_2")
    st.checkbox("3. Verify LVR/CPR competency", key="tvl_new_3")
    st.checkbox("4. Verify EEHA Challenge Test", key="tvl_new_4")

    st.write("**Access to Exposed Conductors**")
    col1, col2 = st.columns([3, 1])
    with col1:
        hv_access = st.checkbox("1. High Voltage Access Permits", key="tvl_access_1")
    with col2:
        if st.button("View Live Permit", key="view_hv_access"):
            st.session_state.show_permit_preview = "High Voltage Access Permit"
    
    col1, col2 = st.columns([3, 1])
    with col1:
        group_iso = st.checkbox("2. Group Isolation Permits", key="tvl_access_2")
    with col2:
        if st.button("View Live Permit", key="view_group_iso"):
            st.session_state.show_permit_preview = "Group Isolation Permit"
    
    col1, col2 = st.columns([3, 1])
    with col1:
        sys_impair = st.checkbox("3. System Impairment Permits – Electrical", key="tvl_access_3")
    with col2:
        if st.button("View Live Permit", key="view_sys_impair"):
            st.session_state.show_permit_preview = "System Impairment Permit"

    if st.session_state.show_permit_preview:
        with st.expander(f"🔍 Live Permit View: {st.session_state.show_permit_preview} (View Only)", expanded=True):
            st.info(f"📋 Showing live {st.session_state.show_permit_preview} for review by TVL Supervisor")
            st.caption("In the full app this would display the actual permit being filled out in real-time (view-only mode)")
            st.text_input("Permit ID", value="HV-2026-001", disabled=True)
            st.text_area("Task Description", value="Isolation of mobile substation for maintenance", disabled=True)
            st.success("✅ Permit is being followed correctly")
            if st.button("Close Live Permit View"):
                st.session_state.show_permit_preview = None
                st.rerun()

    st.write("**Maintenance & Compliance of Electrical Equipment**")
    st.checkbox("1. Have inspections been completed when due?", key="tvl_maint_1")
    st.checkbox("2. Ensure locking mechanisms are maintained", key="tvl_maint_2")

    st.write("**Training**")
    st.checkbox("1. Ensure all coal mine workers have been trained in the isolation procedure", key="tvl_train_1")

    st.write("**Arc Flash Protection**")
    st.checkbox("1. Wearing Arc-Flash Clothing", key="tvl_arc_1")
    st.checkbox("2. Carrying Trolex Non-Contact Voltage Tester", key="tvl_arc_2")

    st.write("**Testing and Tagging**")
    st.checkbox("1. Audit and ensure regular insulation and continuity tests completed", key="tvl_test_1")

    st.text_area("What was done well?", key="tvl_well")
    st.text_area("Opportunities for improvement?", key="tvl_improve")
    st.text_area("Other Comments?", key="tvl_comments")

    if st.button("Submit TVL Observation", key="submit_tvl"):
        st.success("TVL observation logged successfully and linked to selected permit.")

with tab4:  # 12 Step Isolation Reference
    st.subheader("12 Step Isolation Reference (for Permit Holder)")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            img = Image.open("12stepiso.png")
            img = img.resize((int(img.width * 0.5), int(img.height * 0.5)))
            st.image(img, caption="12 Step Isolation Process", use_container_width=True)
        except FileNotFoundError:
            st.info("12stepiso.png not found – please ensure the file is in the same folder as the app.")
    st.caption("This reference is taken directly from our isolation document and is always available for the permit holder.")
    st.write("**The 12 steps are:**")
    steps = [
        "1. Identify energy sources", "2. Advise relevant parties", "3. Stop, isolate and secure",
        "4. Lock and tag", "5. Verify (test for dead)", "6. Commence work",
        "7. Complete work", "8. Check work", "9. Clear area",
        "10. Remove tags and locks", "11. Restore energy", "12. Check operation"
    ]
    for step in steps:
        st.write(step)

with tab5:  # Equipment Library
    st.subheader("Equipment Library")
    st.caption("Catalogued plant with AR verification data")
    search_term = st.text_input("Search by Equipment Name or Type", key="eq_search")
    dummy_equipment = [
        {"Equipment": "Mobile Substation", "Type": "HV", "Isolation Points": 3, "Last Trained": "2026-03-15", "AR Status": "Ready"},
        {"Equipment": "Conveyor Drive Motor", "Type": "LV", "Isolation Points": 2, "Last Trained": "2026-03-20", "AR Status": "Ready"},
        {"Equipment": "HV Switchgear Panel", "Type": "HV", "Isolation Points": 4, "Last Trained": "2026-03-25", "AR Status": "Ready"},
        {"Equipment": "Feeder Breaker", "Type": "HV", "Isolation Points": 1, "Last Trained": "2026-03-10", "AR Status": "Pending"}
    ]
    filtered_eq = [eq for eq in dummy_equipment if search_term.lower() in str(eq).lower()] or dummy_equipment
    st.table(filtered_eq)

with tab6:  # Permit History
    st.subheader("Permit History")
    st.caption("Searchable store of completed permits")
    search_term = st.text_input("Search by Permit ID, Date or Equipment", key="permit_search")
    dummy_history = [
        {"Permit ID": "HV-2026-001", "Date": "2026-03-15", "Equipment": "Mobile Substation", "Status": "Completed"},
        {"Permit ID": "HV-2026-002", "Date": "2026-03-20", "Equipment": "Conveyor Drive", "Status": "Completed"},
        {"Permit ID": "HV-2026-003", "Date": "2026-03-25", "Equipment": "HV Switchgear", "Status": "Completed"}
    ]
    filtered = [p for p in dummy_history if search_term.lower() in str(p).lower()] or dummy_history
    st.table(filtered)

st.caption("MOSLock Lite – Training & Permit Demo. Focused version for underground coal EEM review.")