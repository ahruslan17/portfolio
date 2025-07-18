import os
import logging
from string import Template
import threading
from typing import Optional, Any, Union, Iterator
from datetime import datetime, timedelta, timezone
from enum import IntEnum
import re
import shutil
import hashlib
import random
import pandas as pd
import gc
import numpy as np
from time import sleep
import traceback
import psutil
import tqdm
import concurrent
from functools import partial


from logger_lib import (
    stdout_logger,
)  # "logger_lib" is an anonimized analog of company's logging lib


class DummyTqdm:
    """Stub progress bar for optimized execution in environments like Airflow."""

    def __init__(self, *args, **kwargs):
        pass

    def update(self, n=1):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


class VerbosityLevel(IntEnum):
    """
    `BASIС` - no logfile, only print main info in console
    `DETAILED` - logfile with errors/successful queries
    `EXTRA_LOGGING` - logfile + additional .txt with memory consumption data
    `FULL_LOGGING` - detailed log in consol using logger_lib stdout_logger
    """

    BASIC = 0
    DETAILED = 1
    EXTRA_LOGGING = 2
    FULL_LOGGING = 4


HOUR_CONDITION_TEMPLATE = {
    "regular": Template(
        "AND `${default_timeield}` >= '${start_time_str}Z' AND "
        "`${default_timeield}` < '${end_time_str}Z'"
    ),
    "extra": Template(
        "AND (`${default_timeield}` < '${start_time_str}Z' OR "
        "`${default_timeield}` >= '${end_time_str}Z')"
    ),
}


def set_gte_lte(gte: datetime, lte: datetime):
    """
    Converts datetime boundaries to UTC ISO format strings with millisecond precision.

    Args:
        gte (datetime): Start datetime (greater than or equal).
        lte (datetime): End datetime (less than or equal).

    Returns:
        tuple[str | None, str | None]: UTC datetime strings in ISO format, or (None, None) if inputs are None.
    """
    if gte is None or lte is None:
        return None, None

    if not isinstance(gte, datetime):
        raise ValueError("Parameter 'gte' must be a datetime object.")
    if not isinstance(lte, datetime):
        raise ValueError("Parameter 'lte' must be a datetime object.")

    gte = gte.astimezone(timezone.utc)
    lte = lte.astimezone(timezone.utc)

    gte_str = gte.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] if gte else None
    lte_str = lte.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] if lte else None

    return gte_str, lte_str


