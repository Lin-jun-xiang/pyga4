from collections import Counter
from typing import Any

from pyga4.model.bigquery import Ga4Table


class BaseAnalytic:
    def __init__(self, table: Ga4Table) -> None:
        self.table = table

    @staticmethod
    def attribute_distribution(table: Ga4Table, attribute_name: str) -> Counter:
        attribute_list = getattr(table, attribute_name)
        counts = Counter(attribute_list)

        return counts
   

class UserAnalytic(BaseAnalytic):
    """The features of user"""

    def __init__(self, table: Ga4Table) -> None:
        super().__init__(table)

    @property
    def user_id_distribution(self) -> Counter:
        return self.attribute_distribution(
            self.table, 'user_id_list'
        )

    @property
    def countries_distribution(self) -> Counter:
        return self.attribute_distribution(
            self.table, 'geo_country_list'
        )


class DeviceAnalytic(BaseAnalytic):
    """The features of technology"""

    def __init__(self, table: Ga4Table) -> None:
        super().__init__(table)

    @property
    def os_distribution(self) -> Counter:
        return self.attribute_distribution(
            self.table, 'device_operating_system_list'
        )

    @property
    def category_distribution(self) -> Counter:
        return self.attribute_distribution(
            self.table, 'device_category_list'
        )

    @property
    def browser_distribution(self) -> Counter:
        return self.attribute_distribution(
            self.table, 'device_web_info_browser_list'
        )

    @property
    def mobile_brand_distribution(self) -> Counter:
        return self.attribute_distribution(
            self.table, 'device_mobile_brand_name_list'
        )

    @property
    def mobile_model_distribution(self) -> Counter:
        return self.attribute_distribution(
            self.table, 'device_mobile_model_name_list'
        )


class EventAnalytic(BaseAnalytic):
    """The features of event"""

    def __init__(self, table: Ga4Table) -> None:
        super().__init__(table)

    @property
    def pages_distribution(self) -> Counter:
        """Return most common pages for all users"""
        return self.attribute_distribution(
            self.table, 'page_location_list'
        )

    @staticmethod
    def track_user_loc():
        """Return most common pages for an user"""
        pass

    @staticmethod
    def conversion_rate(engagement_events: Any, target_events: Any) -> float:
        """Calculate the conversion rate

        If your "target" is to measure how many people `place an order`(purchased), 
        so your `ad clicks` would be the "engagement" because the orders resulting 
        from the ad are your "conversions."

        If your "target" is to measure how many people `clicking the ad`,
        then your ad clicks would become the "conversions,"
        and `ad impressions` would become the "engagement."

        Parameters
        ----------
        action_events:
            The engagement events that users perform.

        target_events:
            The target events that represent successful conversions.

        Returns
        -------
        float
            The calculated conversion rate as a percentage.

        Examples
        --------
        If `action_events` contains 1000 page views and `target_events` contains 200 purchases,
        the conversion rate would be calculated as:

        >>> conversion_rate([...,1000], [...,200])
        20.0

        If you have multiple engagement events and target events, you can calculate the combined
        conversion rate as well:

        >>> conversion_rate([1000, 500], [200, 100])
        18.18

        Note that the input lists should contain counts or frequencies of events.

    """
        return len(target_events) / len(engagement_events) * 100.0
