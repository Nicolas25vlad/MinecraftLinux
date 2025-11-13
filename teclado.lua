local keyboard_connector = peripheral.find("tm_keyboard")

keyboard_connector.setFireNativeEvents(true)

shell.run("monitor top shell")