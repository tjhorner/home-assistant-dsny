import voluptuous as vol

from homeassistant import config_entries

from .const import (
    CONF_BOROUGH,
    CONF_HOUSE_NUMBER,
    CONF_STREET_NAME,
    DOMAIN,
    VALID_BOROUGHS,
)  # pylint:disable=unused-import

DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOUSE_NUMBER): str,
        vol.Required(CONF_STREET_NAME): str,
        vol.Required(CONF_BOROUGH): vol.In(VALID_BOROUGHS),
    }
)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            return self.async_create_entry(
                title=f"{user_input[CONF_HOUSE_NUMBER]} {user_input[CONF_STREET_NAME]}",
                data=user_input,
            )

        return self.async_show_form(
            step_id="user", data_schema=DATA_SCHEMA, errors=errors
        )
