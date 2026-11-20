
from app.ingestion.pipeline import initialize_sample_data

def main():
    print("=" * 60)
    print("CO-X SAMPLE DATA INITIALIZATION TEST")
    print("=" * 60)

    result = initialize_sample_data()

    print("\nINITIALIZATION RESULTS")
    print("=" * 60)

    for key, value in result.items():
        print(f"{key}: {value}")

    print("\nInitialization completed successfully!")


if __name__ == "__main__":
    main()
