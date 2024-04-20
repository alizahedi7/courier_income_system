# Courier Income System

This Django project is designed to calculate and track the income of couriers. It takes into account various factors that affect the income of couriers, such as the income related to a trip, increase in income, and deduction from income.

## Models

The project includes the following models:

- `Courier`: Represents a courier with a name.
- `Trip`: Represents a trip made by a courier. Each trip has an associated income.
- `TripPenaltyAward`: Represents an increase or decrease in a courier's income independent of the income related to a trip.
- `DailyIncome`: Represents the total income of a courier on a certain date.
- `WeeklyIncome`: Represents the total income of a courier in a certain week.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/alizahedi7/courier-income-system.git
    ```
2. Install the requirements:
    ```bash
    pip install -r requirements.txt
    ```
3. Make the migrations:
    ```bash
    python manage.py makemigrations
    ```
4. Apply the migrations:
    ```bash
    python manage.py migrate
    ```
5. Run the server:
    ```bash
    python manage.py runserver
    ```

## Usage

You can create and update instances of the models through the Django admin interface or the Django shell. The income of a courier is automatically calculated and updated whenever a trip is made, an income increase is recorded, or an income deduction is recorded.

## Testing

The project includes tests for the models and their methods. You can run the tests with the following command:
    ```bash
    python manage.py test
    ```

## Contributing

Contributions are welcome. Please open an issue to discuss your idea or submit a pull request.