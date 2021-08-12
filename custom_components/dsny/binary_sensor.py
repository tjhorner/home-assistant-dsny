"""Example integration using DataUpdateCoordinator."""

from datetime import timedelta
import logging

import async_timeout
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.util.dt import now

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import CONF_BOROUGH, CONF_HOUSE_NUMBER, CONF_STREET_NAME, DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry, async_add_entities):
    api = hass.data[DOMAIN][entry.entry_id]

    async def async_update_data():
        async with async_timeout.timeout(10):
            house_number = entry.data.get(CONF_HOUSE_NUMBER)
            street_name = entry.data.get(CONF_STREET_NAME)
            borough = entry.data.get(CONF_BOROUGH)
            return await api.async_get_schedule(house_number, street_name, borough)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="sensor",
        update_method=async_update_data,
        update_interval=timedelta(hours=1),
    )

    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        DsnyCollectionTomorrowSensor(
            coordinator, friendly_name, schedule_type, schedule_icon
        )
        for friendly_name, schedule_type, schedule_icon in [
            ["Trash", "GarbageSchedule", "mdi:delete"],
            ["Recycling", "RecyclingSchedule", "mdi:recycle"],
            ["Organics", "OrganicsSchedule", "mdi:food-apple"],
            ["Bulk", "BulkCollection", "mdi:package-variant"],
        ]
    )


class DsnyCollectionTomorrowSensor(CoordinatorEntity, BinarySensorEntity):
    def __init__(self, coordinator, friendly_name, schedule_type, schedule_icon):
        super().__init__(coordinator)
        self.friendly_name = friendly_name
        self.schedule_type = schedule_type
        self.schedule_icon = schedule_icon

    @property
    def unique_id(self):
        return self.schedule_type

    @property
    def name(self):
        return f"{self.friendly_name} Collection Tomorrow"

    @property
    def icon(self):
        return self.schedule_icon

    @property
    def extra_state_attributes(self):
        next_collection = "Unknown"
        matches = [x for x in self.coordinator.data if x[self.schedule_type] == "Y"]
        if len(matches) != 0:
            next_collection = matches[0]["ScheduleDate"]
        return {"next_collection": next_collection}

    @property
    def is_on(self):
        # hacky way to do this but that's what the API gives us
        tomorrow = (now() + timedelta(days=1)).strftime("%-m/%-d/%G")
        matches = [
            x for x in self.coordinator.data if x["ScheduleDate"].startswith(tomorrow)
        ]
        if len(matches) == 0:
            return False
        return matches[0][self.schedule_type] == "Y"
