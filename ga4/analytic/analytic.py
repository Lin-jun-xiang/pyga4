from collections import Counter
from typing import Any

from ga4.model.bigquery import Ga4Table


class User:
    """The features of user"""
    @staticmethod
    def countries_distribution(table: Ga4Table) -> list:
        all_users_country = table.geo_country_list
        counts = Counter(all_users_country)
        
        return counts


class Device:
    """The features of technology"""
    @staticmethod
    def os_distribution(table: Ga4Table) -> list:
        all_devices_os = table.device_operating_system_list
        counts = Counter(all_devices_os)
        
        return counts

    @staticmethod
    def category_distribution(table: Ga4Table) -> list:
        all_devices_category = table.device_category_list
        counts = Counter(all_devices_category)
        
        return counts

    @staticmethod
    def browser_distribution(table: Ga4Table) -> list:
        all_devices_browser = table.device_web_info_browser_list
        counts = Counter(all_devices_browser)
        
        return counts

    @staticmethod
    def mobile_brand_distribution(table: Ga4Table) -> list:
        all_devices_mobile_brand = table.device_mobile_brand_name_list
        counts = Counter(all_devices_mobile_brand)
        
        return counts

    @staticmethod
    def mobile_model_distribution(table: Ga4Table) -> list:
        all_devices_mobile_model = table.device_mobile_model_name_list
        counts = Counter(all_devices_mobile_model)
        
        return counts


class Event:
    """The features of event"""

    @staticmethod
    def pages_distribution(table: Ga4Table) -> list:
        """Return most common pages for all users"""
        all_pages_loc = table.page_location_list
        counts = Counter(all_pages_loc)
        
        return counts

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
