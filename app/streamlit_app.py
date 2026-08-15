import streamlit as st
from options import load_category_options
from api_client import APIClientError, predict_price, compare_deal


# Page Configuration
st.set_page_config(
    page_title="LaptopWise",
    page_icon="💻",
    layout="centered",
)


# Custom Styling
st.html(
    """
    <style>

        .block-container {
            max-width: 1100px;
            padding-top: 3rem;
            padding-bottom: 3rem;
        }

        .hero-title {
            text-align: center;
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
        }

        .hero-tagline {
            text-align: center;
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
        }

        .hero-description {
            text-align: center;
            font-size: 1.05rem;
            opacity: 0.75;
            max-width: 650px;
            margin: 0 auto 2rem auto;
        }

        .service-card {
            border: 1px solid rgba(128, 128, 128, 0.35);
            border-radius: 14px;
            padding: 1.5rem;
            min-height: 180px;
            margin-bottom: 1rem;
        }

        .service-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }

        .service-title {
            font-size: 1.35rem;
            font-weight: 650;
            margin-bottom: 0.5rem;
        }

        .service-description {
            font-size: 0.95rem;
            opacity: 0.75;
            line-height: 1.5;
        }

        
        /* Streamlit Buttons */

        div.stButton > button,
        div[data-testid="stFormSubmitButton"] > button {
            width: 100%;
            border-radius: 10px;
            border: 1px solid rgba(74, 163, 255, 0.55);
            background: rgba(30, 75, 125, 0.35);
            color: #ffffff;
            font-size: 1rem;
            font-weight: 650;
            padding: 0.65rem 1rem;
            transition: all 0.2s ease;
        }

        div.stButton > button:hover,
        div[data-testid="stFormSubmitButton"] > button:hover {
            border-color: rgba(74, 163, 255, 0.9);
            background: rgba(40, 100, 170, 0.55);
            color: #ffffff;
            transform: translateY(-1px);
        }

        div.stButton > button:active,
        div[data-testid="stFormSubmitButton"] > button:active {
            transform: translateY(0);
        }

        /* Estimate Result */

        .prediction-card {
            margin-top: 28px;
            padding: 32px;
            border-radius: 18px;

            border: 1px solid rgba(74, 163, 255, 0.65);

            background:
                linear-gradient(
                    135deg,
                    rgba(18, 55, 95, 0.95),
                    rgba(12, 24, 42, 0.98)
                );

            box-shadow:
                0 0 28px rgba(22, 131, 255, 0.20);

            text-align: center;
        }

        .prediction-label {
            font-size: 17px;
            font-weight: 600;
            color: #8fc5ff;
            margin-bottom: 8px;
        }

        .prediction-value {
            font-size: 48px;
            line-height: 1.15;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: 0.5px;
            margin-bottom: 10px;
        }

        .prediction-description {
            font-size: 14px;
            color: #b8c4d4;
        }


        /* Deal Result */

        .deal-container {
            margin-top: 28px;
            padding: 28px;
            border-radius: 18px;

            border: 1px solid rgba(128, 128, 128, 0.4);

            background:
                linear-gradient(
                    135deg,
                    rgba(24, 28, 38, 0.98),
                    rgba(15, 18, 25, 0.98)
                );

            box-shadow:
                0 0 25px rgba(0, 0, 0, 0.20);
        }

        .deal-title {
            text-align: center;
            font-size: 28px;
            font-weight: 750;
            color: #ffffff;
            margin-bottom: 24px;
        }

        .deal-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
        }

        .deal-card {
            padding: 22px;
            border-radius: 14px;
            min-height: 125px;

            border: 1px solid rgba(128, 128, 128, 0.35);

            background: rgba(30, 34, 45, 0.95);

            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        .deal-card-label {
            font-size: 14px;
            font-weight: 600;
            color: #aeb8c7;
            margin-bottom: 10px;
        }

        .deal-card-value {
            font-size: 30px;
            line-height: 1.2;
            font-weight: 800;
            color: #ffffff;
        }


        /*  Difference */

        .difference-positive {
            border-color: rgba(217, 74, 92, 0.65);
            background: rgba(120, 25, 40, 0.20);
        }

        .difference-positive .deal-card-value {
            color: #ff7182;
        }

        .difference-negative {
            border-color: rgba(54, 179, 126, 0.65);
            background: rgba(20, 110, 75, 0.20);
        }

        .difference-negative .deal-card-value {
            color: #4ade9b;
        }

        .difference-neutral {
            border-color: rgba(224, 165, 43, 0.65);
            background: rgba(130, 90, 20, 0.18);
        }

        .difference-neutral .deal-card-value {
            color: #f6c453;
        }


        /* Status Card */

        .status-card {
            margin-top: 16px;
            padding: 22px;
            border-radius: 14px;
            text-align: center;

            border: 1px solid rgba(128, 128, 128, 0.35);
        }

        .status-label {
            font-size: 14px;
            font-weight: 600;
            color: #aeb8c7;
            margin-bottom: 8px;
        }

        .status-value {
            font-size: 28px;
            font-weight: 800;
        }

        .status-good {
            border-color: rgba(54, 179, 126, 0.65);
            background: rgba(20, 110, 75, 0.20);
        }

        .status-good .status-value {
            color: #4ade9b;
        }

        .status-bad {
            border-color: rgba(217, 74, 92, 0.65);
            background: rgba(120, 25, 40, 0.20);
        }

        .status-bad .status-value {
            color: #ff7182;
        }

        .status-neutral {
            border-color: rgba(224, 165, 43, 0.65);
            background: rgba(130, 90, 20, 0.18);
        }

        .status-neutral .status-value {
            color: #f6c453;
        }


        /* Mobile Adjustment */

        @media (max-width: 700px) {

            .prediction-value {
                font-size: 38px;
            }

            .deal-grid {
                grid-template-columns: 1fr;
            }

            .deal-card-value {
                font-size: 26px;
            }
        }

    </style>
    """
)


