"""Sample API Client."""
import logging
import asyncio
import socket
import aiohttp
import async_timeout
from datetime import timedelta
from homeassistant.util.dt import now

TIMEOUT = 15
DATE_FORMAT = "%G-%m-%d"

_LOGGER: logging.Logger = logging.getLogger(__package__)


class DsnyApiClient:
    def __init__(self, session: aiohttp.ClientSession) -> None:
        """Sample API Client."""
        self._session = session

    async def async_get_schedule(
        self, house_number: str, street: str, borough: str
    ) -> list[dict]:
        """Get data from the API."""
        url = "https://a827-donatenyc.nyc.gov/DSNYApi/API/SCHEDULE/GetallSchedule"
        tomorrow = (now() + timedelta(days=1)).strftime(DATE_FORMAT)
        next_week = (now() + timedelta(days=7)).strftime(DATE_FORMAT)

        print(tomorrow)
        return await self.get_url(
            url,
            {
                "houseNo": house_number,
                "streetName": street,
                "borough": borough,
                "startdate": tomorrow,
                "enddate": next_week,
            },
        )

    async def get_url(self, url: str, params: dict) -> list[dict]:
        """Get information from the API."""
        try:
            async with async_timeout.timeout(TIMEOUT, loop=asyncio.get_event_loop()):
                response = await self._session.get(url, params=params)
                return await response.json()

        except asyncio.TimeoutError as exception:
            _LOGGER.error(
                "Timeout error fetching information from %s - %s",
                url,
                exception,
            )

        except (KeyError, TypeError) as exception:
            _LOGGER.error(
                "Error parsing information from %s - %s",
                url,
                exception,
            )
        except (aiohttp.ClientError, socket.gaierror) as exception:
            _LOGGER.error(
                "Error fetching information from %s - %s",
                url,
                exception,
            )
        except Exception as exception:  # pylint: disable=broad-except
            _LOGGER.error("Something really wrong happened! - %s", exception)