class QueryConfigurator:
    """
    A utility class for constructing and configuring queries for a generic data retrieval system.

    Description:
        This class helps define query parameters, manage configuration options,
        and control output, logging, and memory behavior.

    Methods:
        get_query(index, hour_condition): Builds a query string for the specified index and time filter.
        log_info(message): Logs informational messages if logging is enabled.
        log_error(message): Logs error messages if logging is enabled.
        log_debug(message): Logs debug messages if logging is enabled and verbosity allows it.
    """

    def __init__(
        self,
        indexes: list[str],
        fields: str,
        name_of_type: str,
        event_type: str,
        extra_condition: str = "",
        output_filename: Optional[str] = None,
        verbose: VerbosityLevel = VerbosityLevel.DETAILED,
        ascending: bool = True,
        temp_files: bool = False,
        return_df: bool = False,
        compress_df: bool = False,
        time_step: int = 4,
        gte: datetime = None,
        lte: datetime = None,
        date_range: Optional[str] = None,
        ignore_exceptions: bool = False,
        isin_container: bool = False,
    ):
        """
        Initializes the QueryConfigurator instance with query parameters and runtime options.

        Parameters:
            indexes (list[str]): List of target indexes to query.
            fields (str): Comma-separated fields to select (must not use "*").
            name_of_type (str): Name of the type field used in filtering.
            event_type (str): Value of the event type filter.
            extra_condition (str): Additional condition appended to each query.
            output_filename (str | None): Path to output file (CSV). If None, default name will be used.
            verbose (VerbosityLevel): Controls the level of logging verbosity.
            ascending (bool): Whether the output should be sorted in ascending time order.
            temp_files (bool): Whether to store intermediate files for reuse.
            return_df (bool): If True, returns result as a DataFrame instead of writing to file.
            compress_df (bool): Whether to downcast DataFrame types to save memory (applies only if return_df=True).
            time_step (int): Number of hours per subquery (between 1 and 12; default is 4).
            gte (datetime): Start of the time range for filtering.
            lte (datetime): End of the time range for filtering.
            date_range (str | None): Name of the time field used in filtering.
            ignore_exceptions (bool): If True, continues execution on failure; if False, stops on first exception.
            isin_container (bool): Enables container-safe behavior (disables memory tracking/logging if True).

        Raises:
            ValueError: If any of the parameters are invalid or have wrong types.
        """
        # === Types validation ===
        validate_type(indexes, list, "'indexes' must be a list of strings.")
        if not all(isinstance(i, str) for i in indexes):
            raise ValueError("'indexes' must be a list of strings.")

        validate_type(fields, str, "'fields' must be a string.")
        validate_type(name_of_type, str, "'name_of_type' must be a string.")
        validate_type(event_type, str, "'event_type' must be a string.")
        validate_type(extra_condition, str, "'extra_condition' must be a string.")

        validate_type(
            output_filename,
            (str, type(None)),
            "'output_filename' must be a string or None.",
        )
        validate_type(
            date_range, (str, type(None)), "'date_range' must be a string or None."
        )
        validate_type(
            verbose, VerbosityLevel, "'verbose' must be an instance of VerbosityLevel."
        )
        validate_type(ascending, bool, "'ascending' must be a boolean.")
        validate_type(temp_files, bool, "'temp_files' must be a boolean.")
        validate_type(return_df, bool, "'return_df' must be a boolean.")
        validate_type(ignore_exceptions, bool, "'ignore_exceptions' must be a boolean.")
        validate_type(isin_container, bool, "'isin_container' must be a boolean.")
        validate_type(compress_df, bool, "'compress_df' must be a boolean.")

        validate_fields(fields)

        # === Init variables ===
        if output_filename is None:
            output_filename = f"{event_type}_out.csv"

        self.name_of_type = name_of_type
        self.query_template = Template(
            f"SELECT $fields FROM `$index` WHERE {self.name_of_type}='$type' $extra_condition"
        )
        self.indexes = indexes
        self.fields = fields
        self.event_type = event_type
        self.extra_condition = extra_condition
        self.output_filename = output_filename
        self.verbose = verbose
        self.ascending = ascending
        self.logger = None
        self.isin_container = isin_container
        self.temp_files = temp_files and not isin_container
        self.return_df = return_df
        self.compress_df = compress_df
        self.gte, self.lte = set_gte_lte(gte, lte)
        self.date_range = date_range
        self.ignore_exceptions = ignore_exceptions

        if time_step > 12 or time_step < 1:
            self.time_step = 4
        else:
            self.time_step = time_step

        if not self.isin_container:
            if self.verbose > 0 and self.verbose < 4:
                self.logger = self._create_logger()
            if self.verbose == 4:
                self.logger = stdout_logger(name=f"{self.event_type}")

    def _create_logger(self) -> logging.Logger:
        """
        Creates a logger for the configurator, if verbosity is enabled.

        Returns:
            logging.Logger: Configured logger object.
        """
        logger = logging.getLogger(f"logger_{self.output_filename}")
        logger.setLevel(logging.INFO)
        log_filename = generate_logfile_name(self.output_filename)
        file_handler = logging.FileHandler(log_filename, mode="w")
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(message)s")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger

    def get_query(self, index: str, hour_condition: str) -> str:
        """
        Constructs a query string based on the index and hour condition.
        You can use it befire downloading data to be sure that your query is correct.

        Args:
            index (str): The index to query.
            hour_condition (str): The time condition to apply for the query.

        Returns:
            str: The constructed query string.
        """
        return self.query_template.substitute(
            fields=self.fields,
            index=index,
            type=self.event_type,
            extra_condition=self.extra_condition + " " + hour_condition,
        )

    def log_debug(self, message: str, console=False) -> None:
        if console and self.verbose < 4:
            print(message)

        if self.logger:
            self.logger.debug(message)

    def log_info(self, message: str, console=False) -> None:
        if console and self.verbose < 4:
            print(message)

        if self.logger:
            self.logger.info(message)

    def log_error(self, message: str, console=False) -> None:
        if console and self.verbose < 4:
            print(message)

        if self.logger:
            self.logger.error(message)

    def __str__(self) -> str:
        return (
            "\nQUERY EXAMPLE: \n"
            + self.query_template.substitute(
                fields=self.fields,
                index=self.indexes[0],
                type=self.event_type,
                extra_condition=self.extra_condition,
            )
            + "\n"
            + f"gte (UTC+0): {self.gte} \n"
            + f"lte (UTC+0): {self.lte} \n"
        )


