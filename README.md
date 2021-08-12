# DSNY Home Assistant

This is a custom Home Assistant integration that can fetch the garbage collection schedule for your address from DSNY's API.

It exposes a binary sensor for each of these collection types:

- Trash collection
- Recycling collection
- Organics collection
- Bulk collection

The binary sensor indicates whether the specified collection is tomorrow or not. There's also an extra attribute `next_collection` which stores the next collection date up to a week out (or "Unknown" if there's none within a week). The sensors update every hour.

## Setup

Setup is pretty simple!

1. Make sure [HACS](https://hacs.xyz/) is installed.
2. Go to HACS > Integrations, click the three dots in the top-right, then "Custom repositories".
3. Enter this repository's URL: https://github.com/tjhorner/home-assistant-dsny
4. Install the DSNY integration from HACS and restart Home Assistant.
5. Add a new DSNY integration from Configuration > Integrations.
6. Enter your address and you're done! (Address data is never sent anywhere except DSNY's API.)

![](https://user-images.githubusercontent.com/2646487/129136562-5ffe64c4-43f5-4697-8759-8edeacbfb8e0.png)

## Fancy Card

![](https://user-images.githubusercontent.com/2646487/129136784-07f514d9-f7ad-49b6-90fd-5ff8a1aa47dc.png)

Here's the YAML for a fancy card which shows all of tomorrow's collections:

```yaml
type: glance
entities:
  - entity: binary_sensor.trash_collection_tomorrow
    name: Trash
  - entity: binary_sensor.recycling_collection_tomorrow
    name: Recycling
  - entity: binary_sensor.organics_collection_tomorrow
    name: Organics
  - entity: binary_sensor.bulk_collection_tomorrow
    name: Bulk
show_name: true
show_state: false
state_color: true
title: "Tomorrow's DSNY Collections"
```