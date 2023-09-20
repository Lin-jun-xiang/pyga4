from functools import wraps

from google.cloud import bigquery


def calculate_bytes_processed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        result = func(self, *args, **kwargs)
        query_job = getattr(self, "_query_job", None)
        total_bytes_processed = query_job.total_bytes_processed / (1024 * 1024)
        print(f"Total bytes processed: {total_bytes_processed} MB")

        return result

    return wrapper


class Client:
    """Instance the bigquery client and define its attributes

    Parameters
    ----------
    query_config:
        if `dry_run=True`,
        the query will not response results,
        but return the bytes usage which indicate cost.

    Examples
    --------
    ```python
    Client().query_config.dry_run = True
    ```
    """
    query_config = bigquery.QueryJobConfig(
        dry_run = False,
        use_query_cache = False
    )
    def __init__(self, client, project_id: str) -> None:
        self.client = client
        self.project_id = project_id


class BaseTable(Client):
    """Connect to the data set from bigquery"""
    def __init__(self, client, project_id: str, dataset_name: str) -> None:
        super().__init__(client, project_id)
        self.dataset_name = dataset_name
        self._table_id = None

    @property
    def table_id(self) -> str:
        return self._table_id

    @table_id.setter
    def table_id(self, table_id) -> None:
        self._table_id = table_id

    @property
    def all_tables_list(self) -> list:
        """Return all tables id from data set"""
        dataset_ref = self.client.dataset(self.dataset_name)
        tables = list(self.client.list_tables(dataset_ref))

        return [table.table_id for table in tables]

    @calculate_bytes_processed
    def to_dataframe(self):
        query = f"""
            SELECT *
            FROM `{self.project_id}.{self.dataset_name}.{self.table_id}`
        """
        query_job = self.client.query(query)
        df = query_job.to_dataframe()

        return df


class Ga4Table(BaseTable):
    def __init__(self, client, project_id: str, dataset_name: str) -> None:
        super().__init__(client, project_id, dataset_name)
        self._query_job = None

    def _query_template(self, query_target: str) -> list:
        query = f"""
            SELECT {query_target}
            FROM `{self.project_id}.{self.dataset_name}.{self.table_id}`
        """
        self._query_job = self.client.query(query, job_config=self.query_config)
        results = self._query_job.result()

        field_name = query_target.split('.')[-1] if '.' in query_target else query_target

        return [getattr(row, field_name) for row in results]

    @property
    @calculate_bytes_processed
    def user_id_list(self) -> list:
        """Return all user_id from data table"""
        return self._query_template('user_id')

    @property
    @calculate_bytes_processed
    def event_date_list(self) -> list:
        """Return all event_date from data table"""
        return self._query_template('event_date')

    @property
    @calculate_bytes_processed
    def event_timestamp_list(self) -> list:
        """Return all event_timestamp from data table"""
        return self._query_template('event_timestamp')

    @property
    @calculate_bytes_processed
    def event_name_list(self) -> list:
        """Return all event_name from data table"""
        return self._query_template('event_name')

    @property
    @calculate_bytes_processed
    def device_category_list(self) -> list:
        """Return all device_category from data table
        ex: mobile, desktop
        """
        return self._query_template('device.category')

    @property
    @calculate_bytes_processed
    def device_mobile_brand_name_list(self) -> list:
        """Return all device_mobile_brand_name from data table
        ex: Apple
        """
        return self._query_template('device.mobile_brand_name')

    @property
    @calculate_bytes_processed
    def device_mobile_model_name_list(self) -> list:
        """Return all device_mobile_model_name from data table
        ex: iPhone
        """
        return self._query_template('device.mobile_model_name')

    @property
    @calculate_bytes_processed
    def device_operating_system_list(self) -> list:
        """Return all device_operating_system from data table
        ex: iOS
        """
        return self._query_template('device.operating_system')

    @property
    @calculate_bytes_processed
    def device_language_list(self) -> list:
        """Return all device_language from data table"""
        return self._query_template('device.language')

    @property
    @calculate_bytes_processed
    def device_language_list(self) -> list:
        """Return all device_language from data table"""
        return self._query_template('device.language')

    @property
    @calculate_bytes_processed
    def device_web_info_browser_list(self) -> list:
        """Return all device_web_info_browser from data table"""
        return self._query_template('device.web_info.browser')

    @property
    @calculate_bytes_processed
    def geo_country_list(self) -> list:
        """Return all user countries from data table"""
        return self._query_template('geo.country')

    @property
    @calculate_bytes_processed
    def geo_region_list(self) -> list:
        """Return all user region from data table"""
        return self._query_template('geo.region')

    @property
    @calculate_bytes_processed
    def geo_city_list(self) -> list:
        """Return all user city from data table"""
        return self._query_template('geo.city')

    @property
    @calculate_bytes_processed
    def geo_sub_continent_list(self) -> list:
        """Return all user sub_continent from data table"""
        return self._query_template('geo.sub_continent')

    @property
    @calculate_bytes_processed
    def geo_metro_list(self) -> list:
        """Return all user metro from data table"""
        return self._query_template('geo.metro')

    @property
    @calculate_bytes_processed
    def page_location_list(self) -> list:
        """Return all event of page location from data table"""
        query = f"""
            SELECT
                param.value.string_value AS param_string_value
            FROM
                `{self.project_id}.{self.dataset_name}.{self.table_id}`,
                UNNEST(event_params) AS param
            WHERE
                param.key = "page_location" OR param.key IS NULL
        """
        self._query_job = self.client.query(query, job_config=self.query_config)
        results = self._query_job.result()

        return [row.param_string_value for row in results]

    @calculate_bytes_processed
    def query(self, query: str) -> list:
        """Custom query from data table"""
        self._query_job = self.client.query(query, job_config=self.query_config)
        results = self._query_job.result()

        return results
