# Robonect — Troubleshooting

## Frequently asked questions

- I am missing many sensors: please verify that the MQTT topic you have entered in the HA config flow equals the MQTT topic in Robonect
- If you would be expecting specific sensors and you don't see them, make sure your Robonect firmware is up to date.

---

## Robot temporarily unreachable

When the robot is powered off, docked, or outside Wi-Fi range, HA will periodically try to reach it and fail. By default, these connection failures are logged at `DEBUG` level only, so they will **not** appear in the HA log under normal conditions.

If you are seeing repeated `WARNING` messages like `ConnectError` or `All connection attempts failed`, make sure you are running the latest version of this integration.

To inspect connectivity issues in detail, enable debug logging for `custom_components.robonect` in your `configuration.yaml`:

```yaml
logger:
  logs:
    custom_components.robonect: debug
```

---

## Enable debug logging

To enable debug logging, go to Settings -> Devices & Services and then click the triple dots for the Robonect integration and click Enable Debug Logging.

![enable-debug-logging](https://raw.githubusercontent.com/geertmeersman/robonect/main/images/screenshots/enable-debug-logging.gif)

---

## Disable debug logging and download logs

Once you enable debug logging, you ideally need to make the error happen. Run your automation, change up your device or whatever was giving you an error and then come back and disable Debug Logging. Disabling debug logging is the same as enabling, but now you will see Disable Debug Logging. After you disable debug logging, it will automatically prompt you to download your log file. Please provide this logfile.

![disable-debug-logging](https://raw.githubusercontent.com/geertmeersman/robonect/main/images/screenshots/disable-debug-logging.gif)
