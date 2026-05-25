from src.deployment.worker_lambda import handler

def main():
    fake_event = {
        "Records": [
            {
                "body": """
                {
                    "ticket_id": "88a89cfe-0f17-485d-b4c8-b2cfe664486f"
                }
                """
            }
        ]
    }

    result = handler(fake_event, None)

    print("\nLambda Result:")
    print(result)


if __name__ == "__main__":
    main()