# Result Display Helpers
def format_price(value):
    return f"₹{float(value):,.0f}"

def render_prediction_result(predicted_price):
    st.html(
        f"""
        <div class="prediction-card">

            <div class="prediction-label">
                Estimated Laptop Price
            </div>

            <div class="prediction-value">
                {format_price(predicted_price)}
            </div>

            <div class="prediction-description">
                Estimated market value based on the
                laptop specifications provided.
            </div>

        </div>
        """
    )


def render_deal_result(result):
    predicted_price = float(result["predicted_price"])
    asking_price = float(result["asking_price"])
    difference = float(result["difference"])
    status = result["status"]

    # Status text
    status_labels = {
        "below_estimated_price": "Below Estimated Price",
        "above_estimated_price": "Above Estimated Price",
        "around_estimated_price": "Around Estimated Price",
    }

    status_text = status_labels.get(status,status,)

    # Styling based on backend status
    if status == "below_estimated_price":
        status_class = "status-good"
        difference_class = "difference-negative"

    elif status == "above_estimated_price":
        status_class = "status-bad"
        difference_class = "difference-positive"

    else:
        status_class = "status-neutral"
        difference_class = "difference-neutral"


    # Deal Result
    st.html(
        f"""
        <div class="deal-container">

            <div class="deal-title">
                Deal Analysis
            </div>


            <div class="deal-grid">

                <!-- Estimated Value -->

                <div class="deal-card">

                    <div class="deal-card-label">
                        Estimated Value
                    </div>

                    <div class="deal-card-value">
                        {format_price(predicted_price)}
                    </div>

                </div>


                <!-- Asking Price -->

                <div class="deal-card">

                    <div class="deal-card-label">
                        Asking Price
                    </div>

                    <div class="deal-card-value">
                        {format_price(asking_price)}
                    </div>

                </div>


                <!-- Difference -->

                <div class="deal-card {difference_class}">

                    <div class="deal-card-label">
                        Difference
                    </div>

                    <div class="deal-card-value">
                        {format_price(abs(difference))}
                    </div>

                </div>


                <!-- Status -->

                <div class="status-card {status_class}">

                    <div class="status-label">
                        Deal Status
                    </div>

                    <div class="status-value">
                        {status_text}
                    </div>

                </div>

            </div>

        </div>
        """
    )


