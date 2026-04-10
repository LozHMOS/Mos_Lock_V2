"""
MOSLock Lite – Training & Permit Demo v0.2
Improved demonstration for Underground Coal Operations.
Standards: STD0930 | FRM1277 | Glencore Fatal Hazard Protocol 7 | AS/NZS 4836
"""

import streamlit as st
from PIL import Image
import datetime
import pandas as pd

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="MOSLock Lite – Training & Permit",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] { gap: 6px; }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        padding: 0 16px;
        background-color: #e8ecf0;
        border-radius: 6px 6px 0 0;
        font-weight: 600;
        font-size: 13px;
        color: #212529;               /* ensures tab text is always dark */
    }
    div[data-testid="metric-container"] {
        background: #f0f4f8;
        border-left: 4px solid #1e3a5f;
        border-radius: 6px;
        padding: 12px;
        color: #212529;
    }
    .section-header {
        background: linear-gradient(90deg, #1e3a5f, #2d6096);
        color: white;
        padding: 8px 16px;
        border-radius: 6px;
        margin: 12px 0 8px 0;
        font-weight: 700;
        font-size: 15px;
    }
    /* Risk boxes – fixed contrast (only change made) */
    .risk-low { 
        background:#d4edda; 
        border-left:4px solid #28a745; 
        padding:8px 14px; 
        border-radius:4px; 
        margin:4px 0; 
        color: #212529 !important; 
    }
    .risk-medium { 
        background:#fff3cd; 
        border-left:4px solid #ffc107; 
        padding:8px 14px; 
        border-radius:4px; 
        margin:4px 0; 
        color: #212529 !important; 
    }
    .risk-high { 
        background:#f8d7da; 
        border-left:4px solid #dc3545; 
        padding:8px 14px; 
        border-radius:4px; 
        margin:4px 0; 
        color: #212529 !important; 
    }
    .lock-counter {
        background: #1e3a5f;
        color: white;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
        font-size: 20px;
        font-weight: 700;
    }
    .step-complete { color: #28a745; font-weight: 700; }
    .step-active { color: #007bff; font-weight: 700; }
    .step-pending { color: #adb5bd; }
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE ───────────────────────────────────────────────────────────────
defaults = {
    'training_complete': False,
    'rules': [],
    'lock_photo': None,
    'show_permit_preview': None,
    'permit_status': 'Draft',
    'parts_complete': set(),
    'signed_on_workers': [],
    'lock_count': 0,
    'active_permits': 2,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── HELPER: safe image loader ───────────────────────────────────────────────────
def safe_image(path, caption="", **kwargs):
    """Load an image or show a placeholder if the file is not found."""
    try:
        img = Image.open(path)
        st.image(img, caption=caption, **kwargs)
        return True
    except FileNotFoundError:
        st.info(f"📷 Image placeholder: *{path}* (place this file in the app directory)")
        return False

# ─── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🔒 MOSLock Lite")
    st.markdown("*Safety-Critical Permit System*")
    st.markdown("---")

    st.markdown("### 👤 Current User")
    user_name = st.text_input("Name", value="J. Smith", key="sidebar_user")
    user_role = st.selectbox(
        "Role",
        ["HV Permit Issuer", "HV Permit Holder", "HV Authorised Isolator",
         "Electrical Engineer", "Supervisor"],
        key="sidebar_role"
    )

    st.markdown("---")
    st.markdown("### 🏭 Site & Shift")
    site = st.selectbox(
        "Mine Site",
        ["Bulga Underground", "Ulan Underground", "Mandalong"],
        key="sidebar_site"
    )
    shift = st.selectbox(
        "Current Shift",
        ["Day (06:00–18:00)", "Night (18:00–06:00)"],
        key="sidebar_shift"
    )

    st.markdown("---")
    st.markdown("### 📊 Live Stats")
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric("Active Permits", st.session_state.active_permits)
    with col_s2:
        st.metric("Locks On Box", st.session_state.lock_count)

    if st.session_state.signed_on_workers:
        st.markdown(f"**Signed On:** {len(st.session_state.signed_on_workers)} worker(s)")
        for w in st.session_state.signed_on_workers:
            st.markdown(f"  ✅ {w}")

    st.markdown("---")
    st.markdown("### 🚨 Emergency Contacts")
    st.markdown("""
**Mine Rescue:** 000  
**Shift Supervisor:** Ch. 1  
**Control Room:** Ch. 3  
**First Aid:** Level 2 South  
""")
    st.markdown("---")
    st.caption("MOSLock Lite v0.2 | STD0930 / FHP-07")

# ─── MAIN HEADER ────────────────────────────────────────────────────────────────
st.title("🔒 MOSLock Lite – Training & Permit System")

# Status banner
if not st.session_state.training_complete:
    st.warning("⚠️  **Setup Required:** Complete Equipment Training (Tab 1 – Training Model) before issuing HV Permits.")
else:
    status_icons = {
        "Draft": "🔵", "Submitted": "🟡", "Issuer Approved": "🟠",
        "Engineer Approved": "🟠", "Active": "🟢", "Completed": "⚫"
    }
    icon = status_icons.get(st.session_state.permit_status, "⚪")
    st.success(
        f"✅ Equipment trained and ready.  Current Permit Status: {icon} **{st.session_state.permit_status}**"
    )

# Top KPI row
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
with kpi1:
    st.metric("Active HV Permits", "2")
with kpi2:
    st.metric("Permits Today", "4", delta="+1")
with kpi3:
    lib_delta = "+1" if st.session_state.training_complete else "0"
    st.metric("Equipment in Library", "4" if st.session_state.training_complete else "3", delta=lib_delta)
with kpi4:
    st.metric("TVL Observations (Week)", "3")
with kpi5:
    compliance = "94%" if st.session_state.training_complete else "87%"
    st.metric("Compliance Score", compliance, delta="+2%")

st.caption("**Demo – Underground Coal Operations** | STD0930 | Glencore Fatal Hazard Protocol 7 | AS/NZS 4836")
st.markdown("---")

# ─── TABS ────────────────────────────────────────────────────────────────────────
tab0, tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Dashboard",
    "🎓 Training Model",
    "⚡ HV Access Permit",
    "👁️ TVL Observation",
    "📋 12 Step Reference",
    "🗄️ Equipment Library",
    "📁 Permit History",
])

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 0 – DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════
with tab0:
    st.subheader("📊 Operational Dashboard")

    # Safety alerts
    st.markdown(
        '<div class="risk-high">🚨 <strong>SAFETY ALERT:</strong> '
        'Permit HV-2026-001 expires in 2 hours — Permit Holder must sign off or request extension.</div>',
        unsafe_allow_html=True
    )
    st.markdown("")
    st.markdown(
        '<div class="risk-medium">⚠️ <strong>NOTICE:</strong> '
        'TVL Observation due today for Zone B Substation.</div>',
        unsafe_allow_html=True
    )
    st.markdown("")

    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.markdown("### 📋 Active Permits")
        active_permits_data = [
            {
                "id": "HV-2026-001", "equipment": "Mobile Substation",
                "holder": "J. Smith", "issuer": "R. Jones",
                "status": "Active", "expires": "Today 18:00",
                "workers": 3, "locks": 4
            },
            {
                "id": "HV-2026-004", "equipment": "Feeder Breaker",
                "holder": "M. Brown", "issuer": "R. Jones",
                "status": "Approved", "expires": "Tomorrow 06:00",
                "workers": 2, "locks": 2
            },
        ]
        for p in active_permits_data:
            status_dot = "🟢" if p["status"] == "Active" else "🔵"
            with st.expander(
                f"{status_dot} **{p['id']}** — {p['equipment']} | "
                f"Status: {p['status']} | Expires: {p['expires']}"
            ):
                c1, c2, c3 = st.columns(3)
                with c1:
                    st.write(f"**Permit Holder:** {p['holder']}")
                    st.write(f"**Issuer:** {p['issuer']}")
                with c2:
                    st.write(f"**Workers Signed On:** {p['workers']}")
                    st.write(f"**Locks on Box:** {p['locks']}")
                with c3:
                    # Lock count safety check: locks should equal workers + 1 (isolator lock)
                    if p['locks'] == p['workers'] + 1:
                        st.markdown('<div class="risk-low">✅ Lock count verified</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(
                            '<div class="risk-high">🚨 Lock count mismatch – investigate immediately</div>',
                            unsafe_allow_html=True
                        )
                    if st.button(f"View Full Permit", key=f"dash_view_{p['id']}"):
                        st.info("Full permit opens in HV Access Permit tab (production behaviour).")

        st.markdown("### 📈 Weekly Permit Activity")
        chart_data = pd.DataFrame({
            "Day": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
            "Permits Issued": [2, 3, 1, 4, 2, 1, 0],
            "Completed": [2, 2, 1, 3, 2, 1, 0],
        })
        st.bar_chart(chart_data.set_index("Day"))

    with col_right:
        st.markdown("### 🔒 Lock Box Status")
        st.markdown(
            f'<div class="lock-counter">🔒<br>{st.session_state.lock_count}<br>'
            f'<small>Locks on Box</small></div>',
            unsafe_allow_html=True
        )
        st.markdown("")

        st.markdown("**Quick Sign-On (Permit HV-2026-001)**")
        new_worker = st.text_input("Worker Name", key="dash_new_worker")
        if st.button("✅ Sign On", key="dash_sign_on"):
            if new_worker and new_worker not in st.session_state.signed_on_workers:
                st.session_state.signed_on_workers.append(new_worker)
                st.session_state.lock_count += 1
                st.rerun()
            elif new_worker in st.session_state.signed_on_workers:
                st.warning(f"{new_worker} is already signed on.")

        if st.session_state.signed_on_workers:
            st.markdown("**Currently Signed On:**")
            for i, w in enumerate(st.session_state.signed_on_workers):
                wc1, wc2 = st.columns([3, 1])
                with wc1:
                    st.write(f"✅ {w}")
                with wc2:
                    if st.button("Off", key=f"dash_signoff_{i}"):
                        st.session_state.signed_on_workers.remove(w)
                        if st.session_state.lock_count > 0:
                            st.session_state.lock_count -= 1
                        st.rerun()

        st.markdown("---")
        st.markdown("### ⚡ Zone Isolation Status")
        st.markdown("""
| Zone | Status |
|------|--------|
| Substation A | 🔴 Isolated |
| Conveyor 3 | 🟢 Live |
| HV Panel B3 | 🔴 Isolated |
| Feeder Breaker | 🟡 Pending |
""")
        st.markdown("---")
        st.markdown("### 📅 Today's Progress")
        st.progress(75, text="3/4 Permits Completed Today")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 – TRAINING MODEL
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.subheader("🎓 New Equipment Training Model")
    st.markdown(
        "Train the AI/AR model on new equipment by defining isolation points, "
        "compartments, indicators, and the IFTTT logic the model will learn."
    )

    # Step progress indicator
    current_step = 4 if st.session_state.training_complete else (3 if st.session_state.rules else 2)

    def step_icon(n):
        if current_step > n:
            return "✅"
        elif current_step == n:
            return "🔵"
        return "⭕"

    st.markdown(f"""
    <div style="display:flex; gap:16px; margin-bottom:16px; padding:12px;
                background:#f0f4f8; border-radius:8px; flex-wrap:wrap;">
        <span class="{'step-complete' if current_step>1 else 'step-active' if current_step==1 else 'step-pending'}">
            {step_icon(1)} Step 1: Equipment Photo
        </span> →
        <span class="{'step-complete' if current_step>2 else 'step-active' if current_step==2 else 'step-pending'}">
            {step_icon(2)} Step 2: Define Points
        </span> →
        <span class="{'step-complete' if current_step>3 else 'step-active' if current_step==3 else 'step-pending'}">
            {step_icon(3)} Step 3: Logic Rules
        </span> →
        <span class="{'step-complete' if st.session_state.training_complete else 'step-pending'}">
            {step_icon(4)} Step 4: Submit
        </span>
    </div>
    """, unsafe_allow_html=True)

    # ── Step 1 ──────────────────────────────────────────────────────────────────
    st.markdown('<div class="section-header">Step 1 – Equipment Photo & Details</div>', unsafe_allow_html=True)

    col_photo, col_meta = st.columns([2, 1])
    with col_photo:
        safe_image(
            "Substation.jpeg",
            caption="Equipment – Mobile Substation (clean photo for AI training)",
            use_container_width=True
        )
        custom_photo = st.file_uploader(
            "Upload a custom equipment photo",
            type=["jpg", "jpeg", "png"],
            key="custom_photo"
        )
        if custom_photo:
            st.image(custom_photo, caption="Custom Equipment Photo", use_container_width=True)
            st.success("✅ Custom photo loaded for training.")

    with col_meta:
        st.markdown("**Equipment Details**")
        eq_name     = st.text_input("Equipment Name", value="Mobile Substation", key="eq_name")
        eq_type     = st.selectbox("Voltage Class", ["HV (>1000 V)", "LV (≤1000 V)", "Control Circuit"], key="eq_type")
        eq_voltage  = st.text_input("System Voltage", value="11 kV", key="eq_voltage")
        eq_location = st.text_input("Typical Location", value="Zone B – Underground", key="eq_location")
        eq_make     = st.text_input("Make / Model", key="eq_make")
        eq_serial   = st.text_input("Serial / Asset No.", key="eq_serial")

    # ── Step 2 ──────────────────────────────────────────────────────────────────
    st.markdown(
        '<div class="section-header">Step 2 – Define Isolation Points, Compartments & Indicators</div>',
        unsafe_allow_html=True
    )
    st.info(
        "💡 **Full app:** Tap directly on the equipment photo to pin each point. "
        "Here, use the selectors to define counts, then label each point below."
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        num_iso   = st.selectbox("Isolation Points", [1, 2, 3, 4, 5], index=2, key="num_iso")
    with c2:
        num_comp  = st.selectbox("Compartments",     [1, 2, 3, 4, 5], index=2, key="num_comp")
    with c3:
        num_ind   = st.selectbox("Indicators",       [1, 2, 3],       index=1, key="num_ind")
    with c4:
        num_earth = st.selectbox("Earth Points",     [0, 1, 2, 3, 4], index=1, key="num_earth")

    st.markdown("**Label each Isolation Point:**")
    iso_cols = st.columns(num_iso)
    for i, col in enumerate(iso_cols):
        with col:
            st.markdown(f"**IP {i+1}**")
            st.selectbox(
                "Device Type",
                ["Circuit Breaker", "Isolator Switch", "Fuse", "Disconnect"],
                key=f"ip_type_{i}"
            )
            st.text_input("Label / ID", value=f"ISO-{i+1:02d}", key=f"ip_label_{i}")

    # ── Step 3 ──────────────────────────────────────────────────────────────────
    st.markdown(
        '<div class="section-header">Step 3 – If This Then That (IFTTT) Logic Rules</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        "Define what the AI model should expect when each isolation point is operated. "
        "These rules drive the AR verification engine."
    )

    btn_add, btn_clear = st.columns([1, 5])
    with btn_add:
        if st.button("➕ Add Rule", key="add_rule"):
            st.session_state.rules.append({
                "iso": 1, "cond": "Isolated",
                "comp": 1, "comp_status": "Isolated",
                "ind": 1,  "ind_status": "Lit",
                "risk": "Safe to Access"
            })
    with btn_clear:
        if st.session_state.rules and st.button("🗑️ Clear All Rules", key="clear_rules"):
            st.session_state.rules = []
            st.rerun()

    for i, rule in enumerate(st.session_state.rules):
        st.markdown("---")
        hdr_col, del_col = st.columns([10, 1])
        with hdr_col:
            st.markdown(f"**Rule {i+1}**")
        with del_col:
            if st.button("❌", key=f"del_rule_{i}"):
                st.session_state.rules.pop(i)
                st.rerun()

        r1, r2, r3, r4 = st.columns(4)
        with r1:
            st.markdown("**🔌 IF** Isolation Point")
            rule["iso"]  = st.selectbox(
                "Point #", list(range(1, num_iso + 1)),
                index=min(rule["iso"] - 1, num_iso - 1), key=f"iso_{i}"
            )
            rule["cond"] = st.selectbox("State", ["Isolated", "Not Isolated"], key=f"cond_{i}")
        with r2:
            st.markdown("**📦 THEN** Compartment")
            rule["comp"]        = st.selectbox(
                "Comp #", list(range(1, num_comp + 1)),
                index=min(rule["comp"] - 1, num_comp - 1), key=f"comp_{i}"
            )
            rule["comp_status"] = st.selectbox("Status", ["Isolated", "Energised"], key=f"comp_status_{i}")
        with r3:
            st.markdown("**💡 AND** Indicator")
            rule["ind"]        = st.selectbox(
                "Indicator #", list(range(1, num_ind + 1)),
                index=min(rule["ind"] - 1, num_ind - 1), key=f"ind_{i}"
            )
            rule["ind_status"] = st.selectbox("State", ["Lit", "Off"], key=f"ind_status_{i}")
        with r4:
            st.markdown("**⚠️ Access Risk**")
            rule["risk"] = st.selectbox(
                "Result",
                ["Safe to Access", "Unsafe – Do Not Access", "Requires Additional Verification"],
                key=f"risk_{i}"
            )
            if rule["risk"] == "Safe to Access":
                st.markdown('<div class="risk-low">🟢 SAFE</div>', unsafe_allow_html=True)
            elif rule["risk"] == "Unsafe – Do Not Access":
                st.markdown('<div class="risk-high">🔴 UNSAFE</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="risk-medium">🟡 VERIFY</div>', unsafe_allow_html=True)

    # ── Step 4 ──────────────────────────────────────────────────────────────────
    st.markdown(
        '<div class="section-header">Step 4 – Submit for AI Library Approval</div>',
        unsafe_allow_html=True
    )

    can_submit = len(st.session_state.rules) > 0
    if not can_submit:
        st.warning("⚠️ Add at least one logic rule (Step 3) before submitting.")

    col_sub, col_trained = st.columns(2)
    with col_sub:
        approved_by = st.text_input(
            "Submitted by (Electrical Engineer or authorised delegate)",
            key="approved_by"
        )
        if st.button(
            "📤 Submit for Approval to AI Library",
            key="submit_ai_library",
            disabled=not can_submit
        ):
            if approved_by.strip():
                st.success(
                    "✅ Equipment submitted. AI model training initiated — awaiting Electrical Engineer approval."
                )
                st.session_state.training_complete = True
                st.session_state.permit_status = "Draft"
                # st.balloons()
            else:
                st.error("Enter the name of the approving Electrical Engineer before submitting.")

    with col_trained:
        if st.session_state.training_complete:
            st.markdown("**✅ Training Complete — AR Annotation Preview:**")
            safe_image(
                "Substation Trained.jpeg",
                caption="Trained equipment with AI/AR visual annotations",
                use_container_width=True
            )
            st.success(
                f"Model trained on {num_iso} isolation point(s), "
                f"{num_comp} compartment(s), {num_ind} indicator(s), "
                f"{len(st.session_state.rules)} logic rule(s)."
            )

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 – HV ACCESS PERMIT (STD0930 — 18 Parts)
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.subheader("⚡ High Voltage Access Permit (STD0930)")

    if not st.session_state.training_complete:
        st.error(
            "🚫 **Cannot issue permit:** Equipment must be trained and approved first. "
            "Complete Tab 1 – Training Model."
        )
        st.stop()

    # Permit workflow status bar
    statuses = ["Draft", "Submitted", "Issuer Approved", "Engineer Approved", "Active", "Completed"]
    current_idx = statuses.index(st.session_state.permit_status) \
        if st.session_state.permit_status in statuses else 0

    st.markdown("**Permit Workflow:**")
    s_cols = st.columns(len(statuses))
    for i, (scol, s) in enumerate(zip(s_cols, statuses)):
        with scol:
            if i < current_idx:
                st.markdown(f"✅ ~~{s}~~")
            elif i == current_idx:
                st.markdown(f"🔵 **{s}**")
            else:
                st.markdown(f"⭕ {s}")

    pct = int((current_idx / (len(statuses) - 1)) * 100)
    st.progress(pct, text=f"Permit Progress: {pct}%")
    parts_done = len(st.session_state.parts_complete)
    st.caption(f"Parts completed: {parts_done} / 18")
    st.markdown("---")

    def mark_done(n):
        st.session_state.parts_complete.add(n)

    # ── Part 1 ──────────────────────────────────────────────────────────────────
    with st.expander("Part 1 – Permit Details", expanded=False):
        mark_done(1)
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Site", value="Bulga Underground Operations", key="permit_site")
            st.text_input("Permit ID Number", value="HV-2026-005", key="permit_id")
            st.date_input("Start Date", value=datetime.date.today(), key="start_date")
            st.date_input("End Date",   value=datetime.date.today(), key="end_date")
        with c2:
            st.text_input("Duration", key="duration")
            st.text_input("HV Permit Issuer",  key="issuer")
            st.text_input("HV Permit Holder",  key="holder")
            st.text_input("Lock Box Number",   key="lock_box")
        st.text_area(
            "Task Description",
            placeholder="Describe the work to be performed under this permit…",
            key="task_desc"
        )
        st.checkbox("Post-work verification — dates and duration confirmed", key="post_work_verify")

    # ── Part 2 ──────────────────────────────────────────────────────────────────
    with st.expander("Part 2 – Permitted Work", expanded=False):
        mark_done(2)
        st.caption("Permit Issuer to complete")
        st.text_area("Description of Work", key="perm_work_desc")
        st.text_input("Work Authorisation Reference", key="work_auth_ref")
        st.text_input("Company", key="company")

    # ── Part 3 ──────────────────────────────────────────────────────────────────
    with st.expander("Part 3 – Mains and Apparatus to be Accessed", expanded=False):
        mark_done(3)
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Location", key="apparatus_location")
        with c2:
            st.text_input("System Voltage", value="11 kV", key="system_voltage")
        st.markdown("**Select equipment from Trained Library:**")
        st.multiselect(
            "Equipment to be accessed",
            [
                "Mobile Substation (HV) — 3 Isolation Points",
                "Conveyor Drive Motor (LV) — 2 Isolation Points",
                "HV Switchgear Panel B3 — 4 Isolation Points",
                "Feeder Breaker (HV) — 1 Isolation Point",
            ],
            key="selected_equipment"
        )

    # ── Part 4 ──────────────────────────────────────────────────────────────────
    with st.expander("Part 4 – Attachments", expanded=False):
        mark_done(4)
        st.file_uploader(
            "Upload attachments (SLD, JSA, risk assessment, procedures, etc.)",
            type=["pdf", "docx", "jpg", "png"],
            accept_multiple_files=True,
            key="attachments"
        )

    # ── Part 5 ──────────────────────────────────────────────────────────────────
    with st.expander("Part 5 – Conditions and Requirements", expanded=False):
        mark_done(5)
        st.caption("Permit Issuer to complete")
        standard_conds = [
            "Wear appropriate arc-flash PPE at all times within the exclusion zone",
            "Test before touch — always verify dead before accessing conductors",
            "Two-person rule applies — no one works alone on HV equipment",
            "Working earths must be applied before access is permitted",
            "Maintain radio contact with control room throughout task",
        ]
        for i, cond in enumerate(standard_conds):
            st.checkbox(cond, value=True, key=f"std_cond_{i}")
        st.text_area("Additional site-specific conditions", key="additional_conds")

    # ── Part 6 ──────────────────────────────────────────────────────────────────
    with st.expander("Part 6 – Permit Approval", expanded=False):
        mark_done(6)
        c1, c2 = st.columns(2)
        with c1:
            st.write("**HV Permit Issuer Signature**")
            st.text_input("Name (printed) – Issuer", key="issuer_sig_name")
            if st.button("✍️ Submit for Issuer Approval", key="submit_issuer"):
                st.session_state.permit_status = "Submitted"
                st.success("✅ Approval request sent to HV Permit Issuer.")
        with c2:
            st.write("**Electrical Engineer (or delegate) Signature**")
            st.text_input("Name (printed) – Engineer", key="engineer_sig_name")
            if st.button("✍️ Submit for Engineer Approval", key="submit_engineer"):
                st.session_state.permit_status = "Engineer Approved"
                st.success("✅ Approval request sent to Electrical Engineer.")

    # ── Part 7 ──────────────────────────────────────────────────────────────────
    with st.expander("Part 7 – Pre-Isolation Tasks", expanded=False):
        mark_done(7)
        st.caption("High Voltage Authorised Isolator to complete")
        pre_iso_items = [
            "All required equipment is available for the job",
            "High voltage test equipment checked and calibrated",
            "Intention to isolate communicated to all affected parties",
            "Working earths available and visually inspected",
            "Nearest live point(s) identified and barriers erected",
            "Latest HV Single Line Diagram attached and reviewed",
            "HV Isolation Verifier confirmed available on site",
        ]
        checks = [st.checkbox(f"{i+1}. {c}", key=f"pre_iso_{i}") for i, c in enumerate(pre_iso_items)]
        remaining = checks.count(False)
        if remaining == 0:
            st.success("✅ All pre-isolation tasks complete.")
        else:
            st.warning(f"⚠️ {remaining} pre-isolation task(s) still to complete.")

    # ── Part 8 – Switching Instructions ─────────────────────────────────────────
    with st.expander("Part 8 – Switching Instructions (12 Step Process)", expanded=False):
        mark_done(8)
        st.warning(
            "⚠️ Fatal Hazard Protocol 7 requires strict adherence to the 12-step isolation process."
        )
        proc_avail = st.radio(
            "Is an approved documented procedure available for this task?",
            ["Yes – attach copy and use in place of these instructions",
             "No – complete switching instructions below"],
            index=1, key="proc_radio"
        )
        if "No" in proc_avail:
            st.write("**Complete the 12 step switching instructions:**")
            switch_df = pd.DataFrame({
                "Step": list(range(1, 13)),
                "Apparatus": [""] * 12,
                "Action":    [""] * 12,
                "Permit Lock No.": [""] * 12,
                "Time":      [""] * 12,
                "HV Isolator Initials":  [""] * 12,
                "HV Verifier Initials":  [""] * 12,
            })
            st.dataframe(switch_df, use_container_width=True)
            st.caption("Table is editable in the full application.")

    # ── Isolation Verification Photo ────────────────────────────────────────────
    with st.expander("Isolation Verification – Photo Capture", expanded=False):
        mark_done(8)
        st.markdown(
            '<div class="risk-high">🚨 Mandatory: Capture or upload a verification photo '
            'before proceeding to Part 9.</div>',
            unsafe_allow_html=True
        )
        st.markdown("")
        cam_col, up_col = st.columns(2)
        with cam_col:
            st.write("**📷 Tablet / Mobile Camera**")
            picture = st.camera_input("Take photo of isolation point", key="isolation_camera")
            if picture:
                st.success("✅ Photo captured and saved to permit record.")
                st.image(picture, use_container_width=True)
        with up_col:
            st.write("**📁 Upload from Device**")
            uploaded = st.file_uploader(
                "Upload isolation photo", type=["jpg", "png", "jpeg"],
                key="isolation_uploader"
            )
            if uploaded:
                st.success("✅ Photo uploaded and saved to permit record.")
                st.image(uploaded, use_container_width=True)

    # ── Part 9 – AR Verification ─────────────────────────────────────────────────
    with st.expander("Part 9 – HV Isolation Verification (AI/AR)", expanded=False):
        mark_done(9)
        st.markdown(
            '<div class="section-header">AI / AR Verification Engine</div>',
            unsafe_allow_html=True
        )

        col_lock_img, col_iso_confirm = st.columns(2)
        with col_lock_img:
            st.write("**🔒 Verification Photo – Lock Attached**")
            safe_image(
                "Sub Locked Out.jpg",
                caption="Verification Photo – Lock Attached",
                use_container_width=True
            )
            st.markdown("""
<div class="risk-low">
    ✅ <strong>AR Recognition Result</strong><br>
    Lock detected at <strong>Isolation Point 3</strong><br>
    Lock Serial: <strong>PL-00342</strong><br>
    Confidence: <strong>98.2%</strong>
</div>""", unsafe_allow_html=True)

        with col_iso_confirm:
            st.write("**⚡ Confirmed Isolation Status**")
            safe_image(
                "Substation Isolated LV.jpeg",
                caption="Confirmed Isolation – Compartments Verified by AR",
                use_container_width=True
            )
            st.markdown("**Compartment Status:**")
            iso_status_df = pd.DataFrame({
                "Compartment":       ["Comp 1 – HV Incoming", "Comp 2 – LV Outgoing", "Comp 3 – Control"],
                "Status":            ["🔴 Isolated",          "🔴 Isolated",           "🟢 Energised"],
                "AR Verified":       ["✅ Yes",               "✅ Yes",                "✅ Yes"],
            })
            st.table(iso_status_df)

        st.write("**📐 Single Line Diagram / Isolation Drawing**")
        try:
            drawing = Image.open("Isolation drawing.jpg")
            drawing = drawing.resize((int(drawing.width * 0.5), int(drawing.height * 0.5)))
            st.image(drawing, caption="Isolation Drawing — AR Overlay Check")
        except FileNotFoundError:
            st.info("📐 Isolation Drawing / SLD placeholder (file not found in demo)")

        c1, c2 = st.columns(2)
        with c1:
            st.write("**HV Authorised Isolator**")
            st.text_input("Name (printed) – Isolator", key="isolator_sig_name")
            st.text_input("Date / Time / Contact",      key="isolator_sig_dt")
        with c2:
            st.write("**Isolation Verifier**")
            st.text_input("Name (printed) – Verifier", key="verifier_sig_name")
            st.text_input("Date / Time / Contact",     key="verifier_sig_dt")

    # ── Part 10 – Permit Activation ──────────────────────────────────────────────
    with st.expander("Part 10 – Permit Activation", expanded=False):
        mark_done(10)
        st.caption("HV Permit Holder verifies isolation and attaches Permit Holder's lock")
        st.text_input("Name (printed) – Permit Holder", key="activation_name")
        ack = st.checkbox(
            "I have personally verified the isolation is complete and I am attaching my personal lock to the lock box",
            key="activation_ack"
        )
        if ack:
            st.session_state.permit_status = "Active"
            if st.session_state.lock_count == 0:
                st.session_state.lock_count = 1
            st.success("✅ Permit Activated — Equipment is isolated and locked out. Work may now commence.")

    # ── Part 11 – Sign-on / Sign-off ────────────────────────────────────────────
    with st.expander("Part 11 – Sign-on / Sign-off", expanded=False):
        mark_done(11)
        st.caption("HV Permit Holder and Workers Sign-on / Sign-off / Handover")
        new_so = st.text_input("Worker Name to Sign On", key="new_signon")
        btn_on, btn_off = st.columns(2)
        with btn_on:
            if st.button("✅ Sign On", key="part11_sign_on"):
                if new_so and new_so not in st.session_state.signed_on_workers:
                    st.session_state.signed_on_workers.append(new_so)
                    st.session_state.lock_count += 1
                    st.success(
                        f"'{new_so}' signed on. Lock added. "
                        f"Total locks on box: {st.session_state.lock_count}."
                    )
        if st.session_state.signed_on_workers:
            st.markdown("**Currently Signed On:**")
            for w in st.session_state.signed_on_workers:
                st.write(f"✅ {w}")
        st.caption("Full sign-on / sign-off roster table (with timestamps and contact numbers) available in production app.")

    # ── Part 12 – Working Earths ────────────────────────────────────────────────
    with st.expander("Part 12 – Working Earth Locations", expanded=False):
        mark_done(12)
        st.markdown(
            '<div class="risk-high">🚨 All working earths MUST be recorded before work commences.</div>',
            unsafe_allow_html=True
        )
        st.markdown("")
        earth_df = pd.DataFrame({
            "Location and Details":         [""] * 4,
            "Placed by (printed name)":     [""] * 4,
            "PH Initials (Place)":          [""] * 4,
            "Removed by (printed name)":    [""] * 4,
            "PH Initials (Remove)":         [""] * 4,
        })
        st.dataframe(earth_df, use_container_width=True)

    # ── Part 13 – Testing ───────────────────────────────────────────────────────
    with st.expander("Part 13 – Testing (Where Applicable)", expanded=False):
        mark_done(13)
        testing_req = st.radio("Testing Required?", ["Required", "Not Required"], key="testing_radio")
        if testing_req == "Required":
            test_items = [
                "All personnel instructed to sign-off and remove personal locks",
                "HV Authorised Isolator instructed to remove working earths",
                "Permit Holder has witnessed and countersigned isolator's removal",
            ]
            for i, item in enumerate(test_items):
                st.checkbox(item, key=f"test_{i}")

    # ── Part 14 – Task Monitoring ───────────────────────────────────────────────
    with st.expander("Part 14 – Task Monitoring and Inspection", expanded=False):
        mark_done(14)
        st.caption("Supervisor, safety representatives, and other monitoring personnel")
        st.text_area("Inspection Notes / Observations", key="inspection_notes")

    # ── Part 15 – Pre-Restoration Checks ────────────────────────────────────────
    with st.expander("Part 15 – Permit Cancellation Pre-Restoration of Power", expanded=False):
        mark_done(15)
        st.markdown(
            '<div class="risk-high">⛔ ALL checks below must be complete before requesting restoration of power.</div>',
            unsafe_allow_html=True
        )
        st.markdown("")
        restore_items = [
            "Visual examination of work area completed",
            "All tests completed and documented",
            "All earth bonds in place and secure",
            "All disconnected cables capped / insulated",
            "All identification labels and warning signs updated",
            "All barrier tape removed",
            "All personal locks removed and all personnel signed off",
            "Work crews confirm equipment is safe to operate",
        ]
        all_done = all(
            st.checkbox(f"{i+1}. {c}", key=f"pre_restore_{i}")
            for i, c in enumerate(restore_items)
        )
        if all_done:
            st.success("✅ All pre-restoration checks complete. Power restoration may be requested.")
        st.text_input("Person notified of intention to restore power", key="notified_person")
        st.checkbox(
            "I confirm all work is complete (or cancelled) and equipment is safe to re-energise",
            key="pre_restore_confirm"
        )

    # ── Part 16 – Restoration of Power ──────────────────────────────────────────
    with st.expander("Part 16 – Restoration of Power", expanded=False):
        mark_done(16)
        st.warning(
            "⚠️ All energy source restorations must include the 12-step process "
            "(Glencore Fatal Hazard Protocol 7)."
        )
        proc_restore = st.radio(
            "Is an approved documented procedure available?",
            ["Yes – attach copy and use in place of these instructions",
             "No – complete switching instructions below"],
            index=1, key="proc_restore_radio"
        )
        if "No" in proc_restore:
            st.write("**Complete 12-step restoration switching instructions below:**")
            restore_df = pd.DataFrame({
                "Step": list(range(1, 13)),
                "Apparatus": [""] * 12,
                "Action":    [""] * 12,
                "Permit Lock No.": [""] * 12,
                "Time":      [""] * 12,
                "HV Isolator Initials":  [""] * 12,
                "HV Verifier Initials":  [""] * 12,
            })
            st.dataframe(restore_df, use_container_width=True)

    # ── Part 17 – Permit Completion ──────────────────────────────────────────────
    with st.expander("Part 17 – Permit Completion (HV Permit Holder)", expanded=False):
        mark_done(17)
        st.warning(
            "⚠️ Only return plant or equipment to service when this permit is complete "
            "or cancelled and all signatures are obtained."
        )
        st.checkbox("Permit activities COMPLETE",                           key="part17_complete")
        st.checkbox("Permit activities INCOMPLETE (state reason in comments)", key="part17_incomplete")
        st.text_area("Comments / Reason for Cancellation", key="part17_comments")
        if st.session_state.get("part17_complete"):
            if st.button("🔴 Mark Permit as Complete", key="cancel_permit"):
                st.session_state.permit_status = "Completed"
                st.success("Permit marked COMPLETED. Equipment may be returned to service.")

    # ── Part 18 – Permit Review ──────────────────────────────────────────────────
    with st.expander("Part 18 – Permit Review", expanded=False):
        mark_done(18)
        st.caption("To be completed by an authorised Electrical Engineer or delegate")
        st.text_area("Review Comments and Follow-up Actions", key="review_comments")
        st.text_input("Reviewer Name (printed)", key="reviewer_name")
        st.checkbox(
            "This permit has been reviewed and complies with all applicable standards",
            key="review_confirm"
        )

    st.markdown("---")
    btn1, btn2, btn3 = st.columns(3)
    with btn1:
        if st.button("💾 Save Draft", key="save_draft"):
            st.info("Draft saved. (Full app: encrypted cloud sync with offline-first capability.)")
    with btn2:
        if st.button("🖨️ Generate PDF Preview", key="gen_pdf"):
            st.info(
                "PDF generation available in full application. "
                "Output matches STD0930 layout for printing and archiving."
            )
    with btn3:
        if st.button("✅ Finalise & Submit Permit", key="finish_permit", type="primary"):
            st.success("✅ HV isolation permit finalised and submitted to records.")
            st.session_state.permit_status = "Completed"
            # st.balloons()

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 – TVL OBSERVATION (FRM1277)
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.subheader("👁️ TVL – Targeted Visible Leadership Observation (FRM1277)")

    # Live compliance score
    tvl_all_keys = [
        "tvl_sup_1", "tvl_sup_2",
        "tvl_lock_1", "tvl_lock_2",
        "tvl_sign_1", "tvl_sign_2", "tvl_sign_3", "tvl_sign_4",
        "tvl_new_1", "tvl_new_2", "tvl_new_3", "tvl_new_4",
        "tvl_access_1", "tvl_access_2", "tvl_access_3",
        "tvl_maint_1", "tvl_maint_2",
        "tvl_train_1",
        "tvl_arc_1", "tvl_arc_2",
        "tvl_test_1",
    ]
    checked = sum(1 for k in tvl_all_keys if st.session_state.get(k, False))
    total   = len(tvl_all_keys)
    score   = int((checked / total) * 100)

    score_col, bar_col = st.columns([1, 3])
    with score_col:
        st.metric("Compliance Score", f"{score}%", delta=f"{score - 87}% vs last TVL")
        if score >= 80:
            st.markdown('<div class="risk-low">🟢 COMPLIANT</div>', unsafe_allow_html=True)
        elif score >= 60:
            st.markdown('<div class="risk-medium">🟡 MONITOR</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="risk-high">🔴 NON-COMPLIANT — escalate immediately</div>', unsafe_allow_html=True)
    with bar_col:
        st.progress(score, text=f"{checked} / {total} items checked — score updates live as you complete the checklist")

    st.markdown("---")

    # Observation details
    dc1, dc2 = st.columns(2)
    with dc1:
        st.markdown("**Observation Details**")
        st.date_input("Date", value=datetime.date.today(), key="tvl_date")
        st.time_input("Time", key="tvl_time")
        st.text_input("Location", key="tvl_location")
        st.selectbox("Shift", ["Day (06:00–18:00)", "Night (18:00–06:00)"], key="tvl_shift")
        st.text_input("Observation Team Leader", key="tvl_leader")
    with dc2:
        st.markdown("**Work Context**")
        st.text_input("Description of Work Being Observed", key="tvl_description")
        linked_job = st.selectbox(
            "Linked Permit / Job",
            ["HV-2026-001 (Mobile Substation)", "HV-2026-002 (Conveyor Drive)", "HV-2026-004 (Feeder Breaker)"],
            key="linked_job"
        )
        if linked_job:
            safe_image(
                "Sub Locked Out.jpg",
                caption=f"Isolation lock photo from permit: {linked_job}",
                use_container_width=True
            )
            st.success("✅ Linked isolation lock photo pulled from permit record.")

    st.markdown("---")

    # Helper to render a checklist section
    def tvl_section(title, items, key_prefix):
        st.markdown(f'<div class="section-header">{title}</div>', unsafe_allow_html=True)
        results = []
        for i, item in enumerate(items):
            results.append(st.checkbox(item, key=f"{key_prefix}_{i+1}"))
        sec_score = sum(results)
        st.caption(f"Section: {sec_score}/{len(items)} ✅")
        return results

    tvl_section("Electrical Supervisor Credentials", [
        "Check of supervisor appointment documentation",
        "Check for presence of No Plan No Work booklet",
    ], "tvl_sup")

    tvl_section("Isolation & Personal Locks", [
        "Audit work area to ensure compliance with isolation procedure",
        "Challenge test a worker — verify they carry personal locks on site",
    ], "tvl_lock")

    tvl_section("Electrical Area Signage", [
        "Signs are relevant and easily understandable",
        "Signage covers all entry points with correct qualification details",
        "Clearly defines all qualification requirements",
        "Legible and compliant with Australian Standards",
    ], "tvl_sign")

    tvl_section("New Starters – Electrical Workers", [
        "Verify Electrical Licence currency",
        "Verify EEHA currency",
        "Verify LVR/CPR competency",
        "Verify EEHA Challenge Test completion",
    ], "tvl_new")

    # Access section — with live permit view buttons
    st.markdown('<div class="section-header">Access to Exposed Conductors</div>', unsafe_allow_html=True)
    access_items = [
        ("High Voltage Access Permits",               "tvl_access_1", "High Voltage Access Permit"),
        ("Group Isolation Permits",                   "tvl_access_2", "Group Isolation Permit"),
        ("System Impairment Permits – Electrical",    "tvl_access_3", "System Impairment Permit"),
    ]
    for label, key, preview_label in access_items:
        ac1, ac2 = st.columns([4, 1])
        with ac1:
            st.checkbox(label, key=key)
        with ac2:
            if st.button("👁️ View Live", key=f"view_{key}"):
                st.session_state.show_permit_preview = preview_label

    if st.session_state.show_permit_preview:
        with st.expander(f"🔍 Live Read-Only Permit: {st.session_state.show_permit_preview}", expanded=True):
            st.info(f"📋 Read-only view of **{st.session_state.show_permit_preview}** | Permit: HV-2026-001")
            lc1, lc2 = st.columns(2)
            with lc1:
                st.text_input("Permit ID",      value="HV-2026-001",                       disabled=True)
                st.text_input("Permit Holder",  value="J. Smith",                          disabled=True)
                st.text_input("Status",         value="Active",                            disabled=True)
            with lc2:
                st.text_input("Equipment",      value="Mobile Substation",                 disabled=True)
                st.text_input("Issued By",      value="R. Jones",                          disabled=True)
                st.text_input("Expires",        value="Today 18:00",                       disabled=True)
            st.text_area(
                "Task Description",
                value="Isolation of mobile substation for scheduled maintenance",
                disabled=True
            )
            st.success("✅ Permit is active and being followed correctly.")
            if st.button("✖️ Close Permit View", key="close_preview"):
                st.session_state.show_permit_preview = None
                st.rerun()

    tvl_section("Maintenance & Compliance of Electrical Equipment", [
        "Inspections completed when due and records sighted",
        "Locking mechanisms maintained and functional",
    ], "tvl_maint")

    tvl_section("Training", [
        "All coal mine workers have been trained in the isolation procedure",
    ], "tvl_train")

    tvl_section("Arc Flash Protection", [
        "Wearing appropriate arc-flash clothing (verified by observation)",
        "Carrying Trolex Non-Contact Voltage Tester (verified)",
    ], "tvl_arc")

    tvl_section("Testing and Tagging", [
        "Regular insulation and continuity tests completed and audited",
    ], "tvl_test")

    st.markdown("---")

    obs1, obs2, obs3 = st.columns(3)
    with obs1:
        st.text_area("✅ What was done well?",        key="tvl_well")
    with obs2:
        st.text_area("🔧 Opportunities for Improvement", key="tvl_improve")
    with obs3:
        st.text_area("💬 Other Comments",               key="tvl_comments")

    if st.button("📤 Submit TVL Observation", key="submit_tvl", type="primary"):
        st.success(
            f"✅ TVL Observation submitted. Compliance score: **{score}%**. "
            f"Linked to permit: {linked_job}."
        )
        if score < 80:
            st.warning(
                "⚠️ Compliance score below 80% — automatic notification sent to "
                "Electrical Engineer and Site Manager for follow-up."
            )

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 – 12 STEP ISOLATION REFERENCE
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.subheader("📋 12 Step Isolation Reference")
    st.caption(
        "Always-available reference for Permit Holders. "
        "Derived from Glencore Fatal Hazard Protocol 7 / AS/NZS 4836."
    )

    ref_img_col, steps_col = st.columns([1, 1])

    with ref_img_col:
        try:
            img = Image.open("12stepiso.png")
            img = img.resize((int(img.width * 0.5), int(img.height * 0.5)))
            st.image(img, caption="12 Step Isolation Process Reference Card", use_container_width=True)
        except FileNotFoundError:
            st.info("📋 12 Step process diagram — place '12stepiso.png' in the app directory.")

    with steps_col:
        st.markdown("### The 12 Steps")
        steps_detail = [
            ("1. Identify Energy Sources",
             "List ALL energy sources: electrical, hydraulic, pneumatic, gravitational, stored mechanical. "
             "Do not begin until all are identified."),
            ("2. Advise Relevant Parties",
             "Notify all affected personnel, supervisors, and control room of the planned isolation. "
             "Record who was notified."),
            ("3. Stop Equipment Safely",
             "Operate equipment through a normal stop cycle where possible. "
             "Do not isolate under load unless necessary."),
            ("4. Isolate Energy Sources",
             "Operate all identified isolation devices to the OFF / OPEN / ISOLATED position."),
            ("5. Lock and Tag",
             "Apply your personal lock AND a danger tag to each isolation device. "
             "No one else may remove your lock."),
            ("6. Verify Isolation",
             "Use approved test equipment to confirm zero energy state at all isolation points. "
             "Test the tester first and last."),
            ("7. Commence Work",
             "Work may ONLY commence after Steps 1–6 are complete and verified by the Isolation Verifier."),
            ("8. Complete Work",
             "Ensure all tools, materials, and personnel are clear of the equipment before proceeding."),
            ("9. Check Work Area",
             "Conduct a final visual inspection. Confirm no tools or materials are left inside equipment."),
            ("10. Clear Area",
             "Ensure all workers are accounted for and physically clear of the equipment."),
            ("11. Remove Locks and Tags",
             "Each worker removes ONLY their own personal lock. Nobody removes another person's lock — ever."),
            ("12. Restore Energy",
             "Re-energise in the reverse order of isolation following approved switching instructions. "
             "Record all switching actions with time and initials."),
        ]
        for step, detail in steps_detail:
            with st.expander(f"**{step}**"):
                st.write(detail)

    st.markdown("---")
    st.markdown(
        '<div class="risk-high">🚨 <strong>CRITICAL REMINDERS:</strong> '
        'Never remove another person\'s lock. '
        'Never work on equipment without your own lock applied. '
        'Treat ALL equipment as live until you have personally tested it and proven it dead. '
        'When in doubt — STOP and seek guidance.</div>',
        unsafe_allow_html=True
    )

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 – EQUIPMENT LIBRARY
# ═══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.subheader("🗄️ Equipment Library")
    st.caption("Catalogued plant with AI/AR verification data, isolation history, and permit linkage.")

    # Search & filter bar
    sc1, sc2, sc3, sc4 = st.columns([3, 1, 1, 1])
    with sc1:
        search_term = st.text_input(
            "🔍 Search", placeholder="Name, type, location, serial…", key="eq_search"
        )
    with sc2:
        ar_filter   = st.selectbox("AR Status",     ["All", "Ready", "Pending", "Training Required"], key="ar_filter")
    with sc3:
        type_filter = st.selectbox("Voltage Class", ["All", "HV", "LV"], key="type_filter")
    with sc4:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("➕ Add New Equipment", key="add_eq"):
            st.info("Opens Training Model tab with new equipment form (production behaviour).")

    equipment_data = [
        {
            "name": "Mobile Substation",      "type": "HV", "voltage": "11 kV",
            "iso_points": 3, "compartments": 3, "earth_points": 2,
            "last_trained": "2026-03-15", "ar_status": "Ready",
            "location": "Zone B – Underground", "permits_issued": 5,
        },
        {
            "name": "Conveyor Drive Motor",   "type": "LV", "voltage": "415 V",
            "iso_points": 2, "compartments": 2, "earth_points": 1,
            "last_trained": "2026-03-20", "ar_status": "Ready",
            "location": "Conveyor 3",          "permits_issued": 3,
        },
        {
            "name": "HV Switchgear Panel B3", "type": "HV", "voltage": "11 kV",
            "iso_points": 4, "compartments": 4, "earth_points": 3,
            "last_trained": "2026-03-25", "ar_status": "Ready",
            "location": "Substation B",        "permits_issued": 7,
        },
        {
            "name": "Feeder Breaker",         "type": "HV", "voltage": "3.3 kV",
            "iso_points": 1, "compartments": 2, "earth_points": 1,
            "last_trained": "2026-03-10", "ar_status": "Pending",
            "location": "Zone A",             "permits_issued": 2,
        },
    ]

    # Apply filters
    filtered_eq = [
        e for e in equipment_data
        if (not search_term or search_term.lower() in str(e).lower())
        and (ar_filter   == "All" or e["ar_status"] == ar_filter)
        and (type_filter == "All" or e["type"]      == type_filter)
    ]

    st.markdown(f"**{len(filtered_eq)} of {len(equipment_data)} items shown**")
    st.markdown("---")

    for eq in filtered_eq:
        icon    = "⚡" if eq["type"] == "HV" else "🔌"
        ar_icon = "✅" if eq["ar_status"] == "Ready" else "⏳"

        eqc1, eqc2, eqc3, eqc4 = st.columns([1, 3, 2, 2])
        with eqc1:
            st.markdown(
                f"<div style='font-size:40px; text-align:center;'>{icon}</div>"
                f"<div style='text-align:center;'>{ar_icon} {eq['ar_status']}</div>",
                unsafe_allow_html=True
            )
        with eqc2:
            st.markdown(f"**{eq['name']}**")
            st.write(f"🏭 {eq['location']}  |  ⚡ {eq['voltage']}")
            st.write(
                f"🔌 {eq['iso_points']} Isolation Points  |  "
                f"📦 {eq['compartments']} Compartments  |  "
                f"🌍 {eq['earth_points']} Earth Points"
            )
            st.caption(f"Last trained: {eq['last_trained']}")
        with eqc3:
            st.metric("Permits Issued", eq["permits_issued"])
        with eqc4:
            st.button("👁️ View Details",  key=f"view_eq_{eq['name']}")
            st.button("⚡ Start Permit",  key=f"start_permit_{eq['name']}")
            st.button("🔄 Re-train",      key=f"retrain_{eq['name']}")

        st.markdown("---")

# ═══════════════════════════════════════════════════════════════════════════════
# TAB 6 – PERMIT HISTORY
# ═══════════════════════════════════════════════════════════════════════════════
with tab6:
    st.subheader("📁 Permit History")
    st.caption("Searchable, auditable record of all HV permits. Immutable once closed.")

    # Search & filter
    hc1, hc2, hc3 = st.columns([3, 1, 1])
    with hc1:
        h_search = st.text_input(
            "🔍 Search Permits", placeholder="Permit ID, equipment, person, date…",
            key="permit_search"
        )
    with hc2:
        h_status = st.selectbox(
            "Status", ["All", "Active", "Approved", "Completed", "Cancelled"],
            key="hist_status_filter"
        )
    with hc3:
        h_date = st.selectbox(
            "Date Range", ["All Time", "Today", "This Week", "This Month"],
            key="hist_date_filter"
        )

    permit_history = [
        {
            "id": "HV-2026-001", "date": "2026-03-15",
            "equipment": "Mobile Substation",   "holder": "J. Smith",
            "issuer": "R. Jones",  "status": "Active",
            "parts": 18, "tvl": "Linked",
        },
        {
            "id": "HV-2026-002", "date": "2026-03-20",
            "equipment": "Conveyor Drive",       "holder": "M. Brown",
            "issuer": "R. Jones",  "status": "Completed",
            "parts": 18, "tvl": "Linked",
        },
        {
            "id": "HV-2026-003", "date": "2026-03-25",
            "equipment": "HV Switchgear Panel",  "holder": "T. Davis",
            "issuer": "R. Jones",  "status": "Completed",
            "parts": 18, "tvl": "Not Linked",
        },
        {
            "id": "HV-2026-004", "date": "2026-04-01",
            "equipment": "Feeder Breaker",        "holder": "J. Smith",
            "issuer": "R. Jones",  "status": "Approved",
            "parts": 6,  "tvl": "Pending",
        },
    ]

    filtered_hist = [
        p for p in permit_history
        if (not h_search or h_search.lower() in str(p).lower())
        and (h_status == "All" or p["status"] == h_status)
    ]

    # Summary metrics
    hm1, hm2, hm3, hm4 = st.columns(4)
    with hm1:
        st.metric("Total Permits", len(permit_history))
    with hm2:
        st.metric("Active",        sum(1 for p in permit_history if p["status"] == "Active"))
    with hm3:
        st.metric("Completed",     sum(1 for p in permit_history if p["status"] == "Completed"))
    with hm4:
        st.metric("TVL Linked",    sum(1 for p in permit_history if p["tvl"] == "Linked"))

    st.markdown(f"**Showing {len(filtered_hist)} of {len(permit_history)} permit(s)**")
    st.markdown("---")

    status_icons = {
        "Active": "🟢", "Completed": "⚫", "Approved": "🔵",
        "Cancelled": "🔴", "Pending": "🟡"
    }

    for p in filtered_hist:
        dot = status_icons.get(p["status"], "⚪")
        with st.expander(
            f"{dot} **{p['id']}**  |  {p['equipment']}  |  "
            f"Holder: {p['holder']}  |  {p['date']}  |  {p['status']}"
        ):
            hpc1, hpc2, hpc3 = st.columns(3)
            with hpc1:
                st.write(f"**Permit ID:** {p['id']}")
                st.write(f"**Date Issued:** {p['date']}")
                st.write(f"**Equipment:** {p['equipment']}")
            with hpc2:
                st.write(f"**Permit Holder:** {p['holder']}")
                st.write(f"**Issuer:** {p['issuer']}")
                st.write(f"**Parts Complete:** {p['parts']}/18")
            with hpc3:
                st.write(f"**Status:** {dot} {p['status']}")
                st.write(f"**TVL Observation:** {p['tvl']}")
                hb1, hb2, hb3 = st.columns(3)
                with hb1:
                    st.button("👁️ View", key=f"hist_view_{p['id']}")
                with hb2:
                    st.button("🖨️ PDF",  key=f"hist_pdf_{p['id']}")
                with hb3:
                    st.button("📊 Audit", key=f"hist_audit_{p['id']}")

# ─── FOOTER ─────────────────────────────────────────────────────────────────────
st.markdown("---")
fc1, fc2, fc3 = st.columns(3)
with fc1:
    st.caption("**MOSLock Lite** – Training & Permit Demo v0.2")
with fc2:
    st.caption("Standards: STD0930 | FRM1277 | Glencore FHP-07 | AS/NZS 4836")
with fc3:
    st.caption("Underground Coal Operations – Safety Critical System")