# ===== UTILS =====
def validate_type(
    value: Any, expected_type: Union[type, tuple], error_message: str
) -> None:
    """Validates a parameter's type and optionally applies an additional condition."""
    if not isinstance(value, expected_type):
        raise ValueError(error_message)


def validate_fields(fields: str):
    pattern = r"^(\`[\w.$@]+\`|[\w.$@]+)(, (\`[\w.$@]+\`|[\w.$@]+))*$"

    if not re.match(pattern, fields):
        raise ValueError(f"Invalid format: {fields}")
    return True


def summary(
    configurator: QueryConfigurator,
    start_exec_time: datetime,
    success_count: int,
    error_count: int,
    peak_memory_usage: list[float],
):
    # Calculate execution duration
    end_exec_time = datetime.now()
    exec_duration = (end_exec_time - start_exec_time).total_seconds()

    # Create formatted messages
    placeholder = "-----------------"
    execution_time_message = f"Execution time: {exec_duration} seconds"
    success_error_message = f"Successes: {success_count}, Errors: {error_count}"
    peak_memory_message = f"Peak memory usage: {peak_memory_usage[0]:.2f} MB"

    # Logging to file
    configurator.log_info(placeholder, console=True)
    configurator.log_info(execution_time_message, console=True)
    configurator.log_info(success_error_message, console=True)

    if peak_memory_usage[0] > 0:
        configurator.log_info(peak_memory_message, console=True)


def create_cache_dir(configurator: QueryConfigurator):
    # Base temporary directory
    temp_dir = os.path.join(os.getcwd(), "cache_storage")
    configurator.log_info(f"Temporary directory path: {temp_dir}")
    os.makedirs(temp_dir, exist_ok=True)

    # Generate unique subdirectory name based on configuration
    unique_dir_name = generate_unique_dir_name(configurator)
    nested_dir = os.path.join(temp_dir, unique_dir_name)

    # Check if directory already exists
    is_old_cache = os.path.exists(nested_dir)

    # Create it if it doesn't exist yet
    if not is_old_cache:
        os.makedirs(nested_dir, exist_ok=True)
    configurator.log_info(f"Cache subdirectory path: {nested_dir}")

    return nested_dir, is_old_cache


def generate_unique_dir_name(configurator: QueryConfigurator) -> str:
    """
    Generates a unique directory name based on configuration parameters using MD5 hashing.

    Args:
        configurator (QueryConfigurator): Configuration object containing relevant parameters.

    Returns:
        str: A unique hashed directory name.
    """
    # Concatenate config parameters to form a base string for hashing
    base_string = (
        configurator.fields
        + configurator.name_of_type
        + configurator.event_type
        + configurator.extra_condition
        + str(configurator.time_step)
    )

    # Generate MD5 hash
    hash_object = hashlib.md5(base_string.encode("utf-8"))
    return hash_object.hexdigest()


def delete_directory(configurator: QueryConfigurator, directory: str):
    if os.path.isdir(directory):
        try:
            shutil.rmtree(directory)
            configurator.log_info(f"Directory {directory} is sucessfully deleted")
        except Exception as e:
            configurator.log_info(
                f"Unable to delete directory {directory}. Reason: {e}"
            )
    else:
        configurator.log_info(f"Directory {directory} does not exist.")