# Helper: Laptop Input Fields
def render_laptop_fields(category_options):
    # Basic Information
    st.markdown("### Basic Information")

    col1, col2 = st.columns(2)

    with col1:
        brand = st.selectbox(
            "Brand",
            options=category_options["Brand"],
            index=None,
            placeholder="Select a brand",
        )

    with col2:
        series = st.selectbox(
            "Series",
            options=category_options["Series"],
            index=None,
            placeholder="Select a series",
        )


    # Physical Specifications
    st.markdown("### Physical Specifications")

    col1, col2, col3 = st.columns(3)

    with col1:
        thickness = st.number_input(
            "Thickness (mm)",
            min_value=0.0,
            value=None,
            step=0.1,
            placeholder="Enter thickness",
        )

    with col2:
        weight = st.number_input(
            "Weight (kg)",
            min_value=0.0,
            value=None,
            step=0.1,
            placeholder="Enter weight",
        )

    with col3:
        display_size = st.number_input(
            "Display Size (inches)",
            min_value=0.0,
            value=None,
            step=0.1,
            placeholder="Enter display size",
        )


    # Software & Display
    st.markdown("### Software & Display")

    col1, col2 = st.columns(2)

    with col1:
        operating_system = st.selectbox(
            "Operating System",
            options=category_options["Operating System"],
            index=None,
            placeholder="Select an operating system",
        )

    with col2:
        display_touchscreen = st.selectbox(
            "Display Touchscreen",
            options=category_options["Display Touchscreen"],
            index=None,
            placeholder="Select touchscreen option",
        )


    # Performance
    st.markdown("### ⚙️ Performance")

    col1, col2 = st.columns(2)

    with col1:
        processor = st.selectbox(
            "Processor",
            options=category_options["Processor"],
            index=None,
            placeholder="Select a processor",
        )

    with col2:
        graphic_processor = st.selectbox(
            "Graphic Processor",
            options=category_options["Graphic Processor"],
            index=None,
            placeholder="Select a graphic processor",
        )


    # Memory & Storage
    st.markdown("### Memory & Storage")

    col1, col2 = st.columns(2)

    with col1:
        ram_capacity = st.number_input(
            "RAM Capacity (GB)",
            min_value=0.0,
            value=None,
            step=1.0,
            placeholder="Enter RAM capacity",
        )

    with col2:
        ram_type = st.selectbox(
            "RAM Type",
            options=category_options["RAM Type"],
            index=None,
            placeholder="Select RAM type",
        )

    col1, col2 = st.columns(2)

    with col1:
        ssd_capacity = st.number_input(
            "SSD Capacity (GB)",
            min_value=0.0,
            value=None,
            step=1.0,
            placeholder="Enter SSD capacity",
        )

    with col2:
        hdd_capacity = st.number_input(
            "HDD Capacity (GB)",
            min_value=0.0,
            value=None,
            step=1.0,
            placeholder="Enter HDD capacity",
        )


    # Battery & Security
    st.markdown("### 🔋 Battery & 🔐 Security")

    col1, col2 = st.columns(2)

    with col1:
        battery_capacity = st.number_input(
            "Battery Capacity (Wh)",
            min_value=0.0,
            value=None,
            step=0.1,
            placeholder="Enter battery capacity",
        )

    with col2:
        fingerprint_scanner = st.selectbox(
            "Fingerprint Scanner",
            options=category_options["Fingerprint scanner"],
            index=None,
            placeholder="Select fingerprint option",
        )


    # Store the 15 features
    return {
        "Brand": brand,
        "Series": series,
        "Thickness": thickness,
        "Weight": weight,
        "Operating System": operating_system,
        "Display Size": display_size,
        "Display Touchscreen": display_touchscreen,
        "Processor": processor,
        "Graphic Processor": graphic_processor,
        "RAM_Capacity_GB": ram_capacity,
        "RAM Type": ram_type,
        "SSD Capacity": ssd_capacity,
        "HDD Capacity": hdd_capacity,
        "Battery Capacity": battery_capacity,
        "Fingerprint scanner": fingerprint_scanner,
    }


# Helper: Frontend Validation
def validate_laptop_form(form_data):
    missing_fields = []

    for feature, value in form_data.items():

        if value is None:
            missing_fields.append(feature)

    if missing_fields:
        return (
            False,
            "Please provide the following required fields: "
            + ", ".join(missing_fields),
        )

    if (
        form_data["Thickness"] <= 0
        or form_data["Weight"] <= 0
        or form_data["Display Size"] <= 0
        or form_data["RAM_Capacity_GB"] <= 0
        or form_data["Battery Capacity"] <= 0
    ):

        return (
            False,
            "Thickness, weight, display size, RAM capacity, "
            "and battery capacity must be greater than zero.",
        )

    return True, None


