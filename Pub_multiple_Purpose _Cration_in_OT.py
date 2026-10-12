
import requests
API_TOKEN = "Paste_your_token_here"
HOSTNAME = "https://host_name.onetrust.com"


# Purpose Category ID
PURPOSE_CATEGORY_ID = "Paste_PURPOSE_CATEGORY_ID"

# Organization ID
ORGANIZATION_ID = "Paste_ORGANIZATION_ID"

# API Headers
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}


# ============================================================
# OPTIONS
# ============================================================

DIVISIONS = [
    "Div_1",
    "Div_2"
]

PURPOSE_TYPES = [
    "PURPOSE_TYPE_1",
    "PURPOSE_TYPE_2"


]


# ============================================================
# CHOOSE OPTION
# ============================================================

def choose_option(options, title):

    print("\n" + "=" * 46)
    print(title)
    print("=" * 46)

    for index, option in enumerate(options, start=1):
        print(f"{index}. {option}")

    while True:

        try:
            choice = int(
                input("\nEnter your choice (number): ").strip()
            )

            if 1 <= choice <= len(options):
                return options[choice - 1]

            print(
                f"Please enter a number between 1 and {len(options)}."
            )

        except ValueError:
            print("Please enter a valid number.")


# ============================================================
# CREATE PURPOSE
# ============================================================

def create_purpose(purpose_name):

    url = (
        f"{HOSTNAME}/api/consentmanager/v1/purposes"
        f"?isInternalOrg=true"
    )

    payload = {
        "Organizations": [
            ORGANIZATION_ID
        ],
        "Name": purpose_name,
        "Description": f"<p>{purpose_name}&nbsp;</p>",
        "ConsentLifeSpan": 0,
        "ImplicitConsentLifeSpan": 0,
        "DefaultLanguage": "en-us",
        "CustomPreferenceIds": [],
        "PurposeCategory": {
            "id": PURPOSE_CATEGORY_ID
        }
    }

    print("\nCreating Purpose...")

    try:

        response = requests.post(
            url,
            headers=HEADERS,
            json=payload,
            timeout=60
        )

    except requests.exceptions.RequestException as error:

        print("\nERROR:")
        print("Unable to connect to OneTrust.")
        print(f"Details: {error}")

        return False

    # --------------------------------------------------------
    # SUCCESS
    # --------------------------------------------------------

    if response.status_code in [200, 201]:

        try:
            data = response.json()

        except ValueError:
            data = {}

        purpose_id = (
            data.get("Id")
            or data.get("id")
            or data.get("Guid")
            or data.get("guid")
        )

        print("\n" + "=" * 46)
        print("PURPOSE CREATED SUCCESSFULLY")
        print("=" * 46)

        print(f"Purpose Name : {purpose_name}")

        if purpose_id:
            print(f"Purpose ID   : {purpose_id}")
        else:
            print("Purpose ID   : Not returned in response")

        print("=" * 46)

        return True

    # --------------------------------------------------------
    # ERROR
    # --------------------------------------------------------

    print("\nERROR:")
    print("Unable to create Purpose.")
    print(f"\nStatus Code: {response.status_code}")
    print(f"\nResponse:\n{response.text}")

    return False


# ============================================================
# MAIN PROGRAM
# ============================================================

def main():

    print("\n")
    print("=" * 50)
    print("       ONETRUST PURPOSE CREATION TOOL")
    print("=" * 50)

    while True:

        # ----------------------------------------------------
        # COUNTRY
        # ----------------------------------------------------

        country = input("\nEnter Country: ").strip()

        while not country:

            print("Country cannot be empty.")

            country = input(
                "Enter Country: "
            ).strip()

        # ----------------------------------------------------
        # DIVISION
        # ----------------------------------------------------

        division = choose_option(
            DIVISIONS,
            "Available Divisions"
        )

        # ----------------------------------------------------
        # PURPOSE TYPE
        # ----------------------------------------------------

        purpose_type = choose_option(
            PURPOSE_TYPES,
            "Available Purpose Types"
        )

        # ----------------------------------------------------
        # BRAND
        # ----------------------------------------------------

        brand = input(
            "\nEnter Brand: "
        ).strip()

        while not brand:

            print("Brand cannot be empty.")

            brand = input(
                "Enter Brand: "
            ).strip()

        # ----------------------------------------------------
        # BUILD PURPOSE NAME
        # ----------------------------------------------------

        purpose_name = (
            f"{purpose_type} | "
            f"{country} | "
            f"{division} | "
            f"{brand}"
        )

        # ----------------------------------------------------
        # DISPLAY PURPOSE
        # ----------------------------------------------------

        print("\n")
        print("=" * 46)
        print("PURPOSE")
        print("=" * 46)
        print(purpose_name)
        print("=" * 46)

        # ----------------------------------------------------
        # CONFIRMATION
        # ----------------------------------------------------

        while True:

            confirmation = input(
                "\nDo you want to create this Purpose? (Y/N): "
            ).strip().upper()

            if confirmation in ["Y", "N"]:
                break

            print("Please enter Y or N.")

        # ----------------------------------------------------
        # CREATE
        # ----------------------------------------------------

        if confirmation == "Y":

            create_purpose(purpose_name)

        else:

            print("\nPurpose creation cancelled.")

        # ----------------------------------------------------
        # CREATE ANOTHER?
        # ----------------------------------------------------

        while True:

            another = input(
                "\nDo you want to create another purpose? (Y/N): "
            ).strip().upper()

            if another in ["Y", "N"]:
                break

            print("Please enter Y or N.")

        if another == "N":

            print("\nExiting Purpose Creation Tool.")
            print("Done.")

            break

        print("\n")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()