def write_instance_info(instance: QueryConfigurator, file_path: str):
    complete_file_path = os.path.join(file_path, "INFO.md")
    current_indexes = set()
    if os.path.exists(complete_file_path):
        with open(complete_file_path, "r") as file:
            lines = file.readlines()
            indexes_start = lines.index("------------------------------------\n") + 1
            for line in lines[indexes_start:]:
                current_indexes.update(line.strip().split(", "))
    current_indexes.update(instance.indexes)
    sorted_indexes = sorted(current_indexes, key=extract_date_from_index)
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(complete_file_path, "w") as file:
        file.write("Query data: \n")
        file.write(f"Fields: {instance.fields}\n")
        file.write(f"Name of Type: {instance.name_of_type}\n")
        file.write(f"Event Type: {instance.event_type}\n")
        file.write(f"Extra Condition: {instance.extra_condition}\n")
        file.write(f"Time step: {instance.time_step}\n")
        file.write(f"Last Launch Time: {current_time}\n")
        file.write("------------------------------------\n")
        file.write(f"{', '.join(sorted_indexes)}\n")

    instance.log_info(f"File {complete_file_path} with query parameters is created.")


def generate_logfile_name(base_filename: str) -> str:
    return "query_" + base_filename.replace(".csv", ".log")


def move_query_log_file(configurator: QueryConfigurator, temp_dir: str):
    """
    Перемещает лог-файл запросов из текущей рабочей директории в указанную временную директорию.

    Функция формирует имя лог-файла, заменяя расширение файла из конфигуратора на '.log'.
    Ищет файл в текущей рабочей директории и перемещает его в указанную временную директорию.
    """
    tmp_name = generate_logfile_name(configurator.output_filename)
    source_file = os.path.join(os.getcwd(), f"{tmp_name}")
    destination_file = os.path.join(temp_dir, f"{tmp_name}")
    # Проверяем, существует ли файл в текущей рабочей директории
    if os.path.exists(source_file):
        try:
            # Перемещаем файл в целевую директорию
            shutil.move(source_file, destination_file)
        except Exception:
            pass


def extract_date_from_index(index: str) -> datetime:
    """Функция для извлечения даты из строки индекса.
    Возвращает минимально возможную дату для индексов без даты."""
    try:
        # Ищем датаформаты в строке индекса
        match = re.search(r"\d{4}(\.\d{2}){1,2}", index)
        if not match:
            return datetime.min

        date_str = match.group(0)

        if len(date_str) == 7:  # Формат ГГГГ.ММ
            return datetime.strptime(date_str, "%Y.%m")
        if len(date_str) == 10:  # Формат ГГГГ.ММ.ДД
            return datetime.strptime(date_str, "%Y.%m.%d")
    except Exception:
        return datetime.min


