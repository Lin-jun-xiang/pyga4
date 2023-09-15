from collections import Counter
from typing import Any

from ga4.model.bigquery import Ga4Table


class User:
    """The features of user"""
    @staticmethod
    def most_common_countries(table: Ga4Table, n: int = 3) -> list:
        pass


class Technology:
    """The features of technology"""
    @staticmethod
    def most_common_os(table: Ga4Table, n: int = 3) -> list:
        pass

    @staticmethod
    def most_common_browser(table: Ga4Table, n: int = 3) -> list:
        pass


class Page:
    """The features of page"""

    @staticmethod
    def most_common_pages(table: Ga4Table, n: int = 3) -> list:
        """Return most common pages for all users"""
        all_pages_loc = table.page_location_list
        counts = Counter(all_pages_loc)
        top_n = counts.most_common(n)

        return top_n

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
