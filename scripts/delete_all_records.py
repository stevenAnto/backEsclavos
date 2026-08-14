from app.repositories.record_repository import delete_all_records


if __name__ == "__main__":

    deleted = delete_all_records()

    print(f"Registros eliminados: {deleted}")