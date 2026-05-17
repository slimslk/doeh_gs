import os
from abc import ABC, abstractmethod
import pickle
from pathlib import Path


class DefaultLocationService(ABC):

    @abstractmethod
    def create_location(self) -> list[list[list[str]]]:
        pass

    @abstractmethod
    def get_location(self, location_id: str) -> list[list[list[str]]]:
        pass

    @abstractmethod
    def save_location(self, location_id: str, location_data: list[list[list[str]]]):
        pass

    @abstractmethod
    def delete_location(self, location_id: str):
        pass

    @abstractmethod
    def get_start_location(self) -> list[list[list[str]]]:
        pass


class FileLocationService(DefaultLocationService):
    MAIN_LOCATION_ID = "0"
    BASE_DIR = Path(__file__).resolve().parent
    MAP_DIR = BASE_DIR / "locations" / "maps"
    MAP_DIR.mkdir(parents=True, exist_ok=True)

    def create_location(self) -> list[list[list[str]]]:
        pass

    def get_location(self, location_id: str) -> list[list[list[str]]]:
        with open(location_id, "rb") as f:
            return pickle.load(f)

    def save_location(self, location_id: str, location_data: list[list[list[str]]]):
        map_filename_tmp = self.MAP_DIR / f"{location_id}.pkl.tmp"
        map_filename = self.MAP_DIR / f"{location_id}.pkl"
        with open(map_filename_tmp, "wb") as f:
            pickle.dump(location_data, f)
        os.replace(map_filename, map_filename_tmp)
        os.remove(map_filename_tmp)

    def delete_location(self, location_id: str):
        file_path = Path(self.MAP_DIR / f"{location_id}.pkl")
        if file_path.exists():
            file_path.unlink(missing_ok=True)

    def get_start_location(self) -> list[list[list[str]]]:
        return self.get_location(self.MAIN_LOCATION_ID)
