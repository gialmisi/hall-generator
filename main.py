import numpy as np
import pandas as pd

from datetime import date


def linear_model(x: np.ndarray, a: float, b: float, noise_factor: float = 0.0):
    if noise_factor > 0:
        noise = np.random.uniform(-noise_factor, noise_factor, x.shape)
    else:
        noise = 0
    return (a * x + b) + noise


def logistic_model(
    x: np.ndarray,
    mid_point: float,
    max_value: float,
    steepness: float,
    noise_factor: float = 0.0,
):
    if noise_factor > 0:
        noise = np.random.uniform(-noise_factor, noise_factor, x.shape)
    else:
        noise = 0

    return max_value / (1 + np.exp(-steepness * (x - mid_point))) + noise


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # driving current and Hall voltage
    driving_current = np.linspace(-30, 30, 15)
    driving_current += np.random.uniform(-0.1, 0.1, 15)

    hall_voltage = linear_model(driving_current, 0.742, -0.692, noise_factor=1)

    data_1 = np.stack((driving_current, hall_voltage)).T
    data_frame_1 = pd.DataFrame(
        data_1,
        columns=["Ohjausvirta (mA)", "Hall-jännite (mV)"],
        index=[f"{i}" for i in range(1, len(driving_current) + 1)],
    ).round(decimals=1)

    html_table_1 = data_frame_1.to_html()

    # magnetic field and Hall voltage
    magnetic_field = np.linspace(50, 100, 15, dtype=int)

    hall_voltage = linear_model(magnetic_field, 0.223, 0.785, noise_factor=0.5)

    data_2 = np.stack((magnetic_field, hall_voltage)).T
    data_frame_2 = pd.DataFrame(
        data_2,
        columns=["Magneettivuon tiheys (mT)", "Hall-jännite (mV)"],
        index=[f"{i}" for i in range(1, len(magnetic_field) + 1)],
    ).round(decimals=1)

    html_table_2 = data_frame_2.to_html()

    # driving current and voltage
    driving_current = np.linspace(-30, 30, 15)
    driving_current += np.random.uniform(-0.1, 0.1, 15)

    voltage = linear_model(driving_current, 0.062, 0.090, noise_factor=0.1)

    data_3 = np.stack((driving_current, voltage)).T
    data_frame_3 = pd.DataFrame(
        data_3,
        columns=["Ohjausvirta (mA)", "Jännite kiteen yli (V)"],
        index=[f"{i}" for i in range(1, len(driving_current) + 1)],
    ).round(decimals={"Ohjausvirta (mA)": 1, "Jännite kiteen yli (V)": 3})

    html_table_3 = data_frame_3.to_html()

    # temperatrue and Hall-voltage
    temperatures = np.linspace(50, 150, 20)
    hall_voltage = logistic_model(
        temperatures, 100, 22, -0.15, noise_factor=0.15
    )

    data_4 = np.stack((temperatures, hall_voltage)).T
    data_frame_4 = pd.DataFrame(
        data_4,
        columns=["Lämpotila (°C)", "Hall-jännite (mV)"],
        index=[f"{i}" for i in range(1, len(temperatures) + 1)],
        ).round(decimals={"Lämpotila (°C)": 0, "Hall-jännite (mV)": 1}).astype({"Lämpotila (°C)": "int32"})

    html_table_4 = data_frame_4.to_html()

    # other info
    title = f"<h1>Generoitu mittauspöytäkirja ({date.today()})</h1>"
    assignment_name = f"<h2>FYSA2010/1 Hallin ilmiö</h2>"

    gear = [
        [
            "Amprobe 35XP-A",
            "Teslametri",
            "Hall-moduuli, virrat",
            "Hall-moduuli, lämpötila",
        ],
        ["0.5% lu + 1 dig", "2% lu", "1 dig", "1 dig",],
    ]
    gear = list(map(list, zip(*gear)))
    gear_frame = pd.DataFrame(
        gear,
        columns=["Laite", "Virhe"],
        index=[f"{i}" for i in range(1, len(gear) + 1)],
    )
    gear_html = gear_frame.to_html()

    # generate the html
    with open("poytakirja.html", "a") as f:
        f.write(title)
        f.write(assignment_name)

        f.write("<h3>Mittalaitteisto</h3>")
        f.write(
            """
            <figure>
                <img src="./assets/FYSA2010_1_laitteisto.jpg" alt="laitteisto" style="width:100%">
            </figure> 
        """
        )

        f.write("<h3>Mittalaitteiston virheet</h3>")
        f.write(gear_html)

        f.write("<h3>Jännite germanium kiteen yli ohjausvirran funktiona</h3>")
        f.write(html_table_3)

        f.write("<h3>Mittaus 1: vakio magneettikenttä 75,8mT</h3>")
        f.write(html_table_1)

        f.write("<h3>Mittaus 2: vakio ohjausvirta 25mA</h3>")
        f.write(html_table_2)

        f.write(
            "<h3>Mittaus 3: Hall-jännite lämpötilan funktiona, magneettikenttä 72,5mT ja ohjausvirta 30mA</h3>"
        )
        f.write(html_table_4)