def change_time_format(condition: str) -> str:
    def convert_datetime_format(match):
        iso_format_date = match.group(0)
        dt = datetime.fromisoformat(iso_format_date.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S.%f")

    new_condition = re.sub(
        r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z",
        convert_datetime_format,
        condition,
    )
    return new_condition


def prepare_queries(
    configurator: QueryConfigurator,
    temp_dir: str,
    default_timeield: str,
) -> list[list[str]]:
    configurator.log_debug("Start preparing queries...")

    if configurator.date_range:
        default_timeield = configurator.date_range

    result_queries = []

    for ind in configurator.indexes:
        configurator.log_debug(f"Preparing queries for index {ind}...")

        nested_dir = create_directory(temp_dir, ind, configurator)

        date_part = ind.split("-")[1] if "-" in ind else None

        if not date_part:
            handle_index_without_date(
                ind, nested_dir, configurator, result_queries, default_timeield
            )
            return result_queries

        start_date, end_date, is_compressed_index = parse_date_from_index(date_part)

        create_queries_for_date_range(
            configurator,
            ind,
            start_date,
            end_date,
            is_compressed_index,
            default_timeield,
            nested_dir,
            result_queries,
        )

    random.shuffle(result_queries)
    return result_queries


def create_directory(temp_dir: str, ind: str, configurator: QueryConfigurator) -> str:
    nested_dir = os.path.join(temp_dir, f"{ind}")
    os.makedirs(nested_dir, exist_ok=True)
    configurator.log_info(f"Directory for nested files: {nested_dir}")
    return nested_dir


def handle_index_without_date(
    ind: str,
    nested_dir: str,
    configurator: QueryConfigurator,
    result_queries: list,
    default_timeield: str,
):
    configurator.log_debug("Index without specific date format, downloading all data.")
    query = configurator.get_query(ind, "").replace("  ", " ")
    if configurator.gte and configurator.lte:
        hour_condition = HOUR_CONDITION_TEMPLATE["regular"].substitute(
            default_timeield=default_timeield,
            start_time_str=configurator.gte,
            end_time_str=configurator.lte,
        )
        hour_condition = hour_condition.replace("<", "<=")
        if configurator.name_of_type == "Type":
            hour_condition = change_time_format(hour_condition)
        query = query + hour_condition
    if "accounts" in ind:
        configurator.log_debug("Preparing query for accounts...")
        query = (
            query.replace("EventType='' AND ", "")
            .replace("Event.Type='' AND ", "")
            .replace("Type='' AND ", "")
        )
    temp_filename = os.path.join(nested_dir, f"{ind}_full.pkl")
    result_queries.append([query, temp_filename])


def parse_date_from_index(date_part: str):
    parts = date_part.split(".")
    is_compressed_index = len(parts) == 2

    if is_compressed_index:
        start_date = datetime.strptime(f"{parts[0]}.{parts[1]}.01", "%Y.%m.%d")
        end_date = (start_date + timedelta(days=31)).replace(day=1)
    else:
        start_date = datetime.strptime(f"{parts[0]}.{parts[1]}.{parts[2]}", "%Y.%m.%d")
        end_date = start_date + timedelta(days=1)

    return start_date, end_date, is_compressed_index


def create_queries_for_date_range(
    configurator: QueryConfigurator,
    ind: str,
    start_date: datetime,
    end_date: datetime,
    is_compressed_index: bool,
    default_timeield: str,
    nested_dir: str,
    result_queries: list,
):
    delta = timedelta(days=1)
    current_day = start_date

    while current_day < end_date:
        for hour in range(0, 25, configurator.time_step):
            start_time = current_day + timedelta(hours=hour)
            end_time = start_time + timedelta(hours=configurator.time_step)

            start_time_str, end_time_str = get_time_strings(
                hour, configurator, end_time, start_time
            )

            if end_time_str == start_time_str:
                continue

            configurator.log_debug(
                f"Appending query for {start_time_str}, {end_time_str}..."
            )
            append_query(
                configurator,
                ind,
                nested_dir,
                result_queries,
                start_time_str,
                end_time_str,
                start_date,
                end_date,
                default_timeield,
                is_extra_query=False,
            )
            if hour + configurator.time_step > 24:
                break

        if not is_compressed_index:
            append_query(
                configurator,
                ind,
                nested_dir,
                result_queries,
                start_time_str,
                end_time_str,
                start_date,
                end_date,
                default_timeield,
                is_extra_query=True,
            )
        current_day += delta
        if current_day == end_date and is_compressed_index:
            append_query(
                configurator,
                ind,
                nested_dir,
                result_queries,
                start_time_str,
                end_time_str,
                start_date,
                end_date,
                default_timeield,
                is_extra_query=True,
            )


def intersect_time_ranges(start1: str, end1: str, start2: str, end2: str):
    """
    Returns the intersection of two time ranges and a flag indicating which end time "wins",
    represented as strings, or None and the flag if there is no intersection.
    """
    fmt = "%Y-%m-%dT%H:%M:%S.%f"
    start1_dt, end1_dt = datetime.strptime(start1, fmt), datetime.strptime(end1, fmt)
    start2_dt, end2_dt = datetime.strptime(start2, fmt), datetime.strptime(end2, fmt)

    max_start = max(start1_dt, start2_dt)

    # Determine the minimum end and corresponding flag
    if end1_dt < end2_dt:
        min_end, flag = end1_dt, False
    else:
        min_end, flag = end2_dt, True

    # Return the intersection result and the flag
    return (
        ((max_start.strftime(fmt)[:-3], min_end.strftime(fmt)[:-3]), flag)
        if max_start <= min_end
        else (None, flag)
    )


def append_query(
    configurator: QueryConfigurator,
    ind: str,
    nested_dir: str,
    result_queries: list,
    start_time_str: str,
    end_time_str: str,
    start_date: datetime,
    end_date: datetime,
    default_timeield: str,
    is_extra_query: bool,
):
    if is_extra_query:
        temp_filename = os.path.join(
            nested_dir,
            f"{ind}_extra.pkl",
        )
        start_time_str = start_date.strftime("%Y-%m-%dT00:00:00.000")
        end_time_str = end_date.strftime("%Y-%m-%dT00:00:00.000")
        hour_condition = HOUR_CONDITION_TEMPLATE["extra"].substitute(
            default_timeield=default_timeield,
            start_time_str=start_time_str,
            end_time_str=end_time_str,
        )
        if configurator.gte and configurator.lte:
            hour_condition_gte_lte = " " + HOUR_CONDITION_TEMPLATE[
                "regular"
            ].substitute(
                default_timeield=default_timeield,
                start_time_str=configurator.gte,
                end_time_str=configurator.lte,
            )
            hour_condition += hour_condition_gte_lte

    else:
        start_time_filename = start_time_str.replace(":00:00.000", "")
        end_time_filename = end_time_str.replace(":00:00.000", "")
        is_equality = False
        if configurator.gte and configurator.lte:
            result = intersect_time_ranges(
                start_time_str, end_time_str, configurator.gte, configurator.lte
            )
            if not result[0]:
                return
            start_time_str = result[0][0]
            end_time_str = result[0][1]
            is_equality = result[1]

        temp_filename = os.path.join(
            nested_dir,
            f"{ind}_{start_time_filename}_{end_time_filename}.pkl",
        )
        hour_condition = HOUR_CONDITION_TEMPLATE["regular"].substitute(
            default_timeield=default_timeield,
            start_time_str=start_time_str,
            end_time_str=end_time_str,
        )
        if is_equality:
            hour_condition = hour_condition.replace("<", "<=")

    if configurator.name_of_type == "Type":
        hour_condition = change_time_format(hour_condition)

    query = configurator.get_query(ind, hour_condition)
    result_queries.append([query, temp_filename])


def get_time_strings(hour, configurator, end_time, start_time):
    start_time_str = start_time.strftime("%Y-%m-%dT%H:00:00.000")

    if hour + configurator.time_step > 24:
        end_time_str = end_time.strftime("%Y-%m-%dT00:00:00.000")
    else:
        end_time_str = end_time.strftime("%Y-%m-%dT%H:00:00.000")

    return start_time_str, end_time_str


def prepare_header(fields: str) -> pd.DataFrame:
    column_names: str = fields.replace("@", "").replace(".", "_").replace("`", "")
    heads: list = [name.strip() for name in column_names.split(",")]
    df = pd.DataFrame(columns=heads)
    return df


def write_to_csv(df, output_file, header=False):
    df.to_csv(output_file, index=False, header=header, mode="a", encoding="utf-8")


def sort_dataframe_by_time(df: pd.DataFrame, sort_timefield: str, ascending=True):
    if not df.empty:
        if sort_timefield in df.columns:
            df[sort_timefield] = pd.to_datetime(df[sort_timefield], format="mixed")
            df = df.sort_values(by=sort_timefield, ascending=ascending)
        elif "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], format="mixed")
            df = df.sort_values(by="timestamp", ascending=ascending)
    return df


def aggregate_data_to_variable(
    temporary_files: list[str], configurator: QueryConfigurator, sort_timefield: str
) -> pd.DataFrame:
    configurator.log_info("Assembling dataframe to variable...", console=True)
    if len(temporary_files) == 0:
        return pd.DataFrame()

    chunk_dfs = concat_in_chunks(
        read_dataframes(temporary_files, configurator), chunk_size=10
    )
    combined_dataframe = pd.concat(chunk_dfs, ignore_index=True, copy=False)
    gc.collect()

    combined_dataframe = sort_dataframe_by_time(
        combined_dataframe, sort_timefield, configurator.ascending
    )

    mem = combined_dataframe.memory_usage(deep=True).sum() / 1024**2
    configurator.log_info(f"Final DataFrame memory: {mem:.2f} MB", console=True)
    configurator.log_info("Assembly finished.")
    return combined_dataframe if not combined_dataframe.empty else pd.DataFrame()


def read_dataframes(
    temporary_files: list[str], configurator: QueryConfigurator
) -> Iterator[pd.DataFrame]:
    for temp_filename in temporary_files:
        if os.path.exists(temp_filename):
            df = pd.read_pickle(temp_filename)
            if not df.empty:
                if configurator.compress_df:
                    df = optimize_dataframe(df)
                yield df
                del df
                gc.collect()
        else:
            configurator.log_info(f"File {temp_filename} does not exist.")


def concat_in_chunks(
    df_iter: Iterator[pd.DataFrame], chunk_size: int = 10
) -> Iterator[pd.DataFrame]:
    _buffer = []
    for df in df_iter:
        _buffer.append(df)
        if len(_buffer) >= chunk_size:
            yield pd.concat(_buffer, ignore_index=True, copy=False)
            _buffer.clear()
            gc.collect()
    if _buffer:
        yield pd.concat(_buffer, ignore_index=True, copy=False)
        gc.collect()


def optimize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Compresses the DataFrame by downcasting data types to save memory."""
    for col in df.columns:
        try:
            col_data = df[col]
            if pd.api.types.is_integer_dtype(col_data):
                df[col] = pd.to_numeric(col_data, downcast="integer")

            elif pd.api.types.is_float_dtype(col_data):
                for dtype in ["float16", "float32"]:
                    downcasted = col_data.astype(dtype)
                    if np.allclose(
                        col_data, downcasted, rtol=1e-3, atol=1e-3, equal_nan=True
                    ):
                        df[col] = downcasted
                        break

            elif pd.api.types.is_object_dtype(col_data):
                num_unique = col_data.nunique(dropna=False)
                total = len(col_data)
                if num_unique / total < 0.5:
                    df[col] = col_data.astype("category")
        except:
            pass

    return df


def download_data_parallel(
    self,
    configurator: QueryConfigurator,
    num_threads: int = 10,
) -> None | pd.DataFrame:
    """
    Function only for downloading data from OpenSearch and saving .csv file into current working directory.
    Returns `None`. Does not return dataframe.

    Uses number of threads according to the rule: THREADS = min(len(configurator.indexes), num_threads).
    """
    configurator.log_info(f"Starting download data parallel for {configurator}...")
    configurator.log_info(f"Running in container: {configurator.isin_container}...")

    temp_dir, is_old_cache = create_cache_dir(configurator)
    if configurator.temp_files:
        write_instance_info(configurator, temp_dir)

    success_count = 0
    error_count = 0
    counter_lock = threading.Lock()

    Tqdm = (
        tqdm
        if not configurator.isin_container and configurator.verbose < 4
        else DummyTqdm
    )

    peak_memory_usage = [0]
    if not configurator.isin_container:

        def memory_monitor_loop():
            process = psutil.Process(os.getpid())
            while not stop_monitoring.is_set():
                mem = process.memory_info().rss / (1024**2)  # в мегабайтах
                if mem > peak_memory_usage[0]:
                    peak_memory_usage[0] = mem
                sleep(0.5)

        stop_monitoring = threading.Event()
        memory_thread = threading.Thread(target=memory_monitor_loop)
        memory_thread.start()

    start_exec_time = datetime.now()

    queries_to_download = prepare_queries(
        configurator, temp_dir, self.default_timefield
    )

    def _process_single_query(single_query: list[str], pbar):
        nonlocal success_count, error_count
        query = single_query[0]
        temp_filename = single_query[1]

        configurator.log_debug(f"Starting download data for index {query}...")

        try:
            if os.path.exists(temp_filename):
                configurator.log_info(
                    f"Skipping {query} for {temp_filename} as it already exists."
                )
                with counter_lock:
                    success_count += 1
            else:
                data = self.get_dataframe(
                    query,
                    cursor=True,
                    df_columns=configurator.fields.replace("@", "")
                    .replace(".", "_")
                    .replace("`", "")
                    .split(", "),
                )
                if not data.empty:
                    data.to_pickle(temp_filename)
                else:
                    configurator.log_info(f"{query} result is empty.")
                    temp_filename = None
                with counter_lock:
                    success_count += 1
                configurator.log_info(f'"{query}" --- OK')
        except Exception as e:
            if not configurator.ignore_exceptions:
                configurator.log_error(f'"{query}" --- ERROR: {e}', console=True)
                os._exit(1)
            configurator.log_error(f'\n"{query}" --- ERROR: {e}')
            with counter_lock:
                error_count += 1

        pbar.update(1)
        gc.collect()
        return temp_filename

    def finalize_process():
        configurator.log_info("Starting finalize_process.")
        if not configurator.isin_container:
            stop_monitoring.set()
            memory_thread.join()
            configurator.log_info("Joined Memory Thread")

        summary(
            configurator,
            start_exec_time,
            success_count,
            error_count,
            peak_memory_usage,
        )

        configurator.log_info("Summary is sent")

        if configurator.temp_files:
            move_query_log_file(configurator, temp_dir)

        if not configurator.temp_files and not is_old_cache:
            delete_directory(configurator, temp_dir)

    try:
        num_threads = min(num_threads, len(queries_to_download))
        configurator.log_info(
            f"Start download data parallel with {num_threads} threads...",
            console=True,
        )
        with Tqdm(
            total=len(queries_to_download),
            desc=f"Downloading {configurator.event_type}",
            unit="query",
            ncols=150,
            ascii=True,
            bar_format="{l_bar}{bar:40}| \033[92m{n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]\033[0m",
        ) as pbar:
            process_with_pbar = partial(_process_single_query, pbar=pbar)
            with concurrent.futures.ThreadPoolExecutor(
                max_workers=num_threads
            ) as executor:
                all_temp_files = [
                    result
                    for result in executor.map(process_with_pbar, queries_to_download)
                    if result is not None
                ]

        configurator.log_info("Parallel downloading finished.", console=True)
        temporary_files = sorted(all_temp_files, reverse=not configurator.ascending)
        gc.collect()

        sort_timefield = self.default_timefield.replace(".", "_")
        if configurator.return_df:
            result = aggregate_data_to_variable(
                temporary_files, configurator, sort_timefield
            )
            return result

        output_file = configurator.output_filename
        configurator.log_info(f"Starting assembly result file {output_file}")
        file_extension = os.path.splitext(output_file)[1]

        with Tqdm(
            total=len(queries_to_download),
            desc=f"Assembling {configurator.event_type}",
            unit="query",
            ncols=150,
            ascii=True,
            bar_format="{l_bar}{bar:40}| \033[92m{n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]\033[0m",
        ) as pbar1:
            if file_extension == ".csv":
                mode = "w"
                newline = ""
                write_function = write_to_csv
                encoding = "utf-8"
            else:
                raise ValueError("Unsupported file extension")

            heading = prepare_header(configurator.fields)
            with open(
                output_file, mode=mode, newline=newline, encoding=encoding
            ) as f_out:
                write_function(heading, f_out, header=True)
                for temp_file in temporary_files:
                    if os.path.exists(temp_file):
                        df = pd.read_pickle(temp_file)
                        df = sort_dataframe_by_time(
                            df, sort_timefield, configurator.ascending
                        )
                        write_function(df, f_out)
                    pbar1.update(1)
                    gc.collect()

    except Exception as e:
        error_type = type(e).__name__
        tb = traceback.format_exc()
        configurator.log_error(
            f"\nError with {configurator.event_type} using {num_threads} threads: [{error_type}] {e}\n{tb}",
            console=True,
        )
        raise e

    finally:
        finalize_process()