# Hero Section

st.html("<div class='hero-title'>💻 LaptopWise</div>")
st.html("<div class='hero-tagline'>Know the price. Make the right choice.</div>")
st.html(
    """
    <div class="hero-description">
        Estimate a laptop's value and find out whether
        you're getting a good deal.
    </div>
    """
)
st.divider()


# Service Selection
st.subheader("What would you like to do?")

col1, col2 = st.columns(2)

with col1:

    st.html(
        """
        <div class="service-card">
            <div class="service-icon">💰</div>

            <div class="service-title">
                Estimate Price
            </div>

            <div class="service-description">
                Find the estimated value of a laptop
                based on its specifications.
            </div>
        </div>
        """
    )

    estimate_selected = st.button("Estimate Price",use_container_width=True,)

with col2:

    st.html(
        """
        <div class="service-card">
            <div class="service-icon">🏷️</div>

            <div class="service-title">
                Check a Deal
            </div>

            <div class="service-description">
                Compare the asking price with the estimated
                value to see if it's a good deal.
            </div>
        </div>
        """
    )

    deal_selected = st.button("Check a Deal",use_container_width=True,)

# Workflow Selection
if "workflow" not in st.session_state:
    st.session_state.workflow = None

if estimate_selected:
    st.session_state.workflow = "estimate"

elif deal_selected:
    st.session_state.workflow = "deal"

# Load Category Options
category_options = load_category_options()

# ESTIMATE PRICE WORKFLOW
if st.session_state.workflow == "estimate":

    st.divider()

    st.header("Estimate Laptop Price")

    st.write(
        "Enter the laptop specifications to estimate "
        "its expected market price."
    )

    st.subheader("Laptop Specifications")

    st.caption("Select or enter the specifications of the laptop.")

    # Estimate Form
    with st.form("estimate_form"):
        laptop_data = render_laptop_fields(category_options)
        submitted = st.form_submit_button("Estimate Price",use_container_width=True,)

    # Frontend Validation + API Request
    if submitted:
        valid, error_message = validate_laptop_form(laptop_data)

        if not valid:
            st.error(error_message)

        else:
            try:
                with st.spinner("Estimating laptop price..."):

                    result = predict_price(laptop_data)

                predicted_price = result["predicted_price"]

                render_prediction_result(predicted_price)

            except APIClientError as error:

                st.error(str(error))

            except Exception:

                st.error(
                    "Unable to process this prediction right now. "
                    "Please try again."
                )


# CHECK A DEAL WORKFLOW
elif st.session_state.workflow == "deal":

    st.divider()

    st.header("Check a Laptop Deal")

    st.write(
        "Enter the laptop specifications and asking price "
        "to see whether the deal looks reasonable."
    )

    st.subheader("Laptop Specifications")

    st.caption("Select or enter the specifications of the laptop.")

    # Deal Form
    with st.form("deal_form"):

        # Common 15 Laptop Features
        laptop_data = render_laptop_fields(category_options)

        # Asking Price
        st.markdown("### Asking Price")

        asking_price = st.number_input(
            "Asking Price (₹)",
            min_value=0.0,
            value=None,
            step=1000.0,
            placeholder="Enter the seller's asking price",
        )

        # Submit
        submitted = st.form_submit_button("Check the Deal",use_container_width=True,)


    # Frontend Validation
    if submitted:

        # Validate the 15 laptop features
        valid, error_message = validate_laptop_form(laptop_data)

        if not valid:
            st.error(error_message)

        # Validate asking price
        elif asking_price is None:
            st.error("Please provide the Asking Price.")

        elif asking_price <= 0:
            st.error("Asking price must be greater than zero.")

        # Send request to FastAPI
        else:
            try:

                with st.spinner("Analyzing the deal..."):

                    result = compare_deal(laptop_data,asking_price,)

                render_deal_result(result)

            except APIClientError as error:

                st.error(str(error))

            except Exception:

                st.error(
                    "Unable to process the deal comparison right now. "
                    "Please try again."
